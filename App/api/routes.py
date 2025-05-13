# app/api/routes/rephraser.py
from fastapi import APIRouter, HTTPException
# Fix import paths from "App" to "app" (case sensitivity matters)
from App.core.config import settings
from App.model.schemas import TextInput, RephrasedResponse
from App.services.llm_service import rephrase

router = APIRouter(prefix="/rephrase", tags=["rephraser"])

@router.post("/", response_model=RephrasedResponse)
async def rephrase_text(input_data: TextInput):
    """
    Endpoint to rephrase text according to the specified mood
    
    Parameters:
    - text: The original text to rephrase
    - mood: The mood to apply to the text
    
    Returns:
    - original_text: The input text
    - mood: The specified mood
    - rephrased_text: The text rephrased in the specified mood
    """
    # Validate that the mood is in the list of available moods
    if input_data.mood.lower() not in [mood.lower() for mood in settings.AVAILABLE_MOODS]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid mood. Available moods: {', '.join(settings.AVAILABLE_MOODS)}"
        )
    
    # Send the text to Groq for rephrasing
    rephrased = await rephrase(input_data.text, input_data.mood)
    
    # Return the response
    return RephrasedResponse(
        original_text=input_data.text,
        mood=input_data.mood,
        rephrased_text=rephrased
    )