from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING, Tuple
import math
import random

from .math_utils import Vector3, Vector4, Quaternion, Rotor
from .tensor import SoulTensor
from .field import FieldSystem

if TYPE_CHECKING:
    from .entities import Entity


@dataclass
class HolographicBoundary:
    """
    Boundary-only sampler (Holographic Principle).
    Stores potential values on a surface and interpolates for interior points.
    """
    samples: List[Tuple[Vector3, float]] = field(default_factory=list)
    thickness: float = 0.1

    @staticmethod
    def spherical_shell(radius: float = 10.0, resolution: int = 6, center: Optional[Vector3] = None, base_potential: float = -1.0) -> 'HolographicBoundary':
        """
        Builds a simple spherical shell by sampling longitude/latitude rings.
        """
        if center is None:
            center = Vector3(0, 0, 0)

        samples: List[Tuple[Vector3, float]] = []
        # Rough grid on the sphere surface
        for i in range(resolution):
            theta = (i / resolution) * math.pi  # 0..pi
            for j in range(resolution * 2):
                phi = (j / (resolution * 2)) * (2 * math.pi)  # 0..2pi
                x = radius * math.sin(theta) * math.cos(phi) + center.x
                y = radius * math.cos(theta) + center.y
                z = radius * math.sin(theta) * math.sin(phi) + center.z
                samples.append((Vector3(x, y, z), base_potential))
        return HolographicBoundary(samples=samples, thickness=0.25)

    def sample(self, point: Vector3) -> Optional[float]:
        """
        Returns the interpolated potential from boundary samples.
        Uses inverse-distance weighting; zero thickness acts as pure shell.
        """
        if not self.samples:
            return None

        weighted = 0.0
        weight_sum = 0.0
        for pos, potential in self.samples:
            dist = (pos - point).magnitude
            if dist <= self.thickness:
                return potential

            # Inverse distance weighting to approximate interior field
            weight = 1.0 / (dist + 1e-6)
            weighted += weight * potential
            weight_sum += weight

        if weight_sum == 0:
            return None
        return weighted / weight_sum

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
    Acts as a Gravity Well. Now includes SoulTensor for Resonance Gravity.
    """
    id: str
    position: Vector3
    mass: float = 100.0  # Standard mass for an answer
    radius: float = 1.0  # Event horizon/Capture radius
    soul: Optional[SoulTensor] = None # Resonance Gravity

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
    TRANSITION: Moving from O(N^2) Particle Interaction to O(Res) Field System.
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.entities: List[Entity] = []
        self.gravity_constant: float = 1.0
        self.coupling_constant: float = 0.5
        self.time_scale: float = 1.0
        self.holographic_boundary: Optional[HolographicBoundary] = None
        self.spacetime_torsion: Optional[Quaternion] = None

        # New Field System
        self.field_system = FieldSystem()

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def register_entity(self, entity: Entity) -> None:
        if entity not in self.entities:
            self.entities.append(entity)

    def configure_holographic_boundary(self, boundary: HolographicBoundary) -> None:
        """
        Sets a holographic shell to approximate potentials using boundary data only.
        """
        self.holographic_boundary = boundary

    def update_field(self) -> None:
        """
        Updates the Field System based on current entities.
        Replaces the pairwise 'potential' calculation setup.
        """
        # Collect active entities (Optimization: Filter by velocity or range?)
        active_data = []
        for ent in self.entities:
            if ent.soul:
                # Convert Vec3 to Vec4 (W=0 for now, or use mass as W scale?)
                # Default W=0 implies standard depth.
                pos4 = Vector4(0, ent.physics.position.x, ent.physics.position.y, ent.physics.position.z)
                active_data.append((pos4, ent.soul))

        # Include Attractors in the Field Logic
        # Attractors are effectively static, heavy entities
        for att in self.attractors:
             pos4 = Vector4(0, att.position.x, att.position.y, att.position.z)
             # Create a pseudo-soul for the attractor if it doesn't have one
             # Mass -> Amplitude
             soul = att.soul
             if not soul:
                 # Default attractor soul: High Mass, Neutral Freq
                 soul = SoulTensor(amplitude=att.mass, frequency=0.0, phase=0.0)

             active_data.append((pos4, soul))

        self.field_system.update_field(active_data)

    def calculate_potential(self, position: Vector3, target_soul: Optional[SoulTensor] = None) -> float:
        """
        Legacy: Calculates Potential from Field System instead of Iteration.
        """
        # Map Vec3 to Vec4
        pos4 = Vector4(0, position.x, position.y, position.z)

        # Sample Field
        # We use Y-Field as the Potential Analogue (Elevation/Frequency)
        # Low Frequency (Abyss) vs High Frequency (Heaven).
        # Gravity usually pulls towards Mass (W-Field).

        # [Fix Ghost Field] Pass current time tick to ensure fresh data
        w, x, y, z = self.field_system.spatial_map.sample_field(pos4, current_tick=self.field_system.time_tick)

        # Interpret Potential:
        # Classical Gravity is defined by Mass density (W).
        # V ~ -W (High density = Low potential = Attraction)
        return -w * 100.0 # Scale factor

    def get_geodesic_flow(self, target_entity: Entity) -> Vector3:
        """
        Calculates the movement vector based on the Field System.
        """
        pos = target_entity.physics.position
        pos4 = Vector4(0, pos.x, pos.y, pos.z)

        if not target_entity.soul:
             return Vector3(0,0,0)

        # Get Force from Field
        force4, rotor = self.field_system.get_local_forces(pos4, target_entity.soul)

        # Convert back to Vec3 (ignore W force for now)
        force = Vector3(force4.x, force4.y, force4.z)

        # Apply Rotor Torque?
        # If the field spins, the entity's velocity vector should rotate.
        # v' = R v R~
        # We apply this to the current velocity, not force.
        # But here we return Force/Flow vector.
        # Let's add a "Coriolis" term from the Rotor.

        # Tangential velocity induced by rotor?
        # Simple approximation: Add a tangent vector.
        # For now, we trust get_local_forces returns the linear force component.

        # Add Intent (Self-Propulsion)
        intent_force = Vector3(0,0,0)
        if target_entity.soul and not target_entity.soul.is_collapsed:
             forward_ref = Vector3(0, 0, 1)
             intent_direction = target_entity.soul.orientation.rotate(forward_ref)
             intent_mag = target_entity.soul.amplitude * 0.1
             intent_force = intent_direction * intent_mag

        total_force = force + intent_force

        return total_force

    def check_dimensional_binding(self, entity: Entity) -> None:
        """
        Checks if the entity should evolve dimensionally (Point -> Line).
        And promotes Entanglement.
        """
        if not entity.soul or entity.soul.is_collapsed:
            return

        # TODO: Optimize binding check using Field Spatial Map (Neighbors)
        # For now, legacy O(N) loop is kept but should be replaced by:
        # neighbors = field.get_neighbors(entity.pos)

        for other in self.entities:
            if other.id == entity.id: continue
            if not other.soul: continue

            # Check proximity
            dist = (entity.physics.position - other.physics.position).magnitude
            if dist < 2.0:
                # Check Resonance
                res = entity.soul.resonate(other.soul)

                # BINDING (Fractal Evolution)
                if res['resonance'] > 0.9: # Very high harmony
                    # Bind them!
                    if other.id not in entity.bonds:
                        entity.bonds.append(other.id)
                        # Promote Dimension if not already
                        if entity.dimension == 0: entity.dimension = 1

                    if entity.id not in other.bonds:
                        other.bonds.append(entity.id)
                        if other.dimension == 0: other.dimension = 1

                    # 2D Promotion Check (Triangle)
                    # If I have 2 bonds, I might be a Plane?
                    if len(entity.bonds) >= 2:
                        entity.dimension = 2

                # ENTANGLEMENT (Quantum Link)
                # If they are very close and harmonic, they entangle
                if dist < 0.5 and res['resonance'] > 0.95:
                    entity.soul.entangle(other.soul)

    def step(self, dt: float) -> None:
        """
        The Main Simulation Loop.
        1. Update Field (O(Res))
        2. Move Entities (O(N))
        """
        # 1. Bloom the Field (Eulerian Step)
        self.update_field()

        # 2. Move Entities (Lagrangian Step)
        for entity in self.entities:
            # Calculate Flow from Field
            force = self.get_geodesic_flow(entity)

            # Apply Physics
            entity.physics.apply_force(force, dt)
            entity.physics.step(dt)

            # Check Evolution
            self.check_dimensional_binding(entity)

    def get_net_force(self, target_entity: Entity) -> Vector3:
        """
        Legacy wrapper. Now delegates to Geodesic Flow.
        Note: This assumes update_field() has been called recently.
        """
        flow = self.get_geodesic_flow(target_entity)

        # Check for Dimensional Evolution opportunities
        self.check_dimensional_binding(target_entity)

        # Apply spacetime torsion (optional rotation of the flow field)
        if self.spacetime_torsion:
            return self.spacetime_torsion.rotate(flow)

        return flow
