from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import math

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

    @property
    def kinetic_energy(self) -> float:
        """K = 0.5 * m * v^2"""
        v_sq = self.velocity.dot(self.velocity)
        return 0.5 * self.mass * v_sq


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

    def potential_energy(self, target_pos: Vector3, G: float = 1.0) -> float:
        """
        U = -G * M / r (Gravitational Potential per unit mass)
        Negative because it's a bound state (well).
        """
        dist = (self.position - target_pos).magnitude
        if dist < 0.1:
            dist = 0.1 # Clamp to avoid infinity
        return -(G * self.mass) / dist


class PhysicsWorld:
    """
    Manages the physical interactions (Gravity, etc).
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.gravity_constant: float = 1.0
        self.potential_barriers: List[dict] = [] # Simple barriers: {pos, radius, height}

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def add_barrier(self, position: Vector3, radius: float, height: float) -> None:
        """Adds a region of High Potential (Energy Wall)."""
        self.potential_barriers.append({
            "position": position,
            "radius": radius,
            "height": height
        })

    def get_net_force(self, position: Vector3) -> Vector3:
        """Sum of all gravitational forces at a given position."""
        total_force = Vector3(0, 0, 0)
        for att in self.attractors:
            total_force = total_force + att.calculate_force(position, self.gravity_constant)
        return total_force

    def get_potential_energy(self, position: Vector3) -> float:
        """
        Calculates the total potential energy U at a position.
        U_total = Sum(U_attractor) + Sum(U_barrier)
        """
        u_total = 0.0

        # Attractors (Wells, negative energy)
        for att in self.attractors:
            u_total += att.potential_energy(position, self.gravity_constant)

        # Barriers (Walls, positive energy)
        for bar in self.potential_barriers:
            dist = (position - bar["position"]).magnitude
            if dist < bar["radius"]:
                # Simple rectangular barrier or Gaussian?
                # Let's use a Gaussian-like hill for smooth gradients
                # H * exp(-dist^2 / sigma)
                # But strictly inside radius for now to match "Wall" concept
                u_total += bar["height"] * (1.0 - (dist / bar["radius"]))

        return u_total


class HamiltonianSystem:
    """
    Implements the Hamiltonian (H = T + U).
    Total Energy = Kinetic + Potential.
    """
    def __init__(self, world: PhysicsWorld) -> None:
        self.world = world

    def calculate_hamiltonian(self, state: PhysicsState) -> float:
        """Returns H = T + U"""
        kinetic = state.kinetic_energy
        potential = self.world.get_potential_energy(state.position)
        # Potential is per unit mass in current Attractor code?
        # Attractor.potential_energy is -GM/r.
        # Real U = m * (-GM/r).
        # Let's scale U by mass to be physically consistent.
        potential_total = potential * state.mass

        return kinetic + potential_total
