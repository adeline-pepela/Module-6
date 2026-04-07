FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Install system dependencies with retries
RUN apt-get update -o Acquire::Retries=5 && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_no_shap.txt ./requirements.txt
RUN pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY models/ ./models/
COPY data/ ./data/
COPY frontend/ ./frontend/

WORKDIR /app/backend

# Create database directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/dashboard/metrics || exit 1

# Copy entrypoint script
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Run application
ENTRYPOINT ["/app/docker-entrypoint.sh"]
