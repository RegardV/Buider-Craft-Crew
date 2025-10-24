"""
AI Crew Builder Team - Builder Team Manager
Manages the complete Builder Team workflow and orchestration.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, asdict

from .agent import BaseAgent, AgentTask, get_coordinator
from .config import get_config
from ..agents.builder_agents import create_builder_team

logger = logging.getLogger(__name__)

@dataclass
class ProjectDefinition:
    """Represents a project definition for building an AI crew."""
    name: str
    description: str
    goal: str
    target_agents: List[Dict[str, Any]]
    technical_requirements: Dict[str, Any]
    success_metrics: List[str]
    timeline: str
    budget: float
    status: str = "defined"
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class BuilderSession:
    """Represents a builder team session."""
    id: str
    project: ProjectDefinition
    messages: List[Dict[str, Any]]
    tasks: List[AgentTask]
    status: str = "active"
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

class BuilderTeamManager:
    """Manages the Builder Team and project creation workflow."""

    def __init__(self):
        self.config = get_config()
        self.coordinator = get_coordinator()
        self.agents: Dict[str, BaseAgent] = {}
        self.sessions: Dict[str, BuilderSession] = {}
        self.active_session: Optional[str] = None

        # Callbacks for external integration
        self.message_callbacks: List[Callable] = []
        self.task_callbacks: List[Callable] = []

        # Initialize the team
        self._initialize_team()

    def _initialize_team(self):
        """Initialize all builder team agents."""
        logger.info("Initializing Builder Team...")

        # Create agents
        builder_agents = create_builder_team()
        for agent in builder_agents:
            self.agents[agent.name] = agent
            logger.info(f"Initialized agent: {agent.name}")

        # Start all agents
        asyncio.create_task(self._start_agents())

    async def _start_agents(self):
        """Start all agents."""
        for agent in self.agents.values():
            await agent.start()
            await asyncio.sleep(0.1)  # Small delay between starts

        logger.info("All Builder Team agents started")

    async def create_session(self, project_input: Dict[str, Any]) -> str:
        """Create a new builder session."""
        project = ProjectDefinition(
            name=project_input.get("name", "Untitled Project"),
            description=project_input.get("description", ""),
            goal=project_input.get("goal", ""),
            target_agents=project_input.get("target_agents", []),
            technical_requirements=project_input.get("technical_requirements", {}),
            success_metrics=project_input.get("success_metrics", []),
            timeline=project_input.get("timeline", ""),
            budget=project_input.get("budget", 0.0)
        )

        # Create session
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = BuilderSession(
            id=session_id,
            project=project,
            messages=[],
            tasks=[]
        )

        self.sessions[session_id] = session
        self.active_session = session_id

        logger.info(f"Created builder session: {session_id} for project: {project.name}")

        # Notify callbacks
        await self._notify_session_created(session)

        return session_id

    async def start_project_definition(self, user_input: str) -> str:
        """Start the project definition process."""
        if not self.active_session:
            # Create a temporary session
            await self.create_session({"name": "New Project", "description": user_input})

        session = self.sessions[self.active_session]

        # Add user message
        message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        }
        session.messages.append(message)

        # Get initial analysis from Product Strategist
        product_agent = self.agents["ProductStrategist"]

        prompt = f"""
I'd like to build an AI crew project. Here's my initial idea:

{user_input}

Please help me define this project by asking clarifying questions about:
1. Project goals and objectives
2. Target users and use cases
3. Required AI agents and their roles
4. Technical requirements
5. Success metrics

Be conversational and ask one question at a time to help me think through this systematically.
"""

        response = await product_agent.think(prompt)

        # Add agent response
        agent_message = {
            "role": "assistant",
            "agent": "ProductStrategist",
            "content": response,
            "timestamp": datetime.now().isoformat()
        }
        session.messages.append(agent_message)

        # Notify callbacks
        await self._notify_message_added(session, agent_message)

        return response

    async def process_user_input(self, user_input: str) -> str:
        """Process user input and generate coordinated response."""
        if not self.active_session:
            return await self.start_project_definition(user_input)

        session = self.sessions[self.active_session]

        # Add user message
        message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        }
        session.messages.append(message)

        # Determine which agents should respond
        relevant_agents = await self._determine_relevant_agents(user_input, session)

        # Get coordinated response
        if len(relevant_agents) == 1:
            # Single agent response
            agent = self.agents[relevant_agents[0]]
            response = await agent.think(user_input)
            agent_name = relevant_agents[0]
        else:
            # Multiple agent coordination
            coordinated_results = await self.coordinator.coordinate_task(
                user_input, relevant_agents
            )

            # Combine responses
            response = await self._combine_agent_responses(coordinated_results)
            agent_name = "Coordinator"

        # Add agent response
        agent_message = {
            "role": "assistant",
            "agent": agent_name,
            "content": response,
            "timestamp": datetime.now().isoformat()
        }
        session.messages.append(agent_message)
        session.updated_at = datetime.now()

        # Notify callbacks
        await self._notify_message_added(session, agent_message)

        return response

    async def _determine_relevant_agents(self, user_input: str, session: BuilderSession) -> List[str]:
        """Determine which agents should respond to user input."""
        input_lower = user_input.lower()

        # Keyword-based agent selection
        agent_keywords = {
            "ProductStrategist": [
                "strategy", "vision", "goal", "market", "business", "user", "requirement",
                "feature", "priority", "roadmap", "mvp", "stakeholder", "value"
            ],
            "TechnicalArchitect": [
                "technical", "architecture", "system", "design", "technology", "stack",
                "api", "database", "scalability", "performance", "security", "integration"
            ],
            "UXDesigner": [
                "ux", "design", "interface", "user experience", "workflow", "interaction",
                "wireframe", "prototype", "usability", "accessibility", "visual"
            ],
            "QualityEngineer": [
                "quality", "test", "testing", "qa", "automation", "standards", "review",
                "metrics", "reliability", "bug", "defect", "coverage"
            ],
            "DevOpsSpecialist": [
                "devops", "deployment", "infrastructure", "ci/cd", "monitoring", "security",
                "operations", "scaling", "performance", "backup", "recovery"
            ]
        }

        # Score agents based on keyword matches
        agent_scores = {}
        for agent, keywords in agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in input_lower)
            if score > 0:
                agent_scores[agent] = score

        # Return agents with highest scores
        if agent_scores:
            max_score = max(agent_scores.values())
            top_agents = [agent for agent, score in agent_scores.items() if score == max_score]
            return top_agents

        # Default: Product Strategist for general input
        return ["ProductStrategist"]

    async def _combine_agent_responses(self, responses: Dict[str, str]) -> str:
        """Combine responses from multiple agents into a coherent response."""
        combined = "Here's what the Builder Team thinks:\n\n"

        for agent_name, response in responses.items():
            combined += f"**{agent_name}:**\n{response}\n\n"

        return combined

    async def generate_project_specification(self, session_id: str) -> Dict[str, Any]:
        """Generate complete project specification from session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Get final analysis from all agents
        spec_tasks = {}
        for agent_name, agent in self.agents.items():
            task = AgentTask(
                description=f"Generate final specification for {session.project.name}",
                context={
                    "session_messages": session.messages,
                    "project": asdict(session.project),
                    "agent_role": agent.role
                }
            )

            await agent.assign_task(task)
            spec_tasks[agent_name] = task

        # Wait for all tasks to complete
        for agent_name, task in spec_tasks.items():
            while task.status not in ["completed", "error"]:
                await asyncio.sleep(0.1)

        # Combine specifications
        specification = {
            "project": asdict(session.project),
            "session_summary": {
                "id": session.id,
                "message_count": len(session.messages),
                "duration": (datetime.now() - session.created_at).total_seconds(),
                "status": session.status
            },
            "agent_specifications": {}
        }

        for agent_name, task in spec_tasks.items():
            if task.result:
                specification["agent_specifications"][agent_name] = task.result

        # Add final coordination summary
        coordinator_summary = await self.coordinator.think(
            f"Please provide a final summary and integration plan for this project specification: {session.project.name}"
        )
        specification["coordinator_summary"] = coordinator_summary

        return specification

    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of a builder session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        return {
            "session": {
                "id": session.id,
                "status": session.status,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
                "message_count": len(session.messages)
            },
            "project": asdict(session.project),
            "agents": {
                name: agent.get_status() for name, agent in self.agents.items()
            }
        }

    async def list_sessions(self) -> List[Dict[str, Any]]:
        """List all builder sessions."""
        sessions = []
        for session_id, session in self.sessions.items():
            sessions.append({
                "id": session_id,
                "project_name": session.project.name,
                "status": session.status,
                "created_at": session.created_at.isoformat(),
                "message_count": len(session.messages)
            })

        return sessions

    def add_message_callback(self, callback: Callable):
        """Add callback for message events."""
        self.message_callbacks.append(callback)

    def add_task_callback(self, callback: Callable):
        """Add callback for task events."""
        self.task_callbacks.append(callback)

    async def _notify_session_created(self, session: BuilderSession):
        """Notify callbacks about session creation."""
        for callback in self.message_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback("session_created", session)
                else:
                    callback("session_created", session)
            except Exception as e:
                logger.error(f"Error in session created callback: {e}")

    async def _notify_message_added(self, session: BuilderSession, message: Dict[str, Any]):
        """Notify callbacks about new message."""
        for callback in self.message_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback("message_added", session, message)
                else:
                    callback("message_added", session, message)
            except Exception as e:
                logger.error(f"Error in message added callback: {e}")

    async def shutdown(self):
        """Shutdown the builder team."""
        logger.info("Shutting down Builder Team...")

        for agent in self.agents.values():
            await agent.stop()

        self.agents.clear()
        self.sessions.clear()
        self.active_session = None

        logger.info("Builder Team shutdown complete")

# Global builder team manager instance
builder_team_manager = BuilderTeamManager()

def get_builder_team_manager() -> BuilderTeamManager:
    """Get the global builder team manager instance."""
    return builder_team_manager