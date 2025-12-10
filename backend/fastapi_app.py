from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the agent backend
from agent_backend import RAGAgent

app = FastAPI(
    title="RAG Chatbot API",
    description="API for the Physical AI & Humanoid Robotics RAG Chatbot",
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

# Pydantic models
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    session_id: str
    context: Optional[List[Dict[str, Any]]] = []

class HealthResponse(BaseModel):
    status: str
    version: str

# Initialize the RAG agent
rag_agent = RAGAgent()

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that processes user queries and returns AI-generated responses
    using RAG (Retrieval-Augmented Generation) approach.
    """
    try:
        # Process the chat request using the RAG agent
        response = await rag_agent.process_query(
            query=request.message,
            session_id=request.session_id,
            history=request.history
        )

        return ChatResponse(
            response=response.response_text,
            session_id=response.session_id,
            context=response.context_chunks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)