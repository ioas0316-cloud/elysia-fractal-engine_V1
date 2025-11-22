from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from .physics import Attractor

if TYPE_CHECKING:
    from .entities import Entity


class MatterState(Enum):
    PLASMA = "PLASMA"   # Fire Star: Active, interacting, high cost
    GAS = "GAS"         # Volatile: Moving fast
    LIQUID = "LIQUID"   # Fluid: Flowing
    SOLID = "SOLID"     # Stable: Slow change
    CRYSTAL = "CRYSTAL" # Ice Star: Frozen, no calculation, purely structural


@dataclass
class ThermalState:
    temperature: float = 1000.0 # Default Hot
    cooling_rate: float = 0.1
    state: MatterState = MatterState.PLASMA

    def update_state(self):
        if self.temperature > 800:
            self.state = MatterState.PLASMA
        elif self.temperature > 500:
            self.state = MatterState.GAS
        elif self.temperature > 200:
            self.state = MatterState.LIQUID
        elif self.temperature > 50:
            self.state = MatterState.SOLID
        else:
            self.state = MatterState.CRYSTAL

    def cool_down(self, dt: float):
        if self.state == MatterState.CRYSTAL:
            return # Already frozen absolute zero-ish

        # Newton's Law of Cooling (simplified)
        self.temperature -= self.cooling_rate * dt
        if self.temperature < 0:
            self.temperature = 0
        self.update_state()


class Crystallizer:
    """
    Manages the freezing of entities into static Attractors.
    """
    def freeze(self, entity: Entity) -> Attractor:
        """
        Converts a Crystal Entity into a pure Attractor (Gravity Well).
        The Entity can then be archived/removed from the active loop.
        """
        return Attractor(
            id=f"frozen_{entity.id}",
            position=entity.physics.position,
            mass=entity.physics.mass * 10.0, # Core beliefs are heavy
            radius=entity.physics.mass # Event horizon depends on mass
        )
