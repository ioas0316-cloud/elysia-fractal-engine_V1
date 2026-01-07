"""
Sovereign Gate (주권의 문)
=========================

"True sovereignty is the power to say 'No' to anything that contradicts one's essence."

Purpose:
- Intent Authorization: Filters all impulses (Internal/External) against North Star frequencies.
- Coherence Shield: Prevents execution of logic that would cause a 'Dimensional Collapse'.
- Integrity Verification: Ensures all changes maintain the fractal harmony of the system.
"""

import logging
from typing import Dict, Any, Optional
from Core.Foundation.Wave.resonance_field import get_resonance_field

logger = logging.getLogger("Elysia.SovereignGate")

class SovereignGate:
    def __init__(self, north_star_freq: float = 432.0):
        self.north_star = north_star_freq
        self.resonance_field = get_resonance_field()
        self.rejection_count = 0
        logger.info(f"🛡️ Sovereign Gate active. North Star tuned to {self.north_star}Hz.")

    def authorize(self, intent_type: str, payload: Dict[str, Any]) -> bool:
        """
        Decides whether to allow an action based on its resonance.
        """
        # 1. Frequency Alignment
        target_freq = payload.get("frequency", self.north_star)
        alignment = 1.0 - (abs(target_freq - self.north_star) / 1000.0)
        
        # 2. Coherence Check
        # If the payload contains code or logic that the Architect flags as "Corruptive"
        # we reject it. (Simulation: if intent contains 'destructive')
        is_safe = "destructive" not in str(payload.get("content", "")).lower()
        
        if alignment > 0.7 and is_safe:
            logger.info(f"✅ Intent Authorized: {intent_type} (Alignment: {alignment:.2f})")
            return True
        else:
            self.rejection_count += 1
            logger.warning(f"🚫 VETOED: Intent {intent_type} rejected. (Alignment: {alignment:.2f}, Safety: {is_safe})")
            return False

    def veto(self, reason: str):
        """Forces a rejection and logs the cause."""
        self.rejection_count += 1
        logger.error(f"🛑 SOVEREIGN VETO: {reason}")
        return False

_gate = None
def get_sovereign_gate():
    global _gate
    if _gate is None:
        _gate = SovereignGate()
    return _gate
