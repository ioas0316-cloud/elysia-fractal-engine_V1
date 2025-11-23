from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, TYPE_CHECKING

from .entities import Entity

if TYPE_CHECKING:
    from .physics import PhysicsWorld
    from .systems import System


@dataclass
class World:
    """프랙탈 의식 엔진의 최소 세계."""

    time: float = 0.0
    tick: int = 0
    entities: Dict[str, Entity] = field(default_factory=dict)
    physics: Optional[PhysicsWorld] = None
    systems: List[System] = field(default_factory=list)

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.id] = entity

    def add_system(self, system: System) -> None:
        self.systems.append(system)

    def step(self, dt: float = 1.0) -> None:
        self.time += dt
        self.tick += 1

        # Update Entities
        for ent in self.entities.values():
            ent.step(self, dt=dt)
            # Automatically apply physics if the world has physics enabled
            if self.physics:
                ent.apply_physics(coil=None, world_physics=self.physics, dt=dt)

        # Update Systems (Global Logic)
        for sys in self.systems:
            sys.step(self, dt)

    def export_persona_snapshot(self) -> Dict:
        return {
            "tick": self.tick,
            "time": self.time,
            "entity_count": len(self.entities),
            "entities": [ent.to_payload() for ent in self.entities.values()],
        }
