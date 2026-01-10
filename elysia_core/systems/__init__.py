from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

class System(ABC):
    @abstractmethod
    def step(self, world: World, dt: float) -> None:
        pass

# Optional helper systems
try:
    from .void import VoidSystem  # noqa: F401
except Exception:
    pass
