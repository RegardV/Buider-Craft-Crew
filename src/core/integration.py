"""
AI Crew Builder Team - Integration Layer
Integrates OpenSpec, Builder Team, and Project Generator.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .config import get_config
from .openspec import get_openspec_manager, SpecType, ChangeStatus
from .builder_team import get_builder_team_manager
from .project_generator import get_project_generator

logger = logging.getLogger(__name__)

class BuilderTeamIntegration:
    """Main integration layer for the Builder Team system."""

    def __init__(self):
        self.config = get_config()
        self.openspec = get_openspec_manager()
        self.builder_team = get_builder_team_manager()
        self.project_generator = get_project_generator()

    async def initialize(self):
        """Initialize the integration system."""
        logger.info("Initializing Builder Team Integration...")

        # Ensure directories exist
        self._ensure_directories()

        # Initialize components
        await self._initialize_openspec()
        await self._initialize_builder_team()

        logger.info("Builder Team Integration initialized successfully")

    def _ensure_directories(self):
        """Ensure required directories exist."""
        directories = [
            "logs",
            "data",
            "generated_projects",
            "backups",
            "cache"
        ]

        project_root = Path(self.config.openspec_path).parent
        for directory in directories:
            dir_path = project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)

    async def _initialize_openspec(self):
        """Initialize OpenSpec system."""
        # Create initial system specification if it doesn't exist
        existing_docs = self.openspec.list_documents(SpecType.SYSTEM)
        if not existing_docs:
            await self._create_initial_system_spec()

    async def _initialize_builder_team(self):
        """Initialize Builder Team."""
        # Builder team is initialized in its constructor
        pass

    async def _create_initial_system_spec(self):
        """Create initial system specification."""
        system_spec_content = {
            "system_overview": {
                "name": "AI Crew Builder Team",
                "description": "A system for building AI crew projects using AI",
                "version": "1.0.0",
                "created": datetime.now().isoformat()
            },
            "architecture": {
                "builder_team": {
                    "product_strategist": {"provider": "claude", "role": "strategic_planning"},
                    "technical_architect": {"provider": "claude", "role": "system_design"},
                    "ux_designer": {"provider": "claude", "role": "user_experience"},
                    "quality_engineer": {"provider": "zhipuai", "role": "quality_assurance"},
                    "devops_specialist": {"provider": "zhipuai", "role": "infrastructure"}
                },
                "project_crews": {
                    "provider": "openai",
                    "framework": "crewai"
                }
            },
            "workflows": {
                "project_definition": "Interactive project definition with Builder Team",
                "specification_generation": "OpenSpec-based specification creation",
                "project_generation": "Automated project code generation",
                "quality_assurance": "Review and validation processes"
            },
            "integration_points": {
                "ai_providers": ["anthropic", "zhipuai", "openai"],
                "specification_framework": "openspec",
                "project_framework": "crewai",
                "deployment": "docker"
            }
        }

        await self.openspec.create_document(
            title="AI Crew Builder Team - System Overview",
            content=system_spec_content,
            author="System",
            spec_type=SpecType.SYSTEM,
            version="1.0.0",
            tags=["system", "builder-team", "initial"]
        )

    async def start_project_session(self, project_input: Dict[str, Any]) -> str:
        """Start a new project building session."""
        logger.info(f"Starting project session for: {project_input.get('name', 'Untitled')}")

        # Create Builder Team session
        session_id = await self.builder_team.create_session(project_input)

        # Create OpenSpec change proposal for the project
        change_id = await self.openspec.create_change_proposal(
            title=f"Project Definition: {project_input.get('name', 'Untitled')}",
            description=f"Define and build AI crew project: {project_input.get('description', '')}",
            author="User",
            spec_type=SpecType.FEATURE,
            content={
                "project_input": project_input,
                "session_id": session_id,
                "status": "in_progress",
                "created": datetime.now().isoformat()
            },
            tags=["project", "definition", session_id]
        )

        # Store change ID in session context
        session = self.builder_team.sessions[session_id]
        session.add_memory("openspec_change_id", change_id)

        return session_id

    async def process_user_input(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Process user input and return coordinated response."""
        logger.info(f"Processing input for session {session_id}: {user_input[:100]}...")

        # Get response from Builder Team
        response = await self.builder_team.process_user_input(user_input)

        # Create OpenSpec change for significant interactions
        if self._should_create_change(user_input):
            await self._create_interaction_change(session_id, user_input, response)

        return {
            "session_id": session_id,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }

    def _should_create_change(self, user_input: str) -> bool:
        """Determine if user input should create an OpenSpec change."""
        # Create changes for significant inputs
        significant_keywords = [
            "requirement", "feature", "change", "modify", "add", "remove",
            "decision", "approve", "implement", "design", "architecture"
        ]

        return any(keyword in user_input.lower() for keyword in significant_keywords)

    async def _create_interaction_change(self, session_id: str, user_input: str, response: str):
        """Create OpenSpec change for user interaction."""
        session = self.builder_team.sessions[session_id]

        await self.openspec.create_change_proposal(
            title=f"Project Update: {session.project.name}",
            description=f"User input and Builder Team response",
            author="User",
            spec_type=SpecType.CHANGE,
            content={
                "session_id": session_id,
                "user_input": user_input,
                "builder_response": response,
                "timestamp": datetime.now().isoformat()
            },
            tags=["interaction", "update", session_id]
        )

    async def generate_project_specification(self, session_id: str) -> Dict[str, Any]:
        """Generate complete project specification."""
        logger.info(f"Generating specification for session {session_id}")

        # Get specification from Builder Team
        project_spec = await self.builder_team.generate_project_specification(session_id)

        # Create OpenSpec document for the project
        session = self.builder_team.sessions[session_id]
        doc_id = await self.openspec.create_document(
            title=f"{session.project.name} - Project Specification",
            content=project_spec,
            author="Builder Team",
            spec_type=SpecType.SYSTEM,
            version="1.0.0",
            tags=["project", "specification", session_id]
        )

        # Update the original change proposal
        change_id = session.get_memory("openspec_change_id")
        if change_id and change_id in self.openspec.changes:
            await self.openspec.approve_change(change_id, "Builder Team")

        return {
            "specification": project_spec,
            "document_id": doc_id,
            "session_id": session_id,
            "generated_at": datetime.now().isoformat()
        }

    async def generate_project(self, session_id: str, output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Generate complete project from specification."""
        logger.info(f"Generating project for session {session_id}")

        # Get project specification
        spec_result = await self.generate_project_specification(session_id)
        project_spec = spec_result["specification"]

        # Generate the project
        generation_result = await self.project_generator.generate_project(project_spec, output_dir)

        # Create OpenSpec change for project generation
        await self.openspec.create_change_proposal(
            title=f"Project Generated: {generation_result['project_name']}",
            description=f"Complete AI crew project generated and saved",
            author="Builder Team",
            spec_type=SpecType.CHANGE,
            content={
                "session_id": session_id,
                "generation_result": generation_result,
                "specification_id": spec_result["document_id"],
                "timestamp": datetime.now().isoformat()
            },
            tags=["generation", "project", session_id],
            priority="high"
        )

        return {
            "generation_result": generation_result,
            "specification_result": spec_result,
            "session_id": session_id,
            "completed_at": datetime.now().isoformat()
        }

    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session status."""
        builder_status = await self.builder_team.get_session_status(session_id)

        # Add OpenSpec information
        session = self.builder_team.sessions.get(session_id)
        if session:
            change_id = session.get_memory("openspec_change_id")
            related_changes = self.openspec.list_changes()
            project_changes = [c for c in related_changes if session_id in c.tags]

            builder_status["openspec"] = {
                "main_change_id": change_id,
                "related_changes_count": len(project_changes),
                "latest_changes": [
                    {
                        "id": c.id,
                        "title": c.title,
                        "status": c.status.value,
                        "created": c.created_at.isoformat()
                    }
                    for c in project_changes[-5:]  # Last 5 changes
                ]
            }

        return builder_status

    async def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions with additional metadata."""
        sessions = await self.builder_team.list_sessions()

        # Add OpenSpec metadata to each session
        for session in sessions:
            session_changes = [c for c in self.openspec.list_changes() if session["id"] in c.tags]
            session["openspec_changes"] = len(session_changes)
            session["last_activity"] = max(
                [datetime.fromisoformat(c["created"]) for c in session_changes] or [datetime.now()]
            ).isoformat()

        return sessions

    async def shutdown(self):
        """Shutdown the integration system."""
        logger.info("Shutting down Builder Team Integration...")

        await self.builder_team.shutdown()
        logger.info("Builder Team Integration shutdown complete")

# Global integration instance
integration = BuilderTeamIntegration()

def get_integration() -> BuilderTeamIntegration:
    """Get the global integration instance."""
    return integration