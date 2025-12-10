import os
import asyncio
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import logging
from functools import wraps

# Import required libraries
try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
    import cohere
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from openai import OpenAI
    from agents import Agent, Runner
except ImportError as e:
    print(f"Missing required packages. Please install: {e}")
    raise

# Import settings
from src.config.settings import settings

# Import our new services and agent
from src.services.rag_service import rag_service
from src.services.llm_service import llm_service
from src.agents.rag_agent import rag_agent


class RetrievedChunk(BaseModel):
    """Model for retrieved context chunks"""
    content: str
    source_doc_id: str
    similarity_score: float
    metadata: Optional[Dict[str, Any]] = None


async def retrieve(query: str) -> List[RetrievedChunk]:
    """
    Retrieve relevant context chunks from the vector database based on the query
    """
    try:
        # Use the RAG service to retrieve context
        context_chunks = rag_service.retrieve_context(query)

        # Convert to the expected format
        retrieved_chunks = []
        for chunk in context_chunks:
            retrieved_chunk = RetrievedChunk(
                content=chunk.content,
                source_doc_id=chunk.source_doc_id,
                similarity_score=chunk.similarity_score,
                metadata=chunk.metadata
            )
            retrieved_chunks.append(retrieved_chunk)

        return retrieved_chunks
    except Exception as e:
        logging.error(f"Error retrieving from vector database: {e}")
        return []


async def generate_response(query: str, context_chunks: List[RetrievedChunk]) -> str:
    """
    Generate a response using the LLM based on the query and retrieved context
    """
    try:
        # Format context for the model
        context_text = "\n".join([chunk.content for chunk in context_chunks])

        # Use the LLM service to generate response
        response_text = llm_service.generate_response(query, context_text)

        return response_text
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "I'm sorry, but I encountered an error while generating a response. Please try again."


async def process_query(query: str, conversation_id: str) -> Dict[str, Any]:
    """
    Process a user query through the RAG pipeline using the OpenAI Agents SDK

    Args:
        query: The user's question
        conversation_id: Unique identifier for the conversation

    Returns:
        Dictionary with response, status, and sources
    """
    try:
        # Validate input
        if not query or len(query.strip()) == 0:
            return {
                "response": "Please provide a valid question.",
                "status": "error",
                "sources": []
            }

        if len(query) > settings.max_query_length:
            return {
                "response": f"Query too long. Please limit your query to {settings.max_query_length} characters.",
                "status": "error",
                "sources": []
            }

        # Use the RAG agent to process the query
        result = rag_agent.process_query(query, conversation_id)

        return result

    except Exception as e:
        logging.error(f"Error processing query: {e}")
        return {
            "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
            "status": "error",
            "sources": []
        }


async def process_query_streamed(query: str, conversation_id: str):
    """
    Process a user query through the RAG pipeline with streaming response

    Args:
        query: The user's question
        conversation_id: Unique identifier for the conversation

    Yields:
        Streaming response events
    """
    try:
        # Validate input
        if not query or len(query.strip()) == 0:
            yield {
                "response": "Please provide a valid question.",
                "conversation_id": conversation_id,
                "status": "error",
                "sources": []
            }

        if len(query) > settings.max_query_length:
            yield {
                "response": f"Query too long. Please limit your query to {settings.max_query_length} characters.",
                "conversation_id": conversation_id,
                "status": "error",
                "sources": []
            }

        # Use the RAG agent to process the query with streaming
        # We need to handle this differently as run_streamed is not async
        for result in rag_agent.run_streamed(query, conversation_id):
            yield result

    except Exception as e:
        logging.error(f"Error in streamed query processing: {e}")
        yield {
            "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
            "conversation_id": conversation_id,
            "status": "error",
            "error": str(e),
            "sources": []
        }


async def process_query_streamed_async(query: str, conversation_id: str):
    """
    Async version to process a user query through the RAG pipeline with true streaming response

    Args:
        query: The user's question
        conversation_id: Unique identifier for the conversation

    Yields:
        Streaming response events
    """
    try:
        # Validate input
        if not query or len(query.strip()) == 0:
            yield {
                "response": "Please provide a valid question.",
                "conversation_id": conversation_id,
                "status": "error",
                "sources": []
            }

        if len(query) > settings.max_query_length:
            yield {
                "response": f"Query too long. Please limit your query to {settings.max_query_length} characters.",
                "conversation_id": conversation_id,
                "status": "error",
                "sources": []
            }

        # Use the RAG agent to process the query with true async streaming
        async for result in rag_agent.run_streamed_async(query, conversation_id):
            yield result

    except Exception as e:
        logging.error(f"Error in streamed query processing: {e}")
        yield {
            "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
            "conversation_id": conversation_id,
            "status": "error",
            "error": str(e),
            "sources": []
        }


# Function to initialize the agent (placeholder for future implementation)
def initialize_agent():
    """
    Initialize the RAG agent with required tools and configuration
    """
    logging.info("RAG agent initialized with Cohere, Qdrant, and Gemini integration")
    return {
        "retrieve": retrieve,
        "process_query": process_query
    }


# Initialize the agent when the module is loaded
AGENT = initialize_agent()


# For compatibility with the original plan, also provide a synchronous wrapper
def process_query_sync(query: str, conversation_id: str) -> Dict[str, Any]:
    """
    Synchronous wrapper for process_query to maintain compatibility
    """
    return asyncio.run(process_query(query, conversation_id))