from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .math_utils import Vector3


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
    Acts as a gravity well.
    """
    id: str
    position: Vector3
    mass: float = 100.0  # Standard mass for an answer
    radius: float = 1.0  # Event horizon/Capture radius

    def calculate_force(self, target_pos: Vector3, G: float = 1.0) -> Vector3:
        """
        Calculates gravitational force: F = G * (M*m) / r^2 * direction
        Assumes target mass is 1 for field calculation purposes if not specified.
        """
        diff = self.position - target_pos
        dist = diff.magnitude

        # Prevent singularity at distance 0
        if dist < 0.001:
            return Vector3(0, 0, 0)

        # Normalized direction
        direction = diff.normalize()

        # F = G * M / r^2 (Force per unit mass of the target)
        magnitude = (G * self.mass) / (dist * dist)

        return direction * magnitude


class PhysicsWorld:
    """
    Manages the physical interactions (Gravity, etc).
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.gravity_constant: float = 1.0

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def get_net_force(self, position: Vector3) -> Vector3:
        """Sum of all gravitational forces at a given position."""
        total_force = Vector3(0, 0, 0)
        for att in self.attractors:
            total_force = total_force + att.calculate_force(position, self.gravity_constant)
        return total_force
