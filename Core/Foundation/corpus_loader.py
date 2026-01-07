"""
Corpus Loader
=============
Loads example sentences from a corpus file and bootstraps Elysia's language learning.
"""

from typing import List, Set
import os

from high_engine.sentence_parser import SentenceParser
from high_engine.pattern_extractor import PatternExtractor
from high_engine.language_cortex import LanguageCortex
from hangul_physics import Tensor3D

class CorpusLoader:
    def __init__(self):
        self.parser = SentenceParser()
        self.extractor = PatternExtractor()
    
    def load_corpus(self, file_path: str) -> List[str]:
        """Loads sentences from a text file (one sentence per line)."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Corpus file not found: {file_path}")
        
        sentences = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    sentences.append(line)
        
        return sentences
    
    def bootstrap_from_corpus(
        self, 
        corpus: List[str], 
        cortex: LanguageCortex
    ) -> dict:
        """
        Learns from a corpus of example sentences.
        
        Returns a summary dict with:
        - sentences_processed: int
        - words_learned: int
        - patterns_extracted: int
        """
        sentences_processed = 0
        words_learned_set: Set[str] = set()
        
        for sentence in corpus:
            # Parse the sentence
            parsed = self.parser.parse_sentence(sentence)
            
            # Extract grammar pattern
            grammar_pattern = self.extractor.extract_grammar_pattern(parsed)
            
            # Extract words and ground them
            for token in parsed["tokens"]:
                # Remove particles to get base word
                base_word = self._extract_base(token)
                
                if base_word and base_word not in cortex.vocabulary:
                    # Create a simple tensor for this word
                    # In a real system, this would come from semantic analysis
                    tensor = self._word_to_tensor(base_word)
                    cortex.ground_concept(base_word, tensor)
                    words_learned_set.add(base_word)
            
            sentences_processed += 1
        
        return {
            "sentences_processed": sentences_processed,
            "words_learned": len(words_learned_set),
            "patterns_extracted": len(self.extractor.grammar_patterns),
            "top_patterns": self.extractor.get_top_patterns(5)
        }
    
    def _extract_base(self, word_with_particle: str) -> str:
        """Removes particles from word."""
        particles = ['가', '이', '를', '을', '는', '은', '에', '와', '과', '도', '만', '다', '라']
        for p in particles:
            if word_with_particle.endswith(p):
                return word_with_particle[:-len(p)]
        return word_with_particle
    
    def _word_to_tensor(self, word: str) -> Tensor3D:
        """
        Creates a simple tensor representation of a word.
        This is a placeholder; in a real system, this would use semantic embeddings.
        For now, we use a hash-based approach for consistency.
        """
        # Simple hash to create pseudo-random but consistent tensors
        h = hash(word)
        x = (h % 100) / 10.0 - 5.0  # Range: -5 to 5
        y = ((h // 100) % 100) / 10.0 - 5.0
        z = ((h // 10000) % 100) / 10.0 - 5.0
        
        return Tensor3D(x=x, y=y, z=z)
