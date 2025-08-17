import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from typing import List, Dict
import re

class SemanticClusterer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.pca = PCA(n_components=10)
    
    def create_clusters(self, text: str, n_clusters: int = 5) -> List[Dict]:
        sentences = self._split_sentences(text)
        
        if len(sentences) < n_clusters:
            n_clusters = max(2, len(sentences) // 2)
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(sentences)
            
            if tfidf_matrix.shape[0] < n_clusters:
                n_clusters = tfidf_matrix.shape[0]
            
            reduced = self.pca.fit_transform(tfidf_matrix.toarray())
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(reduced)
            
            feature_names = self.vectorizer.get_feature_names_out()
            cluster_results = []
            
            for i in range(n_clusters):
                cluster_sentences = [s for j, s in enumerate(sentences) if clusters[j] == i]
                cluster_words = self._extract_keywords(cluster_sentences, feature_names)
                
                cluster_results.append({
                    'id': i,
                    'label': self._generate_label(cluster_words),
                    'words': cluster_words[:10],
                    'size': len(cluster_sentences)
                })
            
            return cluster_results
        
        except Exception as e:
            print(f"Clustering error: {e}")
            return self._fallback_clusters(text)
    
    def _split_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]
    
    def _extract_keywords(self, sentences: List[str], feature_names) -> List[str]:
        text = ' '.join(sentences)
        words = text.lower().split()
        word_counts = {}
        
        for word in words:
            if word in feature_names:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words]
    
    def _generate_label(self, words: List[str]) -> str:
        if not words:
            return "General"
        return f"{words[0].capitalize()} Theme"
    
    def _fallback_clusters(self, text: str) -> List[Dict]:
        words = text.lower().split()
        unique_words = list(set(words))[:30]
        
        return [
            {
                'id': i,
                'label': f'Group {i+1}',
                'words': unique_words[i*6:(i+1)*6],
                'size': len(unique_words[i*6:(i+1)*6])
            }
            for i in range(5)
        ]