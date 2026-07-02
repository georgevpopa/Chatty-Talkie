"""
Chatty Talkie - Backend API
FastAPI server providing translation endpoints.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from translator import Translator


# Initialize translator
translator = Translator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the translation model on startup."""
    translator.load_model()
    yield


app = FastAPI(
    title="Chatty Talkie",
    description="Offline translation app for Romanian, Spanish, and English",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    """Request body for translation endpoint."""

    text: str = Field(..., min_length=1, max_length=5000, description="Text to translate")
    source_lang: str = Field(..., pattern="^(en|ro|es)$", description="Source language code")
    target_lang: str = Field(..., pattern="^(en|ro|es)$", description="Target language code")


class TranslationResponse(BaseModel):
    """Response body for translation endpoint."""

    translated_text: str
    source_lang: str
    target_lang: str


class HealthResponse(BaseModel):
    """Response body for health check."""

    status: str
    model_loaded: bool


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check if the service is running and model is loaded."""
    return HealthResponse(
        status="ok",
        model_loaded=translator.is_loaded(),
    )


@app.get("/api/languages")
async def get_languages():
    """Get list of supported languages."""
    return translator.get_supported_languages()


@app.post("/api/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate text between supported languages."""
    if not translator.is_loaded():
        raise HTTPException(status_code=503, detail="Model is still loading. Please wait.")

    if request.source_lang == request.target_lang:
        return TranslationResponse(
            translated_text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )

    try:
        result = translator.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
        return TranslationResponse(
            translated_text=result,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


# Serve frontend static files
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
