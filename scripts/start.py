#!/usr/bin/env python3
"""
AI Crew Builder Team - Interactive Startup Script
Launch the Builder Team interface for building AI crew projects.
"""

import asyncio
import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.live import Live
    from rich.text import Text
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich library not available. Using basic output.")

from core.config import get_config, ensure_directories
from core.integration import get_integration

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BuilderTeamInterface:
    """Interactive interface for the Builder Team."""

    def __init__(self):
        self.config = get_config()
        self.integration = get_integration()
        self.builder_team = self.integration.builder_team
        self.console = Console() if RICH_AVAILABLE else None
        self.session_id = None

    def display_welcome(self):
        """Display welcome message."""
        if self.console:
            panel = Panel(
                "[bold blue]🤖 AI Crew Builder Team[/bold blue]\n\n"
                "Build AI crews with AI - Powered by Claude + ZhipuAI\n\n"
                "[yellow]Your Builder Team:[/yellow]\n"
                "📋 Product Strategist (Claude) - Project vision and planning\n"
                "🏗️  Technical Architect (Claude) - System design and architecture\n"
                "🎨 UX Designer (Claude) - User experience and workflows\n"
                "🔍 Quality Engineer (ZhipuAI) - Testing and quality assurance\n"
                "⚙️  DevOps Specialist (ZhipuAI) - Infrastructure and deployment\n\n"
                "[green]Type your project idea to get started![/green]\n"
                "[dim]Type 'help' for commands, 'exit' to quit[/dim]",
                title="Welcome to AI Crew Builder Team",
                border_style="blue"
            )
            self.console.print(panel)
        else:
            print("""
🤖 AI Crew Builder Team
Build AI crews with AI - Powered by Claude + ZhipuAI

Your Builder Team:
📋 Product Strategist (Claude) - Project vision and planning
🏗️  Technical Architect (Claude) - System design and architecture
🎨 UX Designer (Claude) - User experience and workflows
🔍 Quality Engineer (ZhipuAI) - Testing and quality assurance
⚙️  DevOps Specialist (ZhipuAI) - Infrastructure and deployment

Type your project idea to get started!
Type 'help' for commands, 'exit' to quit
""")

    def display_agent_status(self):
        """Display current agent status."""
        if not self.console:
            return

        table = Table(title="Builder Team Status")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Queue", style="yellow")
        table.add_column("Tasks", style="blue")

        for agent_name, agent in self.builder_team.agents.items():
            status = agent.get_status()
            table.add_row(
                agent_name,
                status["status"],
                str(status["queue_size"]),
                str(status["tasks_completed"])
            )

        self.console.print(table)

    def display_help(self):
        """Display help information."""
        help_text = """
# Available Commands

## Project Commands
- **new** - Start a new project
- **status** - Show current project status
- **spec** - Generate project specification
- **generate** - Generate complete project code
- **save** - Save current session
- **load** - Load previous session

## Agent Commands
- **agents** - Show agent status
- **ask [agent]** - Ask specific agent (e.g., 'ask architect')
- **coordinate** - Coordinate with all agents

## System Commands
- **help** - Show this help
- **clear** - Clear screen
- **config** - Show configuration
- **exit** - Exit the program

## Tips
- Just type naturally about your project idea
- The system will automatically route to relevant agents
- Use 'ask [agent]' for specific expertise
- Type 'spec' when ready to generate the complete project specification
"""

        if self.console:
            md = Markdown(help_text)
            self.console.print(Panel(md, title="Help", border_style="green"))
        else:
            print(help_text)

    def display_configuration(self):
        """Display current configuration."""
        if self.console:
            table = Table(title="Configuration")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="white")

            table.add_row("Project Name", self.config.project_name)
            table.add_row("Environment", self.config.environment)
            table.add_row("Claude Model", self.config.claude_model)
            table.add_row("ZhipuAI Model", self.config.zhipuai_model)
            table.add_row("OpenAI Model", self.config.openai_model)
            table.add_row("Debug Mode", str(self.config.debug_mode))

            self.console.print(table)
        else:
            print(f"""
Configuration:
- Project Name: {self.config.project_name}
- Environment: {self.config.environment}
- Claude Model: {self.config.claude_model}
- ZhipuAI Model: {self.config.zhipuai_model}
- OpenAI Model: {self.config.openai_model}
- Debug Mode: {self.config.debug_mode}
""")

    async def handle_command(self, user_input: str) -> bool:
        """Handle special commands."""
        input_lower = user_input.lower().strip()

        if input_lower in ['exit', 'quit', 'q']:
            return False

        elif input_lower == 'help':
            self.display_help()

        elif input_lower == 'clear':
            os.system('clear' if os.name == 'posix' else 'cls')
            self.display_welcome()

        elif input_lower == 'status':
            if self.session_id:
                status = await self.builder_team.get_session_status(self.session_id)
                if self.console:
                    self.console.print(Panel(
                        json.dumps(status, indent=2),
                        title="Project Status",
                        border_style="blue"
                    ))
                else:
                    print("Project Status:")
                    print(json.dumps(status, indent=2))
            else:
                print("No active project session. Type 'new' to start a project.")

        elif input_lower == 'agents':
            self.display_agent_status()

        elif input_lower == 'config':
            self.display_configuration()

        elif input_lower == 'new':
            await self.start_new_project()

        elif input_lower == 'spec':
            await self.generate_specification()

        elif input_lower == 'generate':
            await self.generate_project()

        elif input_lower.startswith('ask '):
            agent_name = input_lower[4:].strip()
            await self.ask_specific_agent(agent_name)

        elif input_lower == 'coordinate':
            await self.coordinate_all_agents()

        else:
            # Not a command, process as regular input
            return True

        return True

    async def start_new_project(self):
        """Start a new project session."""
        if self.console:
            project_name = Prompt.ask("Enter your project name")
        else:
            project_name = input("Enter your project name: ")

        if not project_name:
            project_name = "New AI Crew Project"

        project_input = {
            "name": project_name,
            "description": "New AI crew project",
            "goal": "",
            "target_agents": [],
            "technical_requirements": {},
            "success_metrics": [],
            "timeline": "",
            "budget": 0.0
        }

        self.session_id = await self.integration.start_project_session(project_input)

        if self.console:
            self.console.print(f"[green]✅ Started new project: {project_name}[/green]")
            self.console.print(f"[dim]Session ID: {self.session_id}[/dim]")
        else:
            print(f"✅ Started new project: {project_name}")
            print(f"Session ID: {self.session_id}")

    async def ask_specific_agent(self, agent_name: str):
        """Ask a specific agent for help."""
        if not self.session_id:
            print("No active project session. Type 'new' to start a project.")
            return

        # Map user-friendly names to agent names
        agent_map = {
            'strategist': 'ProductStrategist',
            'architect': 'TechnicalArchitect',
            'designer': 'UXDesigner',
            'quality': 'QualityEngineer',
            'devops': 'DevOpsSpecialist',
            'product': 'ProductStrategist',
            'tech': 'TechnicalArchitect',
            'ux': 'UXDesigner',
            'qa': 'QualityEngineer'
        }

        actual_agent_name = agent_map.get(agent_name.lower(), agent_name)

        if actual_agent_name not in self.builder_team.agents:
            print(f"Unknown agent: {agent_name}")
            print("Available agents: ProductStrategist, TechnicalArchitect, UXDesigner, QualityEngineer, DevOpsSpecialist")
            return

        if self.console:
            question = Prompt.ask(f"What would you like to ask the {actual_agent_name}?")
        else:
            question = input(f"What would you like to ask the {actual_agent_name}? ")

        if question:
            agent = self.builder_team.agents[actual_agent_name]
            response = await agent.think(question)

            if self.console:
                panel = Panel(
                    response,
                    title=f"🤖 {actual_agent_name}",
                    border_style="blue"
                )
                self.console.print(panel)
            else:
                print(f"\n🤖 {actual_agent_name}:")
                print(response)

    async def coordinate_all_agents(self):
        """Coordinate with all agents."""
        if not self.session_id:
            print("No active project session. Type 'new' to start a project.")
            return

        if self.console:
            question = Prompt.ask("What would you like to coordinate with the team?")
        else:
            question = input("What would you like to coordinate with the team? ")

        if question:
            response = await self.builder_team.process_user_input(f"[TEAM COORDINATION] {question}")

            if self.console:
                panel = Panel(
                    response,
                    title="🤝 Builder Team Response",
                    border_style="green"
                )
                self.console.print(panel)
            else:
                print(f"\n🤝 Builder Team Response:")
                print(response)

    async def generate_specification(self):
        """Generate complete project specification."""
        if not self.session_id:
            print("No active project session. Type 'new' to start a project.")
            return

        print("📋 Generating complete project specification...")
        print("This may take a few moments as all agents contribute...")

        try:
            spec_result = await self.integration.generate_project_specification(self.session_id)
            specification = spec_result["specification"]

            # Save specification to file
            session = self.builder_team.sessions[self.session_id]
            filename = f"project_spec_{session.project.name.replace(' ', '_').lower()}.json"
            filepath = Path.cwd() / "generated" / filename

            # Ensure directory exists
            filepath.parent.mkdir(exist_ok=True)

            with open(filepath, 'w') as f:
                json.dump(specification, f, indent=2, default=str)

            if self.console:
                self.console.print(f"[green]✅ Specification saved to: {filepath}[/green]")
                self.console.print(f"[dim]OpenSpec Document ID: {spec_result['document_id']}[/dim]")

                # Display summary
                panel = Panel(
                    f"Project: {specification['project']['name']}\n"
                    f"Description: {specification['project']['description']}\n"
                    f"Agent Specifications: {len(specification['agent_specifications'])}\n"
                    f"Session Messages: {specification['session_summary']['message_count']}\n"
                    f"OpenSpec Document: {spec_result['document_id']}",
                    title="📋 Specification Generated",
                    border_style="blue"
                )
                self.console.print(panel)
            else:
                print(f"✅ Specification saved to: {filepath}")
                print(f"OpenSpec Document ID: {spec_result['document_id']}")
                print(f"Project: {specification['project']['name']}")
                print(f"Agent Specifications: {len(specification['agent_specifications'])}")

        except Exception as e:
            logger.error(f"Error generating specification: {e}")
            if self.console:
                self.console.print(f"[red]❌ Error generating specification: {e}[/red]")
            else:
                print(f"❌ Error generating specification: {e}")

    async def generate_project(self):
        """Generate complete project from specification."""
        if not self.session_id:
            print("No active project session. Type 'new' to start a project.")
            return

        print("🚀 Generating complete AI crew project...")
        print("This will create a full project structure with code and documentation...")

        try:
            result = await self.integration.generate_project(self.session_id)
            generation_result = result["generation_result"]

            if self.console:
                self.console.print(f"[green]✅ Project generated successfully![/green]")
                self.console.print(f"[dim]Location: {generation_result['project_dir']}[/dim]")
                self.console.print(f"[dim]Files created: {generation_result['files_created']}[/dim]")

                # Display summary
                panel = Panel(
                    f"Project: {generation_result['project_name']}\n"
                    f"Location: {generation_result['project_dir']}\n"
                    f"Files Created: {generation_result['files_created']}\n"
                    f"Generated: {generation_result['generated_at']}\n"
                    f"Agent Count: {generation_result['specifications']['agent_count']}",
                    title="🚀 Project Generated",
                    border_style="green"
                )
                self.console.print(panel)

                # Next steps
                next_steps = Panel(
                    f"Next steps for your project:\n"
                    f"1. cd {generation_result['project_dir']}\n"
                    f"2. python scripts/setup.py\n"
                    f"3. Add your OpenAI API key to .env\n"
                    f"4. python main.py",
                    title="📋 Next Steps",
                    border_style="yellow"
                )
                self.console.print(next_steps)
            else:
                print(f"✅ Project generated successfully!")
                print(f"Location: {generation_result['project_dir']}")
                print(f"Files created: {generation_result['files_created']}")
                print(f"\nNext steps:")
                print(f"1. cd {generation_result['project_dir']}")
                print(f"2. python scripts/setup.py")
                print(f"3. Add your OpenAI API key to .env")
                print(f"4. python main.py")

        except Exception as e:
            logger.error(f"Error generating project: {e}")
            if self.console:
                self.console.print(f"[red]❌ Error generating project: {e}[/red]")
            else:
                print(f"❌ Error generating project: {e}")

    async def process_user_input(self, user_input: str):
        """Process regular user input through the integration layer."""
        try:
            if not self.session_id:
                # Start a new session if none exists
                await self.start_new_project()

            result = await self.integration.process_user_input(self.session_id, user_input)
            response = result["response"]

            if self.console:
                panel = Panel(
                    response,
                    title="🤖 Builder Team",
                    border_style="blue"
                )
                self.console.print(panel)
            else:
                print(f"\n🤖 Builder Team:")
                print(response)

        except Exception as e:
            logger.error(f"Error processing input: {e}")
            if self.console:
                self.console.print(f"[red]❌ Error: {e}[/red]")
            else:
                print(f"❌ Error: {e}")

    async def run_interactive(self):
        """Run the interactive interface."""
        # Ensure directories exist
        ensure_directories()

        # Display welcome
        self.display_welcome()

        # Main interaction loop
        while True:
            try:
                # Get user input
                if self.console:
                    user_input = Prompt.ask("\n💬 You", default="")
                else:
                    user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                should_continue = await self.handle_command(user_input)
                if not should_continue:
                    break

                # If not a command, process as regular input
                if should_continue is True:
                    await self.process_user_input(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                if self.console:
                    self.console.print(f"[red]❌ Unexpected error: {e}[/red]")
                else:
                    print(f"❌ Unexpected error: {e}")

async def main():
    """Main entry point."""
    # Check environment
    config = get_config()

    if not config.anthropic_api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment variables")
        print("Please set your API keys in .env file")
        sys.exit(1)

    if not config.zhipuai_api_key:
        print("❌ ZHIPUAI_API_KEY not found in environment variables")
        print("Please set your API keys in .env file")
        sys.exit(1)

    if not config.openai_api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your API keys in .env file")
        sys.exit(1)

    # Create and run interface
    interface = BuilderTeamInterface()

    # Initialize the integration system
    try:
        await interface.integration.initialize()
        if interface.console:
            interface.console.print("[green]✅ Builder Team system initialized[/green]")
        else:
            print("✅ Builder Team system initialized")
    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        if interface.console:
            interface.console.print(f"[red]❌ Error initializing system: {e}[/red]")
        else:
            print(f"❌ Error initializing system: {e}")
        sys.exit(1)

    try:
        await interface.run_interactive()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        # Shutdown the integration system
        await interface.integration.shutdown()

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--production":
            # Production mode
            print("🚀 Starting AI Crew Builder Team in production mode...")
            # TODO: Implement production mode (FastAPI server)
        elif sys.argv[1] == "--help":
            print("AI Crew Builder Team - Interactive Interface")
            print("Usage: python scripts/start.py [--production]")
            print("  --production: Start in production mode (API server)")
            print("  (no args): Start interactive interface")
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Run interactive mode
        asyncio.run(main())