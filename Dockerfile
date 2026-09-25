# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# System deps needed for psycopg2 and general builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager used by this project)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency manifests first for better layer caching
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies into a project-local venv (no dev deps in the image)
RUN uv sync --frozen --no-dev

# Copy the rest of the project
COPY data_generator/ ./data_generator/
COPY database/ ./database/
COPY src/ ./src/
COPY sql/ ./sql/
COPY tests/ ./tests/
COPY airflow/ ./airflow/

# Make sure the venv's binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Default: run the full pipeline (generate -> validate -> load)
CMD ["sh", "-c", "\
    python data_generator/generate_customers.py && \
    python data_generator/generate_accounts.py && \
    python data_generator/generate_transactions.py && \
    python -m src.etl.validate && \
    python -m src.etl.load"]
