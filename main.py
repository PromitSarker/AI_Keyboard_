# app/main.py
from fastapi import FastAPI
# Fix import paths from "App" to "app" (case sensitivity matters)
from App.api.routes import router
from App.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION
)

# Include routers
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """
    Root endpoint to provide usage information
    """
    return {
        "message": "Mood-Based Text Rephraser API",
        "documentation": "/docs",
        "features": {
            "rephrase": {
                "endpoint": "/api/v1/rephrase",
                "example": {
                    "text": "I need to attend a meeting tomorrow.",
                    "mood": "excited"
                },
                "available_moods": settings.AVAILABLE_MOODS
            },
            "grammar_fix": {
                "endpoint": "/api/v1/fix-grammar",
                "example": {
                    "text": "I has went to the store yesterday."
                }
            }
        }
    }

# Run the application from this file
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)