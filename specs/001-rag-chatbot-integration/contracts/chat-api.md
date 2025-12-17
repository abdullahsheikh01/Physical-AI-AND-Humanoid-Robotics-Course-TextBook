# OpenAPI Specification: RAG Chatbot API with Delete History Support

## Overview
This document describes the API contracts for the RAG Chatbot with Delete History functionality. The Delete History feature is primarily a frontend capability that clears client-side state, but the API supports the overall chat functionality that enables this feature.

## Base URL
- Development: `http://localhost:8000`
- Production: `https://physical-ai-and-humanoid-robotics-course-ha5u.onrender.com`

## Authentication
No authentication required for basic chat functionality. API keys are configured server-side.

## API Endpoints

### Chat Endpoint
```
POST /chat
```

#### Description
Processes user queries and returns AI-generated responses based on the Physical AI & Humanoid Robotics knowledge base. Supports conversation history context for maintaining context across messages. The frontend can clear its history independently, and subsequent requests will have an empty history array.

#### Request Body
```json
{
  "query": "string (required) - The user's question or input text",
  "conversation_id": "string (optional) - Unique identifier for conversation continuity",
  "history": [
    {
      "role": "string (required) - Either 'user' or 'assistant'",
      "message": "string (required) - The content of the message"
    }
  ]
}
```

#### Request Validation
- `query`: Required, 1-2000 characters
- `conversation_id`: Optional, UUID format if provided
- `history`: Required, array of message objects, max 50 items
- Each history item: `role` must be "user" or "assistant", `message` required

#### Example Request
```json
{
  "query": "What is Physical AI?",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "history": [
    {
      "role": "user",
      "message": "Hello, I'd like to learn about Physical AI."
    },
    {
      "role": "assistant",
      "message": "Hello! Physical AI is an approach to robotics that emphasizes the importance of physical interaction with the environment."
    }
  ]
}
```

#### Response
```json
{
  "response": "string (required) - The AI-generated answer",
  "conversation_id": "string (required) - Session identifier",
  "status": "string (required) - 'success' or 'error'",
  "sources": [
    {
      "doc_id": "string - Document identifier used",
      "content": "string - Relevant content snippet",
      "similarity_score": "number - Relevance score (0.0-1.0)"
    }
  ]
}
```

#### Response Validation
- `response`: Required, 10-10000 characters
- `conversation_id`: Required, UUID format
- `status`: Required, "success" or "error"
- `sources`: Optional, array of source objects

#### Example Response
```json
{
  "response": "Physical AI is an approach to robotics that emphasizes the importance of physical interaction with the environment...",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "sources": [
    {
      "doc_id": "physical-ai-intro",
      "content": "Physical AI represents a paradigm shift in robotics...",
      "similarity_score": 0.92
    }
  ]
}
```

#### Error Responses
- `400 Bad Request`: Invalid request format
- `500 Internal Server Error`: Server processing error

### Health Check Endpoint
```
GET /health
```

#### Description
Returns the health status of the application and its external dependencies.

#### Response
```json
{
  "status": "string (required) - 'healthy' or 'unhealthy'",
  "timestamp": "string (required) - ISO 8601 formatted timestamp",
  "services": {
    "cohere": "string - 'available' or 'unavailable'",
    "qdrant": "string - 'available' or 'unavailable'",
    "gemini": "string - 'available' or 'unavailable'"
  }
}
```

#### Example Response
```json
{
  "status": "healthy",
  "timestamp": "2025-12-17T10:30:00Z",
  "services": {
    "cohere": "available",
    "qdrant": "available",
    "gemini": "available"
  }
}
```

## Delete History Feature Considerations

### Frontend State Management
The Delete History functionality operates entirely on the frontend by:
1. Clearing the local history array from the component state
2. Triggering a UI re-render without the previous messages
3. Allowing subsequent chat requests to begin with an empty history context

### API Impact
When history is deleted on the frontend:
- Subsequent `/chat` requests will have an empty `history` array
- The AI agent will respond without prior conversation context
- The conversation starts fresh from the backend perspective

### Expected Frontend Behavior
- Delete History button appears in chat widget header with smooth fade-in animation
- Clicking the button clears frontend state within 0.5 seconds (per SC-011)
- UI provides visual feedback during the clearing process
- New messages start a fresh conversation context