from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World

class System(ABC):
    """
    Abstract base class for Systems in the Elysia Engine.
    Systems contain logic that operates on the World or specific sets of Entities.
    """

    @abstractmethod
    def step(self, world: World, dt: float) -> None:
        """
        Execute the system's logic for the current time step.
        """
        pass
