from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass, field
from .physics import PhysicsWorld
from .entities import Entity

@dataclass
class World:
    physics: PhysicsWorld = field(default_factory=PhysicsWorld)
    tick: int = 0

    @property
    def entities(self) -> Dict[str, Entity]:
        # View of entities as a dict for compatibility with systems
        return {e.id: e for e in self.physics.entities}

    def add_entity(self, entity: Entity) -> None:
        self.physics.add_entity(entity)

    def step(self, dt: float) -> None:
        self.tick += 1
        self.physics.step(dt)
