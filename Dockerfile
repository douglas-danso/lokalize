# Dockerfile for Fashion Localization RAG System
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY quickstart.py .
COPY README.md .

# Create data directory for local storage
RUN mkdir -p data/

# Expose port for potential web interface
EXPOSE 8080

# Default command runs the demo
CMD ["python", "quickstart.py"]
