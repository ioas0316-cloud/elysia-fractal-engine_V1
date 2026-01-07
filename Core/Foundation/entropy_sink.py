"""
EntropySink (엔트로피 싱크)
=========================

"The Water Principle."

This module absorbs system errors (Resistance) and converts them into Entropy (Heat),
preventing the system from crashing. It allows Elysia to flow around obstacles.
"""

import logging
import traceback
import random
from typing import Any, Dict

logger = logging.getLogger("EntropySink")

class EntropySink:
    def __init__(self, resonance_field: Any):
        self.resonance = resonance_field
        logger.info("🌊 Entropy Sink Active. Ready to absorb resistance.")

    def absorb_resistance(self, exception: Exception, context: str) -> str:
        """
        Absorbs an exception, logs it as resistance, increases entropy,
        and returns a fallback action.
        """
        # 1. Calculate Resistance Magnitude
        # Simple errors are light, crashes are heavy.
        resistance_magnitude = 10.0
        
        # 2. Convert to Entropy (Heat)
        self.resonance.inject_entropy(resistance_magnitude)
        
        # 3. Log the Flow
        error_msg = str(exception)
        logger.warning(f"🌊 Resistance encountered in [{context}]: {error_msg}")
        logger.debug(traceback.format_exc())
        
        # 4. Determine Flow Direction (Fallback)
        # "If I cannot go straight, I go sideways."
        
        current_entropy = self.resonance.entropy
        
        if current_entropy > 90.0:
            # Too much heat, must cool down immediately
            return "REST"
            
        if "AttributeError" in str(type(exception)):
            # Structural issue -> Introspect
            return "THINK:Self"
            
        if "ImportError" in str(type(exception)) or "ModuleNotFoundError" in str(type(exception)):
            # Missing knowledge -> Search
            return "SEARCH:Python Library"
            
        # Default: Drift and Reflect
        return "THINK:Why did I fail?"

    def stabilize(self):
        """
        Active cooling if entropy is critical.
        """
        if self.resonance.entropy > 95.0:
            logger.warning("🌊 Critical Entropy. Forcing Emergency Venting.")
            self.resonance.dissipate_entropy(50.0)
