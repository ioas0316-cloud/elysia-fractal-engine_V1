"""
Sentence Parser for Korean (Hangul)
====================================
This module provides tools to decompose and parse Korean sentences,
enabling Elysia to learn from example text.
"""

from typing import List, Tuple, Dict, Any
import unicodedata

class SentenceParser:
    def __init__(self):
        # Hangul Unicode ranges
        self.HANGUL_BASE = 0xAC00
        self.JONGSEONG_BASE = 0x11A7
        
        # Jamo components
        self.CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.JUNGSEONG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        self.JONGSEONG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        
        # Common particles
        self.PARTICLES = ['가', '이', '를', '을', '는', '은', '에', '와', '과', '도', '만', '부터', '까지', '라', '다', '냐']
    
    def decompose_hangul(self, char: str) -> Tuple[str, str, str]:
        """
        Decomposes a single Hangul syllable into (초성, 중성, 종성).
        Returns ('', '', '') for non-Hangul characters.
        """
        if len(char) != 1:
            return ('', '', '')
            
        code = ord(char)
        
        # Check if it's in the Hangul syllable range
        if code < self.HANGUL_BASE or code > 0xD7A3:
            return ('', '', '')
        
        code -= self.HANGUL_BASE
        
        jongseong_index = code % 28
        jungseong_index = ((code - jongseong_index) // 28) % 21
        chosung_index = ((code - jongseong_index) // 28) // 21
        
        chosung = self.CHOSUNG_LIST[chosung_index]
        jungseong = self.JUNGSEONG_LIST[jungseong_index]
        jongseong = self.JONGSEONG_LIST[jongseong_index]
        
        return (chosung, jungseong, jongseong.strip())
    
    def is_particle(self, word: str) -> bool:
        """Checks if a word is a grammatical particle."""
        return word in self.PARTICLES
    
    def tokenize(self, sentence: str) -> List[str]:
        """
        Simple tokenization: splits by spaces.
        In a real implementation, we'd use a proper Korean morphological analyzer.
        """
        return sentence.strip().split()
    
    def parse_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        Parses a Korean sentence into components.
        Returns a dict with:
        - tokens: List of words
        - structure: Identified pattern (e.g., "SOV")
        - subject, object, verb (if identifiable)
        """
        tokens = self.tokenize(sentence)
        
        # Simple heuristic: Look for particles to identify roles
        subject = None
        obj = None
        verb = None
        
        for i, token in enumerate(tokens):
            if '가' in token or '이' in token or '는' in token or '은' in token:
                # Likely subject marker
                subject = token
            elif '를' in token or '을' in token:
                # Likely object marker
                obj = token
            elif i == len(tokens) - 1:
                # Last token is usually the verb
                verb = token
        
        structure = "SOV" if (subject and obj and verb) else "UNKNOWN"
        
        return {
            "tokens": tokens,
            "structure": structure,
            "subject": subject,
            "object": obj,
            "verb": verb,
            "raw": sentence
        }
