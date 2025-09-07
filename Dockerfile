FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY annotatorx/ ./annotatorx/
COPY datasets/ ./datasets/
COPY annotations/ ./annotations/
COPY tests/ ./tests/

# Create directories for outputs
RUN mkdir -p datasets annotations

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "annotatorx", "--help"]
