"""
FastAPI application for RAG Chatbot integration with Physical AI & Humanoid Robotics textbook.
This module handles the API endpoints and connects to the agentic backend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import datetime

from agentic_backend import run_agent


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define request and response models for User Story 1
class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """
    query: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """
    response: str
    conversation_id: Optional[str] = None
    status: str
    sources: Optional[List[Dict[str, Any]]] = []


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    """
    status: str
    timestamp: str
    services: Dict[str, str]


# Create FastAPI app instance
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG Chatbot integration with Physical AI & Humanoid Robotics textbook",
    version="1.0.0"
)


# Add CORS middleware to FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Create a FastAPI which receives input from frontend and give response
    by using `agentic_backend`'s function `run_agent`.
    """
    try:
        # Log the incoming request
        logger.info(f"Received chat request: {request.query[:50]}...")
        print("I have Run!!!")
        
        # Call the agentic backend's run_agent function
        response = await run_agent(request.query)


        # Create and return the response
        return ChatResponse(
            response=response,
            conversation_id=request.conversation_id,
            status="success",
            sources=[]  # Sources would be populated if available from the agent
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        # Add error handling for chat endpoint
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Implement health check endpoint.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.datetime.now().isoformat(),
        services={
            "gemini": "unknown",  # Would check actual service status in production
            "cohere": "unknown",
            "qdrant": "unknown"
        }
    )


# Additional endpoint implementations for User Story 1
@app.get("/")
async def root():
    """
    Root endpoint for basic service verification.
    """
    return {"message": "RAG Chatbot Backend API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)