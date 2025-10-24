"""
AI Crew Builder Team - Project Generator
Automated project generation from Builder Team specifications.
"""

import os
import json
import yaml
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Template, Environment, FileSystemLoader

from .config import get_config
from .openspec import get_openspec_manager, SpecType, ChangeStatus
from .builder_team import get_builder_team_manager

logger = logging.getLogger(__name__)

class ProjectGenerator:
    """Generates complete AI crew projects from Builder Team specifications."""

    def __init__(self):
        self.config = get_config()
        self.openspec = get_openspec_manager()
        self.builder_team = get_builder_team_manager()
        self.template_env = Environment(
            loader=FileSystemLoader(
                str(Path(__file__).parent.parent.parent / "templates")
            )
        )

    async def generate_project(
        self,
        project_spec: Dict[str, Any],
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Generate a complete AI crew project from specifications."""
        if output_dir is None:
            output_dir = Path.cwd() / "generated_projects"

        project_name = project_spec["project"]["name"]
        project_dir = output_dir / project_name.lower().replace(" ", "_")

        logger.info(f"Generating project: {project_name} at {project_dir}")

        # Create project structure
        await self._create_project_structure(project_dir, project_spec)

        # Generate configuration files
        await self._generate_configurations(project_dir, project_spec)

        # Generate agent implementations
        await self._generate_agents(project_dir, project_spec)

        # Generate workflows
        await self._generate_workflows(project_dir, project_spec)

        # Generate documentation
        await self._generate_documentation(project_dir, project_spec)

        # Generate OpenSpec documentation
        await self._generate_openspec_docs(project_dir, project_spec)

        # Create initialization scripts
        await self._generate_scripts(project_dir, project_spec)

        # Create Git repository
        await self._initialize_git_repo(project_dir)

        result = {
            "project_name": project_name,
            "project_dir": str(project_dir),
            "generated_at": datetime.now().isoformat(),
            "files_created": self._count_files(project_dir),
            "specifications": self._extract_specifications(project_spec)
        }

        logger.info(f"Project generation completed: {project_name}")
        return result

    async def _create_project_structure(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Create the basic project directory structure."""
        directories = [
            "config",
            "src",
            "src/agents",
            "src/workflows",
            "src/tools",
            "src/core",
            "tests",
            "tests/unit",
            "tests/integration",
            "docs",
            "scripts",
            "logs",
            "data",
            ".openspec/specs/agents",
            ".openspec/specs/workflows",
            ".openspec/specs/features",
            ".openspec/specs/system",
            ".openspec/changes/proposals",
            ".openspec/changes/approved",
            ".openspec/changes/implemented",
            "templates"
        ]

        for directory in directories:
            dir_path = project_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)

    async def _generate_configurations(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Generate project configuration files."""
        project_data = project_spec["project"]

        # Main project configuration
        config_data = {
            "project": {
                "name": project_data["name"],
                "description": project_data["description"],
                "version": "1.0.0",
                "created": datetime.now().strftime("%Y-%m-%d")
            },
            "ai_provider": {
                "name": "openai",
                "model": project_spec.get("openai_model", "gpt-4-turbo-preview"),
                "api_key_env": "OPENAI_API_KEY"
            },
            "agents": {},
            "workflows": {},
            "settings": {
                "log_level": "INFO",
                "max_concurrent_agents": 5,
                "timeout": 300
            }
        }

        # Add agent configurations
        for agent_spec in project_data.get("target_agents", []):
            agent_name = agent_spec["name"].lower().replace(" ", "_")
            config_data["agents"][agent_name] = {
                "name": agent_spec["name"],
                "role": agent_spec["role"],
                "goal": f"Execute {agent_spec['role'].lower()} tasks",
                "backstory": f"You are {agent_spec['name']}, a specialized {agent_spec['role']} AI agent.",
                "responsibilities": agent_spec.get("responsibilities", []),
                "tools": ["file_operations", "web_search"],
                "allow_delegation": True,
                "verbose": True
            }

        # Save configuration
        config_file = project_dir / "config" / "project.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        # Environment file template
        env_content = f"""# {project_data['name']} Environment Configuration
# Copy this file to .env and fill in your API keys

# AI Provider Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Project Configuration
PROJECT_NAME={project_data['name']}
PROJECT_VERSION=1.0.0
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/project.log

# Performance
MAX_CONCURRENT_AGENTS={len(config_data['agents'])}
AGENT_TIMEOUT=300
"""

        env_file = project_dir / ".env.example"
        with open(env_file, 'w') as f:
            f.write(env_content)

    async def _generate_agents(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Generate Python agent implementations."""
        agents_dir = project_dir / "src" / "agents"

        # Create base agent class
        base_agent_code = '''"""
Base Agent Implementation
Generated by AI Crew Builder Team
"""

import asyncio
import logging
from typing import Dict, List, Any
from crewai import Agent, Task, Crew

logger = logging.getLogger(__name__)

class BaseProjectAgent:
    """Base class for project agents."""

    def __init__(self, name: str, role: str, goal: str, backstory: str, tools: List[str]):
        self.name = name
        self.role = role
        self.goal = goal
        self.backdrop = backstory
        self.tools = tools
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Create CrewAI agent."""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backdrop,
            tools=self.tools,
            verbose=True,
            allow_delegation=True
        )

    def create_task(self, description: str, **kwargs) -> Task:
        """Create a task for this agent."""
        return Task(
            description=description,
            agent=self.agent,
            **kwargs
        )
'''

        base_file = agents_dir / "base_agent.py"
        with open(base_file, 'w') as f:
            f.write(base_agent_code)

        # Generate individual agents
        project_data = project_spec["project"]
        for agent_spec in project_data.get("target_agents", []):
            agent_name = agent_spec["name"].lower().replace(" ", "_")
            agent_code = f'''"""
{agent_spec["name"]} Implementation
Generated by AI Crew Builder Team
"""

from .base_agent import BaseProjectAgent
from typing import List

class {agent_spec["name"].replace(" ", "")}Agent(BaseProjectAgent):
    """{agent_spec["role"]} agent implementation."""

    def __init__(self):
        super().__init__(
            name="{agent_spec["name"]}",
            role="{agent_spec["role"]}",
            goal="Execute {agent_spec['role'].lower()} tasks for the project",
            backstory=f'''You are {agent_spec["name"]}, a specialized {agent_spec["role"]} AI agent working on this project.

Your expertise includes:
{chr(10).join(f"- {resp}" for resp in agent_spec.get("responsibilities", []))}''',
            tools=["file_operations", "web_search", "data_analysis"]
        )

    def create_{agent_name}_task(self, task_description: str) -> 'Task':
        """Create a specialized task for this agent."""
        return self.create_task(
            description=f"""As the {agent_spec["role"]}, {task_description}

Focus on delivering high-quality results that align with the project goals.
Consider dependencies and coordinate with other team members as needed.""",
            expected_output="Detailed results with clear action items and next steps."
        )
'''

            agent_file = agents_dir / f"{agent_name}_agent.py"
            with open(agent_file, 'w') as f:
                f.write(agent_code)

        # Create __init__.py
        init_file = agents_dir / "__init__.py"
        with open(init_file, 'w') as f:
            f.write('"""Project Agents Implementation*/\n\n')
            for agent_spec in project_data.get("target_agents", []):
                agent_name = agent_spec["name"].lower().replace(" ", "_")
                f.write(f'from .{agent_name}_agent import {agent_spec["name"].replace(" ", "")}Agent\n')

    async def _generate_workflows(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Generate workflow implementations."""
        workflows_dir = project_dir / "src" / "workflows"

        # Main workflow
        workflow_code = f'''"""
Main Workflow Implementation
Generated by AI Crew Builder Team
"""

import asyncio
from typing import List, Dict, Any
from crewai import Crew, Task

from ..agents import *
from ..core.config import get_config

class MainWorkflow:
    """Main workflow for the project."""

    def __init__(self):
        self.config = get_config()
        self.agents = self._initialize_agents()
        self.crew = self._create_crew()

    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents."""
        agents = {{}}

        # Initialize agents based on project configuration
'''

        project_data = project_spec["project"]
        for agent_spec in project_data.get("target_agents", []):
            agent_class_name = agent_spec["name"].replace(" ", "")
            workflow_code += f'''
        agents["{agent_spec["name"].lower().replace(" ", "_")}"] = {agent_class_name}Agent()
'''

        workflow_code += '''

        return agents

    def _create_crew(self) -> Crew:
        """Create the crew with all agents."""
        return Crew(
            agents=list(self.agents.values()),
            verbose=True,
            process="sequential"  # or "hierarchical" if you want a manager
        )

    async def execute_workflow(self, task_description: str) -> Dict[str, Any]:
        """Execute the main workflow."""
        # Create tasks for each agent
        tasks = []

        for agent_name, agent in self.agents.items():
            task = agent.create_task(f"Execute: {task_description}")
            tasks.append(task)

        # Execute the workflow
        result = self.crew.kickoff(tasks=tasks)

        return {
            "status": "completed",
            "result": result,
            "agents_involved": list(self.agents.keys()),
            "timestamp": datetime.now().isoformat()
        }

    def create_custom_workflow(self, workflow_config: Dict[str, Any]) -> 'Workflow':
        """Create a custom workflow based on configuration."""
        # Implementation for custom workflows
        pass
'''

        workflow_file = workflows_dir / "main_workflow.py"
        with open(workflow_file, 'w') as f:
            f.write(workflow_code)

        # Create __init__.py
        init_file = workflows_dir / "__init__.py"
        with open(init_file, 'w') as f:
            f.write('"""Workflow Implementations*/\n\nfrom .main_workflow import MainWorkflow\n')

    async def _generate_documentation(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Generate project documentation."""
        docs_dir = project_dir / "docs"

        # README.md
        readme_content = f'''# {project_spec["project"]["name"]}

{project_spec["project"]["description"]}

## Overview

This AI crew project was generated by the AI Crew Builder Team. It includes:

### AI Agents
{chr(10).join(f"- **{agent['name']}**: {agent['role']}" for agent in project_spec["project"].get("target_agents", []))}

### Capabilities
- Intelligent task execution
- Multi-agent coordination
- Workflow automation
- Real-time processing

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Project

```bash
python main.py
```

## Configuration

The project configuration is in `config/project.yaml`. You can modify:

- Agent roles and responsibilities
- Workflow parameters
- AI provider settings
- Performance settings

## Documentation

- [Agent Documentation](docs/agents.md)
- [Workflow Documentation](docs/workflows.md)
- [API Reference](docs/api.md)

## Support

Generated by AI Crew Builder Team
Built with Claude + ZhipuAI + OpenAI
'''

        readme_file = project_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)

        # Requirements.txt
        requirements_content = '''# AI Crew Builder Team Generated Project

# Core AI Framework
crewai>=0.55.0
crewai-tools>=0.10.0

# AI Providers
openai>=1.10.0
anthropic>=0.34.0

# Data and Configuration
pydantic>=2.5.0
pyyaml>=6.0.1
python-dotenv>=1.0.0

# Utilities
asyncio
requests>=2.31.0
loguru>=0.7.0

# Development
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.11.0
'''

        requirements_file = project_dir / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write(requirements_content)

    async def _generate_openspec_docs(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Generate OpenSpec documentation for the project."""
        openspec_dir = project_dir / ".openspec"

        # Create system overview
        system_spec = {
            "id": f"system_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": f"{project_spec['project']['name']} - System Overview",
            "version": "1.0.0",
            "spec_type": "system",
            "content": {
                "project_overview": {
                    "name": project_spec["project"]["name"],
                    "description": project_spec["project"]["description"],
                    "goal": project_spec["project"]["goal"],
                    "created": datetime.now().isoformat()
                },
                "architecture": {
                    "agents": project_spec["project"].get("target_agents", []),
                    "workflows": ["main_workflow"],
                    "tools": ["file_operations", "web_search", "data_analysis"],
                    "ai_provider": "openai"
                },
                "technical_requirements": project_spec["project"].get("technical_requirements", {}),
                "success_metrics": project_spec["project"].get("success_metrics", [])
            },
            "author": "AI Crew Builder Team",
            "tags": ["generated", "crew", "ai"]
        }

        system_file = openspec_dir / "specs" / "system" / f"{system_spec['id']}.yaml"
        with open(system_file, 'w') as f:
            yaml.dump(system_spec, f, default_flow_style=False, sort_keys=False)

        # Create agent specifications
        for agent_spec in project_spec["project"].get("target_agents", []):
            agent_spec_doc = {
                "id": f"agent_{agent_spec['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "title": f"{agent_spec['name']} - Agent Specification",
                "version": "1.0.0",
                "spec_type": "agent",
                "content": {
                    "agent": agent_spec,
                    "implementation": f"src/agents/{agent_spec['name'].lower().replace(' ', '_')}_agent.py",
                    "tools": ["file_operations", "web_search", "data_analysis"],
                    "integration": "Integrated into main workflow"
                },
                "author": "AI Crew Builder Team",
                "tags": ["generated", "agent", "specification"]
            }

            agent_file = openspec_dir / "specs" / "agents" / f"{agent_spec_doc['id']}.yaml"
            with open(agent_file, 'w') as f:
                yaml.dump(agent_spec_doc, f, default_flow_style=False, sort_keys=False)

    async def _generate_scripts(self, project_dir: Path, project_spec: Dict[str, Any]):
        """Generate utility scripts."""
        scripts_dir = project_dir / "scripts"

        # Main script
        main_script_content = f'''"""
Main entry point for {project_spec["project"]["name"]}
Generated by AI Crew Builder Team
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from workflows.main_workflow import MainWorkflow
from core.config import get_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point."""
    config = get_config()

    logger.info(f"Starting {{config.project_name}}")

    try:
        # Initialize workflow
        workflow = MainWorkflow()

        # Example task execution
        task_description = "Process the main project workflow"
        result = await workflow.execute_workflow(task_description)

        logger.info("Workflow completed successfully")
        logger.info(f"Result: {{result}}")

    except Exception as e:
        logger.error(f"Error executing workflow: {{e}}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
'''

        main_file = project_dir / "main.py"
        with open(main_file, 'w') as f:
            f.write(main_script_content)

        # Setup script
        setup_script_content = '''#!/usr/bin/env python3
"""
Setup script for the generated project
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    """Setup the project environment."""
    print("🚀 Setting up project environment...")

    # Create virtual environment
    if not Path(".venv").exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])

    # Install dependencies
    print("Installing dependencies...")
    subprocess.run([".venv/bin/pip" if os.name != "nt" else ".venv\\Scripts\\pip.exe", "install", "-r", "requirements.txt"])

    print("✅ Setup completed!")
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    if os.name == "nt":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("2. Copy .env.example to .env and add your API keys")
    print("3. Run: python main.py")

if __name__ == "__main__":
    main()
'''

        setup_file = scripts_dir / "setup.py"
        with open(setup_file, 'w') as f:
            f.write(setup_script_content)

        # Make setup script executable
        os.chmod(setup_file, 0o755)

    async def _initialize_git_repo(self, project_dir: Path):
        """Initialize Git repository for the generated project."""
        try:
            # Initialize git repository
            subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)

            # Create .gitignore
            gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# Environment
.env
.env.local

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Generated files
output/
temp/
.cache/

# Project specific
data/
*.db
*.sqlite
'''

            gitignore_file = project_dir / ".gitignore"
            with open(gitignore_file, 'w') as f:
                f.write(gitignore_content)

            # Initial commit
            subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial commit: Generated AI crew project"], cwd=project_dir, check=True, capture_output=True)

            logger.info(f"Git repository initialized at {project_dir}")

        except subprocess.CalledProcessError as e:
            logger.warning(f"Git initialization failed: {e}")

    def _count_files(self, project_dir: Path) -> int:
        """Count total files created."""
        count = 0
        for root, dirs, files in os.walk(project_dir):
            count += len(files)
        return count

    def _extract_specifications(self, project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key specifications from the project spec."""
        return {
            "project_name": project_spec["project"]["name"],
            "agent_count": len(project_spec["project"].get("target_agents", [])),
            "technical_requirements": project_spec["project"].get("technical_requirements", {}),
            "success_metrics": project_spec["project"].get("success_metrics", []),
            "generated_by": "AI Crew Builder Team"
        }

# Global project generator instance
project_generator = ProjectGenerator()

def get_project_generator() -> ProjectGenerator:
    """Get the global project generator instance."""
    return project_generator