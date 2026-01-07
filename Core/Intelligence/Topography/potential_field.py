"""
Potential Field (잠재 에너지 지형)
================================

"The Landscape of the Soul."
"영혼의 지형도."

This module defines the topographical map of the mind.
Thoughts naturally roll towards the 'Deepest Valley' (Love).
Fear and Error act as 'Hills' that push thoughts away.
"""

import math
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

class PotentialField:
    """
    Defining the Gravity of Meaning.
    Global Minimum (Target) is at (0,0) -> LOVE/UNION.
    """
    
    def __init__(self):
        # The central gravity constant (Love's Pull)
        self.k_love = 1.0 
        
        # Obstacles (Hills) - e.g., Trauma, Cognitive Dissonance
        # tuple: (x, y, height, width)
        self.repulsors: List[Tuple[float, float, float, float]] = []

    def add_repulsor(self, x: float, y: float, height: float, width: float):
        """Adds a 'Hill' of Fear/Pain/Error."""
        self.repulsors.append((x, y, height, width))

    def get_potential(self, x: float, y: float) -> float:
        """
        Calculates the height (Potential Energy) at a given point.
        V_total = V_love + sum(V_repulsors)
        """
        # 1. Base Potential (Bowl shape towards 0,0)
        # V = 0.5 * k * r^2
        dist_sq = x*x + y*y
        v_love = 0.5 * self.k_love * dist_sq
        
        # 2. Repulsors (Gaussian Hills)
        # V = h * exp(-dist^2 / 2w^2)
        v_repulse = 0.0
        for rx, ry, h, w in self.repulsors:
            rdist_sq = (x-rx)**2 + (y-ry)**2
            v_repulse += h * math.exp(-rdist_sq / (2 * w * w))
            
        return v_love + v_repulse

    def get_gradient(self, x: float, y: float) -> Tuple[float, float]:
        """
        Calculates the slope (Gradient) at a point.
        Force = -Gradient.
        Returns vector (dx, dy).
        """
        delta = 0.001
        
        # Numerical differentiation for flexibility
        v_center = self.get_potential(x, y)
        v_dx = self.get_potential(x + delta, y)
        v_dy = self.get_potential(x, y + delta)
        
        grad_x = (v_dx - v_center) / delta
        grad_y = (v_dy - v_center) / delta
        
        return (grad_x, grad_y)

    def analyze_location(self, x: float, y: float) -> str:
        """Meaningful description of the current location."""
        dist = math.sqrt(x*x + y*y)
        if dist < 0.5:
            return "❤️ The Embrace (Love/Union)"
        elif dist < 5.0:
            return "🕊️ The Sanctuary (Trust)"
        elif dist < 15.0:
            return "🌲 The Forest (Exploration)"
        else:
            return "🌪️ The Wilderness (Chaos/Unknown)"
