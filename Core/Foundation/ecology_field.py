"""Access aggregated ecology-related fields."""

from __future__ import annotations
from typing import Any, Dict

from .utils import ensure_world

ECOLOGY_FIELDS = (
    "hydration_field",
    "threat_field",
    "h_imprint",
    "norms_field",
    "prestige_field",
)


def snapshot(world: Any) -> Dict[str, Any]:
    w = ensure_world(world)
    return {name: getattr(w, name) for name in ECOLOGY_FIELDS if hasattr(w, name)}

__all__ = ["snapshot", "ECOLOGY_FIELDS"]
