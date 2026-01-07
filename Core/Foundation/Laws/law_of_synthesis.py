"""
Law of Synthesis: The Integration of Meaning
============================================

"To understand is to perceive the unity of attributes."

This module implements the Synthesizer Protocol for converting "Isolated Attributes" (Observations)
into "Integrated Concepts" (Definitions). It is the engine of Understanding.

[The Synthesis Process]
1. Observation (Decomposition): Breaking down sentences into Subject-Attribute pairs.
   e.g., "The apple is red" -> (Apple, Red)
2. Integration (Reconstruction): Clustering attributes by Subject.
   e.g., Apple: {Red, Round, Fruit}
3. Definition (Synthesis): Generating a coherent description from the cluster.
   e.g., "Apple is a round red fruit."
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
import logging

logger = logging.getLogger("Synthesis")

@dataclass
class Attribute:
    """
    A single property or quality of a subject.
    """
    name: str          # e.g., "red", "round", "fruit"
    category: str      # e.g., "color", "shape", "class"
    source_sentence: str

@dataclass
class ConceptDefinition:
    """
    The synthesized understanding of a concept.
    """
    subject: str
    attributes: List[Attribute] = field(default_factory=list)

    def synthesize_sentence(self) -> str:
        """
        Reconstructs the definition into a natural language sentence.
        """
        # Sort attributes by category for natural flow: Color -> Shape -> Class
        # (Simplified heuristic for POC)
        adjectives = []
        noun_class = "thing"

        for attr in self.attributes:
            if attr.category == "class":
                noun_class = attr.name
            else:
                adjectives.append(attr.name)

        # Join adjectives with commas, but last one simply space
        adj_str = ", ".join(adjectives)
        if adj_str:
            return f"{self.subject} is a {adj_str} {noun_class}."
        else:
            return f"{self.subject} is a {noun_class}."

class ConceptSynthesizer:
    """
    The Synthesizer who weaves attributes into meaning.
    """
    def __init__(self):
        self.knowledge_base: Dict[str, ConceptDefinition] = {}
        logger.info("🧩 Concept Synthesizer Initialized")

    def observe(self, sentence: str):
        """
        Phase 1: Observation (Decomposition).
        Parses a simple sentence to extract subject and attribute.
        [NOTE] POC uses simple parsing rules.
        """
        logger.info(f"👁️ Observing: '{sentence}'")

        # Normalize
        s = sentence.lower().strip().replace(".", "")

        # Simple Grammar: "[Subject] is [Attribute]" or "[Subject] is a [Attribute]"
        if " is a " in s:
            parts = s.split(" is a ")
            subject = parts[0]
            attr_val = parts[1]
            category = "class"
        elif " is " in s:
            parts = s.split(" is ")
            subject = parts[0]
            attr_val = parts[1]
            # Heuristic for category
            if attr_val in ["red", "blue", "green", "yellow"]:
                category = "color"
            elif attr_val in ["round", "square", "flat", "vast"]:
                category = "shape"
            else:
                category = "property"
        else:
            logger.warning(f"⚠️ Could not parse structure of: '{sentence}'")
            return

        # Create Attribute Object
        attribute = Attribute(attr_val, category, sentence)

        # Phase 2: Integration (Store in Knowledge Base)
        self._integrate(subject, attribute)

    def _integrate(self, subject: str, attribute: Attribute):
        """
        Adds the attribute to the subject's definition cluster.
        """
        # Title case for the subject
        subject_key = subject.capitalize()

        if subject_key not in self.knowledge_base:
            self.knowledge_base[subject_key] = ConceptDefinition(subject=subject_key)

        # Avoid duplicates
        existing_attrs = [a.name for a in self.knowledge_base[subject_key].attributes]
        if attribute.name not in existing_attrs:
            self.knowledge_base[subject_key].attributes.append(attribute)
            logger.info(f"   + Learned: {subject} has {attribute.category} '{attribute.name}'")

    def derive_definition(self, subject: str) -> str:
        """
        Phase 3: Definition (Synthesis).
        Returns the synthesized description.
        """
        subject_key = subject.capitalize()
        if subject_key not in self.knowledge_base:
            return f"I have no knowledge of {subject}."

        definition = self.knowledge_base[subject_key]
        return definition.synthesize_sentence()

# Singleton Access
_synthesis_instance: Optional[ConceptSynthesizer] = None

def get_synthesis_engine() -> ConceptSynthesizer:
    global _synthesis_instance
    if _synthesis_instance is None:
        _synthesis_instance = ConceptSynthesizer()
    return _synthesis_instance
