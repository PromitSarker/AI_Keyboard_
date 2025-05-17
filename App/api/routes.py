# app/api/routes/rephraser.py
from fastapi import APIRouter, HTTPException
# Fix import paths from "App" to "app" (case sensitivity matters)
from App.core.config import settings
from App.model.schemas import TextInput, RephrasedResponse, GrammarFixInput, GrammarFixResponse
from App.services.llm_service import rephrase, fix_grammar

router = APIRouter(prefix="/keyboard", tags=["rephraser"])

@router.post("/fix-grammar", response_model=GrammarFixResponse)
async def fix_text_grammar(input_data: GrammarFixInput):
    """
    Endpoint to fix grammatical errors in text
    
    Parameters:
    - text: The text to fix grammar
    
    Returns:
    - original_text: The input text
    - corrected_text: The text with grammar fixed
    """
    corrected = await fix_grammar(input_data.text)
    
    return GrammarFixResponse(
        original_text=input_data.text,
        corrected_text=corrected
    )

@router.post("/rephrase", response_model=RephrasedResponse)
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