from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import math

from .systems import System
from .math_utils import Vector3

if TYPE_CHECKING:
    from .world import World
    from .physics import PhysicsWorld

class GlobalConsciousness(System):
    """
    Represents the "Whole" (God/System) that observes the "Parts".
    Calculates global metrics (Entropy, Alignment) and performs Divine Intervention.
    """

    def __init__(self, physics: Optional[PhysicsWorld] = None):
        self.physics = physics
        self.global_entropy: float = 0.0
        self.alignment_score: float = 0.0
        self.last_intervention_tick: int = 0

    def step(self, world: World, dt: float) -> None:
        self.calculate_metrics(world)

        # Divine Intervention Logic:
        # If Entropy is too high (Chaos), slow down time or increase gravity to force order.
        # Only intervene every 50 ticks to avoid oscillation
        if self.global_entropy > 0.8 and (world.tick - self.last_intervention_tick) > 50:
            self.divine_intervention(world, "restore_order")

    def calculate_metrics(self, world: World) -> None:
        total_energy = 0.0
        phase_vectors = Vector3(0,0,0) # We'll map phase to a unit vector
        count = 0

        for entity in world.entities.values():
            if not entity.soul: continue

            count += 1
            total_energy += entity.soul.frequency

            # Map phase to vector to check alignment
            # Phase is 0-2pi. Map to x,y on unit circle
            px = math.cos(entity.soul.phase)
            py = math.sin(entity.soul.phase)
            phase_vectors = phase_vectors + Vector3(px, py, 0)

        if count == 0:
            self.global_entropy = 0.0
            return

        # Alignment: Magnitude of the average phase vector.
        # If everyone is phase-aligned, mag is 1.0. If random, it's close to 0.
        avg_phase_vec = phase_vectors * (1.0 / count)
        self.alignment_score = avg_phase_vec.magnitude

        # Entropy is inverse of alignment (Simple definition)
        self.global_entropy = 1.0 - self.alignment_score

    def divine_intervention(self, world: World, intent: str) -> None:
        """
        The System modifies the Universe's Constants based on intent.
        """
        self.last_intervention_tick = world.tick

        if intent == "restore_order":
            # Slow down time to let entities synchronize (conceptually)
            # In practice, we increase Gravity to pull things together.
            if self.physics:
                self.physics.gravity_constant *= 1.5
                # Clamp
                if self.physics.gravity_constant > 50.0:
                     self.physics.gravity_constant = 50.0

            print(f"\n[Global Consciousness] ENTROPY CRITICAL ({self.global_entropy:.2f}). GRAVITY INTENSIFIED to {self.physics.gravity_constant:.1f}.")

        elif intent == "spark_change":
            if self.physics:
                self.physics.coupling_constant *= 2.0
            print(f"\n[Global Consciousness] STAGNATION DETECTED. SOUL COUPLING INCREASED.")
