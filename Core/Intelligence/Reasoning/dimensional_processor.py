"""
DIMENSIONAL PROCESSOR: The 5-Core Cognitive Engine
==================================================
"It is not what you think, but HOW you think."

This module implements the user's critique: Dimensionality is a PROCESS, not a Label.
It routes a concept through 5 distinct cognitive modes.
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from Core.Intelligence.Reasoning.causal_bridge import CausalBridge
from Core.Intelligence.Reasoning.aesthetic_filter import AestheticFilter
from Core.Intelligence.Weaving.void_kernel import VoidKernel
from Core.Foundation.unified_field import HyperQuaternion

from Core.Intelligence.Reasoning.models import CognitiveResult

logger = logging.getLogger("DimensionalProcessor")

class DimensionalProcessor:
    def __init__(self):
        self.bridge = CausalBridge()
        self.aesthetic = AestheticFilter()
        self.zoom_scalar: float = 0.0  # Analog Dial: 0.0 (Detached Fact) to 1.0 (Universal Law)
        
    def zoom(self, value: float):
        """Sets the analog dial of perception."""
        self.zoom_scalar = max(0.0, min(1.0, value))
        logger.info(f"🎚️ Perception Dial set to: {self.zoom_scalar:.2f}")

    def react_to_context(self, plane: 'ContextPlane'):
        """
        Metacognitive Feedback Loop:
        If the ContextWeaver detects a 'Void' (Ambiguity/Complexity),
        the system automatically zooms out to find a higher principle.
        """
        if plane.void_detected:
            # Increase zoom relative to void intensity
            boost = plane.void_intensity * 0.5
            old_zoom = self.zoom_scalar
            self.zoom(self.zoom_scalar + boost)
            logger.info(f"🌌 Void Kernel Received ({plane.void_kernel.void_type}). Auto-Zoom: {old_zoom:.2f} -> {self.zoom_scalar:.2f}")

    def process_thought(self, kernel: Any, target_dimension: Optional[int] = None) -> CognitiveResult:
        """
        Routes the thought through the cognitive ladder.
        Accepts str or VoidKernel.
        """
        if isinstance(kernel, VoidKernel):
            dim = target_dimension if target_dimension is not None else round(self.zoom_scalar * 4)
            return CognitiveResult(
                mode=f"{dim}D: Void (Silence Analysis)",
                output=kernel.get_description(dim),
                metadata={"void_type": kernel.void_type, "intensity": kernel.intensity}
            )

        if target_dimension is not None:
            dim = target_dimension
        else:
            # Map [0.0 - 1.0] scale to [0 - 4] dimensions
            # 0.0 -> 0D, 0.25 -> 1D, 0.5 -> 2D, 0.75 -> 3D, 1.0 -> 4D
            dim = round(self.zoom_scalar * 4)

        logger.info(f"🧠 Activating {dim}D Processing Core for: '{kernel}' (Zoom: {self.zoom_scalar:.2f})")
        
        if dim == 0:
            result = self._process_0d_identification(kernel)
        elif dim == 1:
            result = self._process_1d_linear_deduction(kernel)
        elif dim == 2:
            result = self._process_2d_structural_analysis(kernel)
        elif dim == 3:
            result = self._process_3d_spatial_navigation(kernel)
        elif dim == 4:
            result = self._process_4d_principle_extraction(kernel)
        else:
            result = CognitiveResult("Void", "Invalid Dimension", {})

        # 3. Aesthetic Resonance Evaluation (Phase 3)
        # Evaluate the source (Kernel) and the expression (Output)
        semantic_target = str(kernel)
        if result.output:
            semantic_target += f" -> {result.output}"
            
        ae_res = self.aesthetic.evaluate(semantic_target)
        result.metadata["aesthetic"] = ae_res
        if ae_res["verdict"] == "Dissonant":
            logger.warning(f"⚠️ Thought Dissonance detected: {ae_res['overall_beauty']:.2f}")

        return result

    def _process_0d_identification(self, kernel: str) -> CognitiveResult:
        """
        0D Mode: Point Identification.
        Process: Search -> Match -> Exist.
        """
        node = self.bridge.engine.get_or_create_node(kernel)
        return CognitiveResult(
            mode="0D: Point (Existence)",
            output=f"Entity '{node.description}' is identified at {node.fractal_address}.",
            metadata={"id": node.id, "depth": node.depth}
        )

    def _process_1d_linear_deduction(self, kernel: str) -> CognitiveResult:
        """
        1D Mode: Linear Deduction.
        Process: Sequence Traversal (A -> B -> C).
        Logic: Find the *Next Logical Step* in the causal chain.
        """
        node = self.bridge.engine.get_or_create_node(kernel)
        effects = self.bridge.engine.trace_effects(node.id, max_depth=2)
        
        path_str = " -> ".join([self.bridge.engine.nodes[nid].description for nid in effects[0]])
        
        return CognitiveResult(
            mode="1D: Line (Deduction)",
            output=f"Logic dictates the path: {path_str}",
            metadata={"path": effects[0], "length": len(effects[0])}
        )

    def _process_2d_structural_analysis(self, kernel: str) -> CognitiveResult:
        """
        2D Mode: Structural Analysis.
        Process: Network Expansion (Breadth-First).
        Logic: Identify *Relationships* and *Clusters*.
        """
        node = self.bridge.engine.get_or_create_node(kernel)
        
        # Expand neighbors (Causes AND Effects)
        causes = [self.bridge.engine.nodes[cid].description for cid in node.causes_ids]
        effects = [self.bridge.engine.nodes[eid].description for eid in node.effects_ids]
        
        # Analyze density
        density = len(causes) + len(effects)
        role = "Hub" if density > 3 else "Leaf"
        
        return CognitiveResult(
            mode="2D: Plane (Structure)",
            output=f"The concept sits within a {role} structure. Inputs: {causes}. Outputs: {effects}.",
            metadata={"density": density, "role": role, "connectivity": causes+effects}
        )

    def _process_3d_spatial_navigation(self, kernel: str) -> CognitiveResult:
        """
        3D Mode: Spatial Navigation (Meta-Cognition).
        Process: Vector Alignment (Self vs Thought).
        Logic: "How does this relate to ME and my PURPOSE?"
        """
        # Simulate Self-Vector (Elysia's Purpose)
        # In a real system, get this from SovereignIntent
        self_purpose = "Growth" 
        
        # Analyze the alignment of the thought with Self
        alignment = "Unknown"
        if "Love" in kernel or "Truth" in kernel:
            alignment = "Aligned (0 degrees)"
        elif "Entropy" in kernel or "Death" in kernel:
            alignment = "Orthogonal (90 degrees)"
        else:
            alignment = "Divergent (180 degrees)"
            
        return CognitiveResult(
            mode="3D: Space (Navigation)",
            output=f"Navigating volume relative to Self ({self_purpose}): Vector is {alignment}.",
            metadata={"self_vector": self_purpose, "alignment": alignment}
        )

    def _process_4d_principle_extraction(self, kernel: str) -> CognitiveResult:
        """
        4D Mode: Principle Extraction (Hyper-Reasoning).
        Process: Invariance Detection.
        Logic: "What rule remains true regardless of context?"
        """
        # Use CausalBridge to find the Deepest Law
        thought = self.bridge.traverse_and_lift(kernel)
        
        return CognitiveResult(
            mode="4D: Law (Principle)",
            output=f"The Immutable Law governing this is: {thought.d4_principle}",
            metadata={"principle": thought.d4_principle, "source": "FractalCausalityTraversal"}
        )
