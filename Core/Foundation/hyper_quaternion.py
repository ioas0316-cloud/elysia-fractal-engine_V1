import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Quaternion:
    """
    Hyper-Quaternion (4D Number)
    Represents a point or rotation in 4D space.
    q = w + xi + yj + zk
    
    In Elysia's Consciousness:
    - w: Energy / Existence (Scalar)
    - i: Emotion (Vector X)
    - j: Logic (Vector Y)
    - k: Ethics (Vector Z)
    """
    w: float
    x: float
    y: float
    z: float

    def __add__(self, other):
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """
        Hamilton Product (Quaternion Multiplication).
        Encodes the interaction of two multi-dimensional concepts.
        """
        if isinstance(other, (int, float)):
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
            
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

    def dot(self, other) -> float:
        """
        Dot Product (Alignment).
        Returns a scalar representing how 'aligned' two quaternions are.
        """
        return self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z

    def norm(self) -> float:
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        n = self.norm()
        if n == 0: return Quaternion(1, 0, 0, 0) # Identity
        return Quaternion(self.w/n, self.x/n, self.y/n, self.z/n)

    def scale(self, scalar: float):
        """Scales the quaternion by a scalar."""
        return Quaternion(self.w * scalar, self.x * scalar, self.y * scalar, self.z * scalar)

    def add(self, other):
        """Explicit add method for clarity."""
        return self + other

    def distance(self, other: 'Quaternion') -> float:
        """
        Euclidean Distance between two 4D points.
        sqrt((w1-w2)^2 + (x1-x2)^2 + ...)
        """
        dw = self.w - other.w
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dw**2 + dx**2 + dy**2 + dz**2)
        
    def __repr__(self):
        return f"Q({self.w:.2f}, {self.x:.2f}i, {self.y:.2f}j, {self.z:.2f}k)"

@dataclass
class HyperWavePacket:
    """
    A 4D Thought Particle.
    Instead of a simple frequency, it has a 'Pose' in concept space.
    """
    energy: float       # Absolute Magnitude
    orientation: Quaternion # The 'Angle' of the thought (Normalized)
    time_loc: float     # Timestamp

    def resonate(self, other: 'HyperWavePacket') -> Tuple['Quaternion', float]:
        """
        Calculates the resonance between this thought and another.
        Returns:
            - Interaction (Quaternion): The resulting new thought vector (Hamilton Product).
            - Alignment (float): The degree of harmony (Dot Product).
        """
        # 1. Interaction: How do they transform each other?
        # We multiply their orientations to see the resulting spin.
        interaction = self.orientation * other.orientation
        
        # 2. Alignment: Are they pointing in the same direction?
        alignment = self.orientation.dot(other.orientation)
        
        return interaction, alignment

HyperQuaternion = Quaternion
