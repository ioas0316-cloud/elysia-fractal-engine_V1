"""
Linguistic Pattern Distiller (The Style Collector)
==================================================

"Meaning is the Soul, but Style is the Body."

This module extracts *Structural Patterns* and *Vocabulary Styles* from raw text.
It bridges the gap between Abstract Quaternions and Natural Language.
"""

import logging
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

logger = logging.getLogger("LanguageLearner")

class LanguageLearner:
    def __init__(self, genome_path: str = "Core/Memory/style_genome.json"):
        self.genome_path = Path(genome_path)
        self.genome = self._load_genome()
        
        # Regex patterns for structure mining
        self.structure_patterns = {
            "Causal": r"(.+) 때문에, (.+)", # A implies B
            "Contrast": r"(.+)지만, (.+)", # A but B
            "Conditional": r"만약 (.+)라면, (.+)", # If A then B
            "Definition": r"(.+)[은는]\s+(.+)이다" # A is B (Robust)
        }
        
    def _load_genome(self):
        if not self.genome_path.exists():
            return {
                "rhetoric": {"vocabulary_bank": {}, "templates": defaultdict(list)},
                "meta": {"evolution_stage": 0}
            }
        try:
            with open(self.genome_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure structure exists
                if "templates" not in data.get("rhetoric", {}):
                    if "rhetoric" not in data: data["rhetoric"] = {}
                    data["rhetoric"]["templates"] = {}
                return data
        except Exception as e:
            logger.warning(f"Failed to load genome: {e}")
            return {"rhetoric": {"vocabulary_bank": {}, "templates": {}}}

    def save_genome(self):
        """Persist learned patterns."""
        try:
            with open(self.genome_path, 'w', encoding='utf-8') as f:
                json.dump(self.genome, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save genome: {e}")

    def learn_from_text(self, text: str, category: str = "General"):
        """
        Distills linguistic patterns from a text block.
        """
        sentences = re.split(r'[.!?]\s*', text)
        
        learned_count = 0
        for sent in sentences:
            sent = sent.strip()
            if not sent: continue
            
            # 1. Mine Structural Templates
            for p_name, p_regex in self.structure_patterns.items():
                match = re.match(p_regex, sent)
                if match:
                    # Convert to template: "Love is pain" -> "{0} is {1}"
                    # This is a simplified crystallization
                    # A real implementation would use POS tagging.
                    # Here we trust the regex structure.
                    template = sent # For now, store the example as a 'soft template'
                    # In a real system, we'd replace the caught groups with slots due to complexity, 
                    # but for now let's just save the 'style' of the sentence.
                    
                    self._add_template(p_name, sent)
                    learned_count += 1
            
            # 2. Mine Stylistic Vocabulary (Simple Heuristic)
            # If the category is specific (e.g. "War", "Love"), grab adjectives/verbs
            if category in ["Emotion", "Logic", "War", "Nature"]:
                words = sent.split()
                # Naive: grab words > 3 chars
                for w in words:
                    if len(w) > 3:
                        self._add_vocab(category, w)
        
        if learned_count > 0:
            logger.info(f"📚 Distilled {learned_count} linguistic patterns from text.")
            self.save_genome()

    def _add_template(self, type_name: str, example: str):
        """Adds a sentence template to the bank."""
        templates = self.genome["rhetoric"]["templates"]
        if type_name not in templates:
            templates[type_name] = []
        
        # Limit distinct templates to avoid bloat
        if example not in templates[type_name]:
            templates[type_name].append(example)
            if len(templates[type_name]) > 50: # Cap
                templates[type_name].pop(0)

    def _add_vocab(self, category: str, word: str):
        """Adds a word to the vocabulary bank."""
        bank = self.genome.get("vocabulary_bank", {})
        
        # Map categories to shapes if needed, or keep distinct
        # Mapping to existing shapes for compatibility
        shape_map = {
            "War": "Sharp",
            "Logic": "Block",
            "Nature": "Round",
            "Emotion": "Round",
            "System": "Block"
        }
        
        shape = shape_map.get(category, "Balance")
        
        if shape not in bank:
            bank[shape] = []
            
        if word not in bank[shape]:
            bank[shape].append(word)
            if len(bank[shape]) > 100:
                bank[shape].pop(0)
        
        self.genome["vocabulary_bank"] = bank # update link

if __name__ == "__main__":
    # Test
    learner = LanguageLearner()
    learner.learn_from_text("그는 마치 폭풍처럼 몰아쳤다.", "War")
    learner.learn_from_text("사랑은 벚꽃처럼 지는 것이다.", "Nature")
    print("Learned!")
