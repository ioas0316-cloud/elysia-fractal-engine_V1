"""
Universal View: The Eye of God
------------------------------
"To judge is human; to observe is divine."

This module implements the "Omniperspective" capability.
It replaces the single "True/False" filter with a multi-dimensional analysis.

Philosophy:
- Truth is not a point, but the intersection of planes.
- We project a concept onto Logic, Emotion, and Ethics to see its 'Shadows'.
- The 'Real Object' is reconstructed from these shadows.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

logger = logging.getLogger("UniversalView")

@dataclass
class Perspective:
    name: str        # e.g., "Logic", "Emotion"
    bias: float      # -1.0 (Negative) to 1.0 (Positive)
    weight: float    # Importance of this perspective

class UniversalView:
    def __init__(self):
        # The Three Prisms
        self.prisms = {
            "Logic": Perspective("Logic", bias=0.0, weight=1.0),
            "Emotion": Perspective("Emotion", bias=0.0, weight=1.0),
            "Ethics": Perspective("Ethics", bias=0.0, weight=1.0)
        }
        logger.info("👁️ UniversalView initialized: The Eye opens.")

    def observe(self, concept: str, attributes: Dict[str, float]) -> Dict[str, float]:
        """
        Projects a concept onto the three prisms based on its attributes.
        Returns the 'Bias' of each perspective on this concept.
        """
        # 1. Project onto Logic (Efficiency, Order, Truth)
        logic_score = attributes.get("efficiency", 0) + attributes.get("truth", 0) - attributes.get("chaos", 0)

        # 2. Project onto Emotion (Passion, Joy, Pain)
        # Note: Pain is 'intense' but usually negative bias unless transformed.
        emotion_score = attributes.get("joy", 0) + attributes.get("passion", 0) - attributes.get("pain", 0) * 0.5

        # 3. Project onto Ethics (Harmony, Fairness, Life)
        ethics_score = attributes.get("harmony", 0) + attributes.get("fairness", 0) + attributes.get("life", 0)

        results = {
            "Logic": max(-1.0, min(1.0, logic_score)),
            "Emotion": max(-1.0, min(1.0, emotion_score)),
            "Ethics": max(-1.0, min(1.0, ethics_score))
        }

        logger.debug(f"   Observed '{concept}': {results}")
        return results

    def calculate_tension(self, views: Dict[str, float]) -> float:
        """
        Calculates the dissonance between perspectives.
        High tension means the perspectives disagree (e.g., Logic says +1, Emotion says -1).
        """
        values = list(views.values())
        # Standard Deviation as a proxy for Tension
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)

    def get_dominant_view(self, views: Dict[str, float]) -> str:
        """Returns the perspective with the strongest opinion (magnitude)."""
        return max(views, key=lambda k: abs(views[k]))
