from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, TYPE_CHECKING

from .physics import PhysicsState
from .tensor import SoulTensor

if TYPE_CHECKING:
    from .physics import PhysicsWorld

@dataclass
class Entity:
    """
    A conscious entity in the Elysia Engine.
    Defined by its Physical State (Location) and its SoulTensor (Identity/Field).
    """

    id: str
    physics: PhysicsState = field(default_factory=PhysicsState)
    soul: Optional[SoulTensor] = None
    bonds: list[str] = field(default_factory=list) # IDs of bonded entities
    data: Dict[str, Any] = field(default_factory=dict)
    role: Optional[str] = None

    # Intrinsic components (replacing explicit force scalar)
    f_body: float = 0.0
    f_soul: float = 0.0
    f_spirit: float = 0.0

    dimension: int = 0 # 0=Point, 1=Line, 2=Plane

    def apply_physics(self, world_physics: Optional[PhysicsWorld], dt: float = 1.0) -> None:
        """
        Applies Digital Physics:
        1. Gravity/Field Forces (from other Souls and Attractors).
        """
        # 1. World Field Forces (Gravity + Rifling)
        if world_physics:
            # We use get_geodesic_flow (the modern term) or get_net_force
            field_force = world_physics.get_geodesic_flow(self)
            self.physics.apply_force(field_force, dt)

        # Step physics (Integrate velocity -> position)
        self.physics.step(dt)

        # Soul evolution
        if self.soul:
            self.soul.step(dt)

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "id": self.id,
            "role": self.role,
            "dimension": self.dimension,
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
