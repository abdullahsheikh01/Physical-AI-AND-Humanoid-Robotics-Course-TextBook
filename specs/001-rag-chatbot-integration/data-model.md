# Data Model: RAG Chatbot Backend

## Core Entities

### User Query
- **Fields**:
  - `query`: string (required) - The user's question or input text
  - `conversation_id`: string (optional) - Unique identifier for conversation continuity
  - `timestamp`: datetime - When the query was submitted
  - `user_id`: string (optional) - Identifier for the requesting user

- **Validation**:
  - Query must be 1-2000 characters
  - Conversation ID follows UUID format if provided
  - Timestamp is auto-generated

### Knowledge Base Document
- **Fields**:
  - `doc_id`: string (required) - Unique document identifier
  - `content`: string (required) - The document text content
  - `metadata`: dict - Additional document information (source, date, etc.)
  - `embedding`: list[float] - Vector representation for semantic search

- **Validation**:
  - Content must be 10-50000 characters
  - Embedding must be a valid vector array
  - Metadata must be valid JSON

### Document Embedding
- **Fields**:
  - `doc_id`: string (required) - Reference to the source document
  - `vector`: list[float] (required) - High-dimensional vector representation
  - `text_chunk`: string (required) - Text segment that was embedded
  - `chunk_id`: string (required) - Unique identifier for this chunk

- **Validation**:
  - Vector must have consistent dimensions
  - Text chunk must be 50-1000 characters
  - Chunk ID follows format: `{doc_id}:{chunk_number}`

### Retrieved Context Chunk
- **Fields**:
  - `content`: string (required) - The relevant text content retrieved
  - `source_doc_id`: string (required) - Reference to source document
  - `similarity_score`: float (required) - Relevance score (0.0-1.0)
  - `metadata`: dict - Additional context information

- **Validation**:
  - Similarity score between 0.0 and 1.0
  - Content must be 50-2000 characters

### Generated Response
- **Fields**:
  - `response`: string (required) - The AI-generated answer
  - `conversation_id`: string (required) - Session identifier
  - `timestamp`: datetime - When response was generated
  - `sources`: list[dict] - References to documents used in response
  - `status`: string - "success" or "error"

- **Validation**:
  - Response must be 10-10000 characters
  - Conversation ID follows UUID format
  - Status must be one of allowed values

### Conversation Session
- **Fields**:
  - `session_id`: string (required) - Unique session identifier
  - `created_at`: datetime - When session started
  - `last_interaction`: datetime - When last query was processed
  - `history`: list[dict] - Array of query-response pairs
  - `user_id`: string (optional) - Associated user identifier

- **Validation**:
  - Session ID follows UUID format
  - History array has max 50 items
  - Timestamps are in ISO format

## FastAPI Handler Data Models

### Request Models
- **ChatRequest**:
  - `query`: string (required) - User's question
  - `conversation_id`: string (optional) - Session identifier
  - `user_id`: string (optional) - User identifier

### Response Models
- **ChatResponse**:
  - `response`: string (required) - AI-generated answer
  - `conversation_id`: string (required) - Session identifier
  - `status`: string (required) - "success" or "error"
  - `sources`: list[dict] (optional) - Source documents used

- **HealthResponse**:
  - `status`: string (required) - "healthy" or "unhealthy"
  - `timestamp`: datetime (required) - Current timestamp
  - `services`: dict (required) - Status of external services

## AI Agent Data Models

### Agent Configuration
- **Fields**:
  - `gemini_api_key`: string (required) - API key for Gemini access
  - `cohere_api_key`: string (required) - API key for Cohere embeddings
  - `qdrant_url`: string (required) - Qdrant database endpoint
  - `qdrant_api_key`: string (optional) - Qdrant authentication
  - `collection_name`: string (required) - Vector collection to use

### Tool Response
- **Fields**:
  - `tool_name`: string (required) - Name of the tool used
  - `status`: string (required) - "success" or "error"
  - `result`: any (optional) - Tool output data
  - `error_message`: string (optional) - Error details if status is "error"

## State and Configuration Models

### System Configuration
- **Fields**:
  - `environment`: string - "development", "staging", or "production"
  - `debug_mode`: bool - Whether to enable debug logging
  - `max_concurrent_requests`: int - Maximum concurrent API requests
  - `request_timeout`: int - Timeout for external API calls (seconds)
  - `retry_attempts`: int - Number of retry attempts for failed calls

### Error Models
- **APIError**:
  - `error_code`: string - Standardized error code
  - `message`: string - Human-readable error message
  - `details`: dict (optional) - Additional error context
  - `timestamp`: datetime - When error occurred

## Validation Rules

### Input Sanitization
- All user inputs must be sanitized to prevent injection attacks
- Query text is limited to 2000 characters maximum
- All string fields are validated for proper encoding

### Business Rules
- Each query must be associated with a valid conversation context
- Agent must retrieve relevant context before generating responses
- Conversation history is maintained for session continuity
- External API calls have timeout and retry mechanisms

### Data Relationships
- User queries link to conversation sessions
- Retrieved context chunks link to knowledge base documents
- Generated responses link to source documents used
- Conversation sessions maintain query-response history