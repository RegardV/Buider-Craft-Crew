# AI Crew Builder Team Template

A comprehensive template for building AI crew projects using a double-layer builder team approach with OpenSpec-driven development and multi-provider AI support.

## 🎯 What This Template Provides

This template enables you to build any AI crew project through a structured approach:

1. **Builder Team Framework** - Two-layer AI team for strategic guidance and execution
2. **Multi-Provider AI Support** - Claude + ZhipuAI for building, OpenAI for project crews
3. **OpenSpec Integration** - Structured change management and specification-driven development
4. **Project Initialization** - Interactive setup for defining your target AI crew
5. **Automation Scripts** - Team coordination and Git publishing workflows

## 🤖 AI Provider Configuration

### Builder Team (Development Phase)
- **Claude (Anthropic)** - Primary for strategic planning, architecture, and design
- **ZhipuAI (GLM)** - Secondary for quality assurance, infrastructure, and deployment

### Project Crews (Runtime)
- **OpenAI (GPT)** - Primary for executing your AI crew projects
- Configurable models (GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- Cost management with budget controls

## 🚀 Quick Start

### Step 1: Set Up Environment

Install required dependencies:

```bash
# Clone the template
git clone <your-repo-url> my-ai-crew-project
cd my-ai-crew-project

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Step 2: Configure API Keys

You'll need API keys for the AI providers:

```bash
# Required for Builder Team (development)
export ANTHROPIC_API_KEY=your_anthropic_key
export ZHIPUAI_API_KEY=your_zhipuai_key

# Required for Project Crews (runtime)
export OPENAI_API_KEY=your_openai_key
```

### Step 3: Initialize Your Project

Run the interactive initialization script:

```bash
python scripts/init-project.py
```

This will guide you through defining:
- Project goals and description
- Target AI crew agents and their roles
- Technical requirements
- OpenAI model selection
- Budget limits
- Success metrics
- Timeline

### Step 4: Review Generated Configuration

The script creates:
- `config/project.json` - Project configuration
- `config/crew-config.yaml` - Your AI crew configuration
- `.env.example` - Environment variables template
- `openspec/specs/system/project-overview.md` - Project specification

## 📁 Template Structure

```
BuilderTeam/
├── scripts/
│   └── init-project.py          # Interactive project initialization
├── config/
│   ├── builder-crew-config.yaml     # Builder team configuration
│   ├── project-crew-config-template.yaml # Project crew template
│   └── ai-providers.yaml            # AI provider configurations
├── openspec/
│   ├── specs/                    # Specifications
│   │   ├── agents/              # Agent specifications
│   │   ├── workflows/           # Workflow definitions
│   │   ├── features/            # Feature specifications
│   │   └── system/              # System architecture
│   ├── changes/                 # Change management
│   │   ├── proposals/           # Change proposals
│   │   ├── approved/            # Approved changes
│   │   └── implemented/         # Implemented changes
│   └── templates/               # Reusable templates
├── builder-team/                # Builder team configurations
│   ├── advisory/                # Advisory team configs
│   └── application/             # Application team configs
├── docs/                        # Documentation
│   ├── baseline/                # Baseline documentation
│   ├── advisory_team/           # Advisory team docs
│   └── application_team/        # Application team docs
└── templates/                   # Project templates
```

## 🛠️ AI Provider Details

### Claude (Anthropic)
- **Used by**: Builder Team (Advisory Team)
- **Models**: Claude 3.5 Sonnet, Claude 3.5 Haiku
- **Best for**: Strategic planning, technical architecture, UX design
- **Pricing**: ~$0.015/1K input, $0.075/1K output

### ZhipuAI (GLM)
- **Used by**: Builder Team (Quality & DevOps)
- **Models**: GLM-4.6, GLM-4
- **Best for**: Quality assurance, infrastructure, deployment
- **Pricing**: ~$0.01/1K input, $0.03/1K output

### OpenAI (GPT)
- **Used by**: Project Crews (Runtime)
- **Models**: GPT-4 Turbo, GPT-4, GPT-3.5 Turbo
- **Best for**: General AI crew execution
- **Pricing**: $0.0015-$0.03/1K tokens depending on model

## 🔄 Development Workflow

### Phase 0: Foundation (2-3 days)
1. **Initialize project** with `init-project.py`
2. **Set up environment** with API keys
3. **Validate builder team** configuration
4. **Create baseline** documentation

### Phase 1: Advisory Team Setup (1 week)
1. **Configure advisory team** agents (Claude + ZhipuAI)
2. **Establish communication** protocols
3. **Set up strategic planning** framework
4. **Create project roadmap**

### Phase 2: Application Team Design (1-2 weeks)
1. **Design target AI crew** architecture
2. **Define application team** agent roles
3. **Create workflow** specifications
4. **Set up development** framework

### Phase 3: Implementation (2-3 weeks)
1. **Implement application team** agents
2. **Integrate advisory team** guidance
3. **Execute OpenSpec-driven** development
4. **Build target AI crew** functionality

### Phase 4: Testing & Optimization (1 week)
1. **Comprehensive testing** of both teams
2. **Performance optimization**
3. **Security validation**
4. **Documentation completion**

## 💰 Cost Management

### Builder Team Costs
- Claude: ~$500/month limit (strategic tasks)
- ZhipuAI: ~$300/month limit (support tasks)
- Usage during development phase only

### Project Crew Costs
- OpenAI: User-defined budget (default $100/month)
- Configurable per project
- Runtime usage

### Cost Controls
- Daily and monthly limits
- Model selection based on task complexity
- Smart caching and optimization
- Usage monitoring and alerts

## 🎯 Example Projects You Can Build

### Content Creation Crew
```yaml
# Configuration example
agents:
  writer:
    role: "Content Writer"
    provider: "openai"
    model: "gpt-4-turbo-preview"
  editor:
    role: "Content Editor"
    provider: "openai"
    model: "gpt-4-turbo-preview"
  seo_specialist:
    role: "SEO Specialist"
    provider: "openai"
    model: "gpt-3.5-turbo"
```

### E-commerce Support Crew
```yaml
agents:
  customer_service:
    role: "Customer Service Agent"
    provider: "openai"
    model: "gpt-4-turbo-preview"
  order_processor:
    role: "Order Processing Agent"
    provider: "openai"
    model: "gpt-3.5-turbo"
  inventory_manager:
    role: "Inventory Manager"
    provider: "openai"
    model: "gpt-3.5-turbo"
```

### Development Crew
```yaml
agents:
  frontend_developer:
    role: "Frontend Developer"
    provider: "openai"
    model: "gpt-4-turbo-preview"
  backend_developer:
    role: "Backend Developer"
    provider: "openai"
    model: "gpt-4-turbo-preview"
  qa_tester:
    role: "QA Tester"
    provider: "openai"
    model: "gpt-3.5-turbo"
```

## 📋 Requirements

### System Requirements
- Python 3.10+
- Git
- 8GB+ RAM
- 10GB+ disk space

### Required API Keys
- **Anthropic API Key** (for builder team)
- **ZhipuAI API Key** (for builder team)
- **OpenAI API Key** (for project crews)

### Optional Dependencies
- Docker (for containerization)
- Node.js (for frontend projects)
- Database tools (based on project needs)

## 🔧 Configuration Options

### Builder Team Customization
Edit `config/builder-crew-config.yaml` to modify:
- Advisory team agent assignments
- Provider selection rules
- Workflow configurations
- Performance targets

### Project Crew Customization
Generated `config/crew-config.yaml` can be modified:
- Agent roles and responsibilities
- Tool assignments
- Workflow definitions
- Cost limits

### AI Provider Switching
Edit `config/ai-providers.yaml` to:
- Change model selections
- Update cost limits
- Modify provider priorities
- Adjust performance targets

## 🐛 Troubleshooting

### Common Issues

**API Key Problems**
- Verify all required API keys are set
- Check API key permissions and quotas
- Ensure environment variables are loaded

**Provider Failover**
- Builder team automatically switches between Claude and ZhipuAI
- Manual override available in configuration
- Fallback alerts configured

**Cost Overruns**
- Monitor usage in logs/
- Adjust model selections
- Set tighter budget limits
- Enable caching options

### Debug Mode
Enable verbose logging:
```bash
export LOG_LEVEL=DEBUG
python scripts/init-project.py
```

## 🤝 Contributing

This template is designed to be adapted for various AI crew projects while maintaining the builder team approach and OpenSpec methodology.

### Contribution Guidelines
1. Fork the repository
2. Create feature branch
3. Make changes with OpenSpec compliance
4. Test thoroughly
5. Submit pull request

## 📄 License

This template is open source and available under the MIT License.

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review OpenSpec documentation
3. Consult the advisory team configuration
4. Create an issue in the repository

---

*Built with AI Crew Builder Team framework • Claude + ZhipuAI for building, OpenAI for execution*