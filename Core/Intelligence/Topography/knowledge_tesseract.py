from typing import Dict, List, Optional, Union, Tuple
import numpy as np
from Core.Intelligence.Topography.tesseract_geometry import TesseractVector, TesseractGeometry
from Core.Intelligence.Topography.fluid_intention import FluidIntention

class KnowledgeLayer:
    FOUNDATION = "Foundation"
    MEMORY = "Memory"
    CORE = "Core"
    SENSORY = "Sensory"
    SYSTEM = "System"

class TesseractKnowledgeMap:
    """
    Manages the 4D spatial arrangement of Knowledge Layers.
    Implements the 'Intention Folding' logic where the W-axis (Intention)
    determines the adjacency of layers.
    """

    def __init__(self):
        self.geometry = TesseractGeometry()
        self.nodes: Dict[str, TesseractVector] = {}
        self._initialize_base_structure()

    def _initialize_base_structure(self):
        """
        Maps the 5 Layers to initial vertices of a Tesseract (Hypercube).
        A Tesseract has 16 vertices. We map layers to key structural points.

        Origin (0,0,0,0) is LOVE (Elysia's Essence).
        """

        # Foundation: The base. Negative W (Inner/Subconscious), Negative Y (Ground)
        self.nodes[KnowledgeLayer.FOUNDATION] = TesseractVector(0, -1, 0, -1)

        # Memory: The storage. Positive X, Negative W (Inner)
        self.nodes[KnowledgeLayer.MEMORY] = TesseractVector(1, 0, 0, -1)

        # Core: The processing center. Origin-adjacent but active. Zero W (Present)
        self.nodes[KnowledgeLayer.CORE] = TesseractVector(0, 0, 0, 0)

        # Sensory: The interface. Positive W (Outer/Conscious), Positive Z (Forward)
        self.nodes[KnowledgeLayer.SENSORY] = TesseractVector(0, 1, 1, 1)

        # System: The meta-structure. Positive W (Conscious), Positive Y (High)
        self.nodes[KnowledgeLayer.SYSTEM] = TesseractVector(0, 1, 0, 1)

    def get_fluid_map(self, intention: FluidIntention) -> Dict[str, Dict]:
        """
        Returns the Knowledge Map with fluid properties (Resonance Strength).
        Output format:
        {
            "NodeName": {
                "position": (x, y, z),
                "resonance": float (0.0 - 1.0),
                "original_vector": TesseractVector
            }
        }
        """
        fluid_map = {}

        # Phase is determined by the focus of the intention
        phase = intention.focus_w

        for name, vector in self.nodes.items():
            # 1. Calculate Resonance (0.0 to 1.0)
            resonance = intention.get_resonance_strength(vector.w)

            # 2. Apply Spiral Transform (Rotation based on Intention)
            transformed_vector = self.geometry.apply_spiral_transform(vector, phase)

            # 3. Apply "Gravitational Pull" based on Resonance
            # High resonance nodes are pulled closer to the 'Action Plane' (z=0, perspective)
            # Or we can simply use resonance for visual opacity/size

            # Project to 3D
            projected_point = self.geometry.project_to_3d(transformed_vector)

            fluid_map[name] = {
                "position": projected_point,
                "resonance": resonance,
                "original_vector": vector
            }

        return fluid_map

    def get_distance(self, node_a: str, node_b: str, intention_phase: float = 0.0) -> float:
        """
        Calculates the distance between two nodes in the transformed 4D space.
        This represents 'Semantic Distance' modified by 'Intention'.
        """
        if node_a not in self.nodes or node_b not in self.nodes:
            return float('inf')

        vec_a = self.nodes[node_a]
        vec_b = self.nodes[node_b]

        # Transform both vectors by the current intention
        trans_a = self.geometry.apply_spiral_transform(vec_a, intention_phase)
        trans_b = self.geometry.apply_spiral_transform(vec_b, intention_phase)

        diff = trans_a - trans_b
        return diff.magnitude()

    def find_nearest_layers(self, target_layer: str, intention_phase: float) -> List[str]:
        """
        Finds which layers are closest to the target layer under the current intention.
        Demonstrates how 'Folding' brings distant layers together.
        """
        if target_layer not in self.nodes:
            return []

        distances = []
        for name in self.nodes:
            if name == target_layer:
                continue
            dist = self.get_distance(target_layer, name, intention_phase)
            distances.append((name, dist))

        # Sort by distance
        distances.sort(key=lambda x: x[1])
        return [d[0] for d in distances]
