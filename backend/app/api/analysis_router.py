from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
import uuid
from datetime import datetime
from typing import Dict, Any
import json
import logging

from app.models.analysis import (
    AnalysisResult, TextInput, KeynessResult, 
    KeywordItem, SemanticCluster, SentimentResult
)
from app.services.text_processor import TextProcessor
from app.services.keyness_analyzer import KeynessAnalyzer
from app.services.semantic_clustering import SemanticClusterer
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.ollama_service import OllamaService
from app.services.file_handler import FileHandler

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
text_processor = TextProcessor()
keyness_analyzer = KeynessAnalyzer()
semantic_clusterer = SemanticClusterer()
sentiment_analyzer = SentimentAnalyzer()
ollama_service = OllamaService()
file_handler = FileHandler()

# Store for temporary results (in production, use Redis or database)
analysis_cache: Dict[str, Any] = {}

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
    
    # Schedule file deletion in background (RF-22)
    background_tasks.add_task(file_handler.delete_temp_file, file_path)
    
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

async def analyze_text_internal(text: str, analysis_id: str) -> AnalysisResult:
    """Internal text analysis with all NLP features"""
    
    logger.info(f"Starting analysis for ID: {analysis_id}")
    
    # Clean and process text with spaCy (RF-24)
    cleaned_text = text_processor.clean_text(text)
    
    # Get word frequencies using spaCy tokenization
    word_freq = text_processor.get_word_frequencies(cleaned_text)
    
    # Perform analyses
    keyness_results = keyness_analyzer.calculate_keyness(cleaned_text)
    clusters = semantic_clusterer.create_clusters(cleaned_text)
    sentiment = sentiment_analyzer.analyze_sentiment(cleaned_text)
    
    # Get AI insights if Ollama is available
    ai_insights = None
    try:
        insights = ollama_service.analyze_themes(cleaned_text, clusters)
        if insights:
            ai_insights = insights
            logger.info("AI insights generated successfully")
    except Exception as e:
        logger.warning(f"Could not generate AI insights: {e}")
    
    # Create result object
    result = AnalysisResult(
        id=analysis_id,
        timestamp=datetime.now().isoformat(),
        keyness=KeynessResult(
            keywords=[KeywordItem(**k) for k in keyness_results]
        ),
        semanticClusters=[SemanticCluster(**c) for c in clusters],
        sentiment=SentimentResult(**sentiment),
        aiInsights=ai_insights  # Add AI insights to result
    )
    
    # Store in cache
    analysis_cache[analysis_id] = result
    
    logger.info(f"Analysis completed for ID: {analysis_id}")
    
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
            "text_processor": "active",
            "spacy": text_processor.nlp is not None,
            "ollama": ollama_service.client is not None
        }
    }