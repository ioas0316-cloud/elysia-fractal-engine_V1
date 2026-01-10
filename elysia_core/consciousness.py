from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import math
from .systems import System
from .math_utils import Vector3
from .logging_config import get_logger

if TYPE_CHECKING:
    from .world import World
    from .physics import PhysicsWorld

logger = get_logger(__name__)

class GlobalConsciousness(System):
    def __init__(self, physics: Optional[PhysicsWorld] = None):
        self.physics = physics
        self.global_entropy: float = 0.0
        self.alignment_score: float = 0.0
        self.last_intervention_tick: int = 0

    def step(self, world: World, dt: float) -> None:
        self.calculate_metrics(world)
        if self.global_entropy > 0.8 and (world.tick - self.last_intervention_tick) > 50:
            self.divine_intervention(world, "restore_order")

    def calculate_metrics(self, world: World) -> None:
        total_energy = 0.0
        phase_vectors = Vector3(0,0,0)
        count = 0

        for entity in world.entities.values():
            if not entity.soul: continue

            count += 1
            total_energy += entity.soul.frequency
            px = math.cos(entity.soul.phase)
            py = math.sin(entity.soul.phase)
            phase_vectors = phase_vectors + Vector3(px, py, 0)

        if count == 0:
            self.global_entropy = 0.0
            return

        avg_phase_vec = phase_vectors * (1.0 / count)
        self.alignment_score = avg_phase_vec.magnitude
        self.global_entropy = 1.0 - self.alignment_score

    def divine_intervention(self, world: World, intent: str) -> None:
        self.last_intervention_tick = world.tick
        if intent == "restore_order":
            if self.physics:
                self.physics.gravity_constant *= 1.5
                if self.physics.gravity_constant > 50.0:
                     self.physics.gravity_constant = 50.0
            logger.warning("ENTROPY CRITICAL. GRAVITY INTENSIFIED.")

        elif intent == "spark_change":
            if self.physics:
                self.physics.coupling_constant *= 2.0
            logger.info("STAGNATION DETECTED. SOUL COUPLING INCREASED.")
