"""Persona registry for Elysia's fractal consciousness engine.

This module exposes utilities that treat each persona as a focused
avatar of the same underlying Elysia intention field. External
applications (chat UI, VTuber rig, co-creative tool) can import the
registry to discover which personas exist and what channels they
care about.
"""

from .registry import (
    PersonaProfile,
    PERSONA_REGISTRY,
    list_personas,
    get_persona,
    activate_persona,
)

__all__ = [
    "PersonaProfile",
    "PERSONA_REGISTRY",
    "list_personas",
    "get_persona",
    "activate_persona",
]
