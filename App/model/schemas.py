# app/models/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class TextInput(BaseModel):
    """Schema for input text and mood"""
    text: str = Field(..., description="The text to be rephrased", min_length=1)
    mood: str = Field(..., description="The mood to apply to the text")
    
    class Config:
        # Change to model_config format if using newer Pydantic v2 or keep as-is for v1
        schema_extra = {
            "example": {
                "text": "I need to attend a meeting tomorrow.",
                "mood": "excited"
            }
        }

class RephrasedResponse(BaseModel):
    """Schema for the rephrased text response"""
    original_text: str = Field(..., description="The original input text")
    mood: str = Field(..., description="The mood applied to the text")
    rephrased_text: str = Field(..., description="The text rephrased according to the mood")
    
    class Config:
        # Change to model_config format if using newer Pydantic v2 or keep as-is for v1
        schema_extra = {
            "example": {
                "original_text": "I need to attend a meeting tomorrow.",
                "mood": "excited",
                "rephrased_text": "I can't wait to participate in tomorrow's meeting! It's going to be such an energizing opportunity to collaborate with the team and share our ideas!"
            }
        }

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str = Field(..., description="Error message")