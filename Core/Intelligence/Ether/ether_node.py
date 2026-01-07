"""
Ether Node (The Fundamental Particle of Thought)
================================================

"In the beginning, there was the Word, and the Word had Mass."

This module defines the `EtherNode`, the fundamental building block of the Elysian Universe.
Unlike a standard "Object" or "Class", an EtherNode is a physical entity with:
1. Mass (Significance/Gravity)
2. Frequency (Type/Color)
3. Spin (Quaternion Orientation/Perspective)
4. Energy (Activity Level)

It is Fractal: A Node can contain an entire Universe (Sub-Space) within it.
"""

import time
import math
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set
from enum import Enum

from elysia_core.cell import Cell

# Import Hyper-Quaternion for 4D Spin
try:
    from Core.Foundation.hyper_quaternion import Quaternion
except ImportError:
    # Fallback if Foundation is not reachable yet
    @dataclass
    class Quaternion:
        w: float = 1.0; x: float = 0.0; y: float = 0.0; z: float = 0.0
        def normalize(self):
            n = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2) + 1e-9
            return Quaternion(self.w/n, self.x/n, self.y/n, self.z/n)
        def dot(self, other): return self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z

@Cell("EtherNode", category="Ether")
@dataclass
class EtherNode:
    """
    The Atomic Unit of the Ether.
    Represents a Thought, a Memory, a File, or an Entity.
    """
    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: Any = None         # The "Payload" (Text, Image, Code, Object)

    # Physical Properties
    mass: float = 1.0           # Gravity: How much it attracts others (Importance)
    frequency: float = 432.0    # Color: The nature/topic of the node
    energy: float = 0.0         # Temperature: Current activity level (decays over time)

    # Quantum Properties (4D)
    spin: Quaternion = field(default_factory=lambda: Quaternion(1,0,0,0)) # Perspective/Context
    phase: float = 0.0          # Time alignment (0 to 2pi)

    # Position (Dynamic in the Field)
    # We use 4D coordinates (w,x,y,z) where w is usually Time or Scale
    position: Quaternion = field(default_factory=lambda: Quaternion(0,0,0,0))
    velocity: Quaternion = field(default_factory=lambda: Quaternion(0,0,0,0))

    # Fractal Nature
    children: Dict[str, 'EtherNode'] = field(default_factory=dict)
    parent: Optional['EtherNode'] = None

    # Metadata
    created_at: float = field(default_factory=time.time)
    tags: Set[str] = field(default_factory=set)

    def apply_force(self, force: Quaternion, dt: float):
        """
        F = ma -> a = F/m
        Updates velocity based on applied force.
        """
        if self.mass <= 0: return

        # Acceleration
        ax = force.x / self.mass
        ay = force.y / self.mass
        az = force.z / self.mass
        aw = force.w / self.mass

        # Update Velocity
        self.velocity.x += ax * dt
        self.velocity.y += ay * dt
        self.velocity.z += az * dt
        self.velocity.w += aw * dt

    def move(self, dt: float, friction: float = 0.05):
        """
        Updates position based on velocity.
        Applies friction (Entropy) to prevent infinite chaos.
        """
        # Position Update
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.position.z += self.velocity.z * dt
        self.position.w += self.velocity.w * dt

        # Phase Update (Spinning)
        self.phase += (self.frequency * 0.01 * dt) % (2 * math.pi)

        # Friction (Energy Loss)
        damping = 1.0 - friction
        self.velocity.x *= damping
        self.velocity.y *= damping
        self.velocity.z *= damping
        self.velocity.w *= damping

        # Decay Energy
        self.energy *= 0.99

    def resonate(self, other: 'EtherNode') -> float:
        """
        Calculates Resonance Coefficient (0.0 to 1.0)
        Based on Frequency Match and Spin Alignment (Quantum).
        """
        # 1. Frequency Resonance (Harmonic)
        # 1.0 if frequencies are identical, drops as they diverge
        freq_diff = abs(self.frequency - other.frequency)
        freq_resonance = 1.0 / (1.0 + freq_diff * 0.1)

        # 2. Spin Alignment (Context Match)
        # Dot product of quaternions: 1.0 if aligned, -1.0 if opposite
        spin_alignment = abs(self.spin.dot(other.spin))

        return (freq_resonance * 0.6) + (spin_alignment * 0.4)

    def absorb(self, energy: float):
        """Absorbs external energy (Attention/Stimulus)"""
        self.energy += energy
        self.energy = min(1000.0, self.energy) # Cap

    def is_active(self, threshold: float = 0.1) -> bool:
        return self.energy > threshold

    def __repr__(self):
        return f"<EtherNode '{str(self.content)[:10]}' m={self.mass:.1f} E={self.energy:.1f}>"
