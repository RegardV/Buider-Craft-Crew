#!/usr/bin/env python3
"""
AI Crew Builder Team - Complete Environment Setup Script
Sets up both local and Docker environments for the AI Crew Builder Team.
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")

def create_virtual_environment():
    """Create virtual environment"""
    print("\n📦 Creating virtual environment...")
    venv_path = Path.cwd() / ".venv"

    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("Recreate it? (y/N): ").strip().lower()
        if response != 'y':
            print("✅ Using existing virtual environment")
            return
        print("🗑️  Removing existing virtual environment...")
        run_command(f"rm -rf {venv_path}", "Removing virtual environment")

    # Create virtual environment
    success = run_command(f'python{sys.version_info.major}.{sys.version_info.minor} -m venv .venv', "Creating virtual environment")
    if not success:
        print("❌ Failed to create virtual environment")
        sys.exit(1)

def install_dependencies():
    """Install Python dependencies"""
    print("\n📚 Installing Python dependencies...")

    # Upgrade pip
    run_command("python -m pip install --upgrade pip", "Upgrading pip")

    # Install requirements
    success = run_command("pip install -r requirements.txt", "Installing requirements")
    if not success:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")

    directories = [
        "logs",
        "data",
        "uploads",
        "backups",
        "cache",
        "temp",
        "output",
        "generated",
        "Projects_Derived",
        "LLM_output",
        "JSON_output",
        "media_output",
        "PDF_output",
        "src",
        "src/core",
        "src/agents",
        "src/workflows",
        "src/tools",
        "src/api",
        "tests",
        "monitoring",
        "monitoring/grafana/dashboards",
        "monitoring/grafana/datasources"
    ]

    for directory in directories:
        dir_path = Path.cwd() / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}/ directory")

def setup_environment_file():
    """Set up environment file"""
    print("\n🔧 Setting up environment configuration...")

    env_file = Path.cwd() / ".env"
    env_example = Path.cwd() / ".env.example"

    if not env_file.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ Created .env from .env.example")
            print("⚠️  Please edit .env file with your API keys")
        else:
            print("❌ .env.example file not found")
    else:
        print("✅ .env file already exists")

def create_docker_environment():
    """Create Docker-related files"""
    print("\n🐳 Setting up Docker environment...")

    # Create Docker directories
    docker_dirs = ["nginx/ssl", "backups/docker", "logs/nginx"]
    for directory in docker_dirs:
        dir_path = Path.cwd() / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}/ directory")

    # Create self-signed SSL certificates for development
    ssl_dir = Path.cwd() / "nginx" / "ssl"
    cert_file = ssl_dir / "cert.pem"
    key_file = ssl_dir / "key.pem"

    if not cert_file.exists() or not key_file.exists():
        print("🔐 Creating self-signed SSL certificates...")
        run_command(
            f"openssl req -x509 -nodes -days 365 -newkey rsa:2048 "
            f"-keyout {key_file} -out {cert_file} "
            f"-subj '/C=US/ST=State/L=City/O=Organization/CN=localhost'",
            "Creating SSL certificates"
        )

def create_database_init():
    """Create database initialization script"""
    print("\n🗄️  Creating database initialization script...")

    init_sql = """-- AI Crew Builder Team - Database Initialization
CREATE DATABASE IF NOT EXISTS builder_team;
CREATE DATABASE IF NOT EXISTS builder_team_prod;

-- Create user and grant permissions
CREATE USER IF NOT EXISTS appuser WITH PASSWORD 'app_password';
GRANT ALL PRIVILEGES ON DATABASE builder_team TO appuser;
GRANT ALL PRIVILEGES ON DATABASE builder_team_prod TO appuser;

-- Basic tables
\\c builder_team;

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    config JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS builder_sessions (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    session_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS openspec_changes (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    change_type VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(50) DEFAULT 'proposed',
    content JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

    init_script = Path.cwd() / "scripts" / "init-db.sql"
    with open(init_script, 'w') as f:
        f.write(init_sql)
    print("✅ Created database initialization script")

def create_basic_project_structure():
    """Create basic Python project structure"""
    print("\n🏗️  Creating basic project structure...")

    # Create __init__.py files
    init_files = [
        "src/__init__.py",
        "src/core/__init__.py",
        "src/agents/__init__.py",
        "src/workflows/__init__.py",
        "src/tools/__init__.py",
        "src/api/__init__.py",
        "tests/__init__.py"
    ]

    for init_file in init_files:
        file_path = Path.cwd() / init_file
        if not file_path.exists():
            file_path.touch()
            print(f"✅ Created {init_file}")

def test_local_setup():
    """Test local setup"""
    print("\n🧪 Testing local setup...")

    try:
        # Test imports
        import anthropic
        import openai
        import zhipuai
        import yaml
        import dotenv
        print("✅ All major imports successful")

        # Test configuration loading
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loading successful")

        # Test directory structure
        required_dirs = ["config", "scripts", "openspec", "logs", "src"]
        for dir_name in required_dirs:
            dir_path = Path.cwd() / dir_name
            if dir_path.exists():
                print(f"✅ {dir_name}/ directory exists")
            else:
                print(f"❌ {dir_name}/ directory missing")

    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    return True

def test_docker_setup():
    """Test Docker setup"""
    print("\n🐳 Testing Docker setup...")

    # Check Docker
    docker_check = run_command("docker --version", "Checking Docker", check=False)
    if not docker_check:
        print("⚠️  Docker not available - skipping Docker tests")
        return True

    # Check Docker Compose
    compose_check = run_command("docker compose version", "Checking Docker Compose", check=False)
    if not compose_check:
        compose_check = run_command("docker-compose --version", "Checking docker-compose", check=False)

    if not compose_check:
        print("⚠️  Docker Compose not available - skipping Docker tests")
        return True

    print("✅ Docker and Docker Compose are available")
    return True

def print_next_steps(setup_type):
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")

    if setup_type in ["local", "both"]:
        print("\n🏠 Local Development:")
        print("1. Activate virtual environment:")
        if platform.system().lower() == "windows":
            print("   .venv\\Scripts\\activate")
        else:
            print("   source .venv/bin/activate")

        print("2. Edit your environment file:")
        print("   nano .env  # or your preferred editor")
        print("   Add your API keys for Anthropic, ZhipuAI, and OpenAI")

        print("3. Test the builder team:")
        print("   python scripts/start.py")

    if setup_type in ["docker", "both"]:
        print("\n🐳 Docker Development:")
        print("1. Edit your environment file:")
        print("   nano .env")
        print("   Add your API keys")

        print("2. Set up Docker environment:")
        print("   python scripts/docker-setup.py setup")

        print("3. Check service status:")
        print("   python scripts/docker-setup.py status")

        print("4. View logs:")
        print("   python scripts/docker-setup.py logs")

        print("5. Access the application at http://localhost:8000")

    print("\n📚 For help, see README.md")
    print("\n🚀 To initialize a new project:")
    print("   python scripts/init-project.py")

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="AI Crew Builder Team - Environment Setup")
    parser.add_argument("--type", choices=["local", "docker", "both"], default="both",
                       help="Type of setup to perform")
    parser.add_argument("--skip-deps", action="store_true",
                       help="Skip installing Python dependencies")

    args = parser.parse_args()

    print("🚀 AI Crew Builder Team - Complete Environment Setup")
    print("=" * 60)

    # Check Python version
    check_python_version()

    setup_type = args.type

    if setup_type in ["local", "both"]:
        print("\n🏠 Setting up Local Environment")
        print("-" * 30)

        # Create virtual environment
        create_virtual_environment()

        # Install dependencies
        if not args.skip_deps:
            install_dependencies()

        # Create directories
        create_directories()

        # Setup environment file
        setup_environment_file()

        # Create basic structure
        create_basic_project_structure()
        create_database_init()

        # Test local setup
        if test_local_setup():
            print("✅ Local environment setup completed successfully")
        else:
            print("⚠️  Local environment setup completed with warnings")

    if setup_type in ["docker", "both"]:
        print("\n🐳 Setting up Docker Environment")
        print("-" * 30)

        # Create Docker environment
        create_docker_environment()

        # Test Docker setup
        if test_docker_setup():
            print("✅ Docker environment setup completed successfully")
            print("\n💡 To start Docker services:")
            print("   python scripts/docker-setup.py setup")
        else:
            print("⚠️  Docker environment setup completed with warnings")

    # Print next steps
    print_next_steps(setup_type)

    print(f"\n🎯 Setup type: {setup_type}")
    if setup_type == "both":
        print("💡 You can use both local and Docker environments!")
    elif setup_type == "local":
        print("💡 Local environment is ready for development!")
    elif setup_type == "docker":
        print("💡 Docker environment is ready for deployment!")

if __name__ == "__main__":
    main()