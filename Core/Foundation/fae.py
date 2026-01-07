"""Fae-like conceptual agent."""

from __future__ import annotations
from dataclasses import dataclass

from ..cell import Cell


@dataclass
class FaeAgent:
    concept_id: str
    aura: float = 15.0

    def spawn(self, world) -> Cell:
        properties = {
            "label": "fae",
            "element_type": "spirit",
            "mana": self.aura,
            "max_mana": self.aura,
        }
        world.add_cell(self.concept_id, properties=properties)
        return world.materialize_cell(self.concept_id)

__all__ = ["FaeAgent"]
