"""
Field Reasoner
==============
Non-linear reasoning engine using the Concept Field.
Enables resonance-based retrieval, metaphor generation, and emergent understanding.
"""

from typing import List, Dict, Tuple
from Project_Elysia.mechanics.concept_field import ConceptField

class FieldReasoner:
    """
    Reasons about concepts using field dynamics instead of graph paths.
    """
    
    def __init__(self, field: ConceptField):
        self.field = field
    
    def explore_concept(self, concept: str) -> Dict[str, any]:
        """
        Explores a concept by activating it in the field and observing resonance.
        Returns rich, multi-dimensional understanding.
        """
        # Reset field
        self.field.reset()
        
        # Activate the concept
        self.field.activate(concept, intensity=1.0)
        
        # Get resonant concepts
        activated = self.field.get_activated_concepts(threshold=0.1)
        resonant = self.field.find_resonant_concepts(concept, top_k=5)
        shape_analogs = self.field.find_shape_analogs(concept, top_k=3)
        
        return {
            "source": concept,
            "activated_concepts": activated,
            "resonant_concepts": resonant,
            "shape_analogs": shape_analogs
        }
    
    def generate_metaphor(self, concept: str) -> str:
        """
        Generates a metaphor by finding shape-similar concepts.
        Example: "사랑 is like 빛" (based on tensor similarity)
        """
        shape_analogs = self.field.find_shape_analogs(concept, top_k=1)
        
        if not shape_analogs:
            return f"{concept}은 독특하다"
        
        analog, similarity = shape_analogs[0]
        
        if similarity > 0.7:
            return f"{concept}은 {analog}과 같다"
        elif similarity > 0.5:
            return f"{concept}은 {analog}을 닮았다"
        else:
            return f"{concept}은 {analog}과 연결되어 있다"
    
    def synthesize_understanding(self, concept: str) -> str:
        """
        Creates a rich, poetic understanding by combining:
        - Resonant concepts (what it connects to)
        - Shape analogs (what it's like)
        - Activated field (the overall pattern)
        """
        exploration = self.explore_concept(concept)
        
        # Build composite response
        parts = []
        
        # Metaphor (shape)
        metaphor = self.generate_metaphor(concept)
        parts.append(metaphor)
        
        # Resonances (connections)
        if exploration["resonant_concepts"]:
            resonant_names = [name for name, _ in exploration["resonant_concepts"][:3]]
            if resonant_names:
                parts.append(f"{concept}은 {', '.join(resonant_names)}과 공명한다")
        
        # Activated field (what emerges)
        if len(exploration["activated_concepts"]) > 2:
            activated_names = [name for name, _ in exploration["activated_concepts"][1:4]]  # Skip source
            if activated_names:
                parts.append(f"이것은 {', '.join(activated_names)}을 일깨운다")
        
        return ". ".join(parts) if parts else f"{concept}은 존재한다"
