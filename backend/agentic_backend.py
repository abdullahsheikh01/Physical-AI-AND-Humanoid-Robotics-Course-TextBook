"""
Agentic backend for RAG Chatbot integration with Physical AI & Humanoid Robotics textbook.
This module handles the AI agent logic, including Gemini model integration,
Cohere embeddings, Qdrant vector search, and RAG functionality.
"""
import os
from typing import List

import cohere
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents import function_tool


# Load environment variables
load_dotenv()

# Disable tracing for OpenAI Agents SDK
os.environ["OPENAI_DISABLE_TRACING"] = "true"


# Initialize OpenAI-compatible provider with Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

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

qdrant = QdrantClient(
      url=qdrant_url,
      api_key=qdrant_api_key
  )


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
    # Generate embedding for the query
    query_embedding = get_embedding(query)

    # Perform vector search in Qdrant
    search_results = qdrant.query_points(
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        query=query_embedding,
        limit=5
    )

    # Extract text from payload of each result
    retrieved_texts = []
    for result in search_results.points:
        if "text" in result.payload:
            retrieved_texts.append(result.payload["text"])

    return retrieved_texts


# Create the AI agent
assistant_agent = Agent(
    name="Assistant",
    instructions="""
    You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
    Always call the retrieve tool first with the user's question to get relevant context.
    Answer only using the content returned by the retrieve tool.
    If the relevant information is not present in the retrieved results, respond with "I don't know".
    Be helpful, accurate, and concise in your responses.
    """,
    model="gpt-4o",
    tools=[retrieve],
)


async def run_agent(INPUTFROMFASTAPI: str) -> str:
    """
    Synchronously run the previously created agent using the Runner.run_sync method
    from the OpenAI Agents SDK. The function calls Runner.run_sync by passing the
    agent instance as the first argument and providing a variable named INPUTFROMFASTAPI
    as the value of the input parameter, representing the incoming message from a FastAPI endpoint.
    The function stores the result returned by the runner in a variable and returns that result.

    Args:
        INPUTFROMFASTAPI: The input message from the FastAPI endpoint

    Returns:
        The result from the agent
    """
    result = await Runner.run(
        assistant_agent,
        INPUTFROMFASTAPI
    )
    return result.final_output