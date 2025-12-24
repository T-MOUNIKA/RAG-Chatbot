# Deployment Guide

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Storage**: 1GB free space (more for large document collections)
- **Network**: Internet access for OpenAI API calls

### Required Accounts
- **OpenAI Account**: For API access and billing
- **API Key**: GPT-4o-mini access required

## Local Development Setup

### 1. Environment Setup
```bash
# Clone/download project
cd rag-pdf-chatbot-original

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
OPENAI_API_KEY=your_actual_api_key_here
CHROMA_COLLECTION_NAME=rag_pdf_collection
LLM_MODEL=gpt-4o-mini
CHROMA_PERSIST_DIR=./chroma_data
PORT=8000
```

### 3. Document Ingestion
```bash
# Place PDF files in data/ directory
cp your_documents.pdf data/

# Run ingestion
python simple_ingest.py
```

### 4. Start Development Server
```bash
# Start with auto-reload
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Or start without reload
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 5. Verify Installation
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat functionality
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is in the documents?"}'
```

## Production Deployment

### Option 1: Docker Deployment

**Create Dockerfile:**
```dockerfile
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
COPY . .

# Create data and chroma_data directories
RUN mkdir -p data chroma_data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
# Build image
docker build -t rag-chatbot .

# Run container
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/chroma_data:/app/chroma_data \
  -v $(pwd)/.env:/app/.env \
  rag-chatbot
```

### Option 2: Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  rag-chatbot:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./chroma_data:/app/chroma_data
      - ./.env:/app/.env
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Deploy:**
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Cloud Deployment

#### AWS EC2 Deployment
```bash
# Launch EC2 instance (Ubuntu 20.04 LTS)
# Connect via SSH

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Clone project
git clone <your-repo-url>
cd rag-pdf-chatbot-original

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Install process manager
pip install gunicorn

# Run with Gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### Heroku Deployment
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-rag-chatbot

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set LLM_MODEL=gpt-4o-mini

# Create Procfile
echo "web: uvicorn src.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Environment Configuration

### Development Environment
```env
# .env.development
OPENAI_API_KEY=sk-dev-key
LLM_MODEL=gpt-4o-mini
CHROMA_PERSIST_DIR=./chroma_data_dev
PORT=8000
DEBUG=True
```

### Production Environment
```env
# .env.production
OPENAI_API_KEY=sk-prod-key
LLM_MODEL=gpt-4o-mini
CHROMA_PERSIST_DIR=/app/chroma_data
PORT=8000
DEBUG=False
```

## Monitoring and Maintenance

### Health Checks
```bash
# Basic health check
curl http://your-domain:8000/health

# Detailed system check
curl -X POST http://your-domain:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'
```

### Log Management
```bash
# View application logs
tail -f /var/log/rag-chatbot.log

# Docker logs
docker logs -f rag-chatbot

# Docker Compose logs
docker-compose logs -f rag-chatbot
```

### Database Maintenance
```bash
# Backup ChromaDB
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_data/

# Restore ChromaDB
tar -xzf chroma_backup_20240101.tar.gz

# Clear and rebuild database
rm -rf chroma_data/
python simple_ingest.py
```

### Performance Monitoring
```python
# Add to main.py for basic metrics
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Scaling Considerations

### Horizontal Scaling
```bash
# Run multiple instances
uvicorn src.main:app --host 0.0.0.0 --port 8001 &
uvicorn src.main:app --host 0.0.0.0 --port 8002 &
uvicorn src.main:app --host 0.0.0.0 --port 8003 &

# Use load balancer (nginx example)
upstream rag_backend {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}
```

### Database Scaling
- **Read Replicas**: Multiple ChromaDB instances for read operations
- **Sharding**: Distribute documents across multiple collections
- **Caching**: Redis for frequently accessed embeddings

### API Rate Limiting
```python
# Add rate limiting middleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, q: Query):
    # ... existing code
```

## Security Hardening

### API Security
```python
# Add API key authentication
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    if token.credentials != os.getenv("API_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
```

### HTTPS Configuration
```bash
# Generate SSL certificate (Let's Encrypt)
sudo certbot --nginx -d your-domain.com

# Or use self-signed for development
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### Environment Security
```bash
# Restrict file permissions
chmod 600 .env
chmod 700 chroma_data/

# Use secrets management in production
# AWS Secrets Manager, Azure Key Vault, etc.
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

2. **ChromaDB permission errors**
   ```bash
   # Fix permissions
   sudo chown -R $USER:$USER chroma_data/
   chmod -R 755 chroma_data/
   ```

3. **OpenAI API errors**
   ```bash
   # Test API key
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

4. **Memory issues**
   ```bash
   # Monitor memory usage
   htop
   # Increase swap space if needed
   sudo fallocate -l 2G /swapfile
   ```

### Debug Mode
```bash
# Run with debug logging
export PYTHONPATH=/app
export DEBUG=True
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level debug
```