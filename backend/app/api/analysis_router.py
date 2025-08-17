from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import uuid
from datetime import datetime
from typing import Dict, Any

from app.models.analysis import (
    AnalysisResult, TextInput, KeynessResult, 
    KeywordItem, SemanticCluster, SentimentResult
)
from app.services.text_processor import TextProcessor
from app.services.keyness_analyzer import KeynessAnalyzer
from app.services.semantic_clustering import SemanticClusterer
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.ollama_service import OllamaService

router = APIRouter()

text_processor = TextProcessor()
keyness_analyzer = KeynessAnalyzer()
semantic_clusterer = SemanticClusterer()
sentiment_analyzer = SentimentAnalyzer()
ollama_service = OllamaService()

# Store for temporary results (in production, use Redis or database)
analysis_cache: Dict[str, Any] = {}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    
    content = await file.read()
    text = content.decode('utf-8')
    
    analysis_id = str(uuid.uuid4())
    
    # Process immediately
    result = await analyze_text_internal(text)
    analysis_cache[analysis_id] = result
    
    return {"success": True, "message": "File uploaded successfully", "analysisId": analysis_id}

@router.post("/analyze")
async def analyze_text(input_data: TextInput):
    result = await analyze_text_internal(input_data.text)
    return result

async def analyze_text_internal(text: str) -> AnalysisResult:
    analysis_id = str(uuid.uuid4())
    
    # Perform analyses
    keyness_results = keyness_analyzer.calculate_keyness(text)
    clusters = semantic_clusterer.create_clusters(text)
    sentiment = sentiment_analyzer.analyze_sentiment(text)
    
    # Create result object
    result = AnalysisResult(
        id=analysis_id,
        timestamp=datetime.now().isoformat(),
        keyness=KeynessResult(
            keywords=[KeywordItem(**k) for k in keyness_results]
        ),
        semanticClusters=[SemanticCluster(**c) for c in clusters],
        sentiment=SentimentResult(**sentiment)
    )
    
    # Store in cache
    analysis_cache[analysis_id] = result
    
    return result

@router.get("/results/{analysis_id}")
async def get_results(analysis_id: str):
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis_cache[analysis_id]

@router.get("/download/{analysis_id}")
async def download_results(analysis_id: str):
    if analysis_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    result = analysis_cache[analysis_id]
    
    # Clean up after download (privacy protection)
    del analysis_cache[analysis_id]
    
    return JSONResponse(
        content=result.dict(),
        headers={
            "Content-Disposition": f"attachment; filename=analysis-{analysis_id}.json"
        }
    )