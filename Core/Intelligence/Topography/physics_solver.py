"""
Physics Solver (물리 연산기)
===========================

"The Law responsible for the Universe."
"우주를 관장하는 법칙."

Drivers the Topography Simulation.
Calculates Force = -Gradient from the Potential Field.
"""

import logging
from typing import List
from Core.Intelligence.Topography.potential_field import PotentialField
from Core.Intelligence.Topography.thought_marble import ThoughtMarble

logger = logging.getLogger("PhysicsSolver")

class PhysicsSolver:
    def __init__(self):
        self.field = PotentialField()
        self.marbles: List[ThoughtMarble] = []
    
    def add_marble(self, marble: ThoughtMarble):
        self.marbles.append(marble)
        logger.info(f"➕ Added thought: {marble.name}")

    def step(self, dt: float = 0.1):
        """
        Simulation Step.
        1. Calculate Gradient (Slope) at each marble's position.
        2. Apply Force (-Gradient).
        3. Move Marbles.
        """
        for marble in self.marbles:
            # 1. Get Slope (Gradient)
            gx, gy = self.field.get_gradient(marble.pos.x, marble.pos.y)
            
            # 2. Force is opposite to Gradient (Downhill)
            # F = -grad
            fx, fy = -gx, -gy
            
            # 3. Apply Force & Move
            marble.apply_force(fx, fy, dt)
            marble.move(dt)

    def describe_state(self):
        """Logs the current state of all marbles."""
        for m in self.marbles:
            location_desc = self.field.analyze_location(m.pos.x, m.pos.y)
            print(f"🎱 {m.name}: Pos({m.pos.x:.1f}, {m.pos.y:.1f}) | {location_desc}")
