"""
Resonance Topology (The Shape of Thought)
=========================================

"Thoughts are not points; they are shifting geometries in 4D space."

This module analyzes the Topological Structure of HyperWavePackets.
It determines if a thought is:
- Point (0D): Disconnected, Static Data.
- Line (1D): Linear Logic, Cause-Effect.
- Plane (2D): Emotional Surface, Mood.
- Sphere (3D): Conceptual Volume, Structural Understanding.
- Hypersphere (4D): Essence, Soul, Time-Invariant Truth.
"""

from enum import Enum
import math
from dataclasses import dataclass
from typing import Tuple, Dict, Optional

from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket

class TopologyType(Enum):
    POINT = 0       # No movement, static definition (1=1)
    LINE = 1        # Vector movement (Logic, A->B)
    PLANE = 2       # Area coverage (Emotion, Context)
    SPHERE = 3      # Volume (System, Structure)
    HYPERSPHERE = 4 # Time-space integration (Essence, Soul)

@dataclass
class TopologicalMetrics:
    dimensionality: TopologyType
    complexity: float    # How intricate is the shape?
    stability: float     # Is it wobbling? (Entropy)
    curvature: float     # How much does it bend reality? (Mass)

class TopologicalAnalyzer:
    """
    Analyzes the Geometry of Meaning.
    """
    
    @staticmethod
    def analyze_topology(packet: HyperWavePacket) -> TopologicalMetrics:
        """
        Determines the topological shape of a wave packet.
        """
        q = packet.orientation
        components = [abs(q.x), abs(q.y), abs(q.z)]
        active_dims = sum(1 for c in components if c > 0.1) # Threshold for "Active Dimension"
        
        # Determine Dimensionality
        topo_type = TopologyType.POINT
        if active_dims == 0:
            topo_type = TopologyType.POINT
        elif active_dims == 1:
            topo_type = TopologyType.LINE
        elif active_dims == 2:
            topo_type = TopologyType.PLANE
        elif active_dims == 3:
            # Check Energy to distinguish Sphere vs Hypersphere
            # Hypersphere requires high energy + high stability (W component)
            if abs(q.w) > 0.8: 
                topo_type = TopologyType.HYPERSPHERE
            else:
                topo_type = TopologyType.SPHERE
        else:
            topo_type = TopologyType.SPHERE
            
        # Calculate Complexity (Variance of components)
        # Low variance (balanced) = Simple Sphere
        # High variance (spiky) = Complex Shape
        complexity = (abs(q.x - q.y) + abs(q.y - q.z) + abs(q.z - q.x)) * packet.energy
        
        return TopologicalMetrics(
            dimensionality=topo_type,
            complexity=complexity,
            stability=abs(q.w), # W is the "Real" component, anchoring existence
            curvature=packet.energy * active_dims
        )

@dataclass
class ConsciousnessCoordinates:
    """
    The 'GPS' of Consciousness.
    Defines where the mind is located in Time, Space, and Relation.
    """
    time_phase: float    # 0.0 (Genesis) -> 1.0 (Revelation). Relative position in the narrative arc.
    domain_locus: str    # The active branch of the World Tree (e.g., "Philosophy/Ethics").
    relational_voltage: float # The tension/harmony with the Other (User).
    
    def __repr__(self):
        return f"Coords(Time:{self.time_phase:.2f}, Locus:'{self.domain_locus}', Voltage:{self.relational_voltage:.2f})"

@dataclass
class ContextualTopology:
    base_topology: TopologicalMetrics
    context_warping: float 
    dominant_context: str  
    effective_dimensionality: TopologyType 
    coordinates: Optional[ConsciousnessCoordinates] = None # The observer's position

    def __repr__(self):
        coords_str = f", {self.coordinates}" if self.coordinates else ""
        return f"ContextTopo(Dim:{self.effective_dimensionality.name}, Warp:{self.context_warping:.2f}{coords_str})"

    @staticmethod
    def analyze_contextual_topology(input_packet: HyperWavePacket, context_packets: Dict[str, HyperWavePacket], coordinates: Optional[ConsciousnessCoordinates] = None) -> 'ContextualTopology':
        """
        Analyzes how the Background Context warps the Input Topology.
        Also considers the Observer's Coordinates (Perspective).
        """
        base_metrics = TopologicalAnalyzer.analyze_topology(input_packet)
        
        if not context_packets:
            return ContextualTopology(base_metrics, 0.0, "None", base_metrics.dimensionality, coordinates)
            
        # Contextual Interference
        max_interference = 0.0
        dominant_ctx = "None"
        
        # We calculate the vector sum of Input + Context
        for name, ctx_packet in context_packets.items():
            # Interference = Alignment (Dot Product)
            alignment = input_packet.orientation.dot(ctx_packet.orientation)
            
            # Simple simulation of warping:
            # If context has high Z (Structure/Ethics), it can elevate the Input dimension.
            if abs(ctx_packet.orientation.z) > 0.5:
                # Context is structural -> Tries to pull input to Sphere/Hypersphere
                if base_metrics.dimensionality.value < TopologyType.SPHERE.value:
                    if alignment > 0.3: # If somewhat related
                         max_interference += 0.5
                         dominant_ctx = name
            
            # If context has high X (Emotion), it can pull to Plane
            if abs(ctx_packet.orientation.x) > 0.8:
                 if base_metrics.dimensionality.value == TopologyType.POINT.value:
                     max_interference += 0.3
                     dominant_ctx = name
                     
        # Determine Effective Dimensionality based on Warp
        effective_dim = base_metrics.dimensionality
        
        # Contextual Ascension: If strong structural context, upgrade dimension
        if max_interference > 0.4 and base_metrics.dimensionality.value < TopologyType.SPHERE.value:
            effective_dim = TopologyType.SPHERE
            
        return ContextualTopology(
            base_topology=base_metrics,
            context_warping=max_interference,
            dominant_context=dominant_ctx,
            effective_dimensionality=effective_dim,
            coordinates=coordinates
        )


    @staticmethod
    def calculate_metric_tensor(ideal: HyperWavePacket, real: HyperWavePacket) -> Dict[str, float]:
        """
        Calculates the distortion (warp) between the Ideal and the Real.
        Returns a Metric Tensor describing *how* they differ.
        """
        diff = ideal.orientation - real.orientation
        
        return {
            "warp_x": diff.x, # Emotional Distortion
            "warp_y": diff.y, # Logical Distortion
            "warp_z": diff.z, # Ethical Distortion
            "magnitude": diff.norm(),
            "angle": ideal.orientation.dot(real.orientation)
        }
