from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from ..config.settings import settings
import logging


class VectorDBService:
    """
    Service for interacting with Qdrant vector database
    """
    def __init__(self):
        if settings.qdrant_api_key:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key
            )
        else:
            self.client = QdrantClient(url=settings.qdrant_url)

        self.collection_name = settings.qdrant_collection_name
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Ensure the collection exists in Qdrant
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            # Assuming embedding dimension of 1024 for Cohere embeddings
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
            )
            logging.info(f"Created collection '{self.collection_name}' in Qdrant")

    def index_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Index a document in the vector database
        """
        try:
            from .embedding_service import embedding_service

            # Generate embedding for the content
            embedding = embedding_service.generate_embedding(content, input_type="search_document")
            if not embedding:
                logging.error(f"Failed to generate embedding for document {doc_id}")
                return False

            # Prepare the point for Qdrant
            point = models.PointStruct(
                id=doc_id,
                vector=embedding,
                payload={
                    "content": content,
                    "doc_id": doc_id,
                    "metadata": metadata or {}
                }
            )

            # Upsert the point into the collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            return True
        except Exception as e:
            logging.error(f"Error indexing document {doc_id}: {e}")
            return False

    def index_documents_batch(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Index multiple documents in the vector database
        """
        try:
            from .embedding_service import embedding_service

            points = []
            for doc in documents:
                doc_id = doc.get("doc_id")
                content = doc.get("content")
                metadata = doc.get("metadata", {})

                # Generate embedding for the content
                embedding = embedding_service.generate_embedding(content, input_type="search_document")
                if not embedding:
                    logging.warning(f"Failed to generate embedding for document {doc_id}")
                    continue

                # Prepare the point for Qdrant
                point = models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "doc_id": doc_id,
                        "metadata": metadata
                    }
                )
                points.append(point)

            # Upsert all points into the collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            return True
        except Exception as e:
            logging.error(f"Error indexing documents batch: {e}")
            return False

    def search(self, query: str, limit: int = 5, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Search for similar documents in the vector database
        """
        try:
            from .embedding_service import embedding_service

            # Generate embedding for the query
            query_embedding = embedding_service.generate_embedding(query, input_type="search_query")
            if not query_embedding:
                logging.error("Failed to generate embedding for query")
                return []

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=threshold
            )

            # Format results
            results = []
            for result in search_results:
                results.append({
                    "content": result.payload.get("content", ""),
                    "doc_id": result.payload.get("doc_id", ""),
                    "similarity_score": result.score,
                    "metadata": result.payload.get("metadata", {})
                })

            return results
        except Exception as e:
            logging.error(f"Error searching in vector database: {e}")
            return []

    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the vector database
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(points=[doc_id])
            )
            return True
        except Exception as e:
            logging.error(f"Error deleting document {doc_id}: {e}")
            return False

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific document from the vector database
        """
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[doc_id]
            )

            if points:
                point = points[0]
                return {
                    "content": point.payload.get("content", ""),
                    "doc_id": point.payload.get("doc_id", ""),
                    "metadata": point.payload.get("metadata", {})
                }
            return None
        except Exception as e:
            logging.error(f"Error retrieving document {doc_id}: {e}")
            return None


# Global vector database service instance
vector_db_service = VectorDBService()