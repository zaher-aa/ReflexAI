from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, Any, Optional, List
import logging
import json

from app.services.ollama_service import OllamaService
from app.models.analysis import AnalysisResult
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()
ollama_service = OllamaService()

class OllamaRequest(BaseModel):
    text: str
    prompt: Optional[str] = None
    max_tokens: Optional[int] = 300
    temperature: Optional[float] = 0.7

class OllamaThemeRequest(BaseModel):
    text: str
    clusters: List[Dict[str, Any]]

class ModelManagementRequest(BaseModel):
    model_name: str

@router.get("/health")
async def ollama_health():
    """Check Ollama service health and model availability"""
    try:
        is_available = ollama_service.check_model_availability()
        return {
            "status": "healthy" if ollama_service.client else "unavailable",
            "model": ollama_service.model,
            "model_available": is_available,
            "base_url": ollama_service.base_url
        }
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "model": ollama_service.model,
            "model_available": False
        }

@router.post("/analyze-themes")
async def analyze_themes(request: OllamaThemeRequest):
    """Generate AI insights about themes and patterns (US-B3)"""
    if not ollama_service.client:
        raise HTTPException(
            status_code=503, 
            detail="Ollama service is not available. Please ensure Ollama is running and the model is pulled."
        )
    
    try:
        insights = ollama_service.analyze_themes(request.text, request.clusters)
        
        if not insights:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate AI insights. Please try again."
            )
        
        return {
            "success": True,
            "insights": insights,
            "model": ollama_service.model
        }
        
    except Exception as e:
        logger.error(f"Theme analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

@router.post("/generate")
async def generate_text(request: OllamaRequest):
    """Generate text using Ollama (US-B3)"""
    if not ollama_service.client:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available"
        )
    
    try:
        # Use custom prompt or default creative writing analysis prompt
        prompt = request.prompt or f"""
        As a creative writing analyst, provide insights about this text excerpt:
        
        "{request.text[:1000]}..."
        
        Focus on:
        1. Writing style and voice
        2. Thematic elements
        3. Emotional tone and mood
        4. Literary techniques used
        
        Keep your response concise and insightful (2-3 paragraphs).
        """
        
        response = ollama_service.client.generate(
            model=ollama_service.model,
            prompt=prompt,
            options={
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }
        )
        
        return {
            "success": True,
            "response": response['response'],
            "model": ollama_service.model,
            "prompt_tokens": len(prompt.split()),
            "response_tokens": len(response['response'].split())
        }
        
    except Exception as e:
        logger.error(f"Text generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Text generation failed: {str(e)}"
        )

@router.post("/pull-model")
async def pull_model(background_tasks: BackgroundTasks, request: ModelManagementRequest):
    """Pull/download a model (US-B3)"""
    if not ollama_service.client:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available"
        )
    
    try:
        # Start model pulling in background
        background_tasks.add_task(ollama_service.pull_model)
        
        return {
            "success": True,
            "message": f"Started pulling model: {request.model_name}",
            "model": request.model_name
        }
        
    except Exception as e:
        logger.error(f"Model pull failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to pull model: {str(e)}"
        )

@router.get("/models")
async def list_models():
    """List available models (US-B3)"""
    if not ollama_service.client:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available"
        )
    
    try:
        import httpx
        response = httpx.get(f"{ollama_service.base_url}/api/tags")
        
        if response.status_code == 200:
            models_data = response.json()
            return {
                "success": True,
                "models": models_data.get('models', []),
                "current_model": ollama_service.model
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch models from Ollama"
            )
            
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list models: {str(e)}"
        )

@router.post("/switch-model")
async def switch_model(request: ModelManagementRequest):
    """Switch to a different model (US-B3)"""
    try:
        old_model = ollama_service.model
        ollama_service.model = request.model_name
        
        # Verify the model is available
        if not ollama_service.check_model_availability():
            # Revert to old model if new one isn't available
            ollama_service.model = old_model
            raise HTTPException(
                status_code=404,
                detail=f"Model '{request.model_name}' is not available. Please pull it first."
            )
        
        return {
            "success": True,
            "message": f"Switched to model: {request.model_name}",
            "previous_model": old_model,
            "current_model": ollama_service.model
        }
        
    except Exception as e:
        logger.error(f"Model switch failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to switch model: {str(e)}"
        )

@router.get("/status")
async def get_status():
    """Get comprehensive Ollama status (US-B3)"""
    try:
        import httpx
        
        # Check service connectivity
        service_healthy = False
        model_available = False
        models_list = []
        
        try:
            response = httpx.get(f"{ollama_service.base_url}/api/tags", timeout=5.0)
            if response.status_code == 200:
                service_healthy = True
                models_data = response.json()
                models_list = models_data.get('models', [])
                model_available = any(m['name'] == ollama_service.model for m in models_list)
        except:
            pass
        
        return {
            "service_healthy": service_healthy,
            "model_available": model_available,
            "current_model": ollama_service.model,
            "base_url": ollama_service.base_url,
            "available_models": models_list,
            "client_initialized": ollama_service.client is not None
        }
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "service_healthy": False,
            "model_available": False,
            "current_model": ollama_service.model,
            "error": str(e)
        }