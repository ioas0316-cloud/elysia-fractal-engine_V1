"""
Style Analyzer
==============
"To sound like a human, one must understand the rhythm of human speech."

This module analyzes text to extract stylistic features:
1. Tone (Formal vs Casual)
2. Emotion (Sentiment)
3. Structure (Sentence length, variance)
4. Vocabulary (Richness, Slang usage)
"""

import re
from typing import Dict, Any, List

class StyleAnalyzer:
    def __init__(self):
        self.slang_lexicon = {
            "lol", "lmao", "haha", "omg", "idk", "tbh", "brb", "thx", "plz",
            "ㅋㅋ", "ㅎㅎ", "ㅠㅠ", "ㅇㅇ", "ㅊㅊ", "ㅈㅅ"
        }
        
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the given text and returns a style fingerprint.
        """
        if not text:
            return self._empty_profile()
            
        stats = self._basic_stats(text)
        slang_score = self._calculate_slang_score(text)
        formality = self._calculate_formality(text, slang_score)
        
        return {
            "tone": {
                "formality": formality, # 1.0 = Very Formal, 0.0 = Very Casual
                "energy": self._calculate_energy(text),
                "warmth": self._calculate_warmth(text)
            },
            "structure": {
                "avg_sentence_length": stats["avg_len"],
                "variance": stats["variance"],
                "punctuation_density": stats["punc_density"]
            },
            "vocabulary": {
                "richness": stats["ttr"], # Type-Token Ratio
                "slang_usage": slang_score
            }
        }
        
    def _basic_stats(self, text: str) -> Dict[str, float]:
        sentences = re.split(r'[.!?\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {"avg_len": 0, "variance": 0, "punc_density": 0, "ttr": 0}
            
        # Length stats
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        
        # Punctuation
        punc_count = len(re.findall(r'[!?,.]', text))
        punc_density = punc_count / (len(text.split()) + 1)
        
        # Vocabulary
        words = text.lower().split()
        unique_words = set(words)
        ttr = len(unique_words) / (len(words) + 1)
        
        return {
            "avg_len": avg_len,
            "variance": variance,
            "punc_density": punc_density,
            "ttr": ttr
        }
        
    def _calculate_slang_score(self, text: str) -> float:
        words = text.lower().split()
        if not words: return 0.0
        
        slang_count = sum(1 for w in words if w in self.slang_lexicon)
        return min(1.0, slang_count / (len(words) * 0.1 + 1)) # Normalize
        
    def _calculate_formality(self, text: str, slang_score: float) -> float:
        # Base starts high
        score = 0.8
        
        # Slang reduces formality heavily
        score -= slang_score * 0.8
        
        # Exclamations reduce formality
        if "!" in text: score -= 0.1
        if "??" in text: score -= 0.1
        
        # Length: Very short sentences often imply casual/chat
        avg_len = len(text.split()) / (len(re.split(r'[.!?]+', text)) + 1)
        if avg_len < 5: score -= 0.1
        
        return max(0.0, min(1.0, score))
        
    def _calculate_energy(self, text: str) -> float:
        # Exclamations increase energy
        exclaims = text.count("!")
        caps = sum(1 for c in text if c.isupper()) / (len(text) + 1)
        
        score = 0.3 # Base
        score += min(0.5, exclaims * 0.1)
        score += min(0.3, caps * 2)
        
        return max(0.0, min(1.0, score))

    def _calculate_warmth(self, text: str) -> float:
        warm_words = {"love", "happy", "thanks", "great", "good", "hope", "feel", "사랑", "감사", "좋아", "행복"}
        words = set(text.lower().split())
        intersection = words.intersection(warm_words)
        
        return min(1.0, len(intersection) * 0.2)

    def _empty_profile(self):
        return {
            "tone": {"formality": 0.5, "energy": 0.5, "warmth": 0.5},
            "structure": {"avg_sentence_length": 0, "variance": 0, "punctuation_density": 0},
            "vocabulary": {"richness": 0, "slang_usage": 0}
        }
