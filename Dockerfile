# AI Crew Builder Team - Docker Container
# Multi-stage build for optimized production deployment

# ==========================================
# Base Stage - Python Environment
# ==========================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# ==========================================
# Dependencies Stage
# ==========================================
FROM base as dependencies

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ==========================================
# Development Stage
# ==========================================
FROM dependencies as development

# Install development dependencies
RUN pip install pytest pytest-cov black flake8 mypy

# Copy source code
COPY . .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Expose ports
EXPOSE 8000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command for development
CMD ["python", "scripts/start.py"]

# ==========================================
# Production Stage
# ==========================================
FROM dependencies as production

# Copy only necessary files for production
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY openspec/ ./openspec/
COPY templates/ ./templates/
COPY src/ ./src/
COPY requirements.txt .
COPY README.md .
COPY .env.example .

# Create production directories
RUN mkdir -p logs data uploads backups cache temp output generated && \
    chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Expose ports
EXPOSE 8000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["python", "scripts/start.py", "--production"]

# ==========================================
# Testing Stage
# ==========================================
FROM development as testing

# Run tests
RUN python -m pytest tests/ -v --cov=src --cov-report=html

# Default command for testing
CMD ["python", "-m", "pytest", "tests/", "-v"]