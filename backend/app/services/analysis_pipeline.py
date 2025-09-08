import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.analysis import (
    AnalysisResult, AnalysisStatus, KeynessResult, SemanticClusteringResult,
    SentimentResult, TextStatistics, ProcessingMetadata, KeywordItem,
    SemanticCluster, WordCoordinate
)
from app.services.text_processor import TextProcessor
from app.services.keyness_analyzer import KeynessAnalyzer
from app.services.semantic_clustering import SemanticClusterer
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.services.ollama_service import OllamaService

logger = logging.getLogger(__name__)

class AnalysisPipeline:
    """Unified pipeline for all text analysis modules"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.keyness_analyzer = KeynessAnalyzer()
        self.semantic_clusterer = SemanticClusterer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.ollama_service = OllamaService()
        
    async def analyze(
        self, 
        text: str, 
        analysis_id: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """Run complete analysis pipeline"""
        
        start_time = time.time()
        start_timestamp = datetime.now().isoformat()
        
        # Initialize result object
        result = AnalysisResult(
            id=analysis_id,
            timestamp=start_timestamp,
            status=AnalysisStatus.PROCESSING
        )
        
        try:
            logger.info(f"Starting unified analysis pipeline for ID: {analysis_id}")
            
            # Stage 1: Text preprocessing and statistics
            logger.info("Stage 1: Text processing and statistics")
            cleaned_text = self.text_processor.clean_text(text)
            text_stats = self._calculate_text_statistics(text, cleaned_text)
            result.textStatistics = text_stats
            
            # Stage 2: Keyness analysis
            logger.info("Stage 2: Keyness analysis")
            keyness_start = time.time()
            keyness_data = self.keyness_analyzer.calculate_keyness(cleaned_text)
            keyness_time = (time.time() - keyness_start) * 1000
            
            # Enhanced keyness results
            enhanced_keywords = []
            for i, keyword in enumerate(keyness_data):
                enhanced_keywords.append(KeywordItem(
                    word=keyword['word'],
                    score=keyword['score'],
                    frequency=keyword['frequency'],
                    rank=i + 1,
                    effect_size=keyword.get('effect_size', keyword['score']),
                    confidence=keyword.get('confidence', 0.9)
                ))
            
            result.keyness = KeynessResult(
                keywords=enhanced_keywords,
                total_keywords=len(enhanced_keywords),
                processing_time_ms=keyness_time,
                reference_corpus="general_english"
            )
            
            # Stage 3: Semantic clustering
            logger.info("Stage 3: Semantic clustering")
            clustering_start = time.time()
            clusters_data = self.semantic_clusterer.create_clusters(cleaned_text)
            clustering_time = (time.time() - clustering_start) * 1000
            
            # Enhanced clustering results
            enhanced_clusters = []
            for cluster in clusters_data:
                # Generate coordinates for visualization (simple circular layout)
                coordinates = self._generate_word_coordinates(
                    cluster['words'], cluster['id']
                )
                
                enhanced_cluster = SemanticCluster(
                    id=cluster['id'],
                    label=cluster['label'],
                    words=cluster['words'],
                    size=cluster['size'],
                    centroid=cluster.get('centroid'),
                    coherence_score=cluster.get('coherence_score', 0.8),
                    word_coordinates=coordinates
                )
                enhanced_clusters.append(enhanced_cluster)
            
            result.semanticClustering = SemanticClusteringResult(
                clusters=enhanced_clusters,
                total_clusters=len(enhanced_clusters),
                processing_time_ms=clustering_time,
                algorithm="kmeans_embedding",
                similarity_threshold=0.7
            )
            
            # For backward compatibility
            result.semanticClusters = enhanced_clusters
            
            # Stage 4: Sentiment analysis
            logger.info("Stage 4: Sentiment analysis")
            sentiment_start = time.time()
            sentiment_data = self.sentiment_analyzer.analyze_sentiment(cleaned_text)
            sentiment_time = (time.time() - sentiment_start) * 1000
            
            # Enhanced sentiment results
            result.sentiment = SentimentResult(
                overall=sentiment_data['overall'],
                positive=sentiment_data['positive'],
                negative=sentiment_data['negative'],
                neutral=sentiment_data['neutral'],
                compound=sentiment_data.get('compound', sentiment_data['overall']),
                confidence=sentiment_data.get('confidence', 0.85),
                sentence_sentiments=sentiment_data.get('sentence_sentiments', [])
            )
            
            # Stage 5: AI insights (optional)
            logger.info("Stage 5: AI insights generation")
            ai_insights = None
            try:
                if self.ollama_service.client:
                    insights = self.ollama_service.analyze_themes(
                        cleaned_text, 
                        clusters_data
                    )
                    if insights:
                        ai_insights = insights
                        logger.info("AI insights generated successfully")
                else:
                    logger.info("Ollama service not available, skipping AI insights")
            except Exception as e:
                logger.warning(f"AI insights generation failed: {e}")
            
            result.aiInsights = ai_insights
            
            # Finalize result
            end_time = time.time()
            total_time = end_time - start_time
            
            # Build model versions dict without None values
            model_versions = {
                "spacy": getattr(self.text_processor.nlp, 'meta', {}).get('version', 'unknown')
            }
            if ai_insights:
                model_versions["ollama"] = self.ollama_service.model
            
            result.metadata = ProcessingMetadata(
                start_time=start_timestamp,
                end_time=datetime.now().isoformat(),
                processing_time_seconds=total_time,
                file_size_bytes=len(text.encode('utf-8')),
                model_versions=model_versions,
                parameters=parameters or {}
            )
            
            result.status = AnalysisStatus.COMPLETED
            
            logger.info(f"Analysis pipeline completed for ID: {analysis_id} in {total_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis pipeline failed for ID: {analysis_id}: {e}")
            
            # Return failed result
            result.status = AnalysisStatus.FAILED
            result.error_message = str(e)
            result.metadata = ProcessingMetadata(
                start_time=start_timestamp,
                end_time=datetime.now().isoformat(),
                processing_time_seconds=time.time() - start_time,
                parameters=parameters or {}
            )
            
            return result
    
    def _calculate_text_statistics(self, original_text: str, cleaned_text: str) -> TextStatistics:
        """Calculate comprehensive text statistics"""
        
        # Basic counts
        char_count = len(original_text)
        words = cleaned_text.split()
        word_count = len(words)
        
        # Sentence and paragraph counts
        sentences = [s.strip() for s in original_text.split('.') if s.strip()]
        sentence_count = len(sentences)
        
        paragraphs = [p.strip() for p in original_text.split('\n\n') if p.strip()]
        paragraph_count = max(len(paragraphs), 1)
        
        # Advanced metrics
        unique_words = len(set(word.lower() for word in words))
        avg_sentence_length = word_count / max(sentence_count, 1)
        avg_word_length = sum(len(word) for word in words) / max(word_count, 1)
        vocabulary_richness = unique_words / max(word_count, 1)
        
        # Improved Flesch Reading Ease score calculation
        if sentence_count > 0 and word_count > 0:
            # Better syllable estimation
            def count_syllables(word):
                word = word.lower()
                if word.endswith('e'):
                    word = word[:-1]
                vowels = 'aeiouy'
                syllables = 0
                previous_char_was_vowel = False
                for char in word:
                    if char in vowels:
                        if not previous_char_was_vowel:
                            syllables += 1
                        previous_char_was_vowel = True
                    else:
                        previous_char_was_vowel = False
                return max(1, syllables)
            
            # Calculate average syllables per word more accurately
            total_syllables = sum(count_syllables(word) for word in words)
            avg_syllables_per_word = total_syllables / word_count
            
            # Flesch Reading Ease formula
            readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            # Clamp between 0 and 100
            readability_score = max(0, min(100, readability_score))
        else:
            readability_score = 0.0
        
        return TextStatistics(
            character_count=char_count,
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            avg_sentence_length=avg_sentence_length,
            avg_word_length=avg_word_length,
            unique_words=unique_words,
            vocabulary_richness=vocabulary_richness,
            readability_score=readability_score
        )
    
    def _generate_word_coordinates(
        self, 
        words: list, 
        cluster_id: int
    ) -> list[WordCoordinate]:
        """Generate coordinates for word visualization"""
        import math
        
        coordinates = []
        center_x, center_y = 0.0, 0.0
        radius = 1.0
        
        for i, word in enumerate(words[:20]):  # Limit to 20 words for performance
            angle = (i / len(words)) * 2 * math.pi
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            coordinates.append(WordCoordinate(
                word=word,
                x=x,
                y=y,
                cluster_id=cluster_id
            ))
        
        return coordinates