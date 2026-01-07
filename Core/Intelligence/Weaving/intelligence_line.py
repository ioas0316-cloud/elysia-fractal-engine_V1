from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class LineOutput:
    """
    The output of a single Intelligence Line.
    It represents a 1D signal from a specific domain.
    """
    source: str          # Name of the intelligence line (e.g., "Kinesthetic")
    signal: float        # Normalized signal strength or value (0.0 to 1.0, or -1.0 to 1.0)
    description: str     # Human-readable description (e.g., "Body is hot")
    raw_data: Dict[str, Any] # Detailed raw data for debugging or deep weaving

class IntelligenceLine(ABC):
    """
    Abstract Base Class for an Intelligence Line.
    Each line is responsible for monitoring one specific aspect of reality
    and reporting it as a simple signal.
    """

    # Default name (can be overridden by instances or subclasses)
    name: str = "Unknown"

    @abstractmethod
    def perceive(self, context_input: Any = None) -> LineOutput:
        """
        Perceives the environment or internal state and produces a LineOutput.

        Args:
            context_input: Optional external input (e.g., text, event).
                           Kinesthetic lines might ignore this and look at hardware.
        """
        pass
