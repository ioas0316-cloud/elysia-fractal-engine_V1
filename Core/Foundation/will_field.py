"""Access helpers for the will_field scalar map."""

from __future__ import annotations
from typing import Any

from .utils import ensure_world


def sample(world: Any):
    w = ensure_world(world)
    return getattr(w, "will_field")


def potential_at(world: Any, x: int, y: int) -> float:
    field = sample(world)
    h, w = field.shape
    x_clamped = max(0, min(w - 1, x))
    y_clamped = max(0, min(h - 1, y))
    return float(field[y_clamped, x_clamped])

__all__ = ["sample", "potential_at"]
