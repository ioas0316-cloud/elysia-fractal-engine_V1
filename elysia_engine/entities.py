from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Protocol, TYPE_CHECKING

from .efp import EFPState
from .roles import ROLE_PROFILES, RoleProfile
from .physics import PhysicsState
from .tensor import SoulTensor

if TYPE_CHECKING:
    from .tensor_coil import CoilStructure
    from .physics import PhysicsWorld


class WorldLike(Protocol):
    time: float


@dataclass
class Entity:
    """
    A conscious entity in the Elysia Engine.
    Defined by its Physical State (Location) and its SoulTensor (Identity/Field).
    """

    id: str
    state: EFPState = field(default_factory=EFPState)
    physics: PhysicsState = field(default_factory=PhysicsState)
    soul: Optional[SoulTensor] = None # Replaces QuantumDNA
    bonds: list[str] = field(default_factory=list) # IDs of bonded entities (Dimensional Evolution)
    data: Dict[str, Any] = field(default_factory=dict)
    role: Optional[str] = None
    f_body: float = 0.0
    f_soul: float = 0.0
    f_spirit: float = 0.0

    def update_force_components(self, world: WorldLike) -> None:
        """Subclass hook to fill f_body/f_soul/f_spirit."""
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
        Applies Digital Physics:
        1. Gravity/Field Forces (from other Souls and Attractors).
        2. Coil Acceleration (if applicable).
        """
        # 1. World Field Forces (Gravity + Rifling)
        if world_physics:
            # Pass 'self' so we don't attract ourselves, and so the field knows our properties
            # if we wanted to implement specific resonance-based movement.
            # For now, we just feel the net force of the universe.
            field_force = world_physics.get_net_force(self)
            self.physics.apply_force(field_force, dt)

        # 2. Coil / Railgun (Environmental structures)
        if coil:
            coil.railgun_accelerate(self.physics, dt)
            # Hyperdrive check could be here

        # Step physics (Integrate velocity -> position)
        self.physics.step(dt)

    def step(self, world: WorldLike, dt: float = 1.0) -> None:
        self.update_force(world)
        self.state.step(dt=dt)
        if self.soul:
            self.soul.step(dt)

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
        if self.soul:
            payload["soul"] = self.soul.as_dict()
        return payload
