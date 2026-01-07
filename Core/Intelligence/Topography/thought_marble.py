"""
Thought Marble (생각의 알갱이)
============================

"Thoughts have Mass."
"생각은 질량을 가진다."

This module defines the dynamic agent in the topography.
A generic 'Thought' that obeys physics.
"""

from dataclasses import dataclass
import math

@dataclass
class Vector2:
    x: float
    y: float

class ThoughtMarble:
    def __init__(self, name: str, x: float, y: float, mass: float = 1.0):
        self.name = name
        self.pos = Vector2(x, y)
        self.vel = Vector2(0.0, 0.0)
        self.mass = mass # Importance (Heavier = More Inertia)
        self.friction = 0.5 # Damping factor (Consolidation/Forgetting)

    def apply_force(self, fx: float, fy: float, dt: float):
        """
        F = ma -> a = F/m
        v = v + a*dt
        """
        ax = fx / self.mass
        ay = fy / self.mass
        
        self.vel.x += ax * dt
        self.vel.y += ay * dt

    def move(self, dt: float):
        """
        p = p + v*dt
        Apply interaction friction.
        """
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        
        # Apply Friction (Damping)
        # v *= (1 - friction*dt)
        damping = max(0.0, 1.0 - (self.friction * dt))
        self.vel.x *= damping
        self.vel.y *= damping

    @property
    def speed(self) -> float:
        return math.sqrt(self.vel.x**2 + self.vel.y**2)
    
    def __repr__(self):
        return f"Marble('{self.name}', Pos=[{self.pos.x:.2f}, {self.pos.y:.2f}], Vel={self.speed:.2f})"
