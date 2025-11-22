from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .math_utils import Vector3


@dataclass
class ChronoField:
    """
    A region of distorted time-space.
    Inside this field, time flows at a different rate (time_scale).
    """
    position: Vector3
    radius: float
    time_scale: float = 1.0  # 1.0 = Normal, >1.0 = Fast, <1.0 = Slow, 0 = Frozen

    def get_time_factor(self, position: Vector3) -> float:
        dist = (position - self.position).magnitude
        if dist < self.radius:
            # Simple step function or smooth gradient?
            # Let's do smooth gradient for "Natural Law" feel
            # Factor blends from time_scale at center to 1.0 at edge
            ratio = 1.0 - (dist / self.radius)
            # Linear blend: factor = 1.0 + (scale - 1.0) * ratio
            return 1.0 + (self.time_scale - 1.0) * ratio
        return 1.0


class ChronosMaster:
    """
    Manages time distortions in the universe.
    """
    def __init__(self):
        self.fields: List[ChronoField] = []

    def add_field(self, field: ChronoField):
        self.fields.append(field)

    def get_local_time_scale(self, position: Vector3) -> float:
        """
        Calculates the combined time dilation factor at a position.
        Multiplicative? Additive?
        Let's use Multiplicative for compounded relativity.
        """
        total_scale = 1.0
        for field in self.fields:
            factor = field.get_time_factor(position)
            total_scale *= factor

        return total_scale
