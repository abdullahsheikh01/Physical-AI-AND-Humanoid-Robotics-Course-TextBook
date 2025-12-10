from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ...services.embedding_service import embedding_service


# Create API router
router = APIRouter(prefix="/v1")


class EmbeddingRequest(BaseModel):
    text: str
    input_type: str = "search_query"


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    text: str


class BatchEmbeddingRequest(BaseModel):
    texts: List[str]
    input_type: str = "search_query"


class BatchEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    texts: List[str]


@router.post("/embeddings", response_model=EmbeddingResponse)
async def generate_embedding(request: EmbeddingRequest):
    """
    Generate embedding for the given text
    """
    try:
        embedding = embedding_service.generate_embedding(request.text, request.input_type)
        if not embedding:
            raise HTTPException(status_code=500, detail="Failed to generate embedding")

        return EmbeddingResponse(
            embedding=embedding,
            text=request.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/embeddings/batch", response_model=BatchEmbeddingResponse)
async def generate_embeddings_batch(request: BatchEmbeddingRequest):
    """
    Generate embeddings for a batch of texts
    """
    try:
        embeddings = embedding_service.generate_embeddings_batch(request.texts, request.input_type)
        if not embeddings:
            raise HTTPException(status_code=500, detail="Failed to generate embeddings")

        return BatchEmbeddingResponse(
            embeddings=embeddings,
            texts=request.texts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))