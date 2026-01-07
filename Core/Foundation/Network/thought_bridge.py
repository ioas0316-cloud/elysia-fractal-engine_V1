"""
ThoughtBridge: Unified Thought Processing System
==============================================

Integrates:
1. ThoughtLayerBridge (Fractal Layers: 0D -> 3D)
2. EnhancedThoughtLanguageBridge (Language Expression)
3. ResonanceField (System State & Resonance)

Acts as the primary interface for the API Server.
"""

import logging
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
import numpy as np

from Core.Foundation.thought_layer_bridge import ThoughtLayerBridge
from Core.Foundation.enhanced_thought_language_bridge import EnhancedThoughtLanguageBridge, ThoughtPackage
from Core.Foundation.Wave.resonance_field import ResonanceField
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("ThoughtBridge")

class ThoughtBridge:
    """
    Central bridge for thought processing.
    Orchestrates the transition from prompt -> concept -> layers -> expression.
    """

    def __init__(self):
        self.layer_bridge = ThoughtLayerBridge()
        self.language_bridge = EnhancedThoughtLanguageBridge()
        self.resonance_field = ResonanceField()

        # Connect components if needed
        # self.language_bridge.connect_communication(...)

        logger.info("🌉 ThoughtBridge initialized")

    def process_thought(self, prompt: str, layer: str = "2D", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a thought from prompt to result.

        Args:
            prompt: Input text
            layer: Target layer (0D, 1D, 2D, 3D)
            context: Optional context

        Returns:
            Dict containing thought text, resonance, layer info, etc.
        """
        if context is None:
            context = {}

        logger.info(f"Processing thought: '{prompt}' on layer {layer}")

        # 1. Understand Prompt (Text -> ThoughtPackage/Quaternion)
        # Using language bridge to infer concept
        thought_package = self.language_bridge.listen_then_think(prompt)
        quat = thought_package.concept

        # 2. Transform through Fractal Layers (0D -> 3D)
        # This gives us the multi-layered representation
        layer_result = self.layer_bridge.transform_thought(quat)

        # 3. Calculate Resonance
        # We can calculate resonance of this thought with the current field
        current_resonance = self._calculate_field_resonance(quat)

        # 4. Generate Final Output based on requested layer
        final_thought_text = ""

        if layer == "0D":
            final_thought_text = f"Point of View: {layer_result['source']}"
        elif layer == "1D":
            # Causal chain
            chains = [f"{c} -> {e}" for c, e in layer_result['causal']]
            final_thought_text = "Logic Chain: " + "; ".join(chains)
        elif layer == "2D":
            # Wave pattern description or Language Bridge expression
            # Using Language Bridge for "Thinking then Speaking" which is roughly 2D/3D interface
            # But let's use the multimodal output from EnhancedThoughtLanguageBridge for richness
            multimodal = self.language_bridge.express_thought_multimodal(thought_package)
            final_thought_text = multimodal.text
        elif layer == "3D":
            # Manifestation
            final_thought_text = layer_result['manifestation']
        else:
            final_thought_text = f"[{layer}] {prompt}"

        # 5. Update Field (Side Effect)
        # Inject the thought into the resonance field
        # Using w component as frequency proxy (simplified)
        freq = 432.0 * (1.0 + quat.w)
        self.resonance_field.inject_wave(
            frequency=freq,
            intensity=thought_package.energy,
            wave_type="RealityPerception",
            payload=prompt
        )

        return {
            "thought": final_thought_text,
            "layer": layer,
            "resonance": current_resonance,
            "timestamp": datetime.now().isoformat(),
            "details": layer_result,
            "quaternion": {
                "w": quat.w, "x": quat.x, "y": quat.y, "z": quat.z
            }
        }

    def calculate_resonance_between_concepts(self, concept_a: str, concept_b: str) -> Dict[str, Any]:
        """
        Calculate resonance between two text concepts.
        """
        # 1. Convert to Quaternions
        quat_a = self.language_bridge._infer_concept_from_text(concept_a)
        quat_b = self.language_bridge._infer_concept_from_text(concept_b)

        # 2. Calculate Alignment (Dot Product)
        alignment = quat_a.dot(quat_b)

        # 3. Calculate Frequency Ratio (Harmony)
        freq_a = 432.0 * (1.0 + quat_a.w)
        freq_b = 432.0 * (1.0 + quat_b.w)

        ratio = min(freq_a, freq_b) / max(freq_a, freq_b)

        # Combined Score
        score = (alignment + 1.0) * 0.5 * 0.7 + ratio * 0.3 # Normalize alignment (-1 to 1) -> (0 to 1)
        score = max(0.0, min(1.0, score))

        explanation = (
            f"Resonance between '{concept_a}' and '{concept_b}': "
            f"Alignment {alignment:.2f}, Frequency Ratio {ratio:.2f}. "
            f"They {'harmonize well' if score > 0.7 else 'have friction'}."
        )

        return {
            "score": score,
            "explanation": explanation,
            "concepts": [concept_a, concept_b]
        }

    def _calculate_field_resonance(self, quat: Quaternion) -> float:
        """
        Calculate how much a thought resonates with the current system state.
        """
        # Compare with the "Foundation" pillar or average field state
        foundation = self.resonance_field.pillars.get("Foundation")
        if foundation:
            alignment = quat.dot(foundation.quaternion)
            # Normalize -1..1 to 0..1
            return (alignment + 1.0) / 2.0
        return 0.5
