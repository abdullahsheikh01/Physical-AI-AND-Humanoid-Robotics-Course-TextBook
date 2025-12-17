# Quickstart Guide: RAG Chatbot Integration

## Prerequisites

- Python 3.11+
- Node.js 16+ (if modifying frontend)
- Docker (for Qdrant vector database)
- API keys for Cohere, Gemini, and OpenAI

## Environment Setup

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   ```bash
   # Create .env file in backend root
   COHERE_API_KEY=your_cohere_api_key
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=your_qdrant_api_key  # Optional
   ```

3. **Qdrant Vector Database**
   ```bash
   # Option 1: Run with Docker
   docker run -p 6333:6333 -p 6334:6334 \
     -v ./qdrant_storage:/qdrant/storage:z \
     qdrant/qdrant

   # Option 2: Use Qdrant Cloud
   # Update QDRANT_URL in .env
   ```

## Running the Backend

1. **Start the FastAPI server**
   ```bash
   cd backend
   uvicorn fastapi_app:app --reload --port 8000
   ```

2. **Initialize the vector database**
   ```bash
   # Run once to initialize the knowledge base
   python -c "from src.services.vector_db_service import initialize_vector_db; initialize_vector_db()"
   ```

## Frontend Integration

1. **Integrate the Chatbot Widget**
   - The chatbot widget is designed as a React component that can be integrated into the Docusaurus site
   - Add the ChatbotWidget component to your Docusaurus layout

2. **Configuration**
   - Update the API endpoint in the frontend service to point to your backend server
   - The default is configured to connect to http://localhost:8000

## API Usage

### Chat Endpoint
```bash
# Local development
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Physical AI?",
    "conversation_id": "unique-session-id",
    "history": [
      {"role": "user", "message": "Hello"},
      {"role": "assistant", "message": "Hello! How can I help you today?"}
    ]
  }'

# Production (Render)
curl -X POST https://physical-ai-and-humanoid-robotics-course-ha5u.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Physical AI?",
    "conversation_id": "unique-session-id",
    "history": [
      {"role": "user", "message": "Hello"},
      {"role": "assistant", "message": "Hello! How can I help you today?"}
    ]
  }'
```

### Health Check
```bash
# Local development
curl http://localhost:8000/health

# Production (Render)
curl https://physical-ai-and-humanoid-robotics-course-ha5u.onrender.com/health
```

## Running Tests

1. **Backend Tests**
   ```bash
   cd backend
   pytest tests/
   ```

2. **Frontend Tests**
   ```bash
   cd frontend
   npm test
   ```

## Development Workflow

1. **Adding Knowledge Base Content**
   - Add new documents to the knowledge base using the ingestion pipeline
   - Run the embedding generation process to create vector representations
   - Verify the content is searchable in Qdrant

2. **Customizing the Agent**
   - Modify the agent logic in `src/agents/rag_agent.py`
   - Update the tools available to the agent as needed
   - Test the agent behavior with various queries

3. **Frontend Customization**
   - Modify the chatbot widget styling in `styles.module.css`
   - Update the UI components as needed while maintaining CSS Modules compliance
   - Test across different screen sizes to ensure responsive design