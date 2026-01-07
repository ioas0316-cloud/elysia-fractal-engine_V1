"""Helpers for interacting with the value-mass field."""

from __future__ import annotations
from typing import Any

from .utils import ensure_world


def sample(world: Any) -> Any:
    """Return the raw value_mass_field array from the world."""
    w = ensure_world(world)
    return getattr(w, "value_mass_field")


def intensity_at(world: Any, x: int, y: int) -> float:
    """Return the scalar intensity at a given grid coordinate."""
    field = sample(world)
    h, w = field.shape
    x_clamped = max(0, min(w - 1, x))
    y_clamped = max(0, min(h - 1, y))
    return float(field[y_clamped, x_clamped])

__all__ = ["sample", "intensity_at"]
