from typing import Dict, Any, List, Optional
import logging
from agents import Agent, Runner, function_tool, SQLiteSession
from agents import RunResult
from ..services.rag_service import rag_service
from ..services.llm_service import llm_service
from ..services.session_service import session_service
from ..models.chat_models import RetrievedContextChunk, ChatRequest, ChatResponse
from dotenv import load_dotenv
from ..config.settings import settings

load_dotenv()

# Define tools as module-level functions to avoid initialization issues
@function_tool
def retrieve_context_tool(query: str) -> List[Dict[str, Any]]:
    """
    Retrieve relevant context chunks based on the query
    """
    try:
        context_chunks = rag_service.retrieve_context(query)
        # Convert to dict format for the agent
        result = []
        for chunk in context_chunks:
            result.append({
                "content": chunk.content,
                "source_doc_id": chunk.source_doc_id,
                "similarity_score": chunk.similarity_score,
                "metadata": chunk.metadata
            })
        return result
    except Exception as e:
        logging.error(f"Error in agent context retrieval: {e}")
        return []

@function_tool
def generate_response_tool(query: str, context: str) -> str:
    """
    Generate a response using the LLM based on the query and context
    """
    try:
        return llm_service.generate_response(query, context)
    except Exception as e:
        logging.error(f"Error in agent response generation: {e}")
        return "I'm sorry, but I encountered an error while generating a response. Please try again."


class RAGAgent:
    """
    Custom RAG agent using OpenAI Agents SDK with memory management
    """
    def __init__(self):
        # Create the main agent with tools
        self.agent = Agent(
            name="RAG Assistant",
            instructions=(
                "You are a helpful assistant that answers questions based on retrieved context. "
                "Always use the retrieved context to inform your answers. "
                "First, retrieve relevant context using the retrieve_context_tool. "
                "Then, generate a response using the generate_response_tool with the query and context. "
                "If the context doesn't contain relevant information to answer the question, please say so."
            ),
            tools=[
                retrieve_context_tool,
                generate_response_tool
            ],
            model="gpt-4o"  # Using a capable model for RAG tasks
        )

        # Reference to services
        self.rag_service = rag_service
        self.llm_service = llm_service
        self.session_service = session_service

    def process_query(self, query: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline using the agent with session management
        """
        try:
            # Get or create a conversation session
            session_id = conversation_id or "default"
            session = SQLiteSession(session_id, "conversations.db")

            # Run the agent with the query using the session for memory
            result = Runner.run(self.agent, query, session=session)

            # Extract the final response
            response_text = result.final_output

            # Retrieve context for sources
            context_chunks = self.rag_service.retrieve_context(query)

            # Prepare sources information
            sources = [
                {
                    "doc_id": chunk.source_doc_id,
                    "title": chunk.metadata.get("title", f"Document {chunk.source_doc_id}"),
                    "similarity_score": chunk.similarity_score
                }
                for chunk in context_chunks
            ]

            return {
                "response": response_text,
                "conversation_id": session_id,
                "status": "success",
                "sources": sources
            }
        except Exception as e:
            logging.error(f"Error in agent query processing: {e}")
            return {
                "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
                "conversation_id": conversation_id or "default",
                "status": "error",
                "sources": []
            }

    def run_streamed(self, query: str, conversation_id: Optional[str] = None):
        """
        Run the agent with streamed response capability using OpenAI Agents SDK
        Note: For true streaming with the OpenAI Agents SDK, we would need to use
        Runner.run_streamed with proper async implementation. This is a simplified
        version that demonstrates the concept.
        """
        try:
            # Get or create a conversation session
            session_id = conversation_id or "default"
            session = SQLiteSession(session_id, "conversations.db")

            # For now, we'll use the regular runner with session and return the result
            # True streaming would require Runner.run_streamed with async generator
            result = Runner.run(self.agent, query, session=session)

            # Prepare context for sources
            context_chunks = self.rag_service.retrieve_context(query)

            # Prepare sources information
            sources = [
                {
                    "doc_id": chunk.source_doc_id,
                    "title": chunk.metadata.get("title", f"Document {chunk.source_doc_id}"),
                    "similarity_score": chunk.similarity_score
                }
                for chunk in context_chunks
            ]

            yield {
                "response": result.final_output,
                "conversation_id": session_id,
                "status": "complete",
                "sources": sources
            }
        except Exception as e:
            logging.error(f"Error in agent streamed processing: {e}")
            yield {
                "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
                "conversation_id": conversation_id or "default",
                "status": "error",
                "error": str(e),
                "sources": []
            }

    async def run_streamed_async(self, query: str, conversation_id: Optional[str] = None):
        """
        Async version for true streaming with OpenAI Agents SDK
        """
        try:
            # Get or create a conversation session
            session_id = conversation_id or "default"
            session = SQLiteSession(session_id, "conversations.db")

            # Use Runner.run_streamed for true streaming
            result = Runner.run_streamed(self.agent, query, session=session)

            # Stream the events
            async for event in result.stream_events():
                if event.type == "run_item_stream_event":
                    # Process the streamed item
                    item = event.item
                    if hasattr(item, 'content') and item.content:
                        yield {
                            "token": item.content,
                            "conversation_id": session_id,
                            "status": "in_progress"
                        }

            # When complete, return the final result
            final_result = await result.get_final_result()
            context_chunks = self.rag_service.retrieve_context(query)

            # Prepare sources information
            sources = [
                {
                    "doc_id": chunk.source_doc_id,
                    "title": chunk.metadata.get("title", f"Document {chunk.source_doc_id}"),
                    "similarity_score": chunk.similarity_score
                }
                for chunk in context_chunks
            ]

            yield {
                "response": final_result.final_output,
                "conversation_id": session_id,
                "status": "complete",
                "sources": sources
            }
        except Exception as e:
            logging.error(f"Error in agent streamed processing: {e}")
            yield {
                "response": "I'm sorry, but I encountered an error while processing your query. Please try again.",
                "conversation_id": conversation_id or "default",
                "status": "error",
                "error": str(e),
                "sources": []
            }


# Global RAG agent instance
rag_agent = RAGAgent()