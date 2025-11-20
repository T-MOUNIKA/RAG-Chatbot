# 

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    gcc \
    libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install correct LangChain ecosystem packages
RUN pip install --no-cache-dir langchain==0.2.11
RUN pip install --no-cache-dir langchain-community
RUN pip install --no-cache-dir langchain-openai
RUN pip install --no-cache-dir chromadb

# Copy all project files
COPY . .

ENV PYTHONUNBUFFERED=1

# Run FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
