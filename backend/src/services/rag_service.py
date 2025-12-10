from typing import List, Dict, Any, Optional
from ..models.chat_models import RetrievedContextChunk
from ..config.settings import settings
from .vector_db_service import vector_db_service
from .embedding_service import embedding_service
import logging


class RAGService:
    """
    Service for implementing Retrieval-Augmented Generation functionality
    """
    def __init__(self):
        self.vector_db = vector_db_service
        self.embedding_service = embedding_service

    def retrieve_context(self, query: str, limit: int = None, threshold: float = None) -> List[RetrievedContextChunk]:
        """
        Retrieve relevant context chunks based on the query
        """
        if limit is None:
            limit = settings.max_context_chunks
        if threshold is None:
            threshold = settings.similarity_threshold

        try:
            # Search for relevant documents in the vector database
            search_results = self.vector_db.search(
                query=query,
                limit=limit,
                threshold=threshold
            )

            # Convert search results to RetrievedContextChunk objects
            retrieved_chunks = []
            for result in search_results:
                chunk = RetrievedContextChunk(
                    content=result["content"],
                    source_doc_id=result["doc_id"],
                    similarity_score=result["similarity_score"],
                    metadata=result["metadata"]
                )
                retrieved_chunks.append(chunk)

            return retrieved_chunks
        except Exception as e:
            logging.error(f"Error retrieving context: {e}")
            return []

    def process_query_with_context(self, query: str) -> Dict[str, Any]:
        """
        Process a query by retrieving relevant context and preparing for response generation
        """
        try:
            # Retrieve relevant context
            context_chunks = self.retrieve_context(query)

            # Format context for LLM consumption
            context_text = "\n".join([chunk.content for chunk in context_chunks])

            return {
                "query": query,
                "context_chunks": context_chunks,
                "context_text": context_text,
                "has_context": len(context_chunks) > 0
            }
        except Exception as e:
            logging.error(f"Error processing query with context: {e}")
            return {
                "query": query,
                "context_chunks": [],
                "context_text": "",
                "has_context": False
            }

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Add a document to the knowledge base
        """
        try:
            return self.vector_db.index_document(doc_id, content, metadata)
        except Exception as e:
            logging.error(f"Error adding document {doc_id}: {e}")
            return False

    def add_documents_batch(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Add multiple documents to the knowledge base
        """
        try:
            return self.vector_db.index_documents_batch(documents)
        except Exception as e:
            logging.error(f"Error adding documents batch: {e}")
            return False


# Global RAG service instance
rag_service = RAGService()