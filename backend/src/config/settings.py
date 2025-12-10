from pydantic_settings import Settings
from typing import Optional


class Settings(Settings):
    """
    Application settings loaded from environment variables
    """
    # API Keys
    gemini_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    qdrant_api_key: Optional[str] = None

    # Service URLs
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "knowledge_base"

    # Application settings
    environment: str = "development"
    debug_mode: bool = True
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    retry_attempts: int = 3

    # Model settings
    gemini_model: str = "gemini-2.0-flash"
    cohere_model: str = "embed-multilingual-v3.0"

    # RAG settings
    max_context_chunks: int = 5
    similarity_threshold: float = 0.5
    max_query_length: int = 2000
    max_response_length: int = 10000

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()