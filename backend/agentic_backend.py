"""
Agentic backend for RAG Chatbot integration with Physical AI & Humanoid Robotics textbook.
This module handles the AI agent logic, including Gemini model integration,
Cohere embeddings, Qdrant vector search, and RAG functionality.
"""

import os
from typing import List, Dict, Any

import cohere
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import function_tool,set_default_openai_api
set_default_openai_api("chat_completions")


# Load environment variables
load_dotenv()

# Disable tracing for OpenAI Agents SDK
# os.environ["OPENAI_DISABLE_TRACING"] = "true"


# Initialize OpenAI-compatible provider with Gemini API
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY environment variable is required")

# Initialize OpenAI client with Gemini-compatible endpoint
# openai_client = OpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# Create a chat completion model instance using the OpenAIChatCompletionsModel class
# from the OpenAI Agents SDK, specifying "gemini-2.0-flash" as the model name
# and passing the previously created provider instance to the openai_client parameter
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=openai_client
# )


# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")

cohere_client = cohere.Client(cohere_api_key)


# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if not qdrant_url:
    raise ValueError("QDRANT_URL environment variable is required")

# Initialize Qdrant client with optional API key
if qdrant_api_key:
    qdrant = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )
else:
    # For local Qdrant instances, API key might not be required
    qdrant = QdrantClient(url=qdrant_url)


def get_embedding(text: str) -> List[float]:
    """
    Generate an embedding vector using Cohere Embed v3 model.

    Args:
        text: Input text to generate embedding for

    Returns:
        Embedding vector as a list of floats
    """
    response = cohere_client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return response.embeddings[0]


@function_tool
def retrieve(query: str) -> List[str]:
    """
    Retrieve relevant context chunks from the vector database based on the query.

    Args:
        query: User query to search for relevant context

    Returns:
        List of relevant text chunks
    """
    try:
        # Generate embedding for the query
        query_embedding = get_embedding(query)

        # Get collection name from environment
        collection_name = os.getenv("QDRANT_COLLECTION_NAME")
        if not collection_name:
            raise ValueError("QDRANT_COLLECTION_NAME environment variable is required")

        # Perform vector search in Qdrant
        search_results = qdrant.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=5
        )

        # Extract text from payload of each result
        return [result.payload["text"] for result in search_results]
    except Exception as e:
        print(f"Error in retrieve function: {str(e)}")
        # Return empty list if there's an error, allowing the agent to handle it gracefully
        return []


# Validate required environment variables before creating the agent
qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME")
if not qdrant_collection_name:
    raise ValueError("QDRANT_COLLECTION_NAME environment variable is required")

# Create the AI agent
assistant_agent = Agent(
    name="Assistant",
    instructions="""
    You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
    Always call the retrieve tool first with the user's question to get relevant context.
    Answer only using the content returned by the retrieve tool.
    Be helpful, accurate, and concise in your responses and give responses.
    """,
    model="gpt-4o",
    tools=[retrieve],
)


async def run_agent(INPUTFROMFASTAPI: Dict[str, Any]) -> str:
    """
    Run the agent with the provided input which contains query, history, and conversation_id.

    Args:
        INPUTFROMFASTAPI: Dict containing 'query', 'history', and 'conversation_id'

    Returns:
        The result from the agent
    """
    # Extract query and history from the input
    query = INPUTFROMFASTAPI.get('query', '')
    history = INPUTFROMFASTAPI.get('history', [])

    # Combine history with current query to create full context
    # Format as conversation history for the agent - use 'content' instead of 'message'
    full_conversation = []
    for item in history:
        full_conversation.append({"role": item.get('role', ''), "content": item.get('content', '')})

    # Add the current query as the latest user message
    full_conversation.append({"role": "user", "content": query})
    print(full_conversation)
    result = await Runner.run(
        assistant_agent,
        full_conversation
    )
    return result.final_output

