from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import json
import logging
import asyncio
import os

from app.models.analysis import (
    AnalysisResult, TextInput, KeynessResult, 
    KeywordItem, SemanticCluster, SentimentResult, AnalysisStatus
)
from app.services.analysis_pipeline import AnalysisPipeline
from app.services.file_handler import FileHandler

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
analysis_pipeline = AnalysisPipeline()
file_handler = FileHandler()

# Store for temporary results (in production, use Redis or database)
analysis_cache: Dict[str, Any] = {}

# Configuration for automatic cleanup
DELETE_AFTER_ANALYSIS = os.getenv("DELETE_AFTER_ANALYSIS", "true").lower() == "true"
CLEANUP_INTERVAL_SECONDS = int(os.getenv("CLEANUP_INTERVAL_SECONDS", "1800"))  # 30 minutes
MAX_FILE_AGE_SECONDS = int(os.getenv("MAX_FILE_AGE_SECONDS", "3600"))  # 1 hour

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """Upload file with progress tracking (RF-30)"""
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    # Generate session ID for progress tracking
    session_id = str(uuid.uuid4())
    analysis_id = str(uuid.uuid4())
    
    # Save file temporarily (RF-22)
    file_path = await file_handler.save_temp_file(file, session_id)
    
    # Read content
    text = await file_handler.read_temp_file(file_path)
    
    # Process immediately
    result = await analyze_text_internal(text, analysis_id)
    
    # Store in cache
    analysis_cache[analysis_id] = result
    
    # Schedule file deletion in background if enabled
    if DELETE_AFTER_ANALYSIS:
        background_tasks.add_task(file_handler.delete_temp_file, file_path)
        logger.info(f"Scheduled deletion of file: {file_path}")
    
    # Schedule cleanup of old files
    background_tasks.add_task(file_handler.cleanup_old_files, MAX_FILE_AGE_SECONDS)
    
    return {
        "success": True,
        "message": "File uploaded and analyzed successfully",
        "analysisId": analysis_id,
        "progress": file_handler.get_upload_progress(session_id)
    }

@router.get("/upload/progress/{session_id}")
async def get_upload_progress(session_id: str):
    """Get upload progress (RF-30)"""
    progress = file_handler.get_upload_progress(session_id)
    return {"progress": progress}

@router.post("/analyze")
async def analyze_text(input_data: TextInput):
    """Analyze text directly"""
    analysis_id = str(uuid.uuid4())
    result = await analyze_text_internal(input_data.text, analysis_id)
    return result

async def analyze_text_internal(
    text: str, 
    analysis_id: str,
    parameters: Optional[Dict[str, Any]] = None
) -> AnalysisResult:
    """Internal text analysis using unified pipeline"""
    
    logger.info(f"Starting analysis for ID: {analysis_id}")
    
    # Use unified analysis pipeline
    result = await analysis_pipeline.analyze(text, analysis_id, parameters)
    
    # Store in cache
    analysis_cache[analysis_id] = result
    
    logger.info(f"Analysis completed for ID: {analysis_id} with status: {result.status}")
    
    return result

@router.get("/results/{analysis_id}")
async def get_results(analysis_id: str):
    """Get analysis results"""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis_cache[analysis_id]

@router.get("/download/{analysis_id}")
async def download_results(analysis_id: str):
    """Download results as JSON"""
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    result = analysis_cache[analysis_id]
    
    # Convert to JSON
    json_content = json.dumps(result.dict(), indent=2)
    
    # Clean up after download (privacy protection)
    del analysis_cache[analysis_id]
    
    return StreamingResponse(
        iter([json_content]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=analysis-{analysis_id}.json"
        }
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "analysis_pipeline": "active",
            "spacy": analysis_pipeline.text_processor.nlp is not None,
            "ollama": analysis_pipeline.ollama_service.client is not None
        },
        "file_cleanup": {
            "enabled": DELETE_AFTER_ANALYSIS,
            "max_file_age_seconds": MAX_FILE_AGE_SECONDS,
            "cleanup_interval_seconds": CLEANUP_INTERVAL_SECONDS
        }
    }

@router.get("/files/stats")
async def get_file_stats():
    """Get temporary file directory statistics"""
    return file_handler.get_temp_directory_stats()

@router.post("/files/cleanup")
async def manual_cleanup(background_tasks: BackgroundTasks):
    """Manually trigger file cleanup"""
    background_tasks.add_task(file_handler.cleanup_old_files, MAX_FILE_AGE_SECONDS)
    return {
        "success": True,
        "message": "File cleanup initiated",
        "max_age_seconds": MAX_FILE_AGE_SECONDS
    }