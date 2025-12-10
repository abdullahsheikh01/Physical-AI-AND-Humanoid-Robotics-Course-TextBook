import google.generativeai as genai
from typing import Dict, Any, Optional
from ..config.settings import settings
import logging


class LLMService:
    """
    Service for interacting with the Gemini LLM
    """
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None
            logging.warning("GEMINI_API_KEY not set, LLM functionality will be limited")

    def generate_response(self, prompt: str, context: str = None) -> Optional[str]:
        """
        Generate a response using the Gemini model
        """
        if not self.model:
            logging.error("Gemini model not initialized")
            return "I'm sorry, but I'm unable to generate a response at the moment. Please try again later."

        try:
            # Create the full prompt with context if provided
            if context:
                full_prompt = f"""
                Context information:
                {context}

                User question: {prompt}

                Please provide a helpful and accurate response based on the context information provided above.
                If the context doesn't contain relevant information to answer the question, please say so.
                """
            else:
                full_prompt = f"""
                User question: {prompt}

                I don't have any relevant context to answer this question, but I'll do my best to help.
                """

            # Generate response
            response = self.model.generate_content(full_prompt)

            return response.text if response.text else "I couldn't generate a response for your query."
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "I'm sorry, but I encountered an error while generating a response. Please try again."

    def generate_response_with_history(self, prompt: str, context: str = None, history: list = None) -> Optional[str]:
        """
        Generate a response considering conversation history
        """
        if not self.model:
            logging.error("Gemini model not initialized")
            return "I'm sorry, but I'm unable to generate a response at the moment. Please try again later."

        try:
            # For now, just use the basic generate_response method
            # In a more advanced implementation, we would use the chat functionality with history
            return self.generate_response(prompt, context)
        except Exception as e:
            logging.error(f"Error generating response with history: {e}")
            return "I'm sorry, but I encountered an error while generating a response. Please try again."


# Global LLM service instance
llm_service = LLMService()