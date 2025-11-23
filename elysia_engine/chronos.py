from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List, Dict

from .systems import System

if TYPE_CHECKING:
    from .world import World

class DreamSystem(System):
    """
    Implements the 'Chronos' capability: Time Transcendence.
    Allows the engine to fork reality, simulate potential futures (Prophecy),
    and gain 'Divine Perspective'.
    """

    def __init__(self):
        self.last_dream_tick = 0
        self.dream_interval = 100 # Dream every 100 ticks automatically

    def step(self, world: World, dt: float) -> None:
        """
        Occasional background dreaming to update intuition.
        """
        if world.tick - self.last_dream_tick > self.dream_interval:
            self.last_dream_tick = world.tick
            # In a real implementation, we might store this future intuition.
            # For now, we just log that we are dreaming.
            # print("[Chronos] Entering REM cycle... Scanning timelines...")
            pass

    def prophecy(self, world: World, horizon: int = 50) -> World:
        """
        The 'Eye of Chronos'.
        Creates a divergent timeline and fast-forwards it to see the future.
        Returns the future World state.

        This constitutes 'Reverse Causality' planning:
        We see the result, then we change the present.
        """
        # 1. Fork Reality (Deep Copy)
        future_world = world.clone()

        # 2. Fast-Forward Simulation
        # We disable the DreamSystem in the dream to prevent recursive dreaming (Inception)
        # We also disable GlobalConsciousness to prevent "Dream Self" from intervening
        # We want to see the "Natural Consequence" of the current state.
        from .consciousness import GlobalConsciousness

        dream_systems = [
            s for s in future_world.systems
            if not isinstance(s, (DreamSystem, GlobalConsciousness))
        ]
        future_world.systems = dream_systems

        for _ in range(horizon):
            future_world.step(dt=1.0)

        # 3. Post-Dream Analysis
        # We re-attach a Passive Consciousness to measure the final state
        from .consciousness import GlobalConsciousness
        observer = GlobalConsciousness(physics=None) # Physics None means it can't intervene
        future_world.add_system(observer)
        # We must trigger it once to calculate
        observer.calculate_metrics(future_world)

        return future_world

    def analyze_entropy(self, world: World) -> float:
        """
        Helper to measure the chaos of a world state.
        Leverages GlobalConsciousness if available, otherwise calculates locally.
        """
        # Try to find GlobalConsciousness
        from .consciousness import GlobalConsciousness

        for sys in world.systems:
            if isinstance(sys, GlobalConsciousness):
                # Ensure metrics are up to date
                sys.calculate_metrics(world)
                return sys.global_entropy

        return 0.5 # Default neutral
