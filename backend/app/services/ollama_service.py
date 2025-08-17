import ollama
from typing import Optional

class OllamaService:
    def __init__(self, model: str = "llama3.1"):
        self.model = model
        self.client = None
        self._initialize()
    
    def _initialize(self):
        try:
            self.client = ollama.Client()
        except Exception as e:
            print(f"Ollama initialization failed: {e}")
    
    def generate_insights(self, text: str, analysis_results: dict) -> Optional[str]:
        if not self.client:
            return None
        
        prompt = f"""
        Analyze this creative writing text and provide insights:
        
        Text sample: {text[:500]}...
        
        Key themes identified: {analysis_results.get('themes', [])}
        Sentiment: {analysis_results.get('sentiment', {})}
        
        Provide 3 specific insights about the writer's style and themes.
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            print(f"Ollama generation failed: {e}")
            return None