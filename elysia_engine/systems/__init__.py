from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..world import World

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

# Optional helper systems
try:
    from .spacetime import SpacetimeOrchestrator  # noqa: F401
except Exception:
    # Avoid import issues if optional modules are absent during partial loads.
    pass

try:
    from .thermodynamics import ThermodynamicsSystem, ThermalState  # noqa: F401
except Exception:
    pass

try:
    from .void import VoidSystem  # noqa: F401
except Exception:
    pass

try:
    from .genesis import GenesisSystem  # noqa: F401
except Exception:
    pass

try:
    from .fractal_evolution import (  # noqa: F401
        FractalEvolutionSystem,
        DimensionalState,
        CosmicResonanceField,
    )
except Exception:
    pass
