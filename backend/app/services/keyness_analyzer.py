import numpy as np
from typing import List, Dict
from collections import Counter
import math

class KeynessAnalyzer:
    def calculate_keyness(self, text: str, reference_freq: Dict[str, float] = None) -> List[Dict]:
        words = text.lower().split()
        word_freq = Counter(words)
        total_words = sum(word_freq.values())
        
        if reference_freq is None:
            reference_freq = self._get_default_frequencies()
        
        keyness_scores = []
        
        for word, freq in word_freq.most_common(50):
            relative_freq = freq / total_words
            ref_freq = reference_freq.get(word, 0.0001)
            
            # Log-likelihood calculation (preserving sign for positive/negative keyness)
            if ref_freq > 0:
                score = 2 * freq * math.log(relative_freq / ref_freq)
            else:
                score = 0
            
            # Effect size calculation (standardized difference)
            effect_size = score / math.sqrt(freq) if freq > 0 else 0
            
            keyness_scores.append({
                'word': word,
                'score': abs(score),  # Keep abs for ranking
                'raw_score': score,   # Keep raw score for effect direction
                'effect_size': effect_size,
                'frequency': freq,
                'confidence': min(0.95, freq / total_words * 10)  # Simple confidence metric
            })
        
        # Sort by absolute score but include both positive and negative
        sorted_scores = sorted(keyness_scores, key=lambda x: x['score'], reverse=True)[:30]
        
        # Add some underused words (negative keyness) if they exist in reference
        underused_words = []
        for word in list(reference_freq.keys())[:20]:
            if word not in word_freq and reference_freq[word] > 0.005:  # Common words not in text
                effect_size = -reference_freq[word] * 10  # Negative effect for missing words
                underused_words.append({
                    'word': word,
                    'score': reference_freq[word] * 100,
                    'raw_score': -reference_freq[word] * 100,
                    'effect_size': effect_size,
                    'frequency': 0,
                    'confidence': 0.7
                })
        
        # Add top underused words to show negative keyness
        if underused_words:
            sorted_scores.extend(sorted(underused_words, key=lambda x: x['score'], reverse=True)[:5])
        
        return sorted_scores
    
    def _get_default_frequencies(self) -> Dict[str, float]:
        # Simplified default frequencies
        return {
            'the': 0.07, 'be': 0.04, 'to': 0.04, 'of': 0.03,
            'and': 0.03, 'a': 0.03, 'in': 0.02, 'that': 0.01,
            'have': 0.01, 'i': 0.01, 'it': 0.01, 'for': 0.01
        }