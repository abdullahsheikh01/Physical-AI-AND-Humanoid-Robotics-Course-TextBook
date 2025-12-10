from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class UserQuery(BaseModel):
    """
    Model for user queries
    """
    query: str
    conversation_id: Optional[str] = None
    timestamp: datetime = datetime.now()
    user_id: Optional[str] = None

    def __init__(self, **data):
        if 'conversation_id' not in data or data['conversation_id'] is None:
            data['conversation_id'] = str(uuid.uuid4())
        super().__init__(**data)


class RetrievedContextChunk(BaseModel):
    """
    Model for retrieved context chunks
    """
    content: str
    source_doc_id: str
    similarity_score: float
    metadata: Optional[Dict[str, Any]] = None


class GeneratedResponse(BaseModel):
    """
    Model for generated responses
    """
    response: str
    conversation_id: str
    timestamp: datetime = datetime.now()
    sources: Optional[List[Dict[str, Any]]] = []
    status: str = "success"


class ConversationSession(BaseModel):
    """
    Model for conversation sessions
    """
    session_id: str = str(uuid.uuid4())
    created_at: datetime = datetime.now()
    last_interaction: datetime = datetime.now()
    history: List[Dict[str, str]] = []
    user_id: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }