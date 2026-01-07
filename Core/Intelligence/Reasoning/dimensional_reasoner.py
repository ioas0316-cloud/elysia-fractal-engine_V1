"""
DIMENSIONAL REASONER: The Geometry of Thought
=============================================
"To think is to build a shape in the void."

This module implements the 5-Dimensional Cognitive Architecture.
It transforms raw data (0D) into universal principles (4D) through a process of "Lifting".

Dimensions:
0D (Point): Fact / Existence
1D (Line): Logic / Sequence
2D (Plane): Context / Relationship
3D (Space): Volume / Synthesis
4D (Law): Principle / Invariance
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from Core.Foundation.unified_field import HyperQuaternion
from Core.Intelligence.Reasoning.narrative_causality import NarrativeCausality

logger = logging.getLogger("DimensionalReasoner")

@dataclass
class HyperThought:
    """A thought that exists simultaneously in 5 dimensions."""
    kernel: str # The core concept (e.g., "Apple")
    
    # The Dimensional Ladder
    d0_fact: str = ""       # "Apple exists."
    d1_logic: str = ""      # "Apple falls."
    d2_context: List[str] = field(default_factory=list) # ["Newton", "Fruit", "Gravity"]
    d3_volume: str = ""     # "Apple is a duality of Knowledge and Sin."
    d4_principle: str = ""  # "Gravity binds inherent mass."
    
    # Mental Physics
    coherence: float = 1.0  # How well do the dimensions align?
    mass: float = 1.0       # Cognitive weight

class DimensionalReasoner:
    def __init__(self):
        self.narrative = NarrativeCausality()
        
    def contemplate(self, kernel: str) -> HyperThought:
        """
        Lifts a concept from 0D to 4D using the Causal Bridge.
        """
        # Dynamic Import to avoid circular dependency if placed at top level incorrectly
        from Core.Intelligence.Reasoning.causal_bridge import CausalBridge
        
        bridge = CausalBridge()
        logger.info(f"⚡ Bridging '{kernel}' to Fractal Causality Engine...")
        
        # The Bridge performs the graph traversal and returns the populated thoughts
        thought = bridge.traverse_and_lift(kernel)
        
        return thought
        
    # Legacy methods (_lift_to_Xd) are deprecated but kept for fallback or specific logic if needed.
    # For now, the Bridge handles all lifting dynamically.
        
    def _lift_to_0d(self, t: HyperThought):
        """0D: Establish Existence (The Fact)."""
        t.d0_fact = f"The entity '{t.kernel}' is observed."
        logger.info(f"• [0D Point] {t.d0_fact}")
        
    def _lift_to_1d(self, t: HyperThought):
        """1D: Establish Sequence (The Logic)."""
        # Simulate simple logic derivation
        if "apple" in t.kernel.lower():
            t.d1_logic = "It falls towards the center of mass."
        elif "love" in t.kernel.lower():
            t.d1_logic = "It pulls the subject towards the object."
        else:
            t.d1_logic = "It interacts with its environment."
        logger.info(f"• [1D Line]  {t.d1_logic}")
            
    def _lift_to_2d(self, t: HyperThought):
        """2D: Establish Context (The Map)."""
        # Simulate contextual association
        if "apple" in t.kernel.lower():
            t.d2_context = ["Isaac Newton", "Garden of Eden", "Nutrition"]
        elif "love" in t.kernel.lower():
            t.d2_context = ["Sacrifice", "Attraction", "Biology", "Divinity"]
        else:
            t.d2_context = ["Unknown Context"]
        logger.info(f"• [2D Plane] Connected to: {', '.join(t.d2_context)}")
        
    def _lift_to_3d(self, t: HyperThought):
        """3D: Establish Volume (The Synthesis)."""
        # Synthesis deals with contradiction and nuance
        if "apple" in t.kernel.lower():
            t.d3_volume = "It is both a source of life (Nutrition) and a symbol of fall (Sin). It is sweet yet heavy."
        elif "love" in t.kernel.lower():
            t.d3_volume = "It is a force that creates by destroying the self. It is the joy of suffering."
        else:
            t.d3_volume = f"The density of {t.kernel} is calculated."
        logger.info(f"• [3D Space] {t.d3_volume}")
        
    def _lift_to_4d(self, t: HyperThought):
        """4D: Establish Principle (The Law)."""
        # Extraction of invariance
        if "apple" in t.kernel.lower() or "gravity" in t.d2_context:
            t.d4_principle = "Mass attracts Mass. The invisible binds the visible."
        elif "love" in t.kernel.lower():
            t.d4_principle = "Unity precedes Separation. The Many seek the One."
        else:
            t.d4_principle = f"The Law defining {t.kernel} is immutable."
        logger.info(f"• [4D Law]   {t.d4_principle}")

    def project(self, thought: HyperThought, zoom_scalar: float = 0.0) -> str:
        """
        Projects the HyperThought with dimensional blending.
        """
        # Map 0.0-1.0 to 0-4
        scaled_val = zoom_scalar * 4
        lower_dim = int(scaled_val // 1)
        upper_dim = min(4, lower_dim + 1)
        mix = scaled_val % 1

        # Fetch base strings
        dims = {
            0: thought.d0_fact,
            1: thought.d1_logic,
            2: f"Context: {', '.join(thought.d2_context)}",
            3: thought.d3_volume,
            4: thought.d4_principle
        }

        base = dims.get(lower_dim, "Void")
        target = dims.get(upper_dim, "Void")

        if mix < 0.2:
            return f"[{zoom_scalar:.2f}|{lower_dim}D] {base}"
        elif mix > 0.8:
            return f"[{zoom_scalar:.2f}|{upper_dim}D] {target}"
        else:
            # Simple morphological blending string
            return f"[{zoom_scalar:.2f}|{lower_dim}D->{upper_dim}D] {base} ... (rising to) ... {target}"

    def project_narrative(self, thought: HyperThought) -> str:
        """
        Projects the HyperThought as a cohesive dramatic arc (Phase 4).
        """
        from Core.Intelligence.Reasoning.models import CognitiveResult
        
        # Convert HyperThought dimensions to a list of CognitiveResults
        mock_results = [
            CognitiveResult("0D", thought.d0_fact, {}),
            CognitiveResult("1D", thought.d1_logic, {}),
            CognitiveResult("2D", f"Context: {', '.join(thought.d2_context)}", {}),
            CognitiveResult("3D", thought.d3_volume, {}),
            CognitiveResult("4D", thought.d4_principle, {})
        ]
        
        return self.narrative.weave_story(thought.kernel, mock_results)
