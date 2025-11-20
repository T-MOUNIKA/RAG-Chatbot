FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies in one step and clean cache to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    gcc \
    libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker cache for dependency installs
COPY requirements.txt .

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir langchain chromadb
# Copy the application code last to maximize cache usage for dependencies
COPY . .

# Set environment variable to ensure logs are output properly
ENV PYTHONUNBUFFERED=1

# Default command to run your FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
