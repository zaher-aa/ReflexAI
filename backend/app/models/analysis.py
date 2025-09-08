from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class KeywordItem(BaseModel):
    word: str
    score: float
    frequency: int
    rank: int
    effect_size: Optional[float] = None
    confidence: Optional[float] = None

class KeynessResult(BaseModel):
    keywords: List[KeywordItem]
    total_keywords: int
    processing_time_ms: Optional[float] = None
    reference_corpus: Optional[str] = None

class WordCoordinate(BaseModel):
    word: str
    x: float
    y: float
    cluster_id: int

class SemanticCluster(BaseModel):
    id: int
    label: str
    words: List[str]
    size: int
    centroid: Optional[Dict[str, float]] = None
    coherence_score: Optional[float] = None
    word_coordinates: Optional[List[WordCoordinate]] = None

class SemanticClusteringResult(BaseModel):
    clusters: List[SemanticCluster]
    total_clusters: int
    processing_time_ms: Optional[float] = None
    algorithm: Optional[str] = None
    similarity_threshold: Optional[float] = None

class SentimentResult(BaseModel):
    overall: float
    positive: float
    negative: float
    neutral: float
    compound: Optional[float] = None
    confidence: Optional[float] = None
    sentence_sentiments: Optional[List[Dict[str, float]]] = None

class TextStatistics(BaseModel):
    character_count: int
    word_count: int
    sentence_count: int
    paragraph_count: int
    avg_sentence_length: float
    avg_word_length: float
    unique_words: int
    vocabulary_richness: float
    readability_score: Optional[float] = None

class ProcessingMetadata(BaseModel):
    start_time: str
    end_time: str
    processing_time_seconds: float
    file_size_bytes: Optional[int] = None
    model_versions: Optional[Dict[str, Optional[str]]] = None
    parameters: Optional[Dict[str, Any]] = None
    
    class Config:
        # Allow None values in model_versions dict
        extra = "allow"

class AnalysisResult(BaseModel):
    id: str
    timestamp: str
    status: AnalysisStatus
    keyness: Optional[KeynessResult] = None
    semanticClusters: Optional[List[SemanticCluster]] = None  # For backward compatibility
    semanticClustering: Optional[SemanticClusteringResult] = None
    sentiment: Optional[SentimentResult] = None
    textStatistics: Optional[TextStatistics] = None
    aiInsights: Optional[Dict] = None
    metadata: Optional[ProcessingMetadata] = None
    error_message: Optional[str] = None

class TextInput(BaseModel):
    text: str
    parameters: Optional[Dict[str, Any]] = None