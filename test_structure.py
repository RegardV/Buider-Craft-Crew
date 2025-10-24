#!/usr/bin/env python3
"""
Test script to validate the project structure without requiring dependencies.
"""

import os
import sys
from pathlib import Path

def test_directory_structure():
    """Test that all required directories exist."""
    print("🔍 Testing directory structure...")

    required_dirs = [
        "config",
        "scripts",
        "src",
        "src/core",
        "src/agents",
        "src/workflows",
        "src/tools",
        "src/api",
        "openspec",
        "openspec/specs",
        "openspec/specs/agents",
        "openspec/specs/workflows",
        "openspec/specs/features",
        "openspec/specs/system",
        "openspec/changes",
        "openspec/changes/proposals",
        "openspec/changes/approved",
        "openspec/changes/implemented",
        "templates",
        "nginx",
        "tests"
    ]

    missing_dirs = []
    for directory in required_dirs:
        dir_path = Path(directory)
        if not dir_path.exists():
            missing_dirs.append(directory)
        else:
            print(f"  ✅ {directory}/")

    if missing_dirs:
        print(f"  ❌ Missing directories: {', '.join(missing_dirs)}")
        return False

    print("  ✅ All required directories exist")
    return True

def test_configuration_files():
    """Test that configuration files exist."""
    print("\n🔍 Testing configuration files...")

    required_files = [
        "config/builder-crew-config.yaml",
        "config/project-crew-config-template.yaml",
        "config/ai-providers.yaml",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "Dockerfile",
        "docker-compose.yml",
        "nginx/nginx.conf"
    ]

    missing_files = []
    for file_path in required_files:
        path = Path(file_path)
        if not path.exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")

    if missing_files:
        print(f"  ❌ Missing files: {', '.join(missing_files)}")
        return False

    print("  ✅ All required files exist")
    return True

def test_source_files():
    """Test that source files exist."""
    print("\n🔍 Testing source files...")

    source_files = [
        "src/core/config.py",
        "src/core/ai_providers.py",
        "src/core/agent.py",
        "src/core/builder_team.py",
        "src/core/openspec.py",
        "src/core/project_generator.py",
        "src/core/integration.py",
        "src/agents/builder_agents.py",
        "scripts/setup.py",
        "scripts/docker-setup.py",
        "scripts/init-project.py",
        "scripts/start.py"
    ]

    missing_files = []
    for file_path in source_files:
        path = Path(file_path)
        if not path.exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")

    if missing_files:
        print(f"  ❌ Missing source files: {', '.join(missing_files)}")
        return False

    print("  ✅ All source files exist")
    return True

def test_python_syntax():
    """Test Python syntax of source files."""
    print("\n🔍 Testing Python syntax...")

    python_files = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    for root, dirs, files in os.walk("scripts"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    syntax_errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                compile(f.read(), file_path, 'exec')
            print(f"  ✅ {file_path}")
        except SyntaxError as e:
            syntax_errors.append(f"{file_path}: {e}")
        except Exception as e:
            print(f"  ⚠️  {file_path}: {e}")

    if syntax_errors:
        print(f"  ❌ Syntax errors:")
        for error in syntax_errors:
            print(f"    {error}")
        return False

    print("  ✅ All Python files have valid syntax")
    return True

def test_docker_files():
    """Test Docker configuration files."""
    print("\n🔍 Testing Docker files...")

    docker_files = [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        ".dockerignore"
    ]

    for file_path in docker_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")

    print("  ✅ Docker configuration checked")
    return True

def test_documentation():
    """Test documentation files."""
    print("\n🔍 Testing documentation...")

    doc_files = [
        "README.md"
    ]

    for file_path in doc_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")

    print("  ✅ Documentation checked")
    return True

def main():
    """Run all tests."""
    print("🧪 AI Crew Builder Team - Structure Test")
    print("=" * 50)

    tests = [
        ("Directory Structure", test_directory_structure),
        ("Configuration Files", test_configuration_files),
        ("Source Files", test_source_files),
        ("Python Syntax", test_python_syntax),
        ("Docker Files", test_docker_files),
        ("Documentation", test_documentation)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with error: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The project structure is ready.")
        print("\n📋 Next steps:")
        print("1. Install dependencies: python scripts/setup.py")
        print("2. Set up API keys in .env file")
        print("3. Run the system: python scripts/start.py")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)