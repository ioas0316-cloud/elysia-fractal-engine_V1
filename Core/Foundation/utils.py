"""Utility helpers shared by Elysia field modules."""

from __future__ import annotations
from typing import Any

from ..world import World


def ensure_world(world: Any) -> World:
    if isinstance(world, World):
        return world
    raise TypeError("Expected an elysia_world.world.World instance")

__all__ = ["ensure_world"]
