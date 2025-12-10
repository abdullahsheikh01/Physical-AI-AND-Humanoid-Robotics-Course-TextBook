import os
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from agents import Agent, Runner, function_tool
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents.extensions.models.litellm_model import LitellmModel
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class QueryResponse:
    response_text: str
    session_id: str
    context_chunks: List[Dict[str, Any]]

class RAGAgent:
    """
    RAG (Retrieval-Augmented Generation) Agent that combines:
    - Qdrant vector database for knowledge retrieval
    - Cohere for text embeddings
    - OpenAI Agents SDK for agent orchestration and response generation
    """

    def __init__(self):
        # Initialize API clients
        self.cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )

        # Create the OpenAI agent using LitellmModel to support various LLM providers
        self.agent = Agent(
            name="Physical-AI-RAG-Assistant",
            instructions=prompt_with_handoff_instructions(
                "You are an AI assistant for the Physical AI & Humanoid Robotics E-book. "
                "Always retrieve relevant context from the knowledge base before answering. "
                "Use the provided context to answer questions accurately and helpfully. "
                "If the context doesn't contain the information needed, say so politely."
            ),
            model=LitellmModel(
                model="gemini-2.0-flash",  # Using Gemini through LiteLLM
                api_key=os.getenv("GEMINI_API_KEY")
            ),
        )

        # Create Qdrant collection if it doesn't exist
        self._setup_qdrant_collection()

    def _setup_qdrant_collection(self):
        """Set up the Qdrant collection for storing document embeddings"""
        try:
            # Check if collection exists
            self.qdrant_client.get_collection("physical_ai_docs")
        except:
            # Create collection if it doesn't exist
            self.qdrant_client.create_collection(
                collection_name="physical_ai_docs",
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
            )

    def embed_text(self, text: str) -> List[float]:
        """Generate embeddings for text using Cohere"""
        response = self.cohere_client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings[0]

    def store_document(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Store a document in the Qdrant vector database"""
        if metadata is None:
            metadata = {}

        # Generate embedding
        embedding = self.embed_text(text)

        # Generate a unique ID for the document
        doc_id = str(uuid.uuid4())

        # Store in Qdrant
        self.qdrant_client.upsert(
            collection_name="physical_ai_docs",
            points=[
                models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        "metadata": metadata
                    }
                )
            ]
        )

        return doc_id

    def retrieve_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant context from the vector database based on the query"""
        query_embedding = self.embed_text(query)

        # Search for similar documents
        search_results = self.qdrant_client.search(
            collection_name="physical_ai_docs",
            query_vector=query_embedding,
            limit=limit
        )

        # Extract context chunks
        context_chunks = []
        for result in search_results:
            context_chunks.append({
                "text": result.payload["text"],
                "score": result.score,
                "metadata": result.payload.get("metadata", {})
            })

        return context_chunks

    async def generate_response_with_context(self, query: str, context: List[Dict[str, Any]], history: List[Dict[str, str]] = None) -> str:
        """Generate a response using the OpenAI Agent with the provided context"""
        if history is None:
            history = []

        # Format the context for the agent
        context_str = "\n".join([chunk["text"] for chunk in context])

        # Create the prompt with context
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics E-book.
        Use the following context to answer the user's question:

        Context:
        {context_str}

        Question: {query}

        Please provide a helpful, accurate response based on the context provided.
        If the context doesn't contain the information needed to answer the question,
        please say so and suggest where the user might find the information.
        """

        # Run the agent with the prompt
        result = await Runner.run(self.agent, prompt)
        return result.final_output

    async def process_query(
        self,
        query: str,
        session_id: Optional[str] = None,
        history: List[Dict[str, str]] = None
    ) -> QueryResponse:
        """
        Process a user query using RAG approach:
        1. Retrieve relevant context from the knowledge base
        2. Generate a response using the context and query
        """
        # Generate session ID if not provided
        if session_id is None:
            session_id = str(uuid.uuid4())

        # Retrieve relevant context
        context_chunks = self.retrieve_context(query)

        # Generate response using the context
        response_text = await self.generate_response_with_context(query, context_chunks, history)

        return QueryResponse(
            response_text=response_text,
            session_id=session_id,
            context_chunks=context_chunks
        )

# Example usage for document ingestion (to be called separately)
def ingest_documents():
    """
    Function to ingest documents into the vector database.
    This would typically be called during setup or periodically.
    """
    # This is a placeholder - in a real implementation, you would:
    # 1. Read documents from various sources (PDFs, text files, etc.)
    # 2. Chunk the documents appropriately
    # 3. Store each chunk in the vector database

    # Example document chunks (in practice, these would come from actual documents)
    example_docs = [
        {
            "text": "Physical AI is an approach that integrates artificial intelligence directly with physical systems, enabling robots and other devices to learn and adapt through interaction with the real world.",
            "metadata": {"source": "physical_ai_introduction", "section": "definition"}
        },
        {
            "text": "Humanoid robotics focuses on creating robots with human-like form and behavior. These robots often have applications in assistive technology, research, and human-robot interaction studies.",
            "metadata": {"source": "humanoid_robotics_basics", "section": "definition"}
        },
        {
            "text": "Embodied AI refers to artificial intelligence systems that interact with the physical world through a body or robot. This approach emphasizes the importance of physical interaction in developing intelligent behavior.",
            "metadata": {"source": "embodied_ai_principles", "section": "definition"}
        }
    ]

    agent = RAGAgent()
    for doc in example_docs:
        agent.store_document(doc["text"], doc["metadata"])