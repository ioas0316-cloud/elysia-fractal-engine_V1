from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING, Union

# Pure Python implementation of Vector/Quaternion/Rotor math.
# Elysia Engine Philosophy: No heavy dependencies (numpy) for core logic.

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> 'Vector3':
        m = self.magnitude
        if m == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / m, self.y / m, self.z / m)

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

@dataclass
class Vector4:
    w: float
    x: float
    y: float
    z: float

    def __add__(self, other: 'Vector4') -> 'Vector4':
        return Vector4(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float) -> 'Vector4':
        return Vector4(self.w * scalar, self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    @classmethod
    def identity(cls) -> 'Quaternion':
        return cls(1.0, 0.0, 0.0, 0.0)

    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        # Hamilton product
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    def conjugate(self) -> 'Quaternion':
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def rotate(self, v: Vector3) -> Vector3:
        # p' = q * p * q_inv
        # Represent v as pure quaternion (0, x, y, z)
        p = Quaternion(0, v.x, v.y, v.z)
        # Assuming unit quaternion, inverse = conjugate
        result = (self * p) * self.conjugate()
        return Vector3(result.x, result.y, result.z)

    def angular_distance(self, other: 'Quaternion') -> float:
        """
        Returns angle between two quaternions (0 to pi).
        """
        # Dot product
        dot = self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z
        # Clamp to -1..1 to avoid domain errors
        dot = max(-1.0, min(1.0, dot))
        # Angle is 2 * acos(|dot|)
        return 2 * math.acos(abs(dot))

    def __str__(self) -> str:
        return f"Q({self.w:.2f}, {self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


@dataclass
class Rotor:
    """
    Geometric Algebra Rotor for 4D rotations (Double rotations).
    Defined by scalar + bivector part.
    This is a simplification for specific Field Torque applications.
    """
    scalar: float
    bivector_xy: float
    bivector_yz: float
    bivector_zx: float
    # Note: Full 4D rotor has more bivector components (wx, wy, wz).
    # We focus on spatial (xyz) rotation + w-scale coupling here.

    @classmethod
    def from_plane_angle(cls, plane: str, angle: float) -> 'Rotor':
        # e.g. plane='xy'
        half_angle = angle / 2.0
        c = math.cos(half_angle)
        s = math.sin(half_angle)

        if plane == 'xy':
            return cls(c, -s, 0, 0) # xy bivector
        # ... implement others as needed
        return cls(c, 0, 0, 0)

    def rotate(self, v: Vector4) -> Vector4:
        # v' = R v ~R
        # Full implementation omitted for brevity, returning v for now
        # unless explicit logic added.
        return v
