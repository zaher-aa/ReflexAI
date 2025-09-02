import re
import nltk
import spacy
from typing import List, Dict, Tuple
from collections import Counter
import logging

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        try:
            # Load spaCy model for advanced NLP
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("SpaCy model loaded successfully")
        except:
            logger.warning("SpaCy model not found, using basic processing")
            self.nlp = None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation for sentence detection
        text = re.sub(r'[^\w\s\.\!\?]', '', text)
        return text.strip()
    
    def tokenize_with_spacy(self, text: str) -> Tuple[List[str], List[Dict]]:
        """Advanced tokenization using spaCy"""
        if not self.nlp:
            return self.basic_tokenize(text), []
        
        doc = self.nlp(text)
        
        # Extract tokens (excluding punctuation and spaces)
        tokens = [token.text.lower() for token in doc 
                 if not token.is_punct and not token.is_space]
        
        # Extract entities and POS tags for enriched analysis
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        
        # Extract lemmatized tokens for better clustering
        lemmas = [token.lemma_.lower() for token in doc 
                 if not token.is_punct and not token.is_space and not token.is_stop]
        
        return lemmas, entities
    
    def basic_tokenize(self, text: str) -> List[str]:
        """Fallback basic tokenization"""
        return word_tokenize(text.lower())
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from token list"""
        return [t for t in tokens if t not in self.stop_words and len(t) > 2]
    
    def get_word_frequencies(self, text: str) -> Dict[str, int]:
        """Get word frequencies using spaCy if available"""
        if self.nlp:
            tokens, _ = self.tokenize_with_spacy(text)
        else:
            tokens = self.basic_tokenize(text)
        
        filtered = self.remove_stopwords(tokens)
        return dict(Counter(filtered))
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences using spaCy or NLTK"""
        if self.nlp:
            doc = self.nlp(text)
            return [sent.text.strip() for sent in doc.sents]
        else:
            return sent_tokenize(text)