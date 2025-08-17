from textblob import TextBlob
from typing import Dict
import re

class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        blob = TextBlob(text)
        
        sentences = blob.sentences
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for sentence in sentences:
            polarity = sentence.sentiment.polarity
            if polarity > 0.1:
                positive_count += 1
            elif polarity < -0.1:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(sentences) if sentences else 1
        
        return {
            'overall': blob.sentiment.polarity,
            'positive': (positive_count / total) * 100,
            'negative': (negative_count / total) * 100,
            'neutral': (neutral_count / total) * 100
        }