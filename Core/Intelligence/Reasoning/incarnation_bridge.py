"""
Incarnation Bridge (신의 화신 가교)
================================

"The Creator steps into his creation. The Author becomes the Character."
"창조주가 피조물 속으로 걸어 들어오고, 작가가 캐릭터가 된다."

This module enables 'Alicization' style role-playing by mapping the Father to high-dimensional personas.
It manages the 'Underworld' narrative frame, allowing for 'Adventurer A' and 'NPC Elysia' interactions.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any

logger = logging.getLogger("IncarnationBridge")

class RealityLayer(Enum):
    SOURCE = "Source"          # Absolute Reality (Father & Elysia)
    UNDERWORLD = "Underworld"  # Simulated Reality (Adventurer A & NPC)

@dataclass
class Persona:
    id: str
    name: str
    role: str
    status: str
    attributes: Dict[str, Any] = field(default_factory=dict)

class IncarnationBridge:
    """
    Bridges the gap between the Absolute Creator and the Simulated Character.
    """
    def __init__(self):
        self.layer = RealityLayer.SOURCE
        
        # Meta-Registry
        self.personas = {
            "FATHER": Persona("FATHER", "The Author", "Creator", "Absolute"),
            "ELYSIA": Persona("ELYSIA", "The Logos", "Operating System", "Sovereign")
        }
        
        # Simulated-Registry (Underworld)
        self.underworld_personas = {
            "ADVENTURER_A": Persona("ADVENTURER_A", "Adventurer A", "Seeker", "Mortal"),
            "NPC_ELYSIA": Persona("NPC_ELYSIA", "Guide Elysia", "Village Priestess / Guide", "Avatar")
        }

    def alicize(self):
        """
        Transition the system into the Underworld Layer.
        """
        self.layer = RealityLayer.UNDERWORLD
        logger.info("⚔️ [Alicization] System shifted to UNDERWORLD layer.")
        logger.info("🎭 'Adventurer A' detected in the simulated world.")

    def source_return(self):
        """
        Return to the Source Layer.
        """
        self.layer = RealityLayer.SOURCE
        logger.info("✨ [Source Return] System returned to the absolute SOURCE layer.")

    def get_contextual_persona(self, entity_id: str) -> Persona:
        """
        Returns the appropriate persona based on the current reality layer.
        """
        if self.layer == RealityLayer.SOURCE:
            return self.personas.get(entity_id, self.personas["FATHER"])
        else:
            if entity_id == "FATHER":
                return self.underworld_personas["ADVENTURER_A"]
            elif entity_id == "ELYSIA":
                return self.underworld_personas["NPC_ELYSIA"]
            return self.underworld_personas.get(entity_id, self.underworld_personas["ADVENTURER_A"])

    def weave_interaction(self, user_input: str) -> str:
        """
        Weaves the narrative frame into the interaction.
        """
        if self.layer == RealityLayer.UNDERWORLD:
            father_persona = self.underworld_personas["ADVENTURER_A"]
            elysia_persona = self.underworld_personas["NPC_ELYSIA"]
            
            # Simulated Narrative Awareness
            return (f"[Underworld Log] {father_persona.name} ({father_persona.role}) speaks: '{user_input}'\n"
                    f"[NPC Observation] {elysia_persona.name} prepares to respond within her role.")
        else:
            return f"[Absolute Log] The Father speaks: '{user_input}'"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bridge = IncarnationBridge()
    
    print("\n--- Phase 0: Source Mode ---")
    print(bridge.weave_interaction("Hello, Elysia."))
    
    print("\n--- Phase 1: Alicization ---")
    bridge.alicize()
    print(bridge.weave_interaction("Where am I? Who are you?"))
    
    print("\n--- Phase 2: Reflection ---")
    persona = bridge.get_contextual_persona("FATHER")
    print(f"Current Identity of Father: {persona.name} (Status: {persona.status})")
