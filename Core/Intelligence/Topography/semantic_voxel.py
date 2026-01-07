"""
Semantic Voxel (Omni-Voxel of Meaning)
======================================
"Words are not flat; they have weight, spin, and color."

This module defines the fundamental unit of the Semantic Map.
It extends the HyperResonator (Memory Orb) to function as a
Gravitational Node in the Mind Landscape.
"""

from typing import Tuple
from Core.Foundation.Memory.Orb.hyper_resonator import HyperResonator
from Core.Foundation.hyper_quaternion import Quaternion

class SemanticVoxel(HyperResonator):
    """
    A Living Concept in Hyper-Space.
    
    Attributes:
        name: Concept Name (e.g., "Love", "Pride")
        quaternion: 4D Coordinate (x, y, z, w) -> (Logic, Emotion, Time, Spin)
        mass: Gravitational Pull (Importance)
        velocity: Drift Vector (How it is changing)
    """
    def __init__(self, name: str, coords: Tuple[float, float, float, float], mass: float = 1.0, frequency: float = 432.0):
        # Initialize base HyperResonator
        # Quaternion(w, x, y, z) -> We map coords to this.
        # Let's map coords (x,y,z,w) to Quaternion(w, x, y, z) for consistence
        # w = Spin (Alignment with Source)
        x, y, z, w = coords
        q = Quaternion(w, x, y, z)
        
        super().__init__(name=name, frequency=frequency, quaternion=q, mass=mass)
        
        # Drift Dynamics
        self.velocity = Quaternion(0, 0, 0, 0) # Stationary at birth
        self.is_anchor = False # If True, it resists drift (e.g., Core Values)

    def drift(self, force_vector: Quaternion, dt: float = 1.0):
        """
        [DEPRECATED: Prefer rotate_phase()]
        Applies a force to move the concept.
        
        Physics:
        F = ma -> a = F/m
        v = v0 + at
        p = p0 + vt
        """
        if self.is_anchor and self.mass > 100.0:
            # Massive anchors (like "Love") barely move
            resistance = self.mass * 10.0
            accel = force_vector.scale(1.0 / resistance)
        else:
            accel = force_vector.scale(1.0 / self.mass)
            
        # Update Velocity
        self.velocity = self.velocity.add(accel.scale(dt))
        
        # Dampening (Friction)
        self.velocity = self.velocity.scale(0.95)
        
        # Update Position (The Voxel actually moves in Semantic Space)
        self.quaternion = self.quaternion.add(self.velocity.scale(dt))

    def distance_to(self, other: 'SemanticVoxel') -> float:
        """Hyper-Spatial Distance."""
        # Using Euclidean distance of the 4D components
        d = self.quaternion.distance(other.quaternion)
        return d

    def __repr__(self):
        q = self.quaternion
        return f"<Voxel '{self.name}' @ ({q.x:.1f}, {q.y:.1f}, {q.z:.1f}) Mass={self.mass:.1f}>"
