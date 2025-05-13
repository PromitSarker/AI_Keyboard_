# app/core/config.py
import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    # Project settings
    PROJECT_NAME: str = "Mood-Based Text Rephraser"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API for rephrasing text according to specified mood using Groq AI"
    
    # API settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    LLM_MODEL: str = "llama3-70b-8192"
    
    # Rephrasing settings
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0.7
    
    # Available moods
    AVAILABLE_MOODS: list = [
        "happy", "sad", "excited", "angry", "calm", "professional", 
        "casual", "formal", "humorous", "serious", "romantic", 
        "nostalgic", "optimistic", "pessimistic", "confident"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Initialize settings
settings = Settings()

# Validate required settings
if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable must be set")