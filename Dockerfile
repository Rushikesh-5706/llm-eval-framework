FROM python:3.9-slim

# Prevent Python from writing .pyc files and ensure immediate log output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first to leverage Docker's layer caching
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and configure it to install directly into the system environment
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Register the 'llm-eval' command by installing the project itself
RUN pip install .

# Set the command as the ENTRYPOINT to turn the container into an executable
ENTRYPOINT ["llm-eval"]
CMD ["--help"]
