"""
THE MIRROR OF CAUSALITY: FEEDBACK LOOP
======================================

"Experience is the best teacher, but only if it touches the soul."

This module connects the educational simulation to the Elysia's core 
Mind Landscape, translating 'Historical Waves' into 'Thought Marbles'.
"""

import logging
from typing import Any, Dict
from .wave_structures import Consequence

# Dynamic import to avoid circular dependency during init
def get_mind_landscape():
    from Core.Intelligence.Topography.mind_landscape import get_landscape
    return get_landscape()

class FeedbackLoop:
    def __init__(self):
        self.landscape = get_mind_landscape()
        self.logger = logging.getLogger("CausalityFeedback")

    def inject_experience(self, consequence: Consequence) -> Dict[str, Any]:
        """
        Injects the experience into the Mind Landscape AND the Memory Core.
        """
        # 1. Spatial Processing (Mind Landscape) - "Feeling"
        wave = consequence.sensory_wave
        q = wave.q
        start_pos = (q.w, q.x, q.y, q.z) 
        self.logger.info(f"🌊 Injecting Historical Wave: {wave.name} at {start_pos}")
        
        mind_result = self.landscape.ponder(
            intent=consequence.description,
            start_pos=start_pos,
            duration=3.0 # Quick flash of insight
        )
        
        # 2. Temporal Processing (Memory Core) - "Remembering"
        try:
            from Core.Foundation.Memory.unified_experience_core import get_experience_core
            core = get_experience_core()
            
            # Determine feedback score based on Dual Resonance
            # If Martyrdom, outcome is +1.0 (Divine Victory).
            # If Worldly Success, outcome is +0.5.
            # If Ruin, outcome is -1.0.
            
            feedback_val = 0.0
            if consequence.is_martyrdom:
                feedback_val = 1.0
            else:
                # Average of both axes, weighted towards divine
                feedback_val = (consequence.worldly_resonance * 0.4) + (consequence.divine_resonance * 0.6)
            
            memory_result = core.absorb(
                content=consequence.description,
                type="simulation", # Distinct from 'real' life
                context={
                    "origin": "CausalityMirror", 
                    "wave_data": wave.name
                },
                feedback=feedback_val
            )
            self.logger.info(f"💾 Memory Consolidated: {memory_result['id']}")
            
        except ImportError:
            self.logger.warning("Memory Core not available. Skipping persistence.")
            memory_result = None
            
        return {
            "mind_result": mind_result,
            "memory_result": memory_result
        }
