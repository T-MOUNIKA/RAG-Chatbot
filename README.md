# RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based solely on uploaded PDF documents using OpenAI's GPT models and ChromaDB for vector storage.

## 🚀 Features

- **Document-Restricted Responses**: Only answers questions based on ingested PDF documents
- **Vector Search**: Uses ChromaDB for efficient document retrieval
- **OpenAI Integration**: Powered by GPT-4o-mini for intelligent responses
- **FastAPI Backend**: RESTful API with automatic documentation
- **Web Interface**: Simple HTML frontend for easy interaction
- **CORS Enabled**: Cross-origin requests supported

## 📁 Project Structure

```
rag-pdf-chatbot-original/
├── src/
│   ├── static/
│   │   └── index.html          # Web interface
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── retriever.py            # Document retrieval logic
│   ├── llm.py                  # Language model configuration
│   ├── chroma_client.py        # ChromaDB client
│   ├── utils.py                # Utility functions
│   └── ingest.py               # Document ingestion script
├── data/                       # PDF documents directory
│   ├── DockerKuberntesMasterclassTypedNotes dec.pdf
│   └── sample_langgraph_langchain.pdf
├── chroma_data/                # Vector database storage
├── examples/
│   └── sample.pdf
├── .env                        # Environment variables
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── simple_ingest.py            # Simplified ingestion script
├── test_api.py                 # API testing script
├── test_api.bat                # Windows batch test script
└── README.md                   # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. **Clone/Download the project**
   ```bash
   cd rag-pdf-chatbot-original
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   CHROMA_COLLECTION_NAME=rag_pdf_collection
   EMBEDDING_MODEL=openai
   LLM_MODEL=gpt-4o-mini
   PERSIST=True
   PORT=8000
   CHROMA_PERSIST_DIR=./chroma_data
   ```

4. **Ingest PDF documents**
   ```bash
   python simple_ingest.py
   ```

5. **Start the server**
   ```bash
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 📚 API Documentation

### Endpoints

#### `GET /`
Returns the web interface HTML page.

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "okay"
}
```

#### `POST /api/chat`
Main chat endpoint for asking questions.

**Request Body:**
```json
{
  "question": "What is Docker?"
}
```

**Response:**
```json
{
  "answer": "Docker is a containerization platform..."
}
```

**Restricted Response (when no relevant documents found):**
```json
{
  "answer": "I don't have information about that in the provided documents."
}
```

## 🔧 Core Components

### 1. Document Ingestion (`simple_ingest.py`)
- Extracts text from PDF files using PyPDF2
- Splits text into chunks (1000 characters, 200 overlap)
- Creates embeddings using OpenAI
- Stores in ChromaDB vector database

### 2. Vector Store (`main.py`)
```python
vectorstore = Chroma(
    collection_name='rag_pdf_collection',
    embedding_function=OpenAIEmbeddings(),
    persist_directory='./chroma_data'
)
```

### 3. RAG Pipeline
1. **Query Processing**: Receives user question
2. **Document Retrieval**: Searches vector store for relevant chunks (k=4)
3. **Context Building**: Combines retrieved documents as context
4. **Response Generation**: Uses GPT with custom prompt template
5. **Response Filtering**: Returns document-restricted answers only

### 4. Prompt Template
```python
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the provided context, just say "I don't have information about that in the provided documents."
Do not make up an answer or use information outside of the provided context.

Context:
{context}

Question: {question}
Answer:"""
```

## 🧪 Testing

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Ask about document content:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

**Test restriction (should be declined):**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the weather today?"}'
```

### Using Test Scripts

**Python test:**
```bash
python test_api.py
```

**Windows batch test:**
```bash
test_api.bat
```

## 📝 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `CHROMA_COLLECTION_NAME` | ChromaDB collection name | `rag_pdf_collection` |
| `LLM_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `CHROMA_PERSIST_DIR` | Vector DB storage path | `./chroma_data` |
| `PORT` | Server port | `8000` |

### Adding New Documents

1. Place PDF files in the `data/` directory
2. Run ingestion script:
   ```bash
   python simple_ingest.py
   ```
3. Restart the server

## 🔒 Security Features

- **Document Restriction**: AI only answers from ingested documents
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive exception handling
- **Logging**: Request/response logging for debugging

## 🚨 Troubleshooting

### Common Issues

1. **"No documents found" responses**
   - Ensure PDFs are in `data/` directory
   - Run `python simple_ingest.py`
   - Check ChromaDB path consistency

2. **OpenAI API errors**
   - Verify API key in `.env`
   - Check API quota/billing
   - Ensure model name is correct

3. **Import errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Server won't start**
   - Check port 8000 availability
   - Verify all dependencies installed
   - Check logs for specific errors

### Debug Mode

Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance

- **Response Time**: ~2-5 seconds per query
- **Document Chunks**: 1000 characters with 200 overlap
- **Retrieval**: Top 4 most relevant chunks
- **Memory Usage**: Depends on document corpus size

## 🔄 Workflow

1. **Document Upload** → PDF files placed in `data/`
2. **Ingestion** → Text extraction, chunking, embedding
3. **Storage** → Vector embeddings stored in ChromaDB
4. **Query** → User asks question via API
5. **Retrieval** → Semantic search finds relevant chunks
6. **Generation** → LLM generates answer from context
7. **Response** → Filtered, document-based answer returned

## 📈 Scaling Considerations

- **Large Document Sets**: Consider batch processing
- **High Traffic**: Implement caching and load balancing
- **Storage**: Monitor ChromaDB size and performance
- **Costs**: Track OpenAI API usage

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## 📄 License

This project is open source. Please check the license file for details.