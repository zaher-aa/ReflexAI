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
            
            # Log-likelihood calculation
            score = 2 * freq * math.log(relative_freq / ref_freq) if ref_freq > 0 else 0
            
            keyness_scores.append({
                'word': word,
                'score': abs(score),
                'frequency': freq
            })
        
        return sorted(keyness_scores, key=lambda x: x['score'], reverse=True)[:30]
    
    def _get_default_frequencies(self) -> Dict[str, float]:
        # Simplified default frequencies
        return {
            'the': 0.07, 'be': 0.04, 'to': 0.04, 'of': 0.03,
            'and': 0.03, 'a': 0.03, 'in': 0.02, 'that': 0.01,
            'have': 0.01, 'i': 0.01, 'it': 0.01, 'for': 0.01
        }