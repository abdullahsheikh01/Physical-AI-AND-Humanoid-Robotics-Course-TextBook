# FastAPI Contract: RAG Chatbot Backend

## API Overview
- **Base URL**: `/api/v1`
- **Content-Type**: `application/json`
- **Authentication**: None (for initial implementation)
- **Version**: 1.0

## Endpoints

### Chat Endpoint
- **Path**: `POST /chat`
- **Description**: Process user queries and return AI-generated responses with context retrieval
- **Request Format**:
  ```json
  {
    "query": "string (required) - User's question",
    "conversation_id": "string (optional) - Session identifier"
  }
  ```
- **Response Format**:
  ```json
  {
    "response": "string - AI-generated answer",
    "conversation_id": "string - Session identifier",
    "status": "string - 'success' or 'error'",
    "sources": [
      {
        "doc_id": "string - Document identifier",
        "title": "string - Document title",
        "similarity_score": "number - Relevance score"
      }
    ]
  }
  ```
- **HTTP Status Codes**:
  - `200`: Success
  - `400`: Invalid request format
  - `422`: Validation error
  - `500`: Internal server error
  - `503`: External service unavailable

### Health Check Endpoint
- **Path**: `GET /health`
- **Description**: Check the health status of the backend and its external dependencies
- **Request Format**: No request body required
- **Response Format**:
  ```json
  {
    "status": "string - 'healthy' or 'unhealthy'",
    "timestamp": "string - ISO datetime",
    "services": {
      "gemini": "string - 'available' or 'unavailable'",
      "cohere": "string - 'available' or 'unavailable'",
      "qdrant": "string - 'available' or 'unavailable'"
    }
  }
  ```
- **HTTP Status Codes**:
  - `200`: Healthy
  - `503`: Unhealthy (one or more services unavailable)

### Streaming Chat Endpoint
- **Path**: `POST /chat/stream`
- **Description**: Process user queries and return AI-generated responses as a stream
- **Request Format**:
  ```json
  {
    "query": "string (required) - User's question",
    "conversation_id": "string (optional) - Session identifier"
  }
  ```
- **Response Format**: Server-Sent Events (SSE) with JSON payloads
  ```json
  {
    "token": "string - Next token in the response",
    "conversation_id": "string - Session identifier",
    "status": "string - 'in_progress', 'complete', or 'error'",
    "error": "string (optional) - Error message if status is 'error'"
  }
  ```
- **HTTP Status Codes**:
  - `200`: Success with streaming response
  - `400`: Invalid request format
  - `422`: Validation error
  - `500`: Internal server error

## Error Responses
All error responses follow the same structure:
```json
{
  "error_code": "string - Standardized error code",
  "message": "string - Human-readable error message",
  "details": "object (optional) - Additional error context"
}
```

## Common Headers
- **Request Headers**:
  - `Content-Type: application/json`
  - `Accept: application/json` (for regular endpoints)
  - `Accept: text/event-stream` (for streaming endpoints)

- **Response Headers**:
  - `Content-Type: application/json` (for regular endpoints)
  - `Content-Type: text/event-stream` (for streaming endpoints)
  - `Cache-Control: no-cache`
  - `Connection: keep-alive`

## Validation Rules
- Query text must be 1-2000 characters
- Conversation ID must follow UUID format if provided
- Request body must be valid JSON
- All required fields must be present

## Rate Limiting
- Default: 100 requests per minute per IP
- Burst limit: 10 requests
- Applied to all endpoints except health check

## Security Considerations
- Input sanitization for all user-provided content
- No sensitive information in error messages
- API key validation for external services (handled internally)