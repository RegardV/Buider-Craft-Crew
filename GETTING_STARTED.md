# 🚀 Getting Started with AI Crew Builder Team

Build AI crews with AI! This comprehensive system helps you design, specify, and generate complete AI crew projects using specialized AI agents.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Setup Options](#setup-options)
- [API Keys Configuration](#api-keys-configuration)
- [Using the Builder Team](#using-the-builder-team)
- [Generating Your First Project](#generating-your-first-project)
- [Docker Setup](#docker-setup)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

---

## 🔧 System Requirements

### Minimum Requirements
- **Python:** 3.10 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 10GB free space
- **OS:** Linux, macOS, or Windows

### Optional Requirements
- **Docker:** For containerized deployment
- **Git:** For version control integration

### API Providers
You'll need API keys from three providers:

1. **Anthropic (Claude)** - For strategic guidance
2. **ZhipuAI (GLM)** - For technical tasks
3. **OpenAI (GPT)** - For generated project execution

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/RegardV/Buider-Craft-Crew.git
cd Buider-Craft-Crew
```

### 2. Run the Setup Script
```bash
# For both local and Docker environments
python scripts/setup.py --type both

# Or choose specific setup type:
# python scripts/setup.py --type local      # Local Python environment only
# python scripts/setup.py --type docker     # Docker environment only
```

### 3. Configure API Keys
```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file with your API keys
nano .env  # or your preferred editor
```

Add your API keys:
```bash
# AI Provider API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ZHIPUAI_API_KEY=your_zhipuai_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Start the Builder Team
```bash
python scripts/start.py
```

That's it! You're ready to start building AI crews with AI! 🎉

---

## ⚙️ Setup Options

### Option 1: Local Development Setup

**Best for:** Development, customization, and direct control

```bash
# 1. Set up local Python environment
python scripts/setup.py --type local

# 2. Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# 3. Start the Builder Team
python scripts/start.py
```

**Pros:**
- Direct access to source code
- Easy to customize and debug
- No Docker dependencies
- Fast startup time

**Cons:**
- Manual dependency management
- Local environment conflicts possible

### Option 2: Docker Setup

**Best for:** Production deployment, consistent environments

```bash
# 1. Set up Docker environment
python scripts/docker-setup.py setup

# 2. Start all services
python scripts/docker-setup.py start

# 3. Check status
python scripts/docker-setup.py status

# 4. Access the Builder Team
python scripts/docker-setup.py shell --service builder-team
python scripts/start.py
```

**Pros:**
- Consistent across all platforms
- Complete service stack (database, monitoring, etc.)
- Easy deployment and scaling
- Isolated environment

**Cons:**
- Requires Docker installation
- More resource intensive
- Longer startup time

### Option 3: Hybrid Setup

**Best for:** Development with production testing

```bash
# 1. Set up both environments
python scripts/setup.py --type both

# 2. Develop locally
python scripts/start.py

# 3. Test with Docker when needed
python scripts/docker-setup.py setup
python scripts/docker-setup.py start
```

---

## 🔑 API Keys Configuration

### Getting API Keys

1. **Anthropic (Claude)**
   - Visit: https://console.anthropic.com/
   - Create an account and API key
   - Cost: ~$0.015/1K input, $0.075/1K output

2. **ZhipuAI (GLM)**
   - Visit: https://open.bigmodel.cn/
   - Create an account and API key
   - Cost: ~$0.01/1K input, $0.03/1K output

3. **OpenAI (GPT)**
   - Visit: https://platform.openai.com/
   - Create an account and API key
   - Cost: Varies by model (GPT-4 Turbo ~$0.01/1K tokens)

### Environment Configuration

Create a `.env` file with your keys:

```bash
# Required API Keys
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
ZHIPUAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# Project Configuration
PROJECT_NAME=AI-Crew-Builder-Team
ENVIRONMENT=development

# Optional: Budget limits
MONTHLY_BUDGET_CLAUDE=500.0
MONTHLY_BUDGET_ZHIPUAI=300.0
MONTHLY_BUDGET_OPENAI=1000.0
```

### Security Notes
- **Never commit** your `.env` file to version control
- **Never share** your API keys publicly
- **Use environment variables** in production
- **Monitor usage** to control costs

---

## 🤖 Using the Builder Team

### Starting the Interface

```bash
python scripts/start.py
```

You'll see a welcome screen with your Builder Team:

```
🤖 AI Crew Builder Team
Build AI crews with AI - Powered by Claude + ZhipuAI

Your Builder Team:
📋 Product Strategist (Claude) - Project vision and planning
🏗️  Technical Architect (Claude) - System design and architecture
🎨 UX Designer (Claude) - User experience and workflows
🔍 Quality Engineer (ZhipuAI) - Testing and quality assurance
⚙️  DevOps Specialist (ZhipuAI) - Infrastructure and deployment

Type your project idea to get started!
```

### Basic Commands

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `new` | Start a new project session |
| `status` | Show current project status |
| `agents` | Show Builder Team agent status |
| `spec` | Generate project specification |
| `generate` | Generate complete project code |
| `ask [agent]` | Ask specific agent (e.g., `ask architect`) |
| `coordinate` | Coordinate with all agents |
| `clear` | Clear the screen |
| `exit` | Exit the program |

### Natural Language Interaction

Just type naturally about your project idea:

```
💬 You: I want to build an AI crew for content creation

🤖 Builder Team: Hello! I'm excited to help you build an AI crew for content creation.
The Product Strategist is here to guide us through understanding your vision.

Let me start by asking about your content creation goals: What type of content
do you want to create, and who is your target audience?
```

The system automatically routes your input to the most relevant agents and provides coordinated responses.

### Asking Specific Agents

You can direct questions to specific agents:

```bash
💬 You: ask architect What technology stack should I use?

🤖 TechnicalArchitect: For your content creation AI crew, I recommend the following
technology stack...
```

Available agents:
- `strategist` or `product` - ProductStrategist
- `architect` or `tech` - TechnicalArchitect
- `designer` or `ux` - UXDesigner
- `quality` or `qa` - QualityEngineer
- `devops` - DevOpsSpecialist

---

## 🏗️ Generating Your First Project

### Step 1: Define Your Project

Start by describing your AI crew idea:

```
💬 You: I want to build an AI crew that writes blog posts and creates social media content for tech startups.
```

The Builder Team will ask clarifying questions to understand:
- Project goals and objectives
- Required AI agents and their roles
- Technical requirements
- Success metrics
- Timeline and budget

### Step 2: Generate Specification

Once you have a clear project definition:

```bash
💬 You: spec
```

The system generates a comprehensive project specification including:
- Detailed agent definitions
- Technical architecture
- Implementation plan
- Success metrics

### Step 3: Generate Complete Project

Generate the full project with code and documentation:

```bash
💬 You: generate
```

The system creates:
- Complete Python project structure
- Agent implementations
- Configuration files
- Documentation
- Setup scripts
- Git repository

### Step 4: Use Your Generated Project

Your generated project is ready to use:

```bash
# Navigate to your generated project
cd generated_projects/your_project_name

# Set up the new project
python scripts/setup.py

# Add your OpenAI API key to .env
# Edit .env with: OPENAI_API_KEY=your_key

# Run your AI crew
python main.py
```

---

## 🐳 Docker Setup Guide

### Complete Docker Deployment

```bash
# 1. Set up Docker environment
python scripts/docker-setup.py setup

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# 3. Start all services
python scripts/docker-setup.py start

# 4. Monitor services
python scripts/docker-setup.py status
python scripts/docker-setup.py logs

# 5. Access services
# Main application: http://localhost:8000
# WebSocket: http://localhost:8001
# Monitoring: http://localhost:3000 (Grafana)
# Logs: http://localhost:5601 (Kibana)
```

### Docker Commands

| Command | Description |
|---------|-------------|
| `python scripts/docker-setup.py setup` | Build and start all services |
| `python scripts/docker-setup.py start` | Start services |
| `python scripts/docker-setup.py stop` | Stop services |
| `python scripts/docker-setup.py restart` | Restart services |
| `python scripts/docker-setup.py status` | Check service status |
| `python scripts/docker-setup.py logs` | View logs |
| `python scripts/docker-setup.py shell --service [service]` | Access service shell |

### Services Included

- **builder-team**: Main application
- **redis**: Caching and task queue
- **postgres**: Database
- **nginx**: Reverse proxy
- **grafana**: Monitoring dashboard
- **elasticsearch**: Log storage
- **kibana**: Log visualization
- **worker**: Background task processor
- **scheduler**: Task scheduler

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Module Not Found
```bash
# Error: ModuleNotFoundError: No module named 'pydantic'
# Solution: Install dependencies
python scripts/setup.py --type local
source .venv/bin/activate
```

#### 2. API Key Issues
```bash
# Error: API key not found
# Solution: Check your .env file
cat .env | grep API_KEY
# Ensure all three API keys are set
```

#### 3. Docker Issues
```bash
# Error: Docker not available
# Solution: Install Docker
# Ubuntu/Debian: sudo apt install docker.io docker-compose
# macOS: Download Docker Desktop
# Windows: Download Docker Desktop
```

#### 4. Port Conflicts
```bash
# Error: Port already in use
# Solution: Check what's using the port
sudo netstat -tlnp | grep :8000
# Or use different ports in docker-compose.yml
```

#### 5. Permission Issues
```bash
# Error: Permission denied
# Solution: Check file permissions
ls -la scripts/
chmod +x scripts/*.py
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Edit .env file
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Or set environment variable
export DEBUG_MODE=true
python scripts/start.py
```

### Getting Help

1. **Check the logs:** Look at error messages for specific guidance
2. **Run tests:** `python test_comprehensive.py` to validate setup
3. **Check API keys:** Ensure all three providers are configured
4. **Verify dependencies:** Run setup script if modules are missing

---

## 📚 Examples

### Example 1: Content Creation Crew

```
💬 You: I want to build an AI crew for content creation

💬 You: The crew should create blog posts, social media content, and email newsletters for tech startups.

💬 You: ask architect What technology should I use?

💬 You: spec

💬 You: generate
```

**Generated Project Includes:**
- ContentWriter agent
- SocialMediaManager agent
- EmailMarketing agent
- ContentReview agent
- PublicationManager agent

### Example 2: Customer Service Crew

```
💬 You: Build an AI crew for customer service

💬 You: It should handle customer inquiries, process orders, and manage returns for an e-commerce store.

💬 You: ask quality How should I test the agents?

💬 You: ask devops How should I deploy this?

💬 You: spec

💬 You: generate
```

### Example 3: Data Analysis Crew

```
💬 You: I need an AI crew for data analysis

💬 You: It should analyze sales data, generate reports, and provide business insights.

💬 You: ask strategist What metrics should I track?

💬 You: coordinate How should the agents work together?

💬 You: generate
```

---

## 🎯 Tips for Success

### Best Practices

1. **Start Simple:** Begin with a clear, focused project idea
2. **Be Specific:** Provide detailed requirements for better results
3. **Iterate:** Use the spec command to refine before generating
4. **Test Locally:** Test generated projects before deployment
5. **Monitor Usage:** Keep an eye on API costs and usage

### Project Definition Tips

- **Clear Goals:** Define what success looks like
- **Specific Roles:** Clearly define what each agent should do
- **Realistic Scope:** Start with 3-5 agents rather than 10+
- **Consider Integration:** Think about how agents will work together

### Cost Management

- **Monitor Usage:** The system tracks token usage
- **Set Budgets:** Configure monthly limits in .env
- **Choose Models:** Select appropriate AI models for tasks
- **Review Specifications:** Validate before generating full projects

---

## 🆘 Need Help?

### Resources

- **Repository:** https://github.com/RegardV/Buider-Craft-Crew
- **Issues:** Report bugs or request features on GitHub
- **Documentation:** Check the main README.md for detailed technical info

### Community

- **Examples:** Look in the `examples/` directory for sample projects
- **Templates:** Use the generated projects as starting points
- **Contributing:** Fork and improve the system!

---

## 🎉 You're Ready!

You now have everything you need to build AI crews with AI. The system will guide you through the entire process, from initial idea to complete, working project.

**Remember:** Start with your API keys configured, describe your project clearly, and let the Builder Team handle the technical details.

Happy building! 🚀🤖

---

*Built with Claude Code + Z.ai + OpenSpec*
*Project Lead: Regard Vermeulen*