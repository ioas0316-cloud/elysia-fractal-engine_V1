"""Cell representation used by the simulation world."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class Cell:
    """Lightweight cell with optional DNA and social links."""

    id: str
    dna: Dict[str, Any] | None = None
    properties: Dict[str, Any] = field(default_factory=dict)
    energy: float = 100.0
    hp: float = 100.0
    age: int = 0
    connections: List[Tuple[str, str, float]] = field(default_factory=list)

    @property
    def is_alive(self) -> bool:
        return self.energy > 0 and self.hp > 0

    def connect(self, other: "Cell", relationship_type: str = "related_to", strength: float = 1.0):
        self.connections.append((other.id, relationship_type, float(strength)))
        return self.connections[-1]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "dna": self.dna or {},
            "properties": dict(self.properties),
            "energy": float(self.energy),
            "hp": float(self.hp),
            "age": int(self.age),
        }

    def __repr__(self) -> str:
        return f"Cell(id={self.id}, energy={self.energy:.2f}, hp={self.hp:.2f}, age={self.age})"


__all__ = ["Cell"]
