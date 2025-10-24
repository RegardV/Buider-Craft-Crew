"""
AI Crew Builder Team - Base Agent Class
Defines the base functionality for all Builder Team agents.
"""

import asyncio
import json
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from .ai_providers import Message, AIResponse, get_provider_manager
from .config import get_config

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    RESPONDING = "responding"
    ERROR = "error"

@dataclass
class AgentTask:
    """Represents a task assigned to an agent."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "pending"
    result: Optional[str] = None
    error: Optional[str] = None

@dataclass
class AgentMemory:
    """Agent memory for context retention."""
    short_term: List[Message] = field(default_factory=list)
    long_term: Dict[str, Any] = field(default_factory=dict)
    context_window: int = 10

class BaseAgent(ABC):
    """Base class for all Builder Team agents."""

    def __init__(
        self,
        name: str,
        role: str,
        mbti: str,
        provider: str,
        responsibilities: List[str],
        system_prompt: Optional[str] = None
    ):
        self.name = name
        self.role = role
        self.mbti = mbti
        self.provider = provider
        self.responsibilities = responsibilities
        self.system_prompt = system_prompt or self._generate_system_prompt()

        # State management
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.memory = AgentMemory()

        # Configuration
        self.config = get_config()
        self.provider_manager = get_provider_manager()

        # Event handlers
        self.message_handlers: Dict[str, Callable] = {}
        self.task_handlers: Dict[str, Callable] = {}

        # Statistics
        self.tasks_completed = 0
        self.total_response_time = 0
        self.error_count = 0

        logger.info(f"Initialized agent: {self.name} ({self.role}) using {provider}")

    def _generate_system_prompt(self) -> str:
        """Generate default system prompt for the agent."""
        prompt = f"""You are {self.name}, a {self.role} AI agent.

Your MBTI personality type is {self.mbti}, which influences your approach to problem-solving and communication.

Your core responsibilities:
{chr(10).join(f"- {resp}" for resp in self.responsibilities)}

Guidelines for your responses:
1. Always consider your personality type ({self.mbti}) in your approach
2. Provide clear, actionable advice and solutions
3. Consider the broader project context and team coordination
4. Ask clarifying questions when requirements are ambiguous
5. Document your decisions and reasoning process
6. Collaborate effectively with other team members

Project Context:
You are part of the AI Crew Builder Team, responsible for helping users build and design AI crew projects.
Your role is to provide expert guidance and execute tasks within your domain of expertise.

Communication Style:
- Be professional but approachable
- Provide structured, well-reasoned responses
- Consider practical implementation details
- Focus on delivering value and progress

Always maintain your role's perspective while considering the overall project success."""

        return prompt

    async def start(self):
        """Start the agent's main processing loop."""
        logger.info(f"Starting agent: {self.name}")
        asyncio.create_task(self._process_tasks())

    async def stop(self):
        """Stop the agent."""
        logger.info(f"Stopping agent: {self.name}")
        self.status = AgentStatus.IDLE

    async def assign_task(self, task: AgentTask) -> str:
        """Assign a task to the agent."""
        task.assigned_at = datetime.now()
        await self.task_queue.put(task)
        logger.info(f"Task assigned to {self.name}: {task.description}")
        return task.id

    async def _process_tasks(self):
        """Main task processing loop."""
        while True:
            try:
                # Wait for a task
                self.current_task = await self.task_queue.get()
                self.current_task.started_at = datetime.now()
                self.status = AgentStatus.THINKING

                logger.info(f"{self.name} processing task: {self.current_task.description}")

                # Process the task
                result = await self._process_task(self.current_task)

                # Update task status
                self.current_task.status = "completed"
                self.current_task.result = result
                self.current_task.completed_at = datetime.now()
                self.tasks_completed += 1

                # Calculate response time
                if self.current_task.started_at:
                    response_time = (datetime.now() - self.current_task.started_at).total_seconds()
                    self.total_response_time += response_time

                self.status = AgentStatus.IDLE
                self.current_task = None

                # Mark task as done
                self.task_queue.task_done()

            except Exception as e:
                logger.error(f"Error in {self.name} task processing: {e}")
                if self.current_task:
                    self.current_task.status = "error"
                    self.current_task.error = str(e)
                    self.error_count += 1
                self.status = AgentStatus.ERROR

    @abstractmethod
    async def _process_task(self, task: AgentTask) -> str:
        """Process a specific task. Must be implemented by subclasses."""
        pass

    async def think(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response using the AI provider."""
        try:
            self.status = AgentStatus.THINKING

            # Prepare messages
            messages = [
                Message(role="system", content=self.system_prompt)
            ]

            # Add memory context
            if self.memory.short_term:
                messages.extend(self.memory.short_term[-self.memory.context_window:])

            # Add current prompt
            user_message = Message(role="user", content=prompt)
            messages.append(user_message)

            # Generate response
            response = await self.provider_manager.generate_response(
                self.provider, messages
            )

            # Update memory
            self.memory.short_term.append(user_message)
            self.memory.short_term.append(Message(role="assistant", content=response.content))

            # Trim memory if too long
            if len(self.memory.short_term) > self.memory.context_window * 2:
                self.memory.short_term = self.memory.short_term[-self.memory.context_window:]

            self.status = AgentStatus.IDLE
            return response.content

        except Exception as e:
            logger.error(f"Error in {self.name} thinking: {e}")
            self.status = AgentStatus.ERROR
            raise

    async def think_stream(self, prompt: str, context: Optional[Dict[str, Any]] = None):
        """Generate a streaming response."""
        try:
            self.status = AgentStatus.RESPONDING

            # Prepare messages
            messages = [
                Message(role="system", content=self.system_prompt)
            ]

            # Add memory context
            if self.memory.short_term:
                messages.extend(self.memory.short_term[-self.memory.context_window:])

            # Add current prompt
            user_message = Message(role="user", content=prompt)
            messages.append(user_message)

            # Generate streaming response
            full_response = ""
            async for chunk in self.provider_manager.generate_stream(
                self.provider, messages
            ):
                full_response += chunk
                yield chunk

            # Update memory
            self.memory.short_term.append(user_message)
            self.memory.short_term.append(Message(role="assistant", content=full_response))

            # Trim memory if too long
            if len(self.memory.short_term) > self.memory.context_window * 2:
                self.memory.short_term = self.memory.short_term[-self.memory.context_window:]

            self.status = AgentStatus.IDLE

        except Exception as e:
            logger.error(f"Error in {self.name} streaming: {e}")
            self.status = AgentStatus.ERROR
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "name": self.name,
            "role": self.role,
            "mbti": self.mbti,
            "provider": self.provider,
            "status": self.status.value,
            "current_task": self.current_task.description if self.current_task else None,
            "queue_size": self.task_queue.qsize(),
            "tasks_completed": self.tasks_completed,
            "average_response_time": (
                self.total_response_time / self.tasks_completed
                if self.tasks_completed > 0 else 0
            ),
            "error_count": self.error_count,
            "memory_size": len(self.memory.short_term)
        }

    def clear_memory(self):
        """Clear agent's short-term memory."""
        self.memory.short_term.clear()
        logger.info(f"Cleared memory for {self.name}")

    def add_memory(self, key: str, value: Any):
        """Add information to long-term memory."""
        self.memory.long_term[key] = value

    def get_memory(self, key: str) -> Any:
        """Get information from long-term memory."""
        return self.memory.long_term.get(key)

class CoordinatorAgent(BaseAgent):
    """Special agent for coordinating between other agents."""

    def __init__(self):
        super().__init__(
            name="Coordinator",
            role="Team Coordination and Orchestration",
            mbti="ENTJ",
            provider="claude",
            responsibilities=[
                "Coordinate between advisory team members",
                "Manage task distribution and prioritization",
                "Ensure team communication and collaboration",
                "Monitor overall project progress"
            ]
        )
        self.team_members: Dict[str, BaseAgent] = {}

    def add_team_member(self, agent: BaseAgent):
        """Add a team member to coordinate."""
        self.team_members[agent.name] = agent
        logger.info(f"Added team member: {agent.name}")

    async def coordinate_task(self, task_description: str, target_agents: List[str] = None) -> Dict[str, str]:
        """Coordinate a task across multiple agents."""
        if not target_agents:
            target_agents = list(self.team_members.keys())

        results = {}

        # Create tasks for target agents
        tasks = []
        for agent_name in target_agents:
            if agent_name in self.team_members:
                agent = self.team_members[agent_name]
                task = AgentTask(
                    description=f"Coordination task: {task_description}",
                    context={"coordinator": self.name, "original_task": task_description}
                )
                tasks.append((agent, task))

        # Execute tasks concurrently
        if tasks:
            await asyncio.gather(*[
                agent.assign_task(task) for agent, task in tasks
            ])

            # Wait for completion and collect results
            await asyncio.gather(*[
                self._wait_for_task_completion(agent, task) for agent, task in tasks
            ])

            for agent, task in tasks:
                results[agent.name] = task.result or "No result provided"

        return results

    async def _wait_for_task_completion(self, agent: BaseAgent, task: AgentTask):
        """Wait for a task to complete."""
        while task.status not in ["completed", "error"]:
            await asyncio.sleep(0.1)

    async def _process_task(self, task: AgentTask) -> str:
        """Process coordination tasks."""
        # For now, just think about the task
        result = await self.think(f"Please help coordinate this task: {task.description}")
        return result

# Global coordinator instance
coordinator = CoordinatorAgent()

def get_coordinator() -> CoordinatorAgent:
    """Get the global coordinator instance."""
    return coordinator