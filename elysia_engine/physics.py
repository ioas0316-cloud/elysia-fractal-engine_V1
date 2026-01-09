from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING, Tuple, Dict, Any
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
class SensoryPacket:
    """
    Represents the 'Human Standard' perception of the 4D Field.
    Maps hyperspace fields to somatic senses.
    Now expanded to include Olfactory (Smell) and Gustatory (Taste).
    """
    visual_clarity: float = 0.0      # X-Field: Texture/Sight
    auditory_resonance: float = 0.0  # Y-Field: Harmony/Hearing
    haptic_pressure: float = 0.0     # W-Field: Gravity/Touch
    vestibular_balance: float = 0.0  # Z-Field: Spin/Balance

    olfactory_essence: float = 0.0   # Y-Gradient: Smell (Change in Frequency)
    gustatory_chemistry: float = 0.0 # Resonance * W: Taste (Consumable Energy)

    narrative: str = ""              # Cognitive interpretation

    def as_dict(self) -> Dict[str, Any]:
        return {
            "vision": self.visual_clarity,
            "hearing": self.auditory_resonance,
            "touch": self.haptic_pressure,
            "balance": self.vestibular_balance,
            "smell": self.olfactory_essence,
            "taste": self.gustatory_chemistry,
            "narrative": self.narrative
        }

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
    Now includes 'Perception-Field Mapping' to handle Soul Gaze and Experience.
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

    def get_geodesic_flow(self, target_entity: Entity) -> Tuple[Vector3, Optional[Rotor]]:
        """
        Calculates the movement vector based on the Field System.
        Now returns Tuple(Force, Rotor) to allow torque application.
        """
        pos = target_entity.physics.position
        pos4 = Vector4(0, pos.x, pos.y, pos.z)

        if not target_entity.soul:
             return Vector3(0,0,0), None

        # Get Force from Field
        force4, rotor = self.field_system.get_local_forces(pos4, target_entity.soul)

        # Convert back to Vec3 (ignore W force for now)
        force = Vector3(force4.x, force4.y, force4.z)

        # Add Intent (Self-Propulsion)
        intent_force = Vector3(0,0,0)
        if target_entity.soul and not target_entity.soul.is_collapsed:
             forward_ref = Vector3(0, 0, 1)
             intent_direction = target_entity.soul.orientation.rotate(forward_ref)
             intent_mag = target_entity.soul.amplitude * 0.1
             intent_force = intent_direction * intent_mag

        total_force = force + intent_force

        return total_force, rotor

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

    def perceive(self, entity: Entity, range_dist: float = 2.0) -> SensoryPacket:
        """
        Perception-Field Mapping:
        The Soul projects its internal state (Phase/Frequency) onto the Field via the Hypersphere (Orientation).
        Returns a SensoryPacket (Human Standard).
        Now includes Olfactory (Frequency Gradient) and Gustatory (Resonance Density).
        """
        if not entity.soul:
             return SensoryPacket()

        # 1. Determine Gaze Direction (Hypersphere Rotation)
        forward_ref = Vector3(0, 0, 1)
        gaze_dir = entity.soul.orientation.rotate(forward_ref)

        # 2. Sample the Field at Target
        target_pos = entity.physics.position + gaze_dir * range_dist
        target_pos4 = Vector4(0, target_pos.x, target_pos.y, target_pos.z)

        # Sample Field at Observer (for gradient/contrast)
        obs_pos = entity.physics.position
        obs_pos4 = Vector4(0, obs_pos.x, obs_pos.y, obs_pos.z)

        # Field values: W (Scale), X (Texture), Y (Freq), Z (Spin)
        field_vals = self.field_system.spatial_map.sample_field(target_pos4, current_tick=self.field_system.time_tick)
        w, x, y, z = field_vals

        obs_vals = self.field_system.spatial_map.sample_field(obs_pos4, current_tick=self.field_system.time_tick)
        obs_y = obs_vals[2] # Observer local frequency

        # 3. Calculate Metrics

        # Resonance (Hearing)
        freq_diff = abs(entity.soul.frequency - y)
        resonance = 1.0 / (1.0 + freq_diff)

        # Gradient (Smell): Change in Y-Field (Frequency) over the gaze vector
        # Measures the "Scent Trail"
        y_gradient = abs(y - obs_y)
        smell_intensity = y_gradient * 0.1 # Scaling

        # Consumable Energy (Taste): Density (W) * Resonance
        # High Energy + High Resonance = Sweet/Rich
        # High Energy + Low Resonance = Bitter/Rotten
        taste_value = w * resonance

        # 4. Map to Human Senses
        vision = x
        hearing = resonance
        touch = w
        balance = z
        smell = smell_intensity
        taste = taste_value

        # 5. Narrative Interpretation
        narrative = ""

        # Base Atmosphere
        if resonance > 0.9:
            narrative = "I feel a profound peace."
        elif resonance < 0.1:
            narrative = "The world feels chaotic and alien."
        else:
            narrative = "I sense a mixture of familiar and strange."

        # Scent
        if smell > 2.0:
            if y > 100: narrative += " A sharp, metallic scent hangs in the air."
            elif y < 0: narrative += " The air smells of damp earth and decay."
            else: narrative += " A strong, complex aroma wafts nearby."
        elif smell > 0.5:
            if y > 50: narrative += " A faint floral scent."
            else: narrative += " A subtle musky odor."

        # Taste (if close/intense)
        if taste > 5.0:
            if resonance > 0.8: narrative += " The atmosphere tastes sweet and nourishing."
            else: narrative += " A bitter, metallic taste fills my mouth."

        if touch > 2.0:
            narrative += " The air is heavy."
        if balance > 0.5:
            narrative += " I feel dizzy."

        return SensoryPacket(
            visual_clarity=vision,
            auditory_resonance=hearing,
            haptic_pressure=touch,
            vestibular_balance=balance,
            olfactory_essence=smell,
            gustatory_chemistry=taste,
            narrative=narrative
        )

    def apply_soul_torque(self, entity: Entity, rotor: Optional[Rotor]) -> None:
        """
        Applies the Field's Spin (Z-Field Torque) to the Soul's Orientation.
        This represents the 'Hypersphere Stabilization' or 'Gyroscope'.
        """
        if not entity.soul or not rotor:
            return

        # Rotor is 4D. Soul Orientation is 3D Quaternion.
        # We assume the rotor represents a spatial rotation (xy, yz, zx planes).
        # We extract a simplified axis-angle or convert directly if possible.
        # For optimization, we take the 'xy' plane component of the rotor as Z-axis rotation?
        # A full Rotor to Quaternion conversion is complex in Cl(4,0).
        # But we know get_local_forces constructs the rotor from 'xy' plane angle.
        # R = cos(t/2) - B_xy sin(t/2). This corresponds to Z-axis rotation.

        # Extract angle from rotor.a (scalar part)
        # cos(theta/2) = rotor.a
        # theta = 2 * acos(a)
        # Axis is determined by bivectors.
        # If b_xy is dominant, it's Z-axis rotation.

        # Simplification: Convert Rotor to Quaternion (assuming 3D subset)
        # q = a + b_yz i + b_zx j + b_xy k ? (Dual mapping)
        # standard: b_yz -> x, b_zx -> y, b_xy -> z

        # Let's try to apply a small rotation based on rotor strength
        # We trust the rotor is normalized.

        # Mapping GA Bivectors to Quaternions:
        # B_yz (plane yz) rotates around X -> q.x
        # B_zx (plane zx) rotates around Y -> q.y
        # B_xy (plane xy) rotates around Z -> q.z

        # Note: Rotor definition in math_utils has b_xz, not b_zx. b_xz = -b_zx.

        q_rot = Quaternion(
            w = rotor.a,
            x = -rotor.b_yz, # Convention check needed, assuming - due to duality
            y = rotor.b_xz,  # b_xz is -b_zx
            z = -rotor.b_xy
        )

        # Apply rotation: q_new = q_rot * q_old
        entity.soul.orientation = (q_rot * entity.soul.orientation).normalize()

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
            force, rotor = self.get_geodesic_flow(entity)

            # Apply Translation
            entity.physics.apply_force(force, dt)
            entity.physics.step(dt)

            # Apply Rotation (Perception/Gyroscope)
            self.apply_soul_torque(entity, rotor)

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
        flow, _ = self.get_geodesic_flow(target_entity)

        # Check for Dimensional Evolution opportunities
        self.check_dimensional_binding(target_entity)

        # Apply spacetime torsion (optional rotation of the flow field)
        if self.spacetime_torsion:
            return self.spacetime_torsion.rotate(flow)

        return flow
