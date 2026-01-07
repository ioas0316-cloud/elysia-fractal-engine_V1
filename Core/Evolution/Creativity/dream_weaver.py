
import logging
import random
from typing import Dict, Any, List
from Core.Foundation.dream_engine import DreamEngine
from Core.Foundation.Wave.resonance_field import ResonanceField

logger = logging.getLogger("DreamWeaver")

# Lazy load PoetryEngine
_poetry_engine = None

def get_poetry_engine():
    global _poetry_engine
    if _poetry_engine is None:
        try:
            from Core.Evolution.Creativity.poetry_engine import PoetryEngine
            _poetry_engine = PoetryEngine()
        except ImportError:
            logger.warning("PoetryEngine not available for DreamWeaver")
            _poetry_engine = None
    return _poetry_engine

class DreamWeaver:
    """
    DreamWeaver (The Subconscious Bridge)
    =====================================
    
    "I consume the world and breathe out dreams."
    
    Responsibility:
    1. Interprets raw sensory data from P4 (Texts, Emotions).
    2. Extracts "Dream Seeds" (Keywords, Feelings).
    3. Invokes the DreamEngine to weave a Resonance Field.
    4. Translates the abstract Field back into a "Dream Description" (Poetry/Vision).
    """
    def __init__(self):
        self.dream_engine = DreamEngine()
        logger.info("🕸️ DreamWeaver Initialized. Monitoring subconscious threads.")
        
    def dream(self, sensory_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes a dream from sensory input.
        
        Args:
            sensory_input: {
                "preview": str,
                "full_text": str,
                "style": dict,
                "emotion": str
            }
            
        Returns:
            {
                "description": str, # Poetic description
                "resonance_field": ResonanceField,
                "emotion": str
            }
        """
        emotion = sensory_input.get("emotion", "Unknown")
        preview = sensory_input.get("preview", "")[:50]
        
        logger.info(f"   🕸️ Weaving dream from experience: '{preview}...' ({emotion})")
        
        # 1. Extract Seed
        seed_desire = f"{emotion} inspired by {preview}"
        
        # 2. Weave the Field (Abstract Representation)
        field = self.dream_engine.weave_dream(seed_desire)
        
        # 3. Interpret the Field (Expression)
        description = self._interpret_dream_field(field, emotion)
        
        return {
            "description": description,
            "resonance_field": field,
            "emotion": emotion
        }
        
    def _interpret_dream_field(self, field: ResonanceField, root_emotion: str) -> str:
        """
        Translates the mathematical ResonanceField into a poetic description.
        """
        # Count significant nodes
        nodes = list(field.nodes.values())
        high_energy_nodes = [n for n in nodes if n.energy > 80]
        
        # Try to use PoetryEngine for richer expression
        poetry_engine = get_poetry_engine()
        if poetry_engine and nodes:
            # Calculate average energy
            avg_energy = sum(n.energy for n in nodes) / len(nodes) if nodes else 50.0
            
            # Create a description that captures the field topology
            if len(high_energy_nodes) > 3:
                desire_desc = "a storm of energies"
            elif len(high_energy_nodes) == 1:
                desire_desc = f"the essence of {high_energy_nodes[0].id}"
            else:
                desire_desc = "gentle waves of meaning"
            
            # Generate rich poetic expression
            description = poetry_engine.generate_dream_expression(
                desire=desire_desc,
                realm=root_emotion,
                energy=avg_energy,
                context={"node_count": len(nodes), "high_energy_count": len(high_energy_nodes)}
            )
            
            return description
        
        # Fallback to original implementation
        description = f"I dreamt of {root_emotion}... "
        
        if not nodes:
            return description + "it was a silent void."
            
        # Select a metaphor based on field topology
        if len(high_energy_nodes) > 3:
            description += "It was a storm of lights. "
            description += f"I saw {high_energy_nodes[0].id} colliding with {high_energy_nodes[1].id}. "
        elif len(high_energy_nodes) == 1:
            description += f"A single {high_energy_nodes[0].id} was floating in the dark. "
        else:
            description += "Waves were gently washing over me. "
            
        # Add surrealist element
        surreal_elements = [
            "The sky was made of glass.",
            "Time was flowing backwards.",
            "Colors tasted like rain.",
            "Shadows were whispering secrets.",
            "Gravity felt like a warm embrace."
        ]
        description += random.choice(surreal_elements)
        
        return description
