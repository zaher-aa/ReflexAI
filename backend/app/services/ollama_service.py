import ollama
import httpx
from typing import Optional, Dict, List
import logging
import json

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
        self.base_url = "http://ollama:11434"  # Docker service name
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Ollama client"""
        try:
            # Test connection to Ollama
            response = httpx.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                logger.info("Ollama service connected successfully")
                self.client = ollama.Client(host=self.base_url)
            else:
                logger.warning("Ollama service not responding")
        except Exception as e:
            logger.warning(f"Ollama initialization failed: {e}. AI insights will be disabled.")
            self.client = None
    
    def analyze_themes(self, text: str, clusters: List[Dict]) -> Optional[Dict]:
        """Generate AI insights about themes and patterns"""
        if not self.client:
            return None
        
        try:
            # Prepare context for Ollama
            cluster_summary = "\n".join([
                f"- {c['label']}: {', '.join(c['words'][:5])}" 
                for c in clusters[:5]
            ])
            
            prompt = f"""As a literary analyst, examine this creative writing excerpt and identify key themes and stylistic patterns.

Text excerpt (first 500 characters):
"{text[:500]}..."

Identified word clusters:
{cluster_summary}

Provide a brief analysis (3-4 sentences) focusing on:
1. Main thematic elements
2. Writing style characteristics
3. Emotional tone

Keep the response concise and insightful."""

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "max_tokens": 200
                }
            )
            
            return {
                "ai_insights": response['response'],
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Ollama analysis failed: {e}")
            return None
    
    def check_model_availability(self) -> bool:
        """Check if the model is available"""
        if not self.client:
            return False
        
        try:
            response = httpx.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(m['name'] == self.model for m in models)
        except:
            return False
        
        return False
    
    def pull_model(self):
        """Pull the model if not available"""
        if not self.client:
            return False
        
        try:
            logger.info(f"Pulling Ollama model: {self.model}")
            self.client.pull(self.model)
            return True
        except Exception as e:
            logger.error(f"Failed to pull model: {e}")
            return False