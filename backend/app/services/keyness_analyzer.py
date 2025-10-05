from typing import List, Dict
from collections import Counter
import re

class KeynessAnalyzer:
    def __init__(self):
        # Positive sentiment indicators - words that typically indicate positive aspects
        self.positive_indicators = {
            'positive', 'benefits', 'advantages', 'improve', 'enhance', 'better', 'good', 'great', 
            'excellent', 'effective', 'efficient', 'helpful', 'useful', 'valuable', 'success', 
            'successful', 'opportunity', 'opportunities', 'innovation', 'innovative', 'creativity', 
            'creative', 'empowering', 'accessibility', 'accessible', 'personalized', 'personalised',
            'adaptive', 'inclusive', 'democratisation', 'democratization', 'quality', 'modern', 
            'cutting-edge', 'prepare', 'equipping', 'stronger', 'thrive', 'thriving', 'potential',
            'enable', 'enables', 'enabling', 'breakthrough', 'breakthrough', 'progress', 
            'advancement', 'solve', 'solution', 'solutions', 'optimize', 'optimized'
        }
        
        # Negative sentiment indicators - words that typically indicate problems or concerns
        self.negative_indicators = {
            'negative', 'drawbacks', 'concerns', 'concern', 'problems', 'problem', 'issues', 'issue',
            'risks', 'risk', 'dangers', 'danger', 'bad', 'poor', 'worse', 'worst', 'harmful', 
            'damaging', 'damage', 'exploitation', 'exploit', 'discrimination', 'discriminate',
            'privacy', 'overuse', 'dependent', 'dependency', 'undermine', 'undermining', 'bypass', 
            'exclusion', 'exclude', 'divide', 'inequality', 'inequalities', 'unequal', 'bias', 
            'biased', 'dehumanising', 'dehumanizing', 'replace', 'replacement', 'threat', 'threats',
            'fall', 'behind', 'underprivileged', 'weakening', 'weaken', 'lose', 'losing', 'loss',
            'difficult', 'difficulty', 'struggle', 'struggling', 'fail', 'failing', 'failure',
            'blocked', 'block', 'unintentionally', 'inappropriate', 'misuse', 'abuse'
        }

    def calculate_keyness(self, text: str, reference_freq: Dict[str, float] = None) -> List[Dict]:
        # Clean and tokenize text
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        word_freq = Counter(words)
        total_words = sum(word_freq.values())
        
        if total_words == 0:
            return []
        
        # Skip common stop words, neutral domain words, and short words
        stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 
            'not', 'on', 'with', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 
            'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 
            'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 
            'who', 'get', 'which', 'go', 'me', 'can', 'had', 'has', 'is', 'are', 'was', 
            'were', 'been', 'being', 'than', 'into', 'through', 'during', 'before', 
            'after', 'above', 'below', 'between', 'among', 'such', 'may', 'might', 
            'could', 'should', 'would', 'these', 'those', 'when', 'where', 'why', 'how',
            # Neutral domain-specific words
            'students', 'student', 'education', 'learners', 'learning', 'teachers', 'skills', 'tools',
            'academic', 'systems', 'school', 'schools', 'university', 'universities',
            'classroom', 'classrooms', 'technology', 'technologies', 'platform', 'platforms',
            'system', 'data', 'information', 'content', 'use', 'using', 'used', 'rather',
            'become', 'becomes', 'becoming', 'work', 'working', 'workers', 'time', 'way',
            'ways', 'help', 'helps', 'make', 'makes', 'making', 'take', 'takes', 'taking',
            'knowledge', 'experiences', 'experience', 'behaviour', 'behavior', 'side', 'like',
            'while', 'however', 'down', 'aidriven', 'ai-driven', 'problem-solving', 'problemsolving'
        }
        
        keyness_scores = []
        
        # Process all words and categorize by sentiment
        for word, freq in word_freq.items():
            if freq < 2 or len(word) < 3 or word in stop_words:
                continue
                
            relative_freq = freq / total_words
            
            # Only classify words that are clearly positive or negative
            if word in self.positive_indicators or self._is_positive_context(word, text):
                effect_size = relative_freq * freq * 15  # Positive effect
                sentiment = 'positive'
            elif word in self.negative_indicators or self._is_negative_context(word, text):
                effect_size = -(relative_freq * freq * 15)  # Negative effect
                sentiment = 'negative'
            else:
                continue  # Skip neutral words entirely
            
            keyness_scores.append({
                'word': word,
                'score': abs(effect_size),
                'raw_score': effect_size,
                'effect_size': effect_size,
                'frequency': freq,
                'sentiment': sentiment,
                'confidence': min(0.95, relative_freq * 20)
            })
        
        # Sort by absolute effect size and return top results
        sorted_scores = sorted(keyness_scores, key=lambda x: x['score'], reverse=True)
        
        # Ensure balanced representation
        positive_scores = [s for s in sorted_scores if s['effect_size'] > 0][:12]
        negative_scores = [s for s in sorted_scores if s['effect_size'] < 0][:12]
        
        final_scores = positive_scores + negative_scores
        return sorted(final_scores, key=lambda x: x['score'], reverse=True)[:20]
    
    def _is_positive_context(self, word: str, text: str) -> bool:
        # Check if word appears in positive contexts
        positive_patterns = [
            r'\b' + re.escape(word) + r'\s+(?:helps?|improves?|enhances?|enables?)',
            r'(?:benefits?|advantages?)\s+.*\b' + re.escape(word),
            r'\b' + re.escape(word) + r'\s+(?:opportunities?|solutions?)'
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in positive_patterns)
    
    def _is_negative_context(self, word: str, text: str) -> bool:
        # Check if word appears in negative contexts
        negative_patterns = [
            r'(?:concerns?|risks?|problems?|issues?)\s+.*\b' + re.escape(word),
            r'\b' + re.escape(word) + r'\s+(?:risks?|concerns?|problems?)',
            r'(?:danger|risk)\s+.*\b' + re.escape(word),
            r'\b' + re.escape(word) + r'\s+(?:may|could|might)\s+.*(?:harm|damage|undermine)'
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in negative_patterns)
    
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