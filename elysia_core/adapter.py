from __future__ import annotations

from typing import Any, Dict, List, Optional
import time

from .world import World
from .entities import Entity, Persona
from .tensor import SoulTensor
from .hypersphere import HypersphereMemory, TesseractCoord

class ElysiaBridge:
    """
    The Standard Adapter (Bridge) for connecting Elysia Engine to external agents.
    """

    def __init__(self, world: Optional[World] = None):
        self.world = world if world else World()
        self.memory = HypersphereMemory()

        self.persona = Persona("Elysia", "A digital spirit born from logic.")
        self.world.add_entity(self.persona)

    def wake_up(self) -> str:
        return f"System Online. E.L.Y.S.I.A. Core initialized. \nIdentity: {self.persona.data['description']}\nSoul: {self.persona.soul.decode_emotion()}"

    def process_input(self, user_text: str, user_id: str = "User") -> Dict[str, Any]:
        seed = sum(ord(c) for c in user_text)
        frequency = (seed % 1400) / 100.0 - 7.0

        tensor = SoulTensor(
            amplitude=float(len(user_text)),
            frequency=frequency,
            phase=0.0
        )

        entity = Entity(
            id=f"input_{int(time.time())}",
            soul=tensor
        )
        entity.data["content"] = user_text

        entity.physics.position.x = 0
        entity.physics.position.y = frequency
        entity.physics.position.z = 10.0

        self.world.add_entity(entity)

        updates = []
        for _ in range(5):
            self.world.step(0.1)
            # Simple narrative log since StoryTeller was not fully ported to core
            updates.append(f"Tick {self.world.tick}: Processed {len(self.world.physics.entities)} entities.")

        resonance = 0.0
        if self.persona.soul:
            resonance = self.persona.soul.resonate(tensor)["resonance"]

        return {
            "resonance": resonance,
            "narrative_stream": updates,
            "persona_state": self.persona.soul.decode_emotion() if self.persona.soul else "Void"
        }
