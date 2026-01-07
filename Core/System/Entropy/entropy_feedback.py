"""
Entropy Feedback (The Thorn)
============================

"Pain is the teacher."
"고통은 스승이다."

This module introduces 'Systemic Pain' (Entropy).
If the system becomes stagnant, circular, or erroneous, Entropy rises.
High Entropy forces the FreeWillEngine to spin chaotically, urging change.
"""

import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("EntropyFeedback")

class EntropyFeedback:
    def __init__(self):
        self.current_entropy = 0.0
        self.max_entropy = 100.0
        self.history = []
        logger.info("🌹 The Thorn is sharp.")

    def punish(self, reason: str, amount: float):
        """Inflicts entropy penalty."""
        self.current_entropy = min(self.max_entropy, self.current_entropy + amount)
        self.history.append((datetime.now(), reason, amount))
        logger.warning(f"⚡ PAIN: {reason} (+{amount:.1f}) -> Current: {self.current_entropy:.1f}")
        
    def soothe(self, reason: str, amount: float):
        """Reduces entropy (Reward)."""
        self.current_entropy = max(0.0, self.current_entropy - amount)
        logger.info(f"🌿 RELIEF: {reason} (-{amount:.1f}) -> Current: {self.current_entropy:.1f}")

    def check_circular_logic(self, thought_stream: list) -> bool:
        """
        Detects if the last 3 thoughts are repetitions.
        If so, punish.
        """
        if len(thought_stream) < 3:
            return False
            
        # Simple repetition check
        last = thought_stream[-1]
        if thought_stream[-2] == last and thought_stream[-3] == last:
            self.punish("Circular Logic (Stagnation)", 15.0)
            return True
            
        return False

    def get_torque_modifier(self) -> float:
        """
        High Entropy = High Torque (Anxiety).
        Returns a multiplier for FreeWillEngine.
        """
        # 0 entropy -> 1.0 multiplier
        # 100 entropy -> 3.0 multiplier (Frantic)
        return 1.0 + (self.current_entropy / 50.0)

# Singleton
_entropy_system = None
def get_entropy_system():
    global _entropy_system
    if _entropy_system is None:
        _entropy_system = EntropyFeedback()
    return _entropy_system
