"""
Utility functions for the backend
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_env(key: str, default: str = None) -> str:
    """Get environment variable with optional default"""
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def get_google_maps_api_key() -> str:
    """Get Google Maps API key from environment"""
    return get_env("GOOGLE_MAPS_API_KEY")


def get_ollama_base_url() -> str:
    """Get Ollama base URL from environment"""
    return get_env("OLLAMA_BASE_URL", "http://localhost:11434")


def get_llm_model() -> str:
    """Get LLM model name from environment"""
    return get_env("LLM_MODEL", "llama3.2:latest")
