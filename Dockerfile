FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install django django-pyas2 psycopg2-binary gunicorn

# Copy project files
COPY . /app/
COPY api_views.py /app/api_views.py

# Create data directories
RUN mkdir -p /app/P1/data /app/P2/data

# Expose ports
EXPOSE 8000 8001

# Default command (will be overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
