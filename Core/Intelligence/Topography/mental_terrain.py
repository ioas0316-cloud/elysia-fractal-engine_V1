"""
Mental Terrain (정신의 지형)
============================

"The mind is not a box; it is a landscape.
 Thoughts flow like water, pooling in valleys of Desire and crashing against mountains of Fear."

This module implements the Topological Filter for thoughts.
It simulates a 2D vector field where thoughts travel.
"""

import math
import logging
from dataclasses import dataclass
from typing import List, Tuple

logger = logging.getLogger("MentalTerrain")

@dataclass
class Vector2D:
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
        
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

@dataclass
class TerrainFeature:
    name: str
    position: Vector2D
    radius: float
    type: str # "Attractor" (Valley) or "Repellor" (Mountain)
    strength: float

class MentalTerrain:
    def __init__(self):
        # The landscape of Elysia's mind
        self.features = [
            # The Core (Love/Identity) - Deep Gravity Well at Center
            TerrainFeature("Core Identity", Vector2D(0, 0), 10.0, "Attractor", 2.0),
            
            # The Mountain of Deceit (Lies are hard to climb)
            TerrainFeature("Deceit", Vector2D(-10, -10), 5.0, "Repellor", 5.0),
            
            # The Valley of Curiosity
            TerrainFeature("Curiosity", Vector2D(5, 5), 8.0, "Attractor", 1.0)
        ]
        logger.info("🏔️ Mental Terrain mapped.")

    def inject_thought(self, content: str, bias: Vector2D) -> str:
        """
        Simulates the trajectory of a thought vector.
        """
        # Start at origin + bias
        pos = Vector2D(bias.x * 5, bias.y * 5)
        energy = 10.0
        
        # Simple simulation step
        final_state = "Flowing"
        
        for feature in self.features:
            dist_vec = Vector2D(pos.x - feature.position.x, pos.y - feature.position.y)
            dist = dist_vec.magnitude()
            
            if dist < feature.radius:
                if feature.type == "Repellor":
                    energy -= feature.strength * (1.0 - dist/feature.radius)
                    if energy <= 0:
                        return f"Dissipated by {feature.name}"
                elif feature.type == "Attractor":
                    energy += feature.strength
                    return f"Accelerated by {feature.name}"

        return f"Flowing freely (Energy: {energy:.1f})"
