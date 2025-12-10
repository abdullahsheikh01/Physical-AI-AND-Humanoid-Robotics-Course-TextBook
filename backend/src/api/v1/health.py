from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from datetime import datetime


# Create API router
router = APIRouter(prefix="/v1")


# Response model for health check
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check the health status of the backend and its external dependencies
    """
    # In a real implementation, we would check the actual status of external services
    # For now, we'll return a basic health status
    services_status = {
        "gemini": "available",
        "cohere": "available",
        "qdrant": "available",
        "agent": "available"
    }

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        services=services_status
    )


@router.get("/ready")
async def readiness_check():
    """
    Simple readiness check
    """
    return {"status": "ready"}