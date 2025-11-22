from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import List, Optional, Set

from .math_utils import Vector3, Quaternion


@dataclass
class QuantumState:
    """
    Represents the quantum properties of an entity.
    Approximates a Wave Function using Phase, Frequency, and Spin.
    """
    phase: float = 0.0        # 0 to 2pi
    frequency: float = 1.0    # Energy = h * f
    amplitude: float = 1.0    # Probability density ~ amp^2
    spin: float = 0.5         # Intrinsic angular momentum

    # Entanglement
    entangled_ids: Set[str] = field(default_factory=set)

    def step(self, dt: float) -> None:
        """Evolve phase: theta = theta + omega * t"""
        omega = 2.0 * math.pi * self.frequency
        self.phase = (self.phase + omega * dt) % (2.0 * math.pi)


class EntanglementNetwork:
    """
    Global manager for quantum entanglement.
    Spooky action at a distance.
    """
    _instance = None

    def __init__(self):
        # Map: entity_id -> list of entangled entity_ids
        self.links = {}

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = EntanglementNetwork()
        return cls._instance

    def entangle(self, id_a: str, id_b: str):
        if id_a not in self.links: self.links[id_a] = set()
        if id_b not in self.links: self.links[id_b] = set()

        self.links[id_a].add(id_b)
        self.links[id_b].add(id_a)

    def sync_spin(self, source_id: str, new_spin: float, entities_map: dict):
        """
        If source changes spin, entangled partners flip or sync immediately.
        Simplified model: Spin flip (conservation).
        """
        if source_id not in self.links:
            return

        partners = self.links[source_id]
        for pid in partners:
            if pid in entities_map:
                target_ent = entities_map[pid]
                if hasattr(target_ent, 'quantum') and target_ent.quantum:
                    # Spooky action: Target assumes opposite spin? Or same?
                    # Let's say Anti-correlated (Singlet state)
                    target_ent.quantum.spin = -new_spin


@dataclass
class Photon:
    """
    A specialized 'Light' entity wrapper.
    Mass = 0.
    Velocity magnitude = C (Speed of Light).
    """
    id: str
    position: Vector3
    direction: Vector3
    frequency: float # Color

    def __post_init__(self):
        self.direction = self.direction.normalize()
