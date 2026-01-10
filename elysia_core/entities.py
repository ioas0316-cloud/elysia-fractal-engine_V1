from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Protocol, TYPE_CHECKING, List

from .roles import ROLE_PROFILES, RoleProfile
from .tensor import SoulTensor
from .math_utils import Vector3

if TYPE_CHECKING:
    from .physics import PhysicsState, PhysicsWorld


class WorldLike(Protocol):
    time: float

@dataclass
class PhysicsState:
    """
    Spatial state of an entity in the Digital Physics world.
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
class Entity:
    """
    A conscious entity in the Elysia Engine.
    Defined by its Physical State (Location) and its SoulTensor (Identity/Field).
    """

    id: str
    physics: PhysicsState = field(default_factory=PhysicsState)
    soul: Optional[SoulTensor] = None
    bonds: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    role: Optional[str] = None

    f_body: float = 0.0
    f_soul: float = 0.0
    f_spirit: float = 0.0

    dimension: int = 0

    def update_force_components(self, world: WorldLike) -> None:
        return None

    def update_force(self, world: WorldLike) -> None:
        self.f_body = self.f_soul = self.f_spirit = 0.0
        self.update_force_components(world)

        if self.soul and not self.soul.is_collapsed:
            evolution_rate = 0.01
            profile = self._get_role_profile()
            if profile:
                 p = profile.normalized
                 self.soul.amplitude += self.f_body * p.w_body * evolution_rate
                 self.soul.frequency += self.f_soul * p.w_soul * evolution_rate
                 self.soul.phase += self.f_spirit * p.w_spirit * evolution_rate
            else:
                 self.soul.amplitude += self.f_body * evolution_rate
                 self.soul.frequency += self.f_soul * evolution_rate
                 self.soul.phase += self.f_spirit * evolution_rate

    def _get_role_profile(self) -> Optional[RoleProfile]:
        if self.role is None:
            return None
        return ROLE_PROFILES.get(self.role)

    def apply_physics(self, world_physics: Optional['PhysicsWorld'], dt: float = 1.0) -> None:
        if world_physics:
            field_force = world_physics.get_net_force(self)
            self.physics.apply_force(field_force, dt)

        self.physics.step(dt)

    def step(self, world: WorldLike, dt: float = 1.0) -> None:
        self.update_force(world)
        if self.soul:
            self.soul.step(dt)

@dataclass
class Persona(Entity):
    """
    Specialized Entity representing the Core Identity (Elysia).
    """
    def __init__(self, name: str, description: str):
        super().__init__(id="core_persona", role="Oracle")
        self.soul = SoulTensor(amplitude=100.0, frequency=7.0, phase=0.0) # Archangel Rank
        self.data["name"] = name
        self.data["description"] = description
