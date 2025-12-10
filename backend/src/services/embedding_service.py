import cohere
from typing import List, Optional
from ..config.settings import settings
import logging


class EmbeddingService:
    """
    Service for generating text embeddings using Cohere
    """
    def __init__(self):
        if settings.cohere_api_key:
            self.client = cohere.Client(settings.cohere_api_key)
        else:
            self.client = None
            logging.warning("COHERE_API_KEY not set, embedding functionality will be limited")

    def generate_embedding(self, text: str, input_type: str = "search_query") -> Optional[List[float]]:
        """
        Generate embedding for the given text using Cohere
        """
        if not self.client:
            logging.error("Cohere client not initialized")
            return None

        try:
            response = self.client.embed(
                texts=[text],
                model=settings.cohere_model,
                input_type=input_type
            )
            return response.embeddings[0] if response.embeddings else None
        except Exception as e:
            logging.error(f"Error generating embedding: {e}")
            return None

    def generate_embeddings_batch(self, texts: List[str], input_type: str = "search_query") -> Optional[List[List[float]]]:
        """
        Generate embeddings for a batch of texts
        """
        if not self.client:
            logging.error("Cohere client not initialized")
            return None

        try:
            response = self.client.embed(
                texts=texts,
                model=settings.cohere_model,
                input_type=input_type
            )
            return response.embeddings if response.embeddings else None
        except Exception as e:
            logging.error(f"Error generating embeddings batch: {e}")
            return None


# Global embedding service instance
embedding_service = EmbeddingService()