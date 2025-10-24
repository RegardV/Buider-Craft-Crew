"""
AI Crew Builder Team - OpenSpec Framework
Implementation of the OpenSpec specification management system.
"""

import os
import json
import yaml
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict, field
from enum import Enum

from .config import get_config

logger = logging.getLogger(__name__)

class ChangeStatus(Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    REJECTED = "rejected"

class SpecType(Enum):
    SYSTEM = "system"
    AGENT = "agent"
    WORKFLOW = "workflow"
    FEATURE = "feature"
    CHANGE = "change"

@dataclass
class OpenSpecChange:
    """Represents a change proposal in OpenSpec."""
    id: str
    title: str
    description: str
    author: str
    spec_type: SpecType
    status: ChangeStatus
    content: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    implemented_by: Optional[str] = None
    implemented_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    priority: str = "medium"  # low, medium, high, critical
    dependencies: List[str] = field(default_factory=list)

@dataclass
class OpenSpecDocument:
    """Represents an OpenSpec document."""
    id: str
    title: str
    version: str
    spec_type: SpecType
    content: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    author: str
    status: str = "draft"  # draft, approved, published, deprecated
    tags: List[str] = field(default_factory=list)
    change_history: List[str] = field(default_factory=list)  # Change IDs

class OpenSpecManager:
    """Manages OpenSpec documents and change workflows."""

    def __init__(self):
        self.config = get_config()
        self.openspec_path = Path(self.config.openspec_path)
        self.documents: Dict[str, OpenSpecDocument] = {}
        self.changes: Dict[str, OpenSpecChange] = {}

        # Ensure directories exist
        self._ensure_directory_structure()

        # Load existing documents
        self._load_documents()
        self._load_changes()

    def _ensure_directory_structure(self):
        """Ensure OpenSpec directory structure exists."""
        directories = [
            "specs/system",
            "specs/agents",
            "specs/workflows",
            "specs/features",
            "changes/proposals",
            "changes/approved",
            "changes/implemented",
            "changes/rejected",
            "templates"
        ]

        for directory in directories:
            dir_path = self.openspec_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)

    def _load_documents(self):
        """Load existing OpenSpec documents."""
        specs_dir = self.openspec_path / "specs"

        for spec_dir in specs_dir.iterdir():
            if spec_dir.is_dir():
                for spec_file in spec_dir.glob("*.yaml"):
                    try:
                        doc = self._load_document_from_file(spec_file)
                        if doc:
                            self.documents[doc.id] = doc
                            logger.info(f"Loaded document: {doc.id}")
                    except Exception as e:
                        logger.error(f"Error loading document {spec_file}: {e}")

    def _load_changes(self):
        """Load existing change proposals."""
        changes_dir = self.openspec_path / "changes"

        for change_dir in changes_dir.iterdir():
            if change_dir.is_dir():
                for change_file in change_dir.glob("*.yaml"):
                    try:
                        change = self._load_change_from_file(change_file)
                        if change:
                            self.changes[change.id] = change
                            logger.info(f"Loaded change: {change.id}")
                    except Exception as e:
                        logger.error(f"Error loading change {change_file}: {e}")

    def _load_document_from_file(self, file_path: Path) -> Optional[OpenSpecDocument]:
        """Load document from YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            return OpenSpecDocument(
                id=data['id'],
                title=data['title'],
                version=data['version'],
                spec_type=SpecType(data['spec_type']),
                content=data['content'],
                created_at=datetime.fromisoformat(data['created_at']),
                updated_at=datetime.fromisoformat(data['updated_at']),
                author=data['author'],
                status=data['status'],
                tags=data.get('tags', []),
                change_history=data.get('change_history', [])
            )
        except Exception as e:
            logger.error(f"Error loading document from {file_path}: {e}")
            return None

    def _load_change_from_file(self, file_path: Path) -> Optional[OpenSpecChange]:
        """Load change from YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            return OpenSpecChange(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                author=data['author'],
                spec_type=SpecType(data['spec_type']),
                status=ChangeStatus(data['status']),
                content=data['content'],
                created_at=datetime.fromisoformat(data['created_at']),
                updated_at=datetime.fromisoformat(data['updated_at']),
                reviewed_by=data.get('reviewed_by'),
                reviewed_at=datetime.fromisoformat(data['reviewed_at']) if data.get('reviewed_at') else None,
                implemented_by=data.get('implemented_by'),
                implemented_at=datetime.fromisoformat(data['implemented_at']) if data.get('implemented_at') else None,
                tags=data.get('tags', []),
                priority=data.get('priority', 'medium'),
                dependencies=data.get('dependencies', [])
            )
        except Exception as e:
            logger.error(f"Error loading change from {file_path}: {e}")
            return None

    async def create_change_proposal(
        self,
        title: str,
        description: str,
        author: str,
        spec_type: SpecType,
        content: Dict[str, Any],
        priority: str = "medium",
        tags: List[str] = None,
        dependencies: List[str] = None
    ) -> str:
        """Create a new change proposal."""
        change_id = f"change_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        change = OpenSpecChange(
            id=change_id,
            title=title,
            description=description,
            author=author,
            spec_type=spec_type,
            status=ChangeStatus.PROPOSED,
            content=content,
            priority=priority,
            tags=tags or [],
            dependencies=dependencies or []
        )

        self.changes[change_id] = change
        await self._save_change(change)

        logger.info(f"Created change proposal: {change_id}")
        return change_id

    async def approve_change(self, change_id: str, reviewer: str) -> bool:
        """Approve a change proposal."""
        if change_id not in self.changes:
            return False

        change = self.changes[change_id]
        if change.status != ChangeStatus.PROPOSED:
            return False

        change.status = ChangeStatus.APPROVED
        change.reviewed_by = reviewer
        change.reviewed_at = datetime.now()
        change.updated_at = datetime.now()

        await self._save_change(change)
        await self._move_change_file(change, "proposals", "approved")

        logger.info(f"Approved change: {change_id} by {reviewer}")
        return True

    async def implement_change(self, change_id: str, implementer: str) -> bool:
        """Mark a change as implemented."""
        if change_id not in self.changes:
            return False

        change = self.changes[change_id]
        if change.status != ChangeStatus.APPROVED:
            return False

        change.status = ChangeStatus.IMPLEMENTED
        change.implemented_by = implementer
        change.implemented_at = datetime.now()
        change.updated_at = datetime.now()

        await self._save_change(change)
        await self._move_change_file(change, "approved", "implemented")

        logger.info(f"Implemented change: {change_id} by {implementer}")
        return True

    async def reject_change(self, change_id: str, reviewer: str, reason: str) -> bool:
        """Reject a change proposal."""
        if change_id not in self.changes:
            return False

        change = self.changes[change_id]
        if change.status != ChangeStatus.PROPOSED:
            return False

        change.status = ChangeStatus.REJECTED
        change.reviewed_by = reviewer
        change.reviewed_at = datetime.now()
        change.updated_at = datetime.now()
        change.content['rejection_reason'] = reason

        await self._save_change(change)
        await self._move_change_file(change, "proposals", "rejected")

        logger.info(f"Rejected change: {change_id} by {reviewer}")
        return True

    async def create_document(
        self,
        title: str,
        content: Dict[str, Any],
        author: str,
        spec_type: SpecType,
        version: str = "1.0.0",
        tags: List[str] = None
    ) -> str:
        """Create a new OpenSpec document."""
        doc_id = f"{spec_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        document = OpenSpecDocument(
            id=doc_id,
            title=title,
            version=version,
            spec_type=spec_type,
            content=content,
            author=author,
            tags=tags or []
        )

        self.documents[doc_id] = document
        await self._save_document(document)

        logger.info(f"Created document: {doc_id}")
        return doc_id

    async def update_document(self, doc_id: str, content: Dict[str, Any], author: str, change_id: str = None) -> bool:
        """Update an existing document."""
        if doc_id not in self.documents:
            return False

        document = self.documents[doc_id]
        document.content = content
        document.updated_at = datetime.now()

        if change_id:
            document.change_history.append(change_id)

        await self._save_document(document)
        logger.info(f"Updated document: {doc_id}")
        return True

    async def _save_document(self, document: OpenSpecDocument):
        """Save document to file."""
        spec_dir = self.openspec_path / "specs" / document.spec_type.value
        file_path = spec_dir / f"{document.id}.yaml"

        data = asdict(document)
        data['spec_type'] = document.spec_type.value
        data['created_at'] = document.created_at.isoformat()
        data['updated_at'] = document.updated_at.isoformat()

        # Convert datetime objects in content
        data = self._convert_datetimes(data)

        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    async def _save_change(self, change: OpenSpecChange):
        """Save change to file."""
        status_dir = {
            ChangeStatus.PROPOSED: "proposals",
            ChangeStatus.APPROVED: "approved",
            ChangeStatus.IMPLEMENTED: "implemented",
            ChangeStatus.REJECTED: "rejected"
        }

        change_dir = self.openspec_path / "changes" / status_dir[change.status]
        file_path = change_dir / f"{change.id}.yaml"

        data = asdict(change)
        data['spec_type'] = change.spec_type.value
        data['status'] = change.status.value
        data['created_at'] = change.created_at.isoformat()
        data['updated_at'] = change.updated_at.isoformat()

        if change.reviewed_at:
            data['reviewed_at'] = change.reviewed_at.isoformat()
        if change.implemented_at:
            data['implemented_at'] = change.implemented_at.isoformat()

        # Convert datetime objects in content
        data = self._convert_datetimes(data)

        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    async def _move_change_file(self, change: OpenSpecChange, from_dir: str, to_dir: str):
        """Move change file between status directories."""
        from_path = self.openspec_path / "changes" / from_dir / f"{change.id}.yaml"
        to_path = self.openspec_path / "changes" / to_dir / f"{change.id}.yaml"

        if from_path.exists():
            from_path.rename(to_path)

    def _convert_datetimes(self, obj: Any) -> Any:
        """Convert datetime objects to ISO format strings."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._convert_datetimes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_datetimes(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return self._convert_datetimes(asdict(obj))
        else:
            return obj

    def get_document(self, doc_id: str) -> Optional[OpenSpecDocument]:
        """Get a document by ID."""
        return self.documents.get(doc_id)

    def get_change(self, change_id: str) -> Optional[OpenSpecChange]:
        """Get a change by ID."""
        return self.changes.get(change_id)

    def list_documents(self, spec_type: Optional[SpecType] = None) -> List[OpenSpecDocument]:
        """List documents, optionally filtered by type."""
        docs = list(self.documents.values())
        if spec_type:
            docs = [doc for doc in docs if doc.spec_type == spec_type]
        return docs

    def list_changes(self, status: Optional[ChangeStatus] = None) -> List[OpenSpecChange]:
        """List changes, optionally filtered by status."""
        changes = list(self.changes.values())
        if status:
            changes = [change for change in changes if change.status == status]
        return changes

    def search_documents(self, query: str) -> List[OpenSpecDocument]:
        """Search documents by content."""
        query_lower = query.lower()
        results = []

        for doc in self.documents.values():
            # Search in title, content, and tags
            if (query_lower in doc.title.lower() or
                any(query_lower in str(v).lower() for v in doc.content.values()) or
                any(query_lower in tag.lower() for tag in doc.tags)):
                results.append(doc)

        return results

    def get_pending_changes(self) -> List[OpenSpecChange]:
        """Get all pending change proposals."""
        return self.list_changes(ChangeStatus.PROPOSED)

    def get_document_history(self, doc_id: str) -> List[OpenSpecChange]:
        """Get change history for a document."""
        if doc_id not in self.documents:
            return []

        document = self.documents[doc_id]
        history = []

        for change_id in document.change_history:
            if change_id in self.changes:
                history.append(self.changes[change_id])

        return sorted(history, key=lambda c: c.created_at)

# Global OpenSpec manager instance
openspec_manager = OpenSpecManager()

def get_openspec_manager() -> OpenSpecManager:
    """Get the global OpenSpec manager instance."""
    return openspec_manager