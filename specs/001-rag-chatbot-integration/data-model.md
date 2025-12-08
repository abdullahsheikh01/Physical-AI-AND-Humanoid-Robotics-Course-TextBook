# Data Model: RAG Chatbot Integration

## Core Entities

### User Query
- **id**: string (UUID) - Unique identifier for the query
- **session_id**: string (UUID) - Reference to the conversation session
- **content**: string - The text content of the user's query
- **timestamp**: datetime - When the query was submitted
- **metadata**: object - Additional query metadata (source, user agent, etc.)

### Knowledge Base Document
- **id**: string (UUID) - Unique identifier for the document
- **title**: string - Title of the document
- **content**: string - Full text content of the document
- **source_url**: string - URL where the original document is located
- **embedding**: array<float> - Vector embedding of the document content
- **created_at**: datetime - When the document was added to the knowledge base
- **updated_at**: datetime - When the document was last updated

### Document Chunk
- **id**: string (UUID) - Unique identifier for the chunk
- **document_id**: string (UUID) - Reference to the parent document
- **content**: string - Text content of the chunk
- **chunk_index**: integer - Position of the chunk within the document
- **embedding**: array<float> - Vector embedding of the chunk content
- **metadata**: object - Additional chunk metadata

### Retrieved Context
- **id**: string (UUID) - Unique identifier for the retrieved context
- **query_id**: string (UUID) - Reference to the original query
- **chunks**: array<Chunk> - List of relevant document chunks retrieved
- **relevance_scores**: array<float> - Relevance scores for each chunk
- **retrieval_method**: string - Method used for retrieval (e.g., semantic search)

### Generated Response
- **id**: string (UUID) - Unique identifier for the response
- **query_id**: string (UUID) - Reference to the original query
- **content**: string - The generated response text
- **context_used**: array<string> - IDs of context chunks used in the response
- **timestamp**: datetime - When the response was generated
- **streaming_id**: string - Identifier for streaming response chunks

### Conversation Session
- **id**: string (UUID) - Unique identifier for the session
- **user_id**: string (optional) - Identifier for the user (if available)
- **created_at**: datetime - When the session started
- **updated_at**: datetime - When the session was last active
- **is_active**: boolean - Whether the session is currently active

### Message
- **id**: string (UUID) - Unique identifier for the message
- **session_id**: string (UUID) - Reference to the conversation session
- **sender_type**: enum('user', 'agent') - Who sent the message
- **content**: string - The message content
- **timestamp**: datetime - When the message was sent
- **message_type**: enum('query', 'response', 'system') - Type of message