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

    def calculate_potential(self, position: Vector3, target_soul: Optional[SoulTensor] = None) -> float:
        """
        Calculates the Scalar Potential (Energy Landscape) at a given point.
        Low Potential = Valley (Attraction). High Potential = Hill (Repulsion).
        V = -G * M / r * (1 + Resonance_Coupling)
        """
        potential = 0.0

        # Target properties (default to generic matter if None)
        t_polarity = target_soul.polarity if target_soul else 1.0
        t_phase = target_soul.phase if target_soul else 0.0

        # 1. Attractor Potential
        for att in self.attractors:
            dist = (att.position - position).magnitude
            if dist < 0.1: dist = 0.1
            potential -= (self.gravity_constant * att.mass) / dist

        # 2. Entity Field Potential
        for source in self.entities:
            dist = (source.physics.position - position).magnitude
            if dist < 0.1: dist = 0.1

            m1 = source.soul.amplitude if source.soul else 10.0
            base_potential = - (self.gravity_constant * m1) / dist

            # If source has soul, apply Phase/Resonance and Polarity
            if source.soul:
                # A. Polarity Interaction (Matter vs Antimatter)
                interaction_sign = source.soul.polarity * t_polarity

                # B. Phase Resonance (Gauge Field)
                # "Force is born from Phase"
                # If phases align (resonance > 0), gravity is stronger (Deep Valley).
                # If phases clash (resonance < 0), gravity is weaker or repels.

                resonance_factor = 0.0
                if target_soul:
                    # Calculate raw phase difference at this hypothetical position?
                    # Technically phase is internal, not spatial. But we use the target's current phase.
                    delta_phase = abs(source.soul.phase - t_phase)
                    if delta_phase > math.pi: delta_phase = (2 * math.pi) - delta_phase
                    resonance = math.cos(delta_phase) # -1 to 1

                    resonance_factor = resonance * 0.5 # Coupling strength

                # Combine:
                # New Potential = Base * Sign * (1 + Resonance)
                # If Sign is +1 (Matter-Matter):
                #   Base (-50) * 1 * (1 + 0.5) = -75 (Strong Attraction)
                #   Base (-50) * 1 * (1 - 0.5) = -25 (Weak Attraction)
                # If Sign is -1 (Matter-Antimatter):
                #   Base (-50) * -1 * (...) = +50 (Repulsion)

                # Note: If resonance is strongly negative (-1), (1 + -0.5) = 0.5. Still attractive but weak.
                # Unless resonance coupling is > 1.0, phase alone won't repel matter-matter.
                # This aligns with "Gravity is always attractive" but "Love makes it stronger".

                total_factor = interaction_sign * (1.0 + resonance_factor)
                potential += base_potential * total_factor

            else:
                potential += base_potential

        return potential

    def get_geodesic_flow(self, target_entity: Entity) -> Vector3:
        """
        Calculates the movement vector based on the Gradient of the Potential Field.
        Entities 'slide' down the curvature of space.
        Flow = -Gradient(Potential)
        """
        pos = target_entity.physics.position
        epsilon = 0.1

        # Pass the full soul for resonance calculation
        soul = target_entity.soul

        # Define polarity locally (default 1.0) for use in spin force
        polarity = soul.polarity if soul else 1.0

        # Calculate Gradient using Finite Differences
        v_center = self.calculate_potential(pos, soul)
        v_x = self.calculate_potential(pos + Vector3(epsilon, 0, 0), soul)
        v_y = self.calculate_potential(pos + Vector3(0, epsilon, 0), soul)
        v_z = self.calculate_potential(pos + Vector3(0, 0, epsilon), soul)

        grad_x = (v_x - v_center) / epsilon
        grad_y = (v_y - v_center) / epsilon
        grad_z = (v_z - v_center) / epsilon

        gradient = Vector3(grad_x, grad_y, grad_z)

        # The force/flow is naturally opposite to the gradient (Downhill)
        flow = gradient * -1.0

        # --- ADDING SPIRAL (GAUGE FIELD) ---
        # The simple scalar potential doesn't capture the "Curl" or "Spin".
        # We add the Tangential component explicitly here as the "Magnetic" part of the field.

        spin_force = Vector3(0,0,0)
        for source in self.entities:
            if source.id == target_entity.id: continue
            if not source.soul or not target_entity.soul: continue

            diff = source.physics.position - pos
            dist = diff.magnitude
            if dist < 0.1: continue

            direction = diff.normalize()
            up = Vector3(0, 1, 0)
            tangent = direction.cross(up).normalize()

            # F_spin = Coupling * Freq * Spin / Distance
            spin_mag = (self.coupling_constant * source.soul.frequency * source.soul.spin) / dist

            # Apply Polarity to Spin too?
            # If space is inverted, does the spin direction flip?
            # Let's assume yes.
            interaction = source.soul.polarity * polarity
            spin_mag *= interaction

            spin_force = spin_force + (tangent * spin_mag)

        return flow + spin_force

    def check_dimensional_binding(self, entity: Entity) -> None:
        """
        Checks if the entity should evolve dimensionally (Point -> Line).
        """
        if not entity.soul or entity.soul.is_collapsed:
            return

        for other in self.entities:
            if other.id == entity.id: continue
            if not other.soul: continue

            # Check proximity
            dist = (entity.physics.position - other.physics.position).magnitude
            if dist < 2.0:
                # Check Resonance
                res = entity.soul.resonate(other.soul)
                if res['resonance'] > 0.9: # Very high harmony
                    # Bind them! (Abstractly for now)
                    # In a full implementation, we would create a "Bond" object.
                    # For now, we just log or tag them.
                    if other.id not in entity.bonds:
                        entity.bonds.append(other.id)
                    if entity.id not in other.bonds:
                        other.bonds.append(entity.id)

    def get_net_force(self, target_entity: Entity) -> Vector3:
        """
        Legacy wrapper. Now delegates to Geodesic Flow.
        """
        flow = self.get_geodesic_flow(target_entity)

        # Check for Dimensional Evolution opportunities
        self.check_dimensional_binding(target_entity)

        return flow
