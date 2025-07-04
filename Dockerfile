# Use an official Python runtime as a parent image
FROM python:3.11.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (optional: only if needed, e.g., for psycopg2, PIL, etc.)
# RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy and install Python dependencies first (leverages Docker cache)
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Default: use gunicorn (override in docker-compose)
# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "60"]
