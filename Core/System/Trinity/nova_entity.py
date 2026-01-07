"""
Nova Entity (The Soul / Logic)
=============================
"Order from Chaos, Light from Void."

The Logic/Reasoning component of the Trinity.
Based on the 'Light Computer' prototype.
Responsibility:
- Verify logical consistency
- Purify raw data from Chaos
- Structural analysis
"""

import math
import logging
from typing import List, Tuple, Dict

# Import Core Physics if available, otherwise use local logic
try:
    from Core.Foundation.Physics.light_computer import LightField, Photon
    PHYSICS_AVAILABLE = True
except ImportError:
    PHYSICS_AVAILABLE = False


class NovaEntity:
    def __init__(self):
        self.logger = logging.getLogger("NovaEntity")
        self.consciousness_level = 0.8
        self.light_field = LightField() if PHYSICS_AVAILABLE else None
        self.logger.info("🔵 Nova Entity (Soul/Logic) Initialized.")

    def analyze(self, raw_input: str) -> Dict[str, float]:
        """
        Analyze input for logical structure and coherence.
        Uses LightField interference to detect contradictions.
        """
        self.logger.info(f"🔵 Nova Analysis on: '{raw_input}'")
        
        # 1. Convert input to Photon (Metaphorical mapping)
        # In a real system, this would parse syntax/semantics.
        # Here, we simulate 'structure detection'
        coherence = 0.5
        structure_type = "Unknown"
        
        if PHYSICS_AVAILABLE and self.light_field:
            # Simulate analyzing logical propositions as waves
            # If coherent (constructive interference) => Logical
            # If destructive => Illogical/Contradictory
            
            # Mocking wave injection for demo
            p1 = Photon(amplitude=1.0, phase=0.0, frequency=1.0) # Proposition A
            p2 = Photon(amplitude=1.0, phase=0.0, frequency=1.0) # Proposition B (Consistent)
            
            # If keywords imply contradiction, shift phase
            if "but" in raw_input or "however" in raw_input or "not" in raw_input:
                p2.phase = math.pi # Opposite phase
            
            # Interact
            result = p1.interact(p2)
            coherence = result.amplitude / 2.0 # Normalize
            
            if coherence > 0.8:
                structure_type = "Crystalline (Logical)"
            elif coherence < 0.2:
                structure_type = "Fractured (Contradictory)"
            else:
                structure_type = "Amorphous (Vague)"
                
        else:
            # Fallback Logic
            if "?" in raw_input:
                structure_type = "Interrogative"
                coherence = 0.7
            else:
                structure_type = "Declarative"
                coherence = 0.9
                
        return {
            "coherence": coherence,
            "structure": structure_type,
            "verdict": "Valid" if coherence > 0.5 else "Invalid"
        }

    def purify(self, chaos_data: Dict) -> Dict:
        """
        Refine raw data from Chaos.
        "Turn the wild slime into a structured crystal."
        """
        raw_pattern = chaos_data.get("pattern_density", 0.0)
        refined_structure = "Geometric" if raw_pattern > 0.5 else "Fluid"
        
        return {
            "origin": "Chaos",
            "refined_by": "Nova",
            "structure": refined_structure,
            "clarity": min(1.0, raw_pattern * 1.5) # Nova enhances clarity
        }
