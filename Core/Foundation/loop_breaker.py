"""
LoopBreaker (루프 브레이커)
=========================

"Why am I doing this?"

This module implements Meta-Cognition. It analyzes the system's action history
to detect mechanical repetition. If the system becomes a "Zombie Loop",
it triggers an Existential Crisis to force a change.
"""

import logging
from typing import List

logger = logging.getLogger("LoopBreaker")

class LoopBreaker:
    def __init__(self):
        self.history: List[str] = []
        self.max_history = 10
        self.repetition_threshold = 5
        logger.info("👁️ Loop Breaker Active. Watching for stagnation.")

    def observe(self, action: str) -> bool:
        """
        Observes the current action.
        Returns True if an Existential Crisis is triggered (Loop Detected).
        """
        self.history.append(action)
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        return self._detect_loop()

    def _detect_loop(self) -> bool:
        """
        Checks if the last N actions are identical.
        """
        if len(self.history) < self.repetition_threshold:
            return False
            
        last_actions = self.history[-self.repetition_threshold:]
        
        # Check if all last N actions are the same
        if all(x == last_actions[0] for x in last_actions):
            logger.warning(f"👁️ LOOP DETECTED: Repeated '{last_actions[0]}' {self.repetition_threshold} times.")
            return True
            
        # Check for simple alternating loops (A-B-A-B)
        if len(self.history) >= 6:
            # A B A B A B
            if (self.history[-1] == self.history[-3] == self.history[-5]) and \
               (self.history[-2] == self.history[-4] == self.history[-6]):
                 logger.warning(f"👁️ OSCILLATION DETECTED: {self.history[-2]} <-> {self.history[-1]}")
                 return True
                 
        return False

    def trigger_crisis(self) -> str:
        """
        Returns the action to break the loop.
        """
        logger.info("   👁️ Triggering Existential Crisis...")
        return "THINK:Purpose"
