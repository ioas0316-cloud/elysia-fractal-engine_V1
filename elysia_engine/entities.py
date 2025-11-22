from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Protocol, TYPE_CHECKING, List
import random

from .efp import EFPState
from .roles import ROLE_PROFILES, RoleProfile
from .physics import PhysicsState
from .math_utils import Vector3
from .quantum import QuantumState, EntanglementNetwork

if TYPE_CHECKING:
    from .tensor_coil import CoilStructure
    from .physics import PhysicsWorld, HamiltonianSystem
    from .topology import GravityPath, TensorGate
    from .chronos import ChronosMaster


class WorldLike(Protocol):
    time: float


@dataclass
class Entity:
    """역할과 삼위일체 가중치를 지원하는 기본 존재."""

    id: str
    state: EFPState = field(default_factory=EFPState)
    physics: PhysicsState = field(default_factory=PhysicsState)
    quantum: Optional[QuantumState] = None

    # Time Relavitity
    local_time: float = 0.0

    data: Dict[str, Any] = field(default_factory=dict)
    role: Optional[str] = None
    f_body: float = 0.0
    f_soul: float = 0.0
    f_spirit: float = 0.0

    def update_force_components(self, world: WorldLike) -> None:
        """서브클래스에서 f_body/f_soul/f_spirit를 채워 넣는다."""

        return None

    def update_force(self, world: WorldLike) -> None:
        self.f_body = self.f_soul = self.f_spirit = 0.0
        self.update_force_components(world)

        profile = self._get_role_profile()
        if profile is None:
            total = self.f_body + self.f_soul + self.f_spirit
        else:
            p = profile.normalized
            total = (
                p.w_body * self.f_body
                + p.w_soul * self.f_soul
                + p.w_spirit * self.f_spirit
            )

        self.state.force = total

    def _get_role_profile(self) -> Optional[RoleProfile]:
        if self.role is None:
            return None
        return ROLE_PROFILES.get(self.role)

    def apply_physics(self, coil: Optional[CoilStructure], world_physics: Optional[PhysicsWorld], dt: float = 1.0) -> None:
        """
        Applies the Digital Physics laws:
        1. Coil Acceleration (Railgun)
        2. Gravity (Attractors)
        3. Hyperdrive (Superconductivity)
        """
        # 1. Railgun / Coil field
        if coil:
            coil.railgun_accelerate(self.physics, dt)

        # 2. Gravity
        if world_physics:
            gravity = world_physics.get_net_force(self.physics.position)
            self.physics.apply_force(gravity, dt)

        # 3. Hyperdrive check
        # If we successfully hyperdrive to an attractor, we might stop other processing?
        if coil and world_physics:
            # Try to jump to any attractor
            for attractor in world_physics.attractors:
                did_jump = coil.superconduct(self.physics, attractor)
                if did_jump:
                    # Jump happened. Energy surge?
                    self.state.energy += 100.0
                    break

        # Step physics
        self.physics.step(dt)

    def apply_topology(self, paths: List[GravityPath], gates: List[TensorGate], dt: float = 1.0) -> None:
        """
        Applies interactions with the Topological Terrain (Paths, Gates).
        """
        total_topo_force = self.physics.velocity * 0.0 # Zero vector

        # 1. Paths (Rivers)
        for path in paths:
            force = path.calculate_force(self.physics)
            total_topo_force = total_topo_force + force

        # 2. Gates (Filters)
        for gate in gates:
            force = gate.calculate_interaction(self.physics, self.state.energy, self.state.momentum)
            total_topo_force = total_topo_force + force

        # Apply
        self.physics.apply_force(total_topo_force, dt)

    def apply_quantum_tunneling(self, hamiltonian: HamiltonianSystem, barrier_threshold: float = 50.0) -> bool:
        """
        Attempts to 'Tunnel' through a high energy barrier.
        Probability depends on Resonance (Kinetic Energy vs Barrier Potential).
        """
        h_val = hamiltonian.calculate_hamiltonian(self.physics)

        # If total energy is high enough, we might tunnel
        # even if Kinetic < Barrier height locally (classically forbidden).
        # Simple heuristic:
        # P(tunnel) ~ exp(-(Barrier - Kinetic))

        # Find potential at current spot
        u = hamiltonian.world.get_potential_energy(self.physics.position) * self.physics.mass
        k = self.physics.kinetic_energy

        if u > k and u > barrier_threshold:
            # We are hitting a wall. Classical physics says BOUNCE.
            # Quantum physics says maybe...

            # Probability factor
            delta_e = u - k
            prob = 1.0 / (1.0 + delta_e * 0.1) # Simple decay

            roll = random.random()
            if roll < prob:
                # TUNNEL!
                # Skip past the barrier (move forward by radius)
                # This requires knowing direction. Assume velocity direction.
                jump_vec = self.physics.velocity.normalize() * 5.0
                self.physics.position = self.physics.position + jump_vec
                return True

        return False

    def entangle(self, other: Entity) -> None:
        """Links this entity's quantum state to another."""
        if self.quantum is None:
            self.quantum = QuantumState()
        if other.quantum is None:
            other.quantum = QuantumState()

        # Register with network
        net = EntanglementNetwork.get()
        net.entangle(self.id, other.id)

    def set_quantum_spin(self, spin: float, entities_map: Dict[str, Entity]) -> None:
        """Sets spin and triggers spooky action."""
        if self.quantum:
            self.quantum.spin = spin
            EntanglementNetwork.get().sync_spin(self.id, spin, entities_map)

    def step(self, world: WorldLike, dt: float = 1.0, chronos: Optional[ChronosMaster] = None) -> None:
        """
        Relativistic Step:
        If ChronosMaster is provided, local_dt is adjusted by Time Fields.
        """
        # 1. Calculate Time Dilation
        time_scale = 1.0
        if chronos:
            time_scale = chronos.get_local_time_scale(self.physics.position)

        # 2. Apply relativistic dt
        local_dt = dt * time_scale
        self.local_time += local_dt

        # 3. Regular Updates with Dilated Time
        self.update_force(world)
        self.state.step(dt=local_dt)
        if self.quantum:
            self.quantum.step(local_dt)

    def evolve_to_field(self) -> Optional[Any]:
        """
        Placeholder for Fractal Evolution (Point -> Line -> Plane).
        To be implemented by FractalEvolver.
        """
        return None

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "role": self.role,
            "efp": self.state.as_dict(),
            "physics": asdict(self.physics),
            "local_time": self.local_time,
            "force_components": {
                "body": self.f_body,
                "soul": self.f_soul,
                "spirit": self.f_spirit,
            },
            "data": self.data,
        }
        if self.quantum:
            payload["quantum"] = asdict(self.quantum)
            # exclude circular set
            del payload["quantum"]["entangled_ids"]
        return payload
