from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class KeywordItem(BaseModel):
    word: str
    score: float
    frequency: int

class KeynessResult(BaseModel):
    keywords: List[KeywordItem]

class SemanticCluster(BaseModel):
    id: int
    label: str
    words: List[str]
    size: int

class SentimentResult(BaseModel):
    overall: float
    positive: float
    negative: float
    neutral: float

class AnalysisResult(BaseModel):
    id: str
    timestamp: str
    keyness: KeynessResult
    semanticClusters: List[SemanticCluster]
    sentiment: SentimentResult
    aiInsights: Optional[Dict] = None  # Add AI insights field

class TextInput(BaseModel):
    text: str