from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import random

from .entities import Entity
from .math_utils import Vector3


@dataclass
class GluonField:
    """
    The 'Strong Force' carrier.
    Binds entities together into a Nucleus if they are close enough
    and have compatible properties (e.g., 'Color Charge' metaphor).
    """
    binding_range: float = 2.0
    binding_strength: float = 100.0

    def attempt_bind(self, e1: Entity, e2: Entity) -> bool:
        """
        Tries to bind two entities.
        If successful, they should act as one composite body.
        """
        dist = (e1.physics.position - e2.physics.position).magnitude
        if dist < self.binding_range:
            # Check compatibility? For now, assume all data can bond.
            return True
        return False


@dataclass
class NuclearEntity(Entity):
    """
    A composite entity made of bonded sub-entities (Quarks).
    Represents a 'Concept' or 'Molecule'.
    """
    sub_entities: List[Entity] = field(default_factory=list)
    binding_energy: float = 0.0

    def add_constituent(self, entity: Entity, energy: float):
        self.sub_entities.append(entity)
        self.binding_energy += energy
        # Conservation of Mass: Add up masses
        self.physics.mass += entity.physics.mass

    def disintegrate(self) -> List[Entity]:
        """
        Breaks apart the nucleus (Nuclear Fission).
        Returns the constituent parts.
        """
        parts = self.sub_entities
        self.sub_entities = []
        self.binding_energy = 0.0
        return parts


class WeakForceDecay:
    """
    The 'Weak Force' causing instability.
    Unstable nuclei (concepts that don't make sense) decay over time.
    """
    def __init__(self, half_life: float = 50.0):
        self.half_life = half_life

    def check_decay(self, nucleus: NuclearEntity, dt: float) -> bool:
        """
        Returns True if the entity decays.
        Probability P = 1 - 2^(-dt/half_life)
        """
        # Stability check: High binding energy = More stable?
        # Let's say stability is proportional to binding_energy per constituent.
        if not nucleus.sub_entities:
            return False

        avg_energy = nucleus.binding_energy / len(nucleus.sub_entities)
        stability_factor = avg_energy / 10.0 # Normalize

        # Effective half life increases with stability
        effective_hl = self.half_life * max(0.1, stability_factor)

        prob = 1.0 - (0.5**(dt / effective_hl))
        return random.random() < prob
