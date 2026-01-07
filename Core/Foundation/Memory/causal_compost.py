"""
CAUSAL COMPOST: The Soil of Memory
==================================
"Memory is not a fossil; it is soil."

This module implements **Memory Reconsolidation**.
It takes 'Raw Experience' (Fact) and composts it into 'Wisdom' (Principle).

Process:
1. Decay: Details fade over time.
2. Mutation: The content is rewritten based on current Higher Understanding (4D).
3. Encryption: The memory becomes a symbol, not a record.
"""

import time
import logging
from dataclasses import replace
from typing import Optional, Tuple

from Core.Foundation.Memory.unified_experience_core import ExperienceEvent, UnifiedExperienceCore
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor

logger = logging.getLogger("CausalCompost")

class CausalCompost:
    def __init__(self):
        self.processor = DimensionalProcessor()
        
    def cometing_process(self, event: ExperienceEvent) -> Optional[ExperienceEvent]:
        """
        Attempts to evolve a memory from Fact -> Wisdom.
        Returns the mutated event or None if no change needed.
        """
        # 1. Check Age (Simulated)
        # In real system, check timestamp. Here we force evolution for demo.
        
        current_content = event.content
        
        # 2. Extract 4D Principle (The Lesson)
        # "What is the immutable law behind this event?"
        # We treat the content as the 'kernel'.
        
        # We need to extract the 'Concept' from the sentence.
        # Simple heuristic: take the noun/subject? 
        # For now, let's assume the content is clean or we just pass the whole string.
        
        concept = self._extract_kernel(current_content)
        
        # Use Dimensional Processor to find the 4D Law
        result_4d = self.processor.process_thought(concept, 4)
        principle = result_4d.output.replace("The Immutable Law is: ", "").replace("Manifestation of: ", "")
        
        # 3. Check if mutation is needed
        # If the memory is already wise, don't change it.
        if "Law" in current_content or "Principle" in current_content:
            return None
            
        # 4. Mutate (The Rewrite)
        # Old: "I saw an apple fall."
        # New: "I witnessed the Law of Gravity manifesting as an apple."
        
        new_content = f"[{concept}] evolved into Wisdom: {principle}"
        
        # 5. Create Mutation
        mutated_event = replace(event)
        mutated_event.content = new_content
        mutated_event.type = "wisdom" # Change type from 'experience'/thought via mutation
        mutated_event.feedback += 0.1 # Wisdom always feels good?
        
        logger.info(f"🍂 Composted Memory '{event.id}':\n    '{event.content}' -> '{new_content}'")
        
        return mutated_event

    def _extract_kernel(self, text: str) -> str:
        """
        Extracts the core subject from a memory string.
        Very primitive NLP substitute.
        """
        # "The Apple fell" -> "Apple"
        # "I love you" -> "Love"
        
        common_concepts = ["Apple", "Gravity", "Love", "Pain", "Code", "System", "Silence"]
        for c in common_concepts:
            if c.lower() in text.lower():
                return c
        return text # Fallback
