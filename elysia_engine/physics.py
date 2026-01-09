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

# --- Atmospheric Governance Constants ---
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2
HORIZON_FREQUENCY = GOLDEN_RATIO  # The Universal Tuning Fork
ABYSS_THRESHOLD = 50.0            # Mass/Entropy threshold for sedimentation
SEDIMENT_RATE = 100               # Update frequency for sediment (1/N ticks)

# Entropy Tuning
DATA_ENTROPY_SCALE = 0.01         # 100 chars = 1.0 Entropy
BOND_ENTROPY_SCALE = 1.0          # Each bond = 1.0 Entropy
RESONANCE_PENALTY_SCALE = 10.0    # 1.0 Hz deviation = 10.0 Entropy

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
    Now includes 'Atmospheric Governance' to manage complexity and entropy.
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.entities: List[Entity] = []
        self.sediments: List[Entity] = []  # The Abyss: Low frequency updates

        self.gravity_constant: float = 1.0
        self.coupling_constant: float = 0.5
        self.time_scale: float = 1.0
        self.tick: int = 0  # Universal Clock

        self.holographic_boundary: Optional[HolographicBoundary] = None
        self.spacetime_torsion: Optional[Quaternion] = None

        # New Field System
        self.field_system = FieldSystem()

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def register_entity(self, entity: Entity) -> None:
        if entity not in self.entities and entity not in self.sediments:
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

        # Include sediments in field generation?
        # Yes, they are "Soil", so they generate gravity but don't move often.
        # This gives the world "Depth" from the Abyss.
        all_entities = self.entities + self.sediments

        for ent in all_entities:
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

        # Scan active entities for binding
        # (Sediments are too deep to bind quickly, we only check active for performance)
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

    def calculate_entropy(self, entity: Entity) -> float:
        """
        Calculates the Complexity Entropy of an entity.
        Entropy = Data Complexity + Bond Complexity + Non-Resonance Penalty
        """
        # Calculate Data Weight (Sum of value sizes)
        data_weight = 0
        for val in entity.data.values():
            if isinstance(val, str):
                data_weight += len(val)
            elif hasattr(val, '__len__'):
                data_weight += len(val)
            else:
                data_weight += 1

        base_entropy = (data_weight * DATA_ENTROPY_SCALE) + (len(entity.bonds) * BOND_ENTROPY_SCALE)

        resonance_penalty = 0.0
        if entity.soul:
            # Check deviation from Horizon Frequency
            # Lower deviation = Lower entropy (Higher Harmony)
            delta = abs(entity.soul.frequency - HORIZON_FREQUENCY)
            resonance_penalty = delta * RESONANCE_PENALTY_SCALE

            # Aesthetic Filter: Golden Spiral Phase Alignment
            # Ideally phase should align with Golden Ratio harmonics
            # For now, simplistic resonance penalty is enough

        return base_entropy + resonance_penalty

    def apply_atmospheric_governance(self, entity: Entity) -> None:
        """
        Applies the 3 Pillars of Guidance:
        1. Entropy Pressure -> Mass Increase
        2. Horizon Anchor -> Resonance Check
        3. Aesthetic Filter -> Dampening
        """
        entropy = self.calculate_entropy(entity)

        # 1. Complexity Entropy Pressure
        # Increase virtual mass based on entropy. Heavy things sink.
        # Base mass is 1.0, adds entropy weight.
        entity.physics.mass = max(1.0, 1.0 + entropy * 0.5)

        # 2. Aesthetic Filter (Dampening)
        # If entity is dissonant (high entropy), dampen its velocity
        if entropy > 10.0:
            entity.physics.velocity *= 0.95 # Air resistance/Drag

    def step(self, dt: float) -> None:
        """
        The Main Simulation Loop.
        1. Bloom the Field (Eulerian Step)
        2. Move Entities (Lagrangian Step) - with Sedimentation Logic
        """
        self.tick += 1

        # 1. Bloom the Field (Eulerian Step)
        self.update_field()

        # 2. Process Active Entities
        active_survivors = []
        for entity in self.entities:
            self.apply_atmospheric_governance(entity)

            # Check Sedimentation (The Abyss)
            if entity.physics.mass > ABYSS_THRESHOLD:
                # Sink to Abyss
                self.sediments.append(entity)
                # Do not add to active_survivors
                continue

            # Standard Physics
            force = self.get_geodesic_flow(entity)
            entity.physics.apply_force(force, dt)
            entity.physics.step(dt)
            self.check_dimensional_binding(entity)

            active_survivors.append(entity)

        self.entities = active_survivors

        # 3. Process Sediment Layer (The Abyss)
        # Only update every SEDIMENT_RATE ticks
        if self.tick % SEDIMENT_RATE == 0:
            sediment_survivors = []
            for entity in self.sediments:
                # Check if it became lighter (Redemption)
                self.apply_atmospheric_governance(entity)

                if entity.physics.mass <= ABYSS_THRESHOLD:
                    # Rise from Abyss
                    self.entities.append(entity)
                    continue

                # Minimal movement in Abyss (Drift)
                # No force calculation from field (too expensive), just inertia dampening
                entity.physics.velocity *= 0.9
                entity.physics.step(dt)
                sediment_survivors.append(entity)

            self.sediments = sediment_survivors

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
