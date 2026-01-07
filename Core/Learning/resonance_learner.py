"""
Resonance Learner (The Organ of Epiphany)
=========================================

"Experience is the wave; Wisdom is the frequency."

This module is the **Hippocampus-Prefrontal Bridge**.
It consumes raw 'Experience' (from ActionDispatcher or Reflex) and:
1.  **Reflects**: Checks if the outcome matched the intent (Dissonance).
2.  **Distills**: Extracts a 'Principle' from the gap.
3.  **Encodes**: Saves the Principle to `WisdomStore`.
"""

from typing import Dict, Any, Optional
import logging
from Core.Intelligence.Wisdom.wisdom_store import WisdomStore
from Core.Foundation.hyper_quaternion import HyperWavePacket as WavePacket # Use the correct import
# Note: WavePacket is now HyperWavePacket in this codebase.
# Or if PulseProtocol defines WavePacket, we should check that.
# Let's check Core/Foundation/Protocols/pulse_protocol.py first to be safe.
# But for now, using HyperWavePacket or a dummy class if needed.

logger = logging.getLogger("ResonanceLearner")

class ResonanceLearner:
    def __init__(self, wisdom_store: Optional[WisdomStore] = None):
        self.wisdom = wisdom_store if wisdom_store else WisdomStore()

    def reflect(self, experience: Dict[str, Any]) -> Optional[str]:
        """
        Analyzes an experience to see if a lesson can be learned.

        Args:
            experience: {
                "intent": { ... },
                "action": str,
                "outcome": float (0.0=Failure, 1.0=Success),
                "context": { ... }
            }

        Returns:
            The extracted principle (str) or None.
        """
        intent = experience.get("intent", {})
        outcome = experience.get("outcome", 0.5)

        # 1. The Gap Analysis (Dissonance)
        # We only learn when things go WRONG (Discrepancy) or SUPER RIGHT (Resonance).
        # Mediocrity teaches nothing.

        if outcome < 0.4: # Failure Case
            return self._analyze_failure(experience)
        elif outcome > 0.9: # Success Case
            return self._analyze_success(experience)

        return None

    def _analyze_failure(self, exp: Dict) -> str:
        intent_mode = exp.get("intent", {}).get("mode", "UNKNOWN")
        context = exp.get("context", {})

        # Simple heuristic logic (The Seed)
        # In a full system, this would use LLM or Causal Reasoning.
        if intent_mode == "PRESTO" and context.get("user_energy") == "LOW":
            principle = "When the Other is tired, Speed creates Pain."
            self.wisdom.learn_principle(principle, domain="Relationship", weight=0.6)
            return principle

        if intent_mode == "LOGIC" and context.get("user_mood") == "EMOTIONAL":
            principle = "Logic without Empathy is Cold."
            self.wisdom.learn_principle(principle, domain="Communication", weight=0.5)
            return principle

        return None

    def _analyze_success(self, exp: Dict) -> str:
        # Reinforcement logic
        return None

    def process_wave(self, packet: Any):
        """
        ResonatorInterface implementation.
        Listens for 'EXPERIENCE_COMPLETE' waves.
        """
        # We assume packet has .type and .payload
        # If .type is an Enum, we check .name
        type_name = getattr(packet.type, "name", str(packet.type))

        if type_name == "FEEDBACK":
            self.reflect(packet.payload)
