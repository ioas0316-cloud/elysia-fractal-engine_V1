from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Protocol, TYPE_CHECKING

from .efp import EFPState
from .roles import ROLE_PROFILES, RoleProfile
from .physics import PhysicsState
from .quantum import QuantumDNA

if TYPE_CHECKING:
    from .tensor_coil import CoilStructure
    from .physics import PhysicsWorld


class WorldLike(Protocol):
    time: float


@dataclass
class Entity:
    """역할과 삼위일체 가중치를 지원하는 기본 존재."""

    id: str
    state: EFPState = field(default_factory=EFPState)
    physics: PhysicsState = field(default_factory=PhysicsState)
    dna: Optional[QuantumDNA] = None
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

    def step(self, world: WorldLike, dt: float = 1.0) -> None:
        self.update_force(world)
        self.state.step(dt=dt)
        if self.dna:
            self.dna.step(dt)

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "role": self.role,
            "efp": self.state.as_dict(),
            "physics": asdict(self.physics),
            "force_components": {
                "body": self.f_body,
                "soul": self.f_soul,
                "spirit": self.f_spirit,
            },
            "data": self.data,
        }
        if self.dna:
            payload["dna"] = self.dna.as_dict()
        return payload
