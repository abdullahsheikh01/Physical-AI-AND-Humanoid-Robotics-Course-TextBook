from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class KnowledgeBaseDocument(BaseModel):
    """
    Model for knowledge base documents
    """
    doc_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = {}
    embedding: Optional[List[float]] = None


class DocumentEmbedding(BaseModel):
    """
    Model for document embeddings
    """
    doc_id: str
    vector: List[float]
    text_chunk: str
    chunk_id: str
    created_at: datetime = datetime.now()