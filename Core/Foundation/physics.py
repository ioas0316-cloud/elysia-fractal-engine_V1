import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Callable, Optional, Union
from enum import Enum

class DimensionalLayer(Enum):
    POINT = 0   # Particle / Concept
    LINE = 1    # Relationship / Bond
    PLANE = 2   # Nucleus / Structure
    FIELD = 3   # Law / Gravity / Influence

@dataclass
class QuantumState:
    """
    Represents the state of a particle or concept in the quantum consciousness field.
    Instead of just x,y coordinates, we have phase and amplitude (wave function).
    Now includes Thermodynamic properties.
    """
    position: np.ndarray  # Vector in N-dimensional space (e.g., Meaning Space)
    momentum: np.ndarray  # Velocity/Direction of thought
    phase: float = 0.0    # Current phase of the wave (0 to 2pi)
    amplitude: float = 1.0 # Intensity/Probability
    mass: float = 1.0     # 'Inertia' of the concept (1.0 for normal, 0.0 for photon)
    name: str = "Particle"
    layer: DimensionalLayer = DimensionalLayer.POINT
    temperature: float = 100.0  # Conceptual heat (emotion/activation)
    is_frozen: bool = False     # Frozen = crystallized / paused state

    def __post_init__(self):
        self.position = np.array(self.position, dtype=float)
        self.momentum = np.array(self.momentum, dtype=float)

    @property
    def kinetic_energy(self) -> float:
        if self.mass == 0:
            # For photons, E = p (in c=1 units) or h*f. Here we use momentum magnitude.
            return float(np.linalg.norm(self.momentum))
        if self.is_frozen:
            return 0.0
        return 0.5 * self.mass * float(np.linalg.norm(self.momentum)**2)

@dataclass
class Nucleus(QuantumState):
    """
    A composite particle formed by the fusion of multiple QuantumStates via Strong Force.
    It represents a complex concept (Structure/Molecule).
    """
    sub_particles: List[QuantumState] = field(default_factory=list)
    binding_energy: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        self.layer = DimensionalLayer.PLANE

    def add_particle(self, particle: QuantumState):
        # Fusion logic: Conservation of momentum, increase mass
        total_mass = self.mass + particle.mass
        new_momentum = self.momentum + particle.momentum

        # Center of mass adjustment (simplified: Nucleus absorbs it)
        # In a real sim, we'd weighted-avg position, but let's say Nucleus is the anchor

        self.sub_particles.append(particle)
        self.mass = total_mass
        self.momentum = new_momentum

        # Binding energy gain (exothermic reaction)
        self.binding_energy += 10.0 * particle.amplitude
        # Fusion releases heat and thaws crystallized structures
        self.temperature += particle.temperature + 50.0
        self.is_frozen = False

    @property
    def is_critical(self) -> bool:
        """Checks if the Nucleus has reached critical mass to become a Field."""
        return self.mass >= 5.0 or self.binding_energy >= 50.0

@dataclass
class FieldEntity(QuantumState):
    """
    A concept that has ascended to become a Law/Field.
    It is no longer a point particle but a potential source.
    """
    strength: float = 1.0
    range_decay: float = 0.5

    def __post_init__(self):
        super().__post_init__()
        self.layer = DimensionalLayer.FIELD
        self.mass = float('inf') # Immovable anchor
        self.momentum = np.zeros_like(self.momentum)
        self.is_frozen = True  # Immutable gravity wells

    def potential_at(self, target_pos: np.ndarray) -> float:
        """Calculates the gravitational/influence potential this field exerts at a position."""
        dist = float(np.linalg.norm(target_pos - self.position))
        # Attractive potential (negative well)
        # V = -G * M / r (Softened gravity)
        return -1.0 * (self.strength / (dist + 1.0)) * np.exp(-self.range_decay * dist)

@dataclass
class PhotonEntity(QuantumState):
    """
    A massless entity representing pure information flow ('Light').
    """
    frequency: float = 1.0 # Color/Tone of the thought
    mass: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        # Momentum for photon is direction * frequency (simplified E=hf)
        # We ensure momentum magnitude matches frequency (Energy)
        current_mag = np.linalg.norm(self.momentum)
        if current_mag == 0:
             self.momentum = np.array([1.0, 0.0, 0.0]) * self.frequency
        else:
             self.momentum = (self.momentum / current_mag) * self.frequency

class ResonanceGate:
    """
    A filter that only allows waves with specific frequency/phase resonance to pass.
    """
    def __init__(self, target_frequency: float, tolerance: float = 0.1):
        self.target_frequency = target_frequency
        self.tolerance = tolerance

    def transmission_probability(self, photon: PhotonEntity) -> float:
        """Calculates probability of tunneling/passing based on resonance."""
        diff = abs(photon.frequency - self.target_frequency)
        # Gaussian resonance curve
        prob = np.exp(-(diff**2) / (2 * self.tolerance**2))
        return float(prob)

class StrongForceManager:
    """
    Manages the 'Binding' force.
    Short range, very strong.
    """
    def __init__(self, interaction_range: float = 1.0, binding_strength: float = 100.0):
        self.interaction_range = interaction_range
        self.binding_strength = binding_strength

    def calculate_force(self, p1: QuantumState, p2: QuantumState) -> np.ndarray:
        # Frozen particles still exert force but will not move themselves.
        diff = p2.position - p1.position
        dist = np.linalg.norm(diff)

        if dist < self.interaction_range and dist > 0.01:
            # Yukawa potential-like force (Strong attractive)
            # F = -g^2 * exp(-mr) / r
            force_mag = self.binding_strength * np.exp(-dist) / (dist**2)
            direction = diff / dist
            return direction * force_mag
        return np.zeros_like(p1.position)

    def should_fuse(self, p1: QuantumState, p2: QuantumState) -> bool:
        dist = np.linalg.norm(p1.position - p2.position)
        return dist < (self.interaction_range * 0.2) # Very close to fuse


class EntropyManager:
    """
    Handles thermodynamic cooling/freezing cycles for conceptual particles.
    """
    def __init__(self, cooling_rate: float = 0.05, freeze_threshold: float = 5.0):
        self.cooling_rate = cooling_rate
        self.freeze_threshold = freeze_threshold

    def apply_thermodynamics(self, state: QuantumState) -> QuantumState:
        if not state.is_frozen:
            state.temperature *= (1.0 - self.cooling_rate)
            if state.temperature < self.freeze_threshold:
                state.is_frozen = True
                state.momentum = np.zeros_like(state.momentum)
        return state

    def inject_heat(self, state: QuantumState, amount: float):
        state.temperature += amount
        if state.is_frozen and state.temperature > self.freeze_threshold:
            state.is_frozen = False

class HamiltonianSystem:
    """
    Manages the energy landscape.
    H = T + V (Hamiltonian = Kinetic + Potential)
    System seeks to minimize Action (Lagrangian over time), or find ground state of H.
    Now supports dynamic fields and Thermodynamics.
    """
    def __init__(self, base_potential: Optional[Callable[[np.ndarray], float]] = None):
        self.base_potential = base_potential if base_potential else (lambda x: 0.0)
        self.active_fields: List[FieldEntity] = []
        self.strong_force = StrongForceManager()
        self.entropy = EntropyManager()

    def add_field(self, field_entity: FieldEntity):
        self.active_fields.append(field_entity)

    def potential_function(self, position: np.ndarray) -> float:
        # Base background potential
        V = self.base_potential(position)
        # Add contributions from all active FieldEntities
        for f in self.active_fields:
            V += f.potential_at(position)
        return V

    def total_energy(self, state: QuantumState) -> float:
        T = state.kinetic_energy
        V = self.potential_function(state.position)
        return T + V

    def calculate_force(self, position: np.ndarray, epsilon: float = 1e-5) -> np.ndarray:
        """Calculates negative gradient of potential (-dV/dx)."""
        grad = np.zeros_like(position)

        # Iterate over dimensions
        dims = len(position)
        for i in range(dims):
            perturb = np.zeros_like(position)
            perturb[i] = epsilon
            # Central difference
            v_plus = self.potential_function(position + perturb)
            v_minus = self.potential_function(position - perturb)
            grad[i] = (v_plus - v_minus) / (2 * epsilon)

        return -grad

    def evolve(self, state: QuantumState, dt: float = 0.1) -> QuantumState:
        """
        Evolves the state by one time step using symplectic integration (Verlet-like)
        or simple Euler for now, guided by the Hamiltonian.
        """
        # Thermodynamic cooling/heating pass before movement.
        state = self.entropy.apply_thermodynamics(state)

        # Frozen states conserve energy but do not move; only phase evolves.
        if state.is_frozen:
            total_E = self.total_energy(state)
            state.phase = (state.phase + total_E * dt) % (2 * np.pi)
            return state

        # 1. External Potential Force
        force = self.calculate_force(state.position)

        if state.mass > 0:
            acceleration = force / state.mass
            # Damping (friction) to allow settling into ground state
            damping = -0.05 * state.momentum
            acceleration += damping / state.mass

            new_momentum = state.momentum + acceleration * dt
            new_position = state.position + new_momentum * dt

            # Update phase (E = hf, phase evolves by energy)
            total_E = self.total_energy(state)
            new_phase = (state.phase + total_E * dt) % (2 * np.pi)

            # Return new instance of appropriate type
            if isinstance(state, Nucleus):
                return Nucleus(
                    new_position,
                    new_momentum,
                    new_phase,
                    state.amplitude,
                    state.mass,
                    state.name,
                    layer=state.layer,
                    temperature=state.temperature,
                    is_frozen=state.is_frozen,
                    sub_particles=state.sub_particles,
                    binding_energy=state.binding_energy
                )
            else:
                return QuantumState(
                    new_position,
                    new_momentum,
                    new_phase,
                    state.amplitude,
                    state.mass,
                    state.name,
                    layer=state.layer,
                    temperature=state.temperature,
                    is_frozen=state.is_frozen
                )
        else:
            # Photon dynamics
            V = self.potential_function(state.position)
            T = state.kinetic_energy

            new_momentum = state.momentum.copy() # Simplified ray tracing
            new_position = state.position + state.momentum * dt
            new_phase = (state.phase + state.frequency * dt) % (2 * np.pi)

            return PhotonEntity(
                new_position,
                state.momentum,
                new_phase,
                state.amplitude,
                mass=0.0,
                frequency=state.frequency,
                name=state.name,
                layer=state.layer
            )

class Entanglement:
    """
    Manages entangled pairs. If one changes, the other updates instantly.
    """
    def __init__(self):
        self.pairs: List[Tuple[QuantumState, QuantumState]] = []

    def entangle(self, p1: QuantumState, p2: QuantumState):
        self.pairs.append((p1, p2))

    def sync(self):
        """
        Synchronize states (simplified: average phase/frequency or spin).
        For this demo, we sync 'phase' to show 'spooky action'.
        """
        for p1, p2 in self.pairs:
            # They share a common wavefunction phase
            avg_phase = (p1.phase + p2.phase) / 2.0
            p1.phase = avg_phase
            p2.phase = avg_phase
