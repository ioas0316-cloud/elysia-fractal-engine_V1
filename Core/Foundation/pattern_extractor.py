"""
Pattern Extractor
=================
Extracts grammatical and semantic patterns from parsed sentences.
"""

from typing import List, Dict, Any, Set
from dataclasses import dataclass

@dataclass
class GrammarPattern:
    template: str  # e.g., "X가 Y를 Z다"
    roles: List[str]  # ["subject", "object", "verb"]
    frequency: int  # How many times this pattern was seen

@dataclass
class SemanticPattern:
    relation: str  # e.g., "causes", "is_a"
    source_concept: str
    target_concept: str
    strength: float

class PatternExtractor:
    def __init__(self):
        self.grammar_patterns: Dict[str, GrammarPattern] = {}
        self.semantic_patterns: List[SemanticPattern] = []
    
    def extract_grammar_pattern(self, parsed_sentence: Dict[str, Any]) -> str:
        """
        Extracts a grammar template from a parsed sentence.
        Example: "나는 사과를 먹는다" -> "X는 Y를 Z다"
        """
        structure = parsed_sentence.get("structure", "UNKNOWN")
        
        if structure == "SOV":
            # Create a template with placeholders
            template = "X가 Y를 Z다"  # Simplified
            
            # Update pattern frequency
            if template not in self.grammar_patterns:
                self.grammar_patterns[template] = GrammarPattern(
                    template=template,
                    roles=["subject", "object", "verb"],
                    frequency=1
                )
            else:
                self.grammar_patterns[template].frequency += 1
            
            return template
        
        return "UNKNOWN"
    
    def extract_semantic_pattern(self, parsed_sentence: Dict[str, Any], concepts: Set[str]) -> List[SemanticPattern]:
        """
        Identifies semantic relationships between concepts in the sentence.
        This is a simplified version; a real implementation would use deeper NLP.
        """
        patterns = []
        
        # Simple heuristic: If sentence is "X는 Y이다", then X is_a Y
        tokens = parsed_sentence.get("tokens", [])
        verb = parsed_sentence.get("verb", "")
        
        if "이다" in verb or "다" in verb:
            # Potential "is_a" relationship
            subject = parsed_sentence.get("subject")
            obj = parsed_sentence.get("object")
            
            if subject and obj:
                # Extract base words (remove particles)
                subj_word = self._extract_base_word(subject)
                obj_word = self._extract_base_word(obj)
                
                if subj_word in concepts and obj_word in concepts:
                    pattern = SemanticPattern(
                        relation="is_a",
                        source_concept=subj_word,
                        target_concept=obj_word,
                        strength=0.8
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _extract_base_word(self, word_with_particle: str) -> str:
        """
        Removes common particles from the end of a word.
        Example: "사과를" -> "사과"
        """
        particles = ['가', '이', '를', '을', '는', '은', '에', '와', '과']
        for p in particles:
            if word_with_particle.endswith(p):
                return word_with_particle[:-len(p)]
        return word_with_particle
    
    def get_top_patterns(self, n: int = 10) -> List[GrammarPattern]:
        """Returns the most frequent grammar patterns."""
        sorted_patterns = sorted(
            self.grammar_patterns.values(),
            key=lambda p: p.frequency,
            reverse=True
        )
        return sorted_patterns[:n]
