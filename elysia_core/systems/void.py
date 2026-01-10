from __future__ import annotations
from . import System
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

class VoidSystem(System):
    def step(self, world: World, dt: float) -> None:
        # Placeholder for void system logic
        pass
