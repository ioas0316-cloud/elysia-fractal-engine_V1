from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, TYPE_CHECKING
import math
import random

# We'll use simple vector/quat classes if available or pure python implementation
# Assuming math_utils or simple implementation
from .tensor import SoulTensor

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> 'Vector3':
        m = self.magnitude
        if m == 0: return Vector3(0,0,0)
        return Vector3(self.x/m, self.y/m, self.z/m)

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )

    def dot(self, other: 'Vector3') -> float:
        return self.x*other.x + self.y*other.y + self.z*other.z

@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def rotate(self, v: Vector3) -> Vector3:
        # Simple implementation
        # q * v * q_inv
        # For now return identity
        return v

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
    Calculates the 'Tensor Field' created by all Entities and Attractors.
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.entities: List[Any] = [] # Track all entities to calculate their mutual fields
        self.gravity_constant: float = 1.0
        self.coupling_constant: float = 0.5 # Strength of the Soul Force (Rifling)
        self.time_scale: float = 1.0
        self.holographic_boundary: Optional[HolographicBoundary] = None
        self.spacetime_torsion: Optional[Quaternion] = None

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def register_entity(self, entity: Any) -> None:
        if entity not in self.entities:
            self.entities.append(entity)

    def configure_holographic_boundary(self, boundary: HolographicBoundary) -> None:
        """
        Sets a holographic shell to approximate potentials using boundary data only.
        """
        self.holographic_boundary = boundary

    def calculate_potential(self, position: Vector3, target_soul: Optional[SoulTensor] = None) -> float:
        """
        Calculates the Scalar Potential (Energy Landscape) at a given point.
        Low Potential = Valley (Attraction). High Potential = Hill (Repulsion).
        V = -G * M / r * (1 + Resonance_Coupling)
        """
        potential = 0.0

        if self.holographic_boundary:
            holographic_val = self.holographic_boundary.sample(position)
            if holographic_val is not None:
                potential += holographic_val

        # Target properties (default to generic matter if None)
        t_polarity = target_soul.polarity if target_soul else 1.0
        t_phase = target_soul.phase if target_soul else 0.0

        # 1. Attractor Potential
        for att in self.attractors:
            dist = (att.position - position).magnitude
            if dist < 0.1: dist = 0.1

            base_potential = - (self.gravity_constant * att.mass) / dist

            # Apply Resonance if Attractor has a Soul
            if att.soul:
                interaction_sign = att.soul.polarity * t_polarity
                resonance_factor = 0.0
                if target_soul:
                    # Phase Resonance
                    delta_phase = abs(att.soul.phase - t_phase)
                    if delta_phase > math.pi: delta_phase = (2 * math.pi) - delta_phase
                    phase_factor = math.cos(delta_phase)

                    # Frequency Resonance (Color Match)
                    # Like attracts Like: Higher resonance if frequencies are close.
                    f_diff = abs(att.soul.frequency - target_soul.frequency)
                    freq_factor = math.exp(-f_diff * 0.02) # Tuning: 50Hz diff -> exp(-1) = 0.36

                    # Combined Resonance
                    resonance = phase_factor * (0.5 + 0.5 * freq_factor)
                    resonance_factor = resonance * 1.0 # Stronger coupling

                total_factor = interaction_sign * (1.0 + resonance_factor)
                potential += base_potential * total_factor
            else:
                potential += base_potential

        # 2. Entity Field Potential
        for source in self.entities:
            # Skip if source doesn't have physics position
            if not hasattr(source, 'physics') or not hasattr(source, 'soul'):
                continue

            dist = (source.physics.position - position).magnitude
            if dist < 0.1: dist = 0.1

            m1 = source.soul.amplitude if source.soul else 10.0
            base_potential = - (self.gravity_constant * m1) / dist

            # If source has soul, apply Phase/Resonance and Polarity
            if source.soul:
                # A. Polarity Interaction (Matter vs Antimatter)
                interaction_sign = source.soul.polarity * t_polarity

                # B. Phase Resonance (Gauge Field)
                resonance_factor = 0.0
                if target_soul:
                    # Phase Resonance
                    delta_phase = abs(source.soul.phase - t_phase)
                    if delta_phase > math.pi: delta_phase = (2 * math.pi) - delta_phase
                    phase_factor = math.cos(delta_phase) # -1 to 1

                    # Frequency Resonance
                    f_diff = abs(source.soul.frequency - target_soul.frequency)
                    freq_factor = math.exp(-f_diff * 0.02)

                    resonance = phase_factor * (0.5 + 0.5 * freq_factor)
                    resonance_factor = resonance * 1.0 # Stronger coupling

                total_factor = interaction_sign * (1.0 + resonance_factor)
                potential += base_potential * total_factor

            else:
                potential += base_potential

        return potential

    def get_geodesic_flow(self, target_entity: Any) -> Vector3:
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
        spin_force = Vector3(0,0,0)
        for source in self.entities:
            if not hasattr(source, 'id') or source.id == target_entity.id: continue
            if not hasattr(source, 'soul') or not source.soul: continue
            if not target_entity.soul: continue

            diff = source.physics.position - pos
            dist = diff.magnitude
            if dist < 0.1: continue

            direction = diff.normalize()
            up = Vector3(0, 1, 0)
            tangent = direction.cross(up).normalize()

            # F_spin = Coupling * Freq * Spin / Distance
            spin_mag = (self.coupling_constant * source.soul.frequency * source.soul.spin) / dist

            interaction = source.soul.polarity * polarity
            spin_mag *= interaction

            spin_force = spin_force + (tangent * spin_mag)

        # --- QUANTUM TUNNELING CHECK ---
        dot_prod = flow.dot(target_entity.physics.velocity)
        if dot_prod < -0.1 and target_entity.soul and not target_entity.soul.is_collapsed:
            barrier_height = self.calculate_potential(pos + target_entity.physics.velocity.normalize(), target_entity.soul)

            energy_diff = target_entity.soul.frequency - barrier_height

            if energy_diff <= 0:
                # Quantum Tunneling attempt
                prob = math.exp(energy_diff * 0.1)
                if random.random() < prob:
                    # TUNNEL!
                    tunnel_dist = 2.0
                    target_entity.physics.position = target_entity.physics.position + (target_entity.physics.velocity.normalize() * tunnel_dist)
                    return Vector3(0,0,0)

        return flow + spin_force
