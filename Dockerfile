FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for caching)
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install --no-cache-dir poetry

# Disable venv creation
RUN poetry config virtualenvs.create false

# Install ONLY dependencies (no project yet)
RUN poetry install --no-root --no-interaction --no-ansi

# Copy application code AFTER deps
COPY . /app

# Install the project itself
RUN poetry install --no-interaction --no-ansi

# Default command
CMD ["llm-eval", "--help"]

