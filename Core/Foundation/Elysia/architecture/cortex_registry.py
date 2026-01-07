from typing import Dict, Any


class CortexRegistry:
    """A registry for all Cortex modules."""

    def __init__(self):
        self._cortexes: Dict[str, Any] = {}

    def register(self, name: str, cortex_instance: Any):
        """Register a Cortex instance."""
        if name in self._cortexes:
            print(f"Warning: Cortex '{name}' is already registered. Overwriting.")
        self._cortexes[name] = cortex_instance

    def get(self, name: str) -> Any:
        """Get a Cortex instance by name."""
        cortex = self._cortexes.get(name)
        if not cortex:
            raise ValueError(f"Cortex '{name}' not found in registry.")
        return cortex
