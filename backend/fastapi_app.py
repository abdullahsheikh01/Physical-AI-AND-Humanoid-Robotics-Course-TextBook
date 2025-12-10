from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routes
from src.api.v1.chat import router as chat_router
from src.api.v1.health import router as health_router
from src.api.v1.embeddings import router as embeddings_router

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for the RAG Chatbot Integration with Physical AI & Humanoid Robotics E-book",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat_router)
app.include_router(health_router)
app.include_router(embeddings_router)

# Additional legacy endpoints for compatibility
from src.models.chat_models import UserQuery, GeneratedResponse
from src.services.session_service import session_service
from agent_backend import process_query, process_query_streamed_async


class LegacyChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None


class SourceInfo(BaseModel):
    doc_id: str
    title: str
    similarity_score: float


class LegacyChatResponse(BaseModel):
    response: str
    conversation_id: str
    status: str
    sources: Optional[List[SourceInfo]] = None


@app.post("/chat", response_model=LegacyChatResponse)
async def legacy_chat_endpoint(request: LegacyChatRequest):
    """
    Legacy chat endpoint for backward compatibility
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Process the query using the agent
        result = await process_query(request.query, conversation_id)

        # Update session with the new interaction
        session_service.update_session(
            session_id=conversation_id,
            query=request.query,
            response=result.get("response", "")
        )

        return LegacyChatResponse(
            response=result.get("response", ""),
            conversation_id=conversation_id,
            status=result.get("status", "success"),
            sources=result.get("sources", [])
        )
    except Exception as e:
        logging.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def legacy_health_check():
    """
    Legacy health check endpoint for backward compatibility
    """
    # Redirect to the v1 health endpoint
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/v1/health")


from fastapi.responses import StreamingResponse
import json

# Streaming endpoint (for Phase 3 implementation)
@app.post("/chat/stream")
async def chat_stream_endpoint(request: LegacyChatRequest):
    """
    Process user queries and return AI-generated responses as a stream
    """
    async def event_generator():
        conversation_id = request.conversation_id or str(uuid.uuid4())

        try:
            # Process the query using the async streaming agent
            async for result in process_query_streamed_async(request.query, conversation_id):
                # Update session with the new interaction if it's the final result
                if result.get("status") == "complete":
                    session_service.update_session(
                        session_id=conversation_id,
                        query=request.query,
                        response=result.get("response", "")
                    )

                # Yield the result as JSON
                yield f"data: {json.dumps(result)}\n\n"
        except Exception as e:
            error_result = {
                "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
                "conversation_id": conversation_id,
                "status": "error",
                "error": str(e),
                "sources": []
            }
            yield f"data: {json.dumps(error_result)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)