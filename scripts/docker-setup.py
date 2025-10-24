#!/usr/bin/env python3
"""
AI Crew Builder Team - Docker Setup Script
Sets up Docker containers and manages the development environment.
"""

import os
import sys
import subprocess
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
            print(f"Error: {e.stderr}")
        return None

def check_docker():
    """Check if Docker is installed and running"""
    print("🐳 Checking Docker installation...")

    # Check Docker command
    result = run_command("docker --version", "Checking Docker version", check=False)
    if not result:
        print("❌ Docker is not installed or not in PATH")
        print("Please install Docker from https://docker.com")
        return False

    # Check Docker daemon
    result = run_command("docker info", "Checking Docker daemon", check=False)
    if not result:
        print("❌ Docker daemon is not running")
        print("Please start Docker Desktop or Docker service")
        return False

    print("✅ Docker is installed and running")
    return True

def check_docker_compose():
    """Check if Docker Compose is installed"""
    print("🔧 Checking Docker Compose...")

    # Check for docker-compose (older versions) or docker compose (newer versions)
    result = run_command("docker-compose --version", "Checking docker-compose", check=False)
    if not result:
        result = run_command("docker compose version", "Checking docker compose", check=False)
        if not result:
            print("❌ Docker Compose is not installed")
            print("Please install Docker Compose from https://docs.docker.com/compose/")
            return False

    print("✅ Docker Compose is available")
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    print("📝 Setting up environment file...")

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
            return False
    else:
        print("✅ .env file already exists")

    return True

def build_images(dev=True):
    """Build Docker images"""
    print(f"🏗️  Building Docker images ({'development' if dev else 'production'})...")

    if dev:
        command = "docker-compose build"
    else:
        command = "docker-compose -f docker-compose.yml -f docker-compose.prod.yml build"

    result = run_command(command, "Building Docker images")
    return result is not None

def start_services(dev=True):
    """Start Docker services"""
    print(f"🚀 Starting Docker services ({'development' if dev else 'production'})...")

    if dev:
        command = "docker-compose up -d"
    else:
        command = "docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d"

    result = run_command(command, "Starting services")
    return result is not None

def stop_services():
    """Stop Docker services"""
    print("🛑 Stopping Docker services...")
    result = run_command("docker-compose down", "Stopping services")
    return result is not None

def show_logs():
    """Show Docker logs"""
    print("📋 Showing Docker logs...")
    run_command("docker-compose logs -f", "Showing logs", check=False)

def show_status():
    """Show Docker service status"""
    print("📊 Docker service status:")
    run_command("docker-compose ps", "Service status")

def clean_docker():
    """Clean Docker resources"""
    print("🧹 Cleaning Docker resources...")

    commands = [
        "docker-compose down -v",
        "docker system prune -f",
        "docker volume prune -f"
    ]

    for command in commands:
        run_command(command, f"Running: {command}")

def backup_data():
    """Backup Docker volumes"""
    print("💾 Backing up Docker volumes...")

    # Create backup directory
    backup_dir = Path.cwd() / "backups" / "docker"
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Backup PostgreSQL
    run_command(
        f"docker-compose exec -T postgres pg_dump -U appuser builder_team > {backup_dir}/postgres_$(date +%Y%m%d_%H%M%S).sql",
        "Backing up PostgreSQL"
    )

    # Backup Redis
    run_command(
        f"docker-compose exec -T redis redis-cli BGSAVE",
        "Triggering Redis backup"
    )

def restore_data(backup_file):
    """Restore Docker volumes from backup"""
    print(f"🔄 Restoring from backup: {backup_file}")

    result = run_command(
        f"docker-compose exec -T postgres psql -U appuser -d builder_team < {backup_file}",
        "Restoring PostgreSQL"
    )

    return result is not None

def shell_service(service_name):
    """Open shell in a service container"""
    print(f"🐚 Opening shell in {service_name}...")
    run_command(f"docker-compose exec {service_name} /bin/bash", f"Shell in {service_name}", check=False)

def run_tests():
    """Run tests in Docker container"""
    print("🧪 Running tests in Docker...")

    # Build test image
    run_command("docker build --target testing -t builder-team-test .", "Building test image")

    # Run tests
    result = run_command("docker run --rm builder-team-test", "Running tests")
    return result is not None

def main():
    """Main Docker setup function"""
    parser = argparse.ArgumentParser(description="AI Crew Builder Team Docker Setup")
    parser.add_argument("command", choices=[
        "setup", "build", "start", "stop", "restart", "logs",
        "status", "clean", "backup", "restore", "shell", "test"
    ], help="Command to run")
    parser.add_argument("--production", action="store_true", help="Use production configuration")
    parser.add_argument("--service", help="Service name for shell command")
    parser.add_argument("--backup-file", help="Backup file for restore command")

    args = parser.parse_args()

    print("🐳 AI Crew Builder Team - Docker Setup")
    print("=" * 40)

    # Check Docker prerequisites
    if not check_docker() or not check_docker_compose():
        sys.exit(1)

    # Create environment file
    if not create_env_file():
        sys.exit(1)

    dev = not args.production

    # Execute command
    if args.command == "setup":
        success = build_images(dev) and start_services(dev)
        if success:
            print("\n🎉 Docker setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Edit your .env file with API keys")
            print("2. Check service status: python scripts/docker-setup.py status")
            print("3. View logs: python scripts/docker-setup.py logs")
            print("4. Access the application at http://localhost:8000")

    elif args.command == "build":
        build_images(dev)

    elif args.command == "start":
        start_services(dev)

    elif args.command == "stop":
        stop_services()

    elif args.command == "restart":
        stop_services()
        start_services(dev)

    elif args.command == "logs":
        show_logs()

    elif args.command == "status":
        show_status()

    elif args.command == "clean":
        clean_docker()

    elif args.command == "backup":
        backup_data()

    elif args.command == "restore":
        if not args.backup_file:
            print("❌ --backup-file is required for restore command")
            sys.exit(1)
        restore_data(args.backup_file)

    elif args.command == "shell":
        if not args.service:
            print("❌ --service is required for shell command")
            print("Available services: builder-team, redis, postgres, nginx, worker, scheduler")
            sys.exit(1)
        shell_service(args.service)

    elif args.command == "test":
        run_tests()

if __name__ == "__main__":
    main()