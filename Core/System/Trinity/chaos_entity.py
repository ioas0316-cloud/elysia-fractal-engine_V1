"""
Chaos Entity (The Body / Instinct)
=================================
"Life from Clay, Motion from Stillness."

The Instinct/Creative component of the Trinity.
Based on 'Slime Mind' and 'Kuramoto Network'.
Responsibility:
- High Entropy Generation (Idea Spawning)
- Pattern Recognition (Fluid Dynamics)
- Emotional Resonance (Raw Feeling)
"""

import random
import math
import logging
from typing import Dict, Any, List

class ChaosEntity:
    def __init__(self):
        self.logger = logging.getLogger("ChaosEntity")
        self.entropy_level = 0.9
        self.logger.info("🔴 Chaos Entity (Body/Instinct) Initialized.")
        
        # Internal State: Mini Slime Grid (Abstracted)
        self.grid_state = [[random.uniform(0,1) for _ in range(5)] for _ in range(5)]

    def feel(self, input_signal: str) -> Dict[str, Any]:
        """
        React to input with raw instinct/emotion.
        Uses non-linear 'feeling' logic.
        """
        self.logger.info(f"🔴 Chaos Feeling on: '{input_signal}'")
        
        # 1. Perturb the grid (Reaction)
        intensity = len(input_signal) / 100.0
        self._agitate(intensity)
        
        # 2. Check for emergence
        pattern_density = self._measure_density()
        
        # 3. Generate Emotional Response
        emotions = ["Excitement", "Confusion", "Boredom", "Passion", "Fear"]
        # Pattern density determines emotion complexity
        idx = int(pattern_density * len(emotions)) % len(emotions)
        emotion = emotions[idx]
        
        return {
            "emotion": emotion,
            "intensity": min(1.0, intensity * 2),
            "pattern_density": pattern_density,
            "raw_impulse": f"I feel {emotion} about this!"
        }

    def _agitate(self, force: float):
        """Simulate fluid agitation."""
        for r in range(5):
            for c in range(5):
                # Non-linear update
                self.grid_state[r][c] += math.sin(force * (r+c)) * 0.1
                self.grid_state[r][c] = max(0.0, min(1.0, self.grid_state[r][c]))

    def _measure_density(self) -> float:
        """Measure how 'thick' the current thought texture is."""
        total = sum(sum(row) for row in self.grid_state)
        return total / 25.0

    def generate_random_seed(self) -> str:
        """Spawn a random creative seed."""
        seeds = ["Crimson Fire", "Silent Ocean", "Broken Clock", "Flying Whale"]
        return random.choice(seeds)
