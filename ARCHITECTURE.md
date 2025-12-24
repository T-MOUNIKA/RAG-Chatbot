# Technical Architecture

## System Overview

The RAG PDF Chatbot is built using a microservices architecture with the following key components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   FastAPI       │    │   OpenAI API    │
│   (Browser)     │◄──►│   Server        │◄──►│   (GPT-4o-mini) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   ChromaDB      │    │   PDF Files     │
                       │ (Vector Store)  │◄───│   (Documents)   │
                       └─────────────────┘    └─────────────────┘
```

## Core Components

### 1. FastAPI Application (`src/main.py`)

**Responsibilities:**
- HTTP request handling
- API endpoint management
- CORS configuration
- Static file serving
- Error handling and logging

**Key Features:**
- Async request processing
- Automatic API documentation
- Pydantic data validation
- Middleware support

### 2. Vector Database (ChromaDB)

**Purpose:**
- Store document embeddings
- Perform similarity search
- Persist vector data

**Configuration:**
```python
vectorstore = Chroma(
    collection_name='rag_pdf_collection',
    embedding_function=OpenAIEmbeddings(),
    persist_directory='./chroma_data'
)
```

**Storage Structure:**
```
chroma_data/
├── chroma.sqlite3          # Metadata database
└── [collection_id]/        # Vector embeddings
    ├── data_level0.bin
    ├── header.bin
    └── length.bin
```

### 3. Document Processing Pipeline

**Ingestion Flow:**
```
PDF Files → Text Extraction → Text Chunking → Embedding Generation → Vector Storage
```

**Text Chunking Strategy:**
- Chunk size: 1000 characters
- Overlap: 200 characters
- Method: Recursive character splitting

### 4. RAG (Retrieval-Augmented Generation) Pipeline

**Query Processing Flow:**
```
User Query → Embedding → Similarity Search → Context Assembly → LLM Generation → Response
```

**Detailed Steps:**
1. **Query Embedding**: Convert user question to vector using OpenAI embeddings
2. **Similarity Search**: Find top-k (k=4) most relevant document chunks
3. **Context Assembly**: Combine retrieved chunks into context string
4. **Prompt Construction**: Insert context and question into template
5. **LLM Generation**: Send to OpenAI GPT-4o-mini for response
6. **Response Filtering**: Ensure answer stays within document scope

### 5. Prompt Engineering

**Template Structure:**
```python
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the provided context, just say "I don't have information about that in the provided documents."
Do not make up an answer or use information outside of the provided context.

Context:
{context}

Question: {question}
Answer:"""
```

**Design Principles:**
- Clear instruction boundaries
- Explicit restriction to context
- Fallback response for unknown queries
- Context-question separation

## Data Flow Architecture

### 1. Document Ingestion
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ PDF Files   │───►│ Text        │───►│ Text        │───►│ Vector      │
│ (data/)     │    │ Extraction  │    │ Chunking    │    │ Storage     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                   │                   │
                    PyPDF2 Library    RecursiveTextSplitter   ChromaDB
```

### 2. Query Processing
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ User Query  │───►│ Vector      │───►│ Document    │───►│ LLM         │
│ (HTTP POST) │    │ Search      │    │ Retrieval   │    │ Generation  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                   │                   │
                   Similarity Search    Top-K Results      OpenAI API
```

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation using Python type annotations

### AI/ML Components
- **LangChain**: Framework for developing LLM applications
- **OpenAI API**: GPT-4o-mini for text generation
- **OpenAI Embeddings**: text-embedding-ada-002 for vector embeddings

### Vector Database
- **ChromaDB**: Open-source embedding database
- **SQLite**: Metadata storage backend

### Document Processing
- **PyPDF2**: PDF text extraction
- **RecursiveCharacterTextSplitter**: Intelligent text chunking

### Development Tools
- **Python-dotenv**: Environment variable management
- **Logging**: Built-in Python logging for debugging

## Security Architecture

### API Security
- **Input Validation**: Pydantic models prevent malformed requests
- **Error Handling**: Comprehensive exception handling
- **CORS Configuration**: Controlled cross-origin access

### Data Security
- **Environment Variables**: Sensitive data (API keys) in .env files
- **Local Storage**: Vector data stored locally, not in cloud
- **No User Data Persistence**: Queries not stored permanently

### AI Safety
- **Prompt Injection Protection**: Template-based prompts
- **Response Filtering**: Explicit instructions to stay within context
- **Content Restriction**: Only document-based responses allowed

## Performance Considerations

### Latency Optimization
- **Async Processing**: Non-blocking request handling
- **Vector Search**: O(log n) similarity search complexity
- **Chunking Strategy**: Balanced chunk size for relevance vs. speed

### Memory Management
- **Lazy Loading**: Documents loaded on-demand
- **Vector Caching**: ChromaDB handles embedding caching
- **Connection Pooling**: Efficient database connections

### Scalability Factors
- **Horizontal Scaling**: Multiple FastAPI instances possible
- **Database Scaling**: ChromaDB supports distributed deployments
- **API Rate Limits**: OpenAI API constraints apply

## Monitoring and Logging

### Application Logging
```python
logging.basicConfig(level=logging.INFO)
```

**Logged Events:**
- Incoming queries
- Document retrieval results
- LLM responses
- Error conditions

### Health Monitoring
- `/health` endpoint for service status
- Exception tracking and reporting
- Response time monitoring

## Deployment Architecture

### Local Development
```
Developer Machine
├── Python Environment
├── Local ChromaDB
├── FastAPI Server (localhost:8000)
└── PDF Documents (data/)
```

### Production Considerations
- **Containerization**: Docker support available
- **Environment Management**: Separate .env files per environment
- **Database Persistence**: Persistent volume for ChromaDB
- **Load Balancing**: Multiple server instances
- **API Gateway**: Rate limiting and authentication

## Configuration Management

### Environment Variables
```env
# Core Configuration
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
PORT=8000

# Vector Database
CHROMA_COLLECTION_NAME=rag_pdf_collection
CHROMA_PERSIST_DIR=./chroma_data

# Processing Parameters
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
```

### Runtime Configuration
- Model parameters (temperature, max_tokens)
- Retrieval parameters (similarity threshold, top-k)
- Chunking parameters (size, overlap)
- API timeouts and retries