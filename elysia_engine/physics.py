from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
import math

from .math_utils import Vector3

if TYPE_CHECKING:
    from .entities import Entity

@dataclass
class PhysicsState:
    """
    Spatial state of an entity in the Digital Physics world.
    Extends the abstract EFP state with concrete geometry.
    """
    position: Vector3 = field(default_factory=lambda: Vector3(0, 0, 0))
    velocity: Vector3 = field(default_factory=lambda: Vector3(0, 0, 0))
    mass: float = 1.0

    def apply_force(self, force: Vector3, dt: float) -> None:
        """F = ma -> a = F/m"""
        if self.mass <= 0:
            return
        acceleration = force * (1.0 / self.mass)
        self.velocity = self.velocity + acceleration * dt

    def step(self, dt: float) -> None:
        """Update position based on velocity."""
        self.position = self.position + self.velocity * dt


@dataclass
class Attractor:
    """
    Represents a 'Answer' or 'Goal' in the semantic space.
    Acts as a simple Gravity Well (no Soul/Frequency).
    """
    id: str
    position: Vector3
    mass: float = 100.0  # Standard mass for an answer
    radius: float = 1.0  # Event horizon/Capture radius

    def calculate_force(self, target_pos: Vector3, G: float = 1.0) -> Vector3:
        """
        Calculates gravitational force: F = G * M / r^2 * direction
        """
        diff = self.position - target_pos
        dist = diff.magnitude

        if dist < 0.001:
            return Vector3(0, 0, 0)

        direction = diff.normalize()
        magnitude = (G * self.mass) / (dist * dist)

        return direction * magnitude


class PhysicsWorld:
    """
    Manages the Digital Physics interactions.
    Calculates the 'Tensor Field' created by all Entities and Attractors.
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.entities: List[Entity] = [] # Track all entities to calculate their mutual fields
        self.gravity_constant: float = 1.0
        self.coupling_constant: float = 0.5 # Strength of the Soul Force (Rifling)

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def register_entity(self, entity: Entity) -> None:
        if entity not in self.entities:
            self.entities.append(entity)

    def get_net_force(self, target_entity: Entity) -> Vector3:
        """
        Calculates the total force acting on a target entity.
        Includes:
        1. Gravity from Attractors (Simple Body Force)
        2. Tensor Fields from other Entities (Body + Soul + Spirit)
        """
        total_force = Vector3(0, 0, 0)
        pos = target_entity.physics.position

        # 1. Attractor Gravity
        for att in self.attractors:
            total_force = total_force + att.calculate_force(pos, self.gravity_constant)

        # 2. Entity Tensor Fields
        for source in self.entities:
            if source.id == target_entity.id:
                continue

            # Calculate vector to source
            diff = source.physics.position - pos
            dist = diff.magnitude
            if dist < 0.1:
                continue # Too close, avoid singularity

            direction = diff.normalize()

            # --- A. BODY FORCE (Gravity/Amplitude) ---
            # F_g = G * (Amp1 * Amp2) / r^2
            # Use source amplitude as Mass. If target has no soul, use mass 1.
            m1 = source.soul.amplitude if source.soul else 10.0
            m2 = target_entity.soul.amplitude if target_entity.soul else 1.0

            grav_mag = (self.gravity_constant * m1 * m2) / (dist * dist)
            total_force = total_force + (direction * grav_mag)

            # --- B. SOUL/SPIRIT FORCE (Rifling/Coil) ---
            # If both have souls, they interact via the Tensor Field
            if source.soul and target_entity.soul:
                # 1. Resonance (Do we attract or repel based on phase?)
                # In-Phase = Attraction, Out-Phase = Repulsion/Damping
                resonance_data = source.soul.resonate(target_entity.soul)
                resonance = resonance_data['resonance'] # -1 to 1

                # 2. Rifling (Spiral Motion)
                # The source creates a "Spinning" field around it.
                # Force direction is Perpendicular to the radius (Curl).
                # Cross product of Direction and Up Vector (roughly)
                # For 3D, we can define the spin axis as (0,1,0) or arbitrary.
                # Let's assume the Spin Axis is the direction of the source's velocity?
                # Or just a fixed vertical axis for this simplified simulation?
                # User said "Spiral", "Rifling".

                # Let's use the Cross Product to create a tangential force.
                # Tangent = Cross(Direction, Up)
                up = Vector3(0, 1, 0)
                tangent = direction.cross(up).normalize()

                # Force Magnitude depends on Frequency (Energy) and Spin direction
                # F_spin = Coupling * Freq * Spin / Distance
                spin_mag = (self.coupling_constant * source.soul.frequency * source.soul.spin) / dist

                # Apply Resonance:
                # If resonating, the spiral pulls them in tighter (adds to gravity).
                # If dissonant, it pushes them away or creates chaos.

                # Let's say:
                # Resonance modifies the Gravity (already done implicitly? No, let's add it)
                # High Resonance -> Stronger Pull
                total_force = total_force + (direction * (grav_mag * resonance * 0.5))

                # Spin Force adds the "Dance"
                total_force = total_force + (tangent * spin_mag)

        return total_force
