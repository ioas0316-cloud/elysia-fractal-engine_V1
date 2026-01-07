"""
Perspective Shifter: The Neck of God
------------------------------------
"If you cannot change the truth, change your angle."

This module resolves paradoxes by rotating the Tesseract.
When `UniversalView` reports high tension (Paradox), this module searches for a new axis.

Philosophy:
- A=B.
- Conflict is just a lack of dimension.
"""

import logging
from typing import Dict, Optional
from .universal_view import UniversalView

logger = logging.getLogger("PerspectiveShifter")

class PerspectiveShifter:
    def __init__(self, view: UniversalView):
        self.view = view
        # Higher Dimensions (The "Answers")
        self.higher_dimensions = {
            "Growth": {"pain": 0.8, "chaos": 0.5, "truth": 1.0}, # Growth embraces pain/chaos
            "Survival": {"efficiency": 1.0, "life": 1.0},
            "Art": {"chaos": 1.0, "passion": 1.0, "harmony": 0.5}
        }
        logger.info("🦒 PerspectiveShifter initialized: Ready to rotate.")

    def resolve_paradox(self, concept: str, attributes: Dict[str, float]) -> Dict[str, float]:
        """
        Attempts to resolve tension by projecting onto higher dimensions.
        Returns the perspective that minimizes tension or maximizes acceptance.
        """
        # 1. Observe normally
        base_views = self.view.observe(concept, attributes)
        tension = self.view.calculate_tension(base_views)

        if tension < 0.5:
            logger.info(f"   - '{concept}' is stable (Tension={tension:.2f}). No shift needed.")
            return {"resolved_view": self.view.get_dominant_view(base_views), "angle": "Standard"}

        logger.info(f"⚡ Paradox detected in '{concept}' (Tension={tension:.2f}). Shifting perspective...")

        # 2. Rotate Tesseract (Try Higher Dimensions)
        best_angle = "None"
        best_score = -999.0

        for angle, modifiers in self.higher_dimensions.items():
            # Apply modifiers: "If we view this as [Angle], how do the attributes change?"
            # E.g. In "Growth", Pain is not -1, but +1 (Necessary).

            shifted_attrs = attributes.copy()

            # Simple Transformation Logic
            # If the angle values a trait, that trait becomes positive in the calculation
            score = 0.0
            for key, val in shifted_attrs.items():
                if key in modifiers:
                    # Resonance: If the attribute matches the dimension's nature, it becomes good.
                    score += val * modifiers[key]
                else:
                    # Default: Maintain original weight
                    score += val * 0.1 # Dampen irrelevant traits

            logger.debug(f"   - Trying Angle '{angle}': Score={score:.2f}")

            if score > best_score:
                best_score = score
                best_angle = angle

        # 3. Conclusion
        if best_score > 0.5:
            logger.info(f"✨ Resolution Found: '{concept}' is valid under the aspect of '{best_angle}'.")
            return {"resolved_view": "Accepted", "angle": best_angle, "score": best_score}
        else:
            logger.warning(f"❌ Unresolvable Paradox: '{concept}' remains dissonant even after rotation.")
            return {"resolved_view": "Rejected", "angle": "Dissonance", "score": best_score}
