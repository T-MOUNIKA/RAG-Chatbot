# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
- Requires OpenAI API key in environment variables
- No user authentication required for API endpoints

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "okay"
}
```

**Status Codes:**
- `200`: Service is healthy

---

### 2. Web Interface
**GET** `/`

Returns the HTML web interface for the chatbot.

**Response:**
- Content-Type: `text/html`
- Returns the complete HTML page

**Status Codes:**
- `200`: HTML page returned successfully

---

### 3. Chat Endpoint
**POST** `/api/chat`

Main endpoint for asking questions to the RAG chatbot.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "string"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | The question to ask the chatbot |

**Response:**
```json
{
  "answer": "string"
}
```

**Example Requests:**

1. **Document-based question:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

Response:
```json
{
  "answer": "Docker is a containerization platform that allows developers to package applications and their dependencies into lightweight, portable containers..."
}
```

2. **Non-document question (restricted):**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the weather today?"}'
```

Response:
```json
{
  "answer": "I don't have information about that in the provided documents."
}
```

**Status Codes:**
- `200`: Successful response
- `422`: Validation error (invalid request body)
- `500`: Internal server error

**Error Response:**
```json
{
  "detail": "Error message description"
}
```

---

## Request/Response Examples

### Successful Document Query
```http
POST /api/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "question": "What are the benefits of using containers?"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "answer": "Based on the provided documents, containers offer several benefits including: 1) Portability across different environments, 2) Resource efficiency compared to virtual machines, 3) Consistent deployment environments, 4) Faster startup times, and 5) Better scalability for applications."
}
```

### Restricted Query (Outside Document Scope)
```http
POST /api/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "question": "How do I cook pasta?"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "answer": "I don't have information about that in the provided documents."
}
```

### Validation Error
```http
POST /api/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "invalid_field": "test"
}
```

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting
- No built-in rate limiting
- Limited by OpenAI API rate limits
- Consider implementing rate limiting for production use

## CORS
- All origins allowed (`*`)
- All methods allowed
- All headers allowed
- Credentials supported

## Logging
All requests are logged with:
- Timestamp
- Question received
- Response generated
- Error details (if any)

## Interactive Documentation
When the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`