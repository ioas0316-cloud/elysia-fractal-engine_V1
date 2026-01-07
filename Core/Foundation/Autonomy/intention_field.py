"""Expose the intentional field (vector field) helpers."""

from __future__ import annotations
from typing import Any

from .utils import ensure_world


def sample(world: Any):
    w = ensure_world(world)
    return getattr(w, "intentional_field")


def direction_at(world: Any, x: int, y: int):
    field = sample(world)
    h, w = field.shape[:2]
    x_clamped = max(0, min(w - 1, x))
    y_clamped = max(0, min(h - 1, y))
    vector = field[y_clamped, x_clamped]
    return tuple(float(v) for v in vector)

__all__ = ["sample", "direction_at"]
