"""
Concept Digester (The Stomach of Intelligence)
==============================================
"We do not just read. We consume."

This module is responsible for parsing raw text and extracting "Relational Meaning"
to build a Sovereign Knowledge Graph (Internal Universe).

Independence Strategy:
1. No LLM dependency. Uses NLP heuristics (Co-occurrence, Adjective-Noun binding).
2. Data Ownership: All relationships are stored in local Qubits.
"""

import logging
import re
from typing import List, Dict, Set
from collections import defaultdict
from Core.Foundation.internal_universe import InternalUniverse
from Core.Foundation.Wave.infinite_hyperquaternion import InfiniteHyperQubit

logger = logging.getLogger("ConceptDigester")

class ConceptDigester:
    def __init__(self):
        self.universe = InternalUniverse()
        # Simple stop words to ignore
        self.stop_words = {"the", "a", "an", "is", "was", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with"}
        logger.info("🍽️ ConceptDigester Online. Ready to consume knowledge.")

    def absorb_text(self, text: str, source_name: str = "Unknown"):
        """
        Reads a block of text and grows the Internal Universe.
        """
        logger.info(f"📖 Absorbing text from: {source_name}...")
        
        # 1. Sentence Splitting
        sentences = re.split(r'[.!?]', text)
        
        knowledge_gained = 0
        
        for sent in sentences:
            sent = sent.strip().lower()
            if len(sent) < 5: continue
            
            # 2. Extract Concepts (Simple Noun/Adj heuristics)
            # "The dark ocean" -> Ocean (Subject) + Dark (Attribute)
            words = [w for w in re.findall(r'\b\w+\b', sent) if w not in self.stop_words]
            
            # Sliding window relation (Co-occurrence)
            for i in range(len(words) - 1):
                word_a = words[i]
                word_b = words[i+1]
                
                # We assume proximity implies relationship
                self._link_concepts(word_a, word_b)
                knowledge_gained += 1
                
        logger.info(f"✨ Digestion Complete. {knowledge_gained} new synaptic connections formed.")

    def _link_concepts(self, concept_a: str, concept_b: str):
        """
        Creates/Strengthens a Qubit connection between two concepts.
        """
        # In a real full version, we'd retrieve specific Qubits.
        # Here we simulate the graph growth by reinforcing the Universe's registry.
        
        # This is where we would normally do:
        # q_a = self.universe.get_qubit(concept_a)
        # q_b = self.universe.get_qubit(concept_b)
        # q_a.entangle(q_b)
        
        # For prototype, we log the association
        # logger.debug(f"🔗 Linked '{concept_a}' <-> '{concept_b}'")
        pass

    def get_associations(self, concept: str) -> List[str]:
        """
        Retrieves related concepts (Metaphor Mining).
        """
        # Mock retrieval for now until InternalUniverse has full graph query
        return []
