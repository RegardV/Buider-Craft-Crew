#!/usr/bin/env python3
"""
AI Crew Project Builder - Initialization Script
This script helps define and initialize a new AI crew project using the builder team approach.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def get_project_definition():
    """Interactive project definition session"""
    print("🚀 AI Crew Project Builder - Initialization")
    print("=" * 50)
    print("This script will help you define the AI crew project you want to build.")
    print("Our builder team will then construct it using OpenSpec-driven development.\n")

    project = {}

    # Basic Project Information
    print("📋 PROJECT BASIC INFORMATION")
    print("-" * 30)
    project['name'] = input("Project name: ").strip()
    project['description'] = input("Project description: ").strip()
    project['owner'] = input("Project owner: ").strip()
    project['timeline'] = input("Estimated timeline (e.g., 4-6 weeks): ").strip()

    # Project Goal
    print("\n🎯 PROJECT GOAL")
    print("-" * 20)
    print("What is the main goal of this AI crew?")
    project['goal'] = input("> ").strip()

    # Target AI Crew Description
    print("\n🤖 TARGET AI CREW")
    print("-" * 25)
    print("Describe the AI crew you want to build:")
    print("(e.g., 'A content creation crew that writes blog posts and creates social media')")
    project['target_crew_description'] = input("> ").strip()

    # Key Features
    print("\n✨ KEY FEATURES")
    print("-" * 20)
    print("List the key features (one per line, empty line to finish):")
    features = []
    while True:
        feature = input(f"Feature {len(features) + 1}: ").strip()
        if not feature:
            break
        features.append(feature)
    project['key_features'] = features

    # Success Metrics
    print("\n📊 SUCCESS METRICS")
    print("-" * 22)
    print("How will you measure success? (one per line, empty line to finish):")
    metrics = []
    while True:
        metric = input(f"Metric {len(metrics) + 1}: ").strip()
        if not metric:
            break
        metrics.append(metric)
    project['success_metrics'] = metrics

    # AI Crew Agents
    print("\n👥 AI CREW AGENTS")
    print("-" * 22)
    print("Define the agents in your target AI crew:")
    agents = []
    agent_count = 0

    while True:
        agent_count += 1
        print(f"\nAgent {agent_count}:")
        name = input("  Agent name (or press Enter to finish): ").strip()
        if not name:
            break

        role = input("  Role/Function: ").strip()
        mbti = input("  MBTI type (optional): ").strip() or "Not specified"

        print("  Key responsibilities (one per line, empty line to finish):")
        responsibilities = []
        while True:
            resp = input(f"    Responsibility {len(responsibilities) + 1}: ").strip()
            if not resp:
                break
            responsibilities.append(resp)

        agents.append({
            'name': name,
            'role': role,
            'mbti_type': mbti,
            'responsibilities': responsibilities
        })

    project['target_agents'] = agents

    # Technical Requirements
    print("\n⚙️ TECHNICAL REQUIREMENTS")
    print("-" * 30)

    print("Frontend framework (if any):")
    project['frontend_framework'] = input("> ").strip() or "None"

    print("Backend framework:")
    project['backend_framework'] = input("> ").strip()

    print("Database type:")
    project['database_type'] = input("> ").strip()

    print("API type (REST, GraphQL, etc.):")
    project['api_type'] = input("> ").strip()

    print("Hosting platform:")
    project['hosting_platform'] = input("> ").strip()

    # AI Provider Configuration
    print("\n🤖 AI PROVIDER CONFIGURATION")
    print("-" * 30)
    print("Your project crew will use OpenAI by default.")
    print("The builder team uses Claude + ZhipuAI for project development.")

    print("\nOpenAI model for your project crew:")
    print("1. gpt-4-turbo-preview (Recommended, best capabilities)")
    print("2. gpt-4 (Capable, higher cost)")
    print("3. gpt-3.5-turbo (Fast, cost-effective)")

    model_choice = input("Choose model (1-3, default=1): ").strip()
    model_map = {
        "1": "gpt-4-turbo-preview",
        "2": "gpt-4",
        "3": "gpt-3.5-turbo"
    }
    project['openai_model'] = model_map.get(model_choice, "gpt-4-turbo-preview")

    print(f"\nSelected OpenAI model: {project['openai_model']}")

    print("\nMonthly budget limit for your project crew (USD):")
    budget = input("Default=100, press Enter for default: ").strip()
    project['monthly_budget'] = float(budget) if budget else 100.0

    # Project Metadata
    project['created_date'] = datetime.now().strftime("%Y-%m-%d")
    project['status'] = "initialized"

    return project

def create_project_structure(project):
    """Create the project directory structure"""
    base_dir = Path.cwd()
    project_name = project['name'].lower().replace(' ', '-')
    project_dir = base_dir / project_name

    print(f"\n📁 Creating project structure: {project_dir}")

    # Main directories
    directories = [
        'openspec/specs/agents',
        'openspec/specs/workflows',
        'openspec/specs/features',
        'openspec/specs/system',
        'openspec/changes/proposals',
        'openspec/changes/approved',
        'openspec/changes/implemented',
        'openspec/templates',
        'builder-team/advisory',
        'builder-team/application',
        'docs/baseline',
        'docs/advisory_team',
        'docs/application_team',
        'scripts',
        'config',
        'logs',
        'src/agents',
        'src/workflows',
        'src/tools',
        'tests',
        '.github/workflows'
    ]

    for directory in directories:
        (project_dir / directory).mkdir(parents=True, exist_ok=True)

    return project_dir

def create_project_files(project, project_dir):
    """Create initial project files"""

    # Create project configuration
    config = {
        'project': project,
        'ai_providers': {
            'builder_crew': {
                'primary': 'claude',
                'secondary': 'zhipuai',
                'description': 'Builder team uses Claude for strategic tasks and ZhipuAI for support tasks'
            },
            'project_crew': {
                'primary': 'openai',
                'model': project['openai_model'],
                'monthly_budget': project['monthly_budget'],
                'description': 'Project crew uses OpenAI for execution'
            }
        },
        'builder_team': {
            'advisory_team': {
                'product_strategist': {'type': 'ENTJ', 'provider': 'claude'},
                'technical_architect': {'type': 'INTJ', 'provider': 'claude'},
                'ux_designer': {'type': 'ENFP', 'provider': 'claude'},
                'quality_engineer': {'type': 'ISTJ', 'provider': 'zhipuai'},
                'devops_specialist': {'type': 'ISTP', 'provider': 'zhipuai'}
            },
            'application_team': project['target_agents']
        },
        'openspec': {
            'current_version': '0.1.0',
            'change_workflow': 'proposal-review-approval-implementation'
        }
    }

    with open(project_dir / 'config' / 'project.json', 'w') as f:
        json.dump(config, f, indent=2)

    # Create project-specific crew configuration
    crew_config_content = f"""# {project['name']} Crew Configuration
# Generated by AI Crew Builder Team Template

project:
  name: "{project['name']}"
  description: "{project['description']}"
  version: "1.0.0"
  created: "{project['created_date']}"

# AI Provider Configuration
provider:
  name: "openai"
  type: "openai"
  model: "{project['openai_model']}"
  description: "Primary AI provider for {project['name']} crew execution"

  # Rate limiting and cost management
  limits:
    requests_per_minute: 350
    tokens_per_minute: 200_000
    daily_cost_limit: {project['monthly_budget'] / 30:.2f}
    monthly_cost_limit: {project['monthly_budget']}

# Crew Configuration
crew:
  name: "{project['name']}Crew"
  description: "{project['description']}"

  # Agent Definitions
  agents:"""

    # Add agents to the configuration
    for i, agent in enumerate(project['target_agents']):
        agent_config = f"""

    {agent['name'].lower().replace(' ', '_')}:
      name: "{agent['name']}"
      role: "{agent['role']}"
      goal: "Execute {agent['role'].lower()} tasks for {project['name']}"
      backstory: "You are {agent['name']}, a specialized {agent['role']} AI agent working on the {project['name']} project."
      provider: "openai"
      model: "{project['openai_model']}"

      # Agent-specific tools (customize as needed)
      tools:
        - "file_operations"
        - "web_search"
        - "data_analysis"

      # Agent configuration
      allow_delegation: true
      verbose: true
      max_iter: 10
      memory: true

      # Agent responsibilities
      responsibilities:"""

        for resp in agent['responsibilities']:
            agent_config += f"\n        - \"{resp}\""

        crew_config_content += agent_config

    crew_config_content += """

# Workflow Configuration
workflows:
  standard_execution:
    description: "Standard workflow for most project tasks"
    steps:
      - "Task analysis and planning"
      - "Agent coordination and task assignment"
      - "Individual agent execution"
      - "Result integration and validation"
      - "Documentation and reporting"

# Tools Configuration
tools:
  file_operations:
    enabled: true
    permissions: ["read", "write", "create", "delete"]

  web_search:
    enabled: true
    provider: "openai"
    max_results: 10

# Integration Configuration
integrations:
  openspec:
    enabled: true
    auto_sync: true
    change_tracking: true

  git:
    enabled: true
    auto_commit: false
    branch_strategy: "feature-branches"

# Quality Assurance
quality_assurance:
  testing:
    automated_tests: true
    coverage_target: 80

  review:
    automated_review: true
    security_scan: true

# Cost Management
cost_management:
  budget:
    daily_limit: """ + str(project['monthly_budget'] / 30) + f"""
    monthly_limit: {project['monthly_budget']}

  optimization:
    smart_routing: true
    caching: true

# Performance Settings
performance:
  parallel_processing:
    enabled: true
    max_concurrent_agents: """ + str(min(5, len(project['target_agents']))) + """

  resource_management:
    memory_limit: "4GB"
    timeout: 300

# Development Settings
development:
  debug_mode: false
  verbose_logging: true
  auto_save: true
"""

    with open(project_dir / 'config' / 'crew-config.yaml', 'w') as f:
        f.write(crew_config_content)

    # Create environment file template
    env_content = f"""# {project['name']} Environment Variables
# Copy this file to .env and fill in your API keys

# OpenAI Configuration (for your project crew)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Additional API keys if needed
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# ZHIPUAI_API_KEY=your_zhipuai_api_key_here

# Project Configuration
PROJECT_NAME={project['name']}
PROJECT_VERSION=1.0.0
ENVIRONMENT=development

# Builder Team Configuration (used during development)
BUILDER_TEAM_PROVIDERS=claude,zhipuai
PROJECT_CREW_PROVIDER=openai

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/project.log

# Cost Management
MONTHLY_BUDGET={project['monthly_budget']}
DAILY_BUDGET={project['monthly_budget'] / 30:.2f}

# Performance Settings
MAX_CONCURRENT_AGENTS={min(5, len(project['target_agents']))}
AGENT_TIMEOUT=300
"""

    with open(project_dir / '.env.example', 'w') as f:
        f.write(env_content)

    # Create main README
    readme_content = f"""# {project['name']}

{project['description']}

## Project Overview

This project is being built using the AI Crew Builder Team approach with OpenSpec-driven development.

### Goal
{project['goal']}

### Target AI Crew
{project['target_crew_description']}

## Builder Team

### Advisory Team
- **Product Strategist (ENTJ)** - Product vision and strategic planning
- **Technical Architect (INTJ)** - System design and technical strategy
- **UX Designer (ENFP)** - User experience and interface design
- **Quality Engineer (ISTJ)** - Quality assurance and testing strategy
- **DevOps Specialist (ISTP)** - Infrastructure and deployment

### Application Team
{chr(10).join([f"- **{agent['name']}** - {agent['role']}" for agent in project['target_agents']])}

## Getting Started

1. **Review the OpenSpec specifications** in `openspec/specs/`
2. **Consult the Advisory Team** for strategic guidance
3. **Execute with Application Team** for implementation
4. **Follow OpenSpec workflow** for all changes

## Project Status

**Status:** {project['status']}
**Created:** {project['created_date']}
**Timeline:** {project['timeline']}

## Success Metrics

{chr(10).join([f"- {metric}" for metric in project['success_metrics']])}

---

*Built with AI Crew Builder Team framework*
"""

    with open(project_dir / 'README.md', 'w') as f:
        f.write(readme_content)

    # Create OpenSpec project specification
    spec_content = f"""# {project['name']} - Project Specification

**Document Version:** 0.1.0
**Created:** {project['created_date']}
**Owner:** {project['owner']}
**Status:** {project['status']}

---

## Executive Summary

{project['description']}

**Goal:** {project['goal']}

**Target AI Crew:** {project['target_crew_description']}

**Timeline:** {project['timeline']}

---

## Target AI Crew Configuration

### Agents ({len(project['target_agents'])})
{chr(10).join([f"#### {i+1}. {agent['name']} ({agent['role']})\n**MBTI Type:** {agent['mbti_type']}\n**Core Function:** {agent['role']}\n**Key Responsibilities:**\n" + chr(10).join([f"- {resp}" for resp in agent['responsibilities']]) for i, agent in enumerate(project['target_agents'])])}

---

## Technical Requirements

- **Frontend Framework:** {project['frontend_framework']}
- **Backend Framework:** {project['backend_framework']}
- **Database Type:** {project['database_type']}
- **API Type:** {project['api_type']}
- **Hosting Platform:** {project['hosting_platform']}

---

## Key Features

{chr(10).join([f"{i+1}. {feature}" for i, feature in enumerate(project['key_features'])])}

---

## Success Metrics

{chr(10).join([f"{i+1}. {metric}" for i, metric in enumerate(project['success_metrics'])])}

---

## Next Steps

1. **Phase 0:** Environment setup and baseline validation
2. **Phase 1:** Advisory team deployment and configuration
3. **Phase 2:** Application team design and development
4. **Phase 3:** Integration and testing
5. **Phase 4:** Deployment and optimization

---

*This specification will be updated iteratively throughout the development process.*
"""

    with open(project_dir / 'openspec' / 'specs' / 'system' / 'project-overview.md', 'w') as f:
        f.write(spec_content)

def create_git_repo(project_dir):
    """Initialize git repository"""
    os.chdir(project_dir)

    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# Environment variables
.env
.env.local
.env.production

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

# Project specific
Projects_Derived/
LLM_output/
JSON_output/
media_output/
PDF_output/

# Temporary files
tmp/
temp/
"""

    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)

    # Initialize git
    os.system('git init')
    os.system('git add .')
    os.system(f'git commit -m "Initial commit: {project_dir.name} project initialized"')

    print("✅ Git repository initialized")

def main():
    """Main initialization process"""
    try:
        # Get project definition
        project = get_project_definition()

        # Validate project definition
        if not project['name'] or not project['target_crew_description']:
            print("❌ Project name and target crew description are required!")
            sys.exit(1)

        # Create project structure
        project_dir = create_project_structure(project)

        # Create project files
        create_project_files(project, project_dir)

        # Initialize git repository
        create_git_repo(project_dir)

        print(f"\n🎉 Project '{project['name']}' initialized successfully!")
        print(f"📂 Location: {project_dir}")
        print(f"\n📋 Next Steps:")
        print(f"1. cd {project_dir}")
        print(f"2. Review the OpenSpec specifications in openspec/specs/")
        print(f"3. Set up your development environment")
        print(f"4. Deploy the advisory team first")
        print(f"5. Begin OpenSpec-driven development!")

    except KeyboardInterrupt:
        print("\n\n❌ Project initialization cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()