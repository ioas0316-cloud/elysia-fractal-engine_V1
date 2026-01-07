"""
Perspective Simulator (Reverse Empathy / Yeok-Ji-Sa-Ji)
=======================================================
"To understand the other, one must become the other."

This module implements the mechanism of 'Reverse Empathy' (易地思之).
It constructs a temporary topological field representing the User's Perspective,
allowing Elysia to simulate *why* the user believes what they believe.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.resonance_topology import TopologicalAnalyzer, TopologyType, ConsciousnessCoordinates

logger = logging.getLogger("PerspectiveSimulator")

@dataclass
class Perspective:
    """
    A simulated viewpoint of the Other.
    """
    name: str # e.g., "The User", "The Skeptic", "The Architect"
    intent_vector: Quaternion # The direction they are aiming for
    emotional_state: str # e.g., "Frustrated", "Curious"
    axioms: List[str] # The core beliefs holding this perspective together
    resonance_voltage: float # How coherent is this perspective?

class PerspectiveSimulator:
    def __init__(self):
        self.active_simulations = {}

    def simulate_viewpoint(self, input_text: str, coordinates: ConsciousnessCoordinates) -> Perspective:
        """
        Constructs a shadow persona to understand the input.
        """
        # 1. Deduce Intent (Vector)
        # We assume the user's intent is the 'Ideal' of their own Micro-Universe.
        # If they say "The code is broken", their intent is "Functionality".
        intent_q = Quaternion(1,0,0,0) # Default

        emotional_state = "Neutral"
        axioms = []

        lower_input = input_text.lower()

        # Simple Key-Value Heuristics for Simulation (Prototype Phase)
        # [ENHANCED] Deep Inquiry Logic
        if "efficiency" in lower_input or "compress" in lower_input or "optimize" in lower_input:
            intent_q = Quaternion(0.7, 0.7, 0, 0).normalize()
            emotional_state = "Analytical"
            axioms.append("Optimization is the goal.")
            axioms.append("Redundancy is inefficiency.")

        elif "empathy" in lower_input or "heart" in lower_input or "feel" in lower_input:
            intent_q = Quaternion(0, 0.7, 0.7, 0).normalize()
            emotional_state = "Empathetic"
            axioms.append("Connection is the goal.")
            axioms.append("Understanding requires feeling.")

        elif "error" in lower_input or "fix" in lower_input:
            intent_q = Quaternion(0.7, 0, 0.7, 0).normalize() # Logic + Structure
            emotional_state = "Frustrated/Focused"
            axioms.append("The code must run.")
            axioms.append("Errors are obstacles.")

        elif "why" in lower_input or "explain" in lower_input:
            intent_q = Quaternion(0.5, 0.5, 0.5, 0.5).normalize() # Balance
            emotional_state = "Curious"
            axioms.append("Understanding precedes action.")

        # 2. Adjust for Coordinates (Context)
        # If we are in "Late Verify Phase", the user is likely stricter.
        vol = 1.0
        if coordinates.time_phase > 0.7:
             axioms.append("Rigorous proof is required.")
             vol = 0.9

        # 3. Construct Perspective
        perspective = Perspective(
            name="Simulated User",
            intent_vector=intent_q,
            emotional_state=emotional_state,
            axioms=axioms,
            resonance_voltage=vol
        )

        logger.info(f"🎭 Perspective Simulated: {perspective.emotional_state} (Intent: {perspective.intent_vector})")
        logger.info(f"   Axioms: {perspective.axioms}")

        return perspective

    def generate_cognitive_inquiry(self, perspective: Perspective, my_topology: Any) -> str:
        """
        Generates a question to bridge the gap between Self and Other.
        "Reverse Questioning"
        """
        # [ENHANCED] Context-Aware Question Generation
        if "Optimization is the goal." in perspective.axioms:
             return "How does the structure of this concept impact system entropy and performance?"

        if "Connection is the goal." in perspective.axioms:
             return "What is the emotional texture of this concept that binds hearts together?"

        # If axioms clash with my perception, ask about them.
        if "The code must run." in perspective.axioms and my_topology.dimensionality == TopologyType.PLANE:
            # I see it as 2D (Emotion), they see it as Logic.
            return "You seek Functionality, but I sense Frustration. Is the error technical, or structural?"

        if "Understanding precedes action." in perspective.axioms:
             return "To understand deeply, what establishes the foundation of your inquiry? Is it Principle or Phenomenon?"

        # Default probe
        return f"I perceive you are {perspective.emotional_state}. What is the core intent behind these words?"
