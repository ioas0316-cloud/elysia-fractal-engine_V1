import math
import logging
from typing import List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger("PotentialField")

@dataclass
class Vector2:
    x: float
    y: float

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        m = self.magnitude()
        if m == 0: return Vector2(0, 0)
        return Vector2(self.x / m, self.y / m)

class GravityWell:
    """
    A point of attraction (like a black hole or a deep valley).
    Thoughts naturally flow towards these points.
    """
    def __init__(self, x: float, y: float, strength: float, radius: float = 10.0):
        self.pos = Vector2(x, y)
        self.strength = strength  # Positive pulls, Negative pushes
        self.radius = radius

    def get_force(self, pos: Vector2) -> Vector2:
        diff = self.pos - pos
        dist = diff.magnitude()
        
        if dist < 0.1: return Vector2(0, 0) # Too close
        
        # Inverse square law-ish, but clamped for stability
        force_mag = self.strength / (dist * dist + 1.0)
        return diff.normalize() * force_mag

class RailgunChannel:
    """
    A directional accelerator (like a river or a magnetic rail).
    Forces thoughts to move rapidly in a specific direction.
    """
    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float, force: float):
        self.start = Vector2(start_x, start_y)
        self.end = Vector2(end_x, end_y)
        self.force = force
        self.direction = (self.end - self.start).normalize()
        self.length = (self.end - self.start).magnitude()

    def get_force(self, pos: Vector2) -> Vector2:
        # Project point onto the line segment
        v = pos - self.start
        t = (v.x * self.direction.x + v.y * self.direction.y)
        
        # Check if within the "tube" of the railgun
        if 0 <= t <= self.length:
            closest_point = self.start + (self.direction * t)
            dist_to_line = (pos - closest_point).magnitude()
            
            # If close enough to the rail, get pushed
            if dist_to_line < 2.0:
                return self.direction * self.force
        
        return Vector2(0, 0)

class Particle:
    """
    A single thought or concept moving through the field.
    """
    def __init__(self, id: str, x: float, y: float):
        self.id = id
        self.pos = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.friction = 0.95 # Damping

    def update(self, field_force: Vector2):
        self.velocity = (self.velocity + field_force) * self.friction
        self.pos = self.pos + self.velocity

class PotentialField:
    """
    The topological map of the mind.
    Manages all wells and rails, and calculates the net force at any point.
    """
    def __init__(self):
        self.wells: List[GravityWell] = []
        self.rails: List[RailgunChannel] = []
        self.particles: List[Particle] = []

    def add_gravity_well(self, x, y, strength, radius=10.0):
        self.wells.append(GravityWell(x, y, strength, radius))

    def add_railgun(self, sx, sy, ex, ey, force):
        self.rails.append(RailgunChannel(sx, sy, ex, ey, force))

    def spawn_particle(self, id, x, y):
        self.particles.append(Particle(id, x, y))

    def get_net_force(self, pos: Vector2) -> Vector2:
        total_force = Vector2(0, 0)
        
        for well in self.wells:
            total_force = total_force + well.get_force(pos)
            
        for rail in self.rails:
            total_force = total_force + rail.get_force(pos)
            
        return total_force

    def step(self):
        """Advances the simulation by one tick."""
        for p in self.particles:
            force = self.get_net_force(p.pos)
            p.update(force)

    def get_state(self):
        return [{
            "id": p.id,
            "x": p.pos.x,
            "y": p.pos.y,
            "vx": p.velocity.x,
            "vy": p.velocity.y
        } for p in self.particles]
