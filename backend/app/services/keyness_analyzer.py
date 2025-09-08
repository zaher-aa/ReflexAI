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
        
        # Calculate keyness for words present in the text
        for word, freq in word_freq.most_common(100):
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
        
        # Add underused/missing words (negative keyness) from reference corpus
        underused_words = []
        for word, ref_freq in reference_freq.items():
            if ref_freq > 0.005:  # Only consider reasonably common words
                text_freq = word_freq.get(word, 0)
                text_rel_freq = text_freq / total_words if total_words > 0 else 0
                
                # Calculate expected vs actual frequency
                if text_rel_freq < ref_freq * 0.5:  # Word is significantly underused
                    # Use log-likelihood for underused words
                    if text_freq > 0:
                        score = 2 * text_freq * math.log(text_rel_freq / ref_freq)
                    else:
                        # For completely missing words, use negative score based on reference frequency
                        score = -ref_freq * total_words * 2
                    
                    effect_size = score / math.sqrt(max(text_freq, 1))
                    
                    underused_words.append({
                        'word': word,
                        'score': abs(score),
                        'raw_score': score,
                        'effect_size': effect_size,
                        'frequency': text_freq,
                        'confidence': 0.8 if text_freq == 0 else 0.9
                    })
        
        # Combine positive and negative keyness
        all_keyness = keyness_scores + underused_words
        
        # Sort by absolute score and take top results
        sorted_scores = sorted(all_keyness, key=lambda x: x['score'], reverse=True)[:40]
        
        # Ensure we have a mix of positive and negative if available
        positive_scores = [s for s in sorted_scores if s['raw_score'] > 0][:20]
        negative_scores = [s for s in sorted_scores if s['raw_score'] < 0][:10]
        
        final_scores = positive_scores + negative_scores
        return sorted(final_scores, key=lambda x: x['score'], reverse=True)[:30]
    
    def _get_default_frequencies(self) -> Dict[str, float]:
        # Enhanced default frequencies based on common English corpus
        return {
            'the': 0.07, 'be': 0.04, 'to': 0.04, 'of': 0.03, 'and': 0.03, 
            'a': 0.03, 'in': 0.02, 'that': 0.015, 'have': 0.015, 'i': 0.015, 
            'it': 0.015, 'for': 0.015, 'not': 0.012, 'on': 0.012, 'with': 0.012,
            'as': 0.011, 'you': 0.011, 'do': 0.01, 'at': 0.01, 'this': 0.01,
            'but': 0.009, 'his': 0.009, 'by': 0.009, 'from': 0.008, 'they': 0.008,
            'we': 0.008, 'say': 0.008, 'her': 0.008, 'she': 0.008, 'or': 0.008,
            'an': 0.007, 'will': 0.007, 'my': 0.007, 'one': 0.007, 'all': 0.007,
            'would': 0.006, 'there': 0.006, 'their': 0.006, 'what': 0.006,
            'so': 0.006, 'up': 0.006, 'out': 0.006, 'if': 0.006, 'about': 0.006,
            'who': 0.005, 'get': 0.005, 'which': 0.005, 'go': 0.005, 'me': 0.005
        }