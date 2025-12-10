from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import json

from ...models.chat_models import UserQuery, GeneratedResponse
from ...services.session_service import session_service
from ...agent_backend import process_query, process_query_streamed, process_query_streamed_async


# Create API router
router = APIRouter(prefix="/v1")


# Request/Response models specific to this API
class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None


class SourceInfo(BaseModel):
    doc_id: str
    title: str
    similarity_score: float


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    status: str
    sources: Optional[List[SourceInfo]] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process user queries and return AI-generated responses with context retrieval
    """
    try:
        # Use provided conversation_id or generate a new one
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Process the query using the agent
        result = await process_query(request.query, conversation_id)

        # Update session with the new interaction
        session_service.update_session(
            session_id=conversation_id,
            query=request.query,
            response=result.get("response", "")
        )

        return ChatResponse(
            response=result.get("response", ""),
            conversation_id=conversation_id,
            status=result.get("status", "success"),
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
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


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get conversation session details
    """
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.session_id,
        "created_at": session.created_at.isoformat(),
        "last_interaction": session.last_interaction.isoformat(),
        "history": session.history,
        "user_id": session.user_id
    }


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a conversation session
    """
    session_service.delete_session(session_id)
    return {"message": "Session deleted successfully"}