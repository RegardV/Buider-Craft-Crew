"""
AI Crew Builder Team - Core Configuration
Manages all configuration settings for the Builder Team system.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig(BaseSettings):
    """Database configuration settings."""
    url: str = Field(default="sqlite:///data/builder_team.db", env="DATABASE_URL")
    pool_size: int = Field(default=5, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")

class RedisConfig(BaseSettings):
    """Redis configuration settings."""
    url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    db: int = Field(default=0, env="REDIS_DB")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")

class AIProviderConfig(BaseSettings):
    """AI Provider configuration."""
    name: str
    type: str
    model: str
    api_key: str
    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 60
    max_retries: int = 3

class BuilderTeamConfig(BaseSettings):
    """Main Builder Team configuration."""

    # Project settings
    project_name: str = Field(default="AI-Crew-Builder-Team", env="PROJECT_NAME")
    project_version: str = Field(default="1.0.0", env="PROJECT_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")

    # AI Provider settings
    anthropic_api_key: str = Field(env="ANTHROPIC_API_KEY")
    zhipuai_api_key: str = Field(env="ZHIPUAI_API_KEY")
    openai_api_key: str = Field(env="OPENAI_API_KEY")

    # Model configurations
    claude_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    zhipuai_model: str = Field(default="glm-4.6", env="ZHIPUAI_MODEL")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")

    # Cost management
    monthly_budget_claude: float = Field(default=500.0, env="MONTHLY_BUDGET_CLAUDE")
    monthly_budget_zhipuai: float = Field(default=300.0, env="MONTHLY_BUDGET_ZHIPUAI")
    monthly_budget_openai: float = Field(default=1000.0, env="MONTHLY_BUDGET_OPENAI")

    # Performance settings
    max_concurrent_agents: int = Field(default=10, env="MAX_CONCURRENT_AGENTS")
    agent_timeout: int = Field(default=300, env="AGENT_TIMEOUT")
    request_timeout: int = Field(default=60, env="REQUEST_TIMEOUT")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/builder-team.log", env="LOG_FILE")

    # OpenSpec settings
    openspec_path: str = Field(default="./openspec", env="OPENSPEC_REPO_PATH")
    openspec_auto_sync: bool = Field(default=True, env="OPENSPEC_AUTO_SYNC")

    # Database and Redis
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()

    # Development settings
    debug_mode: bool = Field(default=False, env="DEBUG_MODE")
    verbose_logging: bool = Field(default=True, env="VERBOSE_LOGGING")

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_ai_providers(self) -> Dict[str, AIProviderConfig]:
        """Get all configured AI providers."""
        return {
            "claude": AIProviderConfig(
                name="claude",
                type="anthropic",
                model=self.claude_model,
                api_key=self.anthropic_api_key,
                max_tokens=4000,
                temperature=0.7
            ),
            "zhipuai": AIProviderConfig(
                name="zhipuai",
                type="zhipuai",
                model=self.zhipuai_model,
                api_key=self.zhipuai_api_key,
                max_tokens=4000,
                temperature=0.7
            ),
            "openai": AIProviderConfig(
                name="openai",
                type="openai",
                model=self.openai_model,
                api_key=self.openai_api_key,
                max_tokens=4000,
                temperature=0.7
            )
        }

    def get_builder_team_config(self) -> Dict[str, Any]:
        """Get Builder Team specific configuration."""
        return {
            "advisory_team": {
                "product_strategist": {
                    "name": "ProductStrategist",
                    "role": "Product vision and strategic planning",
                    "mbti": "ENTJ",
                    "provider": "claude",
                    "responsibilities": [
                        "Define project roadmap and milestones",
                        "Make strategic decisions on feature prioritization",
                        "Coordinate between advisory and application teams",
                        "Validate business logic implementation"
                    ]
                },
                "technical_architect": {
                    "name": "TechnicalArchitect",
                    "role": "System design and technical strategy",
                    "mbti": "INTJ",
                    "provider": "claude",
                    "responsibilities": [
                        "Design overall system architecture",
                        "Make technical decisions and trade-offs",
                        "Review and approve technical implementations",
                        "Ensure scalability and performance requirements"
                    ]
                },
                "ux_designer": {
                    "name": "UXDesigner",
                    "role": "User experience and interface design",
                    "mbti": "ENFP",
                    "provider": "claude",
                    "responsibilities": [
                        "Design user interactions and workflows",
                        "Create wireframes and prototypes",
                        "Ensure accessibility and usability",
                        "Validate user experience implementation"
                    ]
                },
                "quality_engineer": {
                    "name": "QualityEngineer",
                    "role": "Quality assurance and testing strategy",
                    "mbti": "ISTJ",
                    "provider": "zhipuai",
                    "responsibilities": [
                        "Define testing strategies and frameworks",
                        "Review code quality and standards",
                        "Implement automated testing pipelines",
                        "Ensure reliability and stability"
                    ]
                },
                "devops_specialist": {
                    "name": "DevOpsSpecialist",
                    "role": "Infrastructure and deployment",
                    "mbti": "ISTP",
                    "provider": "zhipuai",
                    "responsibilities": [
                        "Set up CI/CD pipelines",
                        "Manage deployment infrastructure",
                        "Monitor system performance and health",
                        "Implement security and compliance measures"
                    ]
                }
            }
        }

# Global configuration instance
config = BuilderTeamConfig()

def get_config() -> BuilderTeamConfig:
    """Get the global configuration instance."""
    return config

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def ensure_directories():
    """Ensure all required directories exist."""
    directories = [
        "logs",
        "data",
        "uploads",
        "backups",
        "cache",
        "temp",
        "output",
        "generated"
    ]

    project_root = get_project_root()
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)