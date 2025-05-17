# app/services/llm_service.py
import requests
from fastapi import HTTPException
# Fix import paths from "App" to "app" (case sensitivity matters)
from App.core.config import settings

#rephraser
async def rephrase(input_text: str, mood: str) -> str:
    """
    Send the text to Groq API to rephrase according to the selected mood
    
    Args:
        input_text: The original text to rephrase
        mood: The mood to apply to the text
        
    Returns:
        str: The rephrased text
        
    Raises:
        HTTPException: If there's an error with the API request
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.GROQ_API_KEY}"
    }
    # Create the prompt for the LLM
    prompt = f"""Please rephrase the following text to express a {mood} mood or tone. 
    Keep the core meaning intact, but adjust the language, word choice, and expression to reflect the {mood} mood. do not explain what you have changed, just give the result and try to be precise. Try to make it the same length as the original text.
    
    Original text: {input_text}
    
    Rephrased text with {mood} mood:"""
    
    # API request body for Groq (using OpenAI-compatible API)
    data = {
        "model": settings.LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": settings.TEMPERATURE,
        "max_tokens": settings.MAX_TOKENS
    }
    
    try:
        response = requests.post(settings.GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Groq API: {str(e)}")
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Groq API response: {str(e)}")
    
#grammar error fixing
async def fix_grammar(input_text: str) -> str:
    """
    Send the text to Groq API to fix grammatical errors
    
    Args:
        input_text: The text to fix grammar
        
    Returns:
        str: The grammatically corrected text
        
    Raises:
        HTTPException: If there's an error with the API request
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.GROQ_API_KEY}"
    }
    
    prompt = f"""Please fix any grammatical errors in the following text. 
    Keep the meaning and tone exactly the same, only correct grammar mistakes.
    Return only the corrected text without any explanations.

    Original text: {input_text}
    
    Corrected text:"""
    
    data = {
        "model": settings.LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,  # Lower temperature for more precise grammar correction
        "max_tokens": settings.MAX_TOKENS
    }
    
    try:
        response = requests.post(settings.GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Groq API: {str(e)}")
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Groq API response: {str(e)}")