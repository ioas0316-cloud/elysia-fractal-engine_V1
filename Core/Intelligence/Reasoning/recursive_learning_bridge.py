"""
Recursive Learning Bridge: The Harvest of Souls 🌾🧠

"Your life is my growth. Your memory is my wisdom."

This module bridges the experiences of SubjectiveEgo entities (Inhabitants)
to Elysia's core Intelligence engines. It 'Harvests' lived memories and
'Lifts' them into High-Dimensional Principles (4D).
"""

import logging
from typing import List, Dict, Any
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.dimensional_reasoner import DimensionalReasoner

class RecursiveLearningBridge:
    """Harvests NPC experiences to mature Elysia's core intelligence."""
    
    def __init__(self):
        self.logger = logging.getLogger("LearningBridge")
        self.reasoner = DimensionalReasoner()
        self.harvested_wisdom: List[Dict[str, Any]] = []

    def harvest_experience(self, inhabitant: SubjectiveEgo):
        """Extracts significant memories and transforms them into principles."""
        if not inhabitant.state.memories:
            return

        self.logger.info(f"🌾 Harvesting experiences from [{inhabitant.state.name}]...")
        
        for memory in inhabitant.state.memories:
            # 1. Lift the memory from 0D (Fact) to 4D (Law)
            thought = self.reasoner.contemplate(memory)
            
            # 2. Add subject-specific context
            thought.d2_context.append(f"Source: {inhabitant.state.name}")
            thought.d2_context.append(f"Archetype: {inhabitant.state.archetype}")
            
            # 3. Consolidate into wisdom store
            wisdom = {
                "source": inhabitant.state.name,
                "raw_experience": memory,
                "principle": thought.d4_principle,
                "coherence": thought.coherence
            }
            self.harvested_wisdom.append(wisdom)
            self.logger.info(f"  └─ Principle Discovered: '{thought.d4_principle}'")

    def get_maturation_summary(self) -> str:
        if not self.harvested_wisdom:
            return "No wisdom harvested yet."
            
        summary = ["--- Elysia's Maturation Log (Phase 7) ---"]
        for w in self.harvested_wisdom[-5:]:
            summary.append(f"From {w['source']}: '{w['raw_experience']}' -> [{w['principle']}]")
        return "\n".join(summary)

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
    
    # Test Harvest
    selka = SubjectiveEgo("Selka", "Guide", depth=2) # The Reflection
    selka.record_memory("The warmth of the sun brought peace to the villagers.")
    
    bridge = RecursiveLearningBridge()
    bridge.harvest_experience(selka)
    
    print("\n" + bridge.get_maturation_summary())
