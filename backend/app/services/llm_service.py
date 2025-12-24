"""
LLM Service for intent extraction using Ollama
"""
import httpx
import json
import logging
from typing import Optional
from app.schemas.models import LLMIntent
from app.utils.env_config import get_ollama_base_url, get_llm_model

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with locally running LLM via Ollama"""
    
    def __init__(self):
        self.base_url = get_ollama_base_url()
        self.model = get_llm_model()
        self.timeout = 30.0
    
    async def extract_intent(self, user_query: str) -> Optional[LLMIntent]:
        """
        Extract structured intent from natural language query
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            LLMIntent object with structured data or None if extraction fails
        """
        system_prompt = """You are a JSON-only intent extraction system. Your ONLY job is to extract structured information from user queries about finding places.

You must respond with ONLY valid JSON in this exact format:
{
  "query": "search term",
  "location": "location string",
  "category": "restaurant"
}

Rules:
- Output ONLY the JSON object, no other text
- Do not make up information
- Extract the food/place type as "query"
- Extract the location as "location"
- Use "restaurant" as the default category
- If location is not specified, use "Jakarta" as default

Example:
User: "Where can I eat ramen near Blok M?"
Response: {"query": "ramen", "location": "Blok M Jakarta", "category": "restaurant"}"""

        user_prompt = f"Extract intent from: {user_query}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Call Ollama API
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{system_prompt}\n\n{user_prompt}",
                        "stream": False,
                        "format": "json"  # Request JSON format
                    }
                )
                response.raise_for_status()
                
                result = response.json()
                generated_text = result.get("response", "")
                
                # Parse the JSON response
                intent_data = json.loads(generated_text)
                
                # Validate and create LLMIntent object
                intent = LLMIntent(**intent_data)
                logger.info(f"Successfully extracted intent: {intent}")
                return intent
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.error(f"Raw response: {generated_text}")
            # Fallback: try to extract manually
            return self._fallback_extraction(user_query)
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling Ollama: {e}")
            return self._fallback_extraction(user_query)
            
        except Exception as e:
            logger.error(f"Unexpected error in LLM service: {e}")
            return self._fallback_extraction(user_query)
    
    def _fallback_extraction(self, user_query: str) -> Optional[LLMIntent]:
        """
        Simple fallback extraction when LLM fails
        """
        try:
            # Very basic extraction
            query_lower = user_query.lower()
            
            # Try to extract food type
            food_keywords = ["ramen", "pizza", "sushi", "coffee", "burger", "noodle", "pasta"]
            query_term = "restaurant"
            for keyword in food_keywords:
                if keyword in query_lower:
                    query_term = keyword
                    break
            
            # Try to extract location
            location = "Jakarta"  # Default
            if "blok m" in query_lower:
                location = "Blok M Jakarta"
            elif "sudirman" in query_lower:
                location = "Sudirman Jakarta"
            elif "menteng" in query_lower:
                location = "Menteng Jakarta"
            
            return LLMIntent(
                query=query_term,
                location=location,
                category="restaurant"
            )
        except Exception as e:
            logger.error(f"Fallback extraction failed: {e}")
            return None


# Singleton instance
llm_service = LLMService()
