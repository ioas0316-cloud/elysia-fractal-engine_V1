from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vector3:
        m = self.magnitude
        if m == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / m, self.y / m, self.z / m)

    def __add__(self, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector3:
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> Vector3:
        return self.__mul__(scalar)

    def dot(self, other: Vector3) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3) -> Vector3:
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __repr__(self) -> str:
        return f"Vec3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    @staticmethod
    def identity() -> Quaternion:
        return Quaternion(1.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_axis_angle(axis: Vector3, angle_rad: float) -> Quaternion:
        half_angle = angle_rad * 0.5
        s = math.sin(half_angle)
        u = axis.normalize()
        return Quaternion(
            w=math.cos(half_angle),
            x=u.x * s,
            y=u.y * s,
            z=u.z * s,
        )

    def normalize(self) -> Quaternion:
        m = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if m == 0:
            return Quaternion.identity()
        return Quaternion(self.w / m, self.x / m, self.y / m, self.z / m)

    def __mul__(self, other: Quaternion) -> Quaternion:
        return Quaternion(
            w=self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            x=self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            y=self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            z=self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def rotate(self, v: Vector3) -> Vector3:
        """Rotate vector v by this quaternion."""
        # q * v * q_conjugate
        # Optimized implementation
        u = Vector3(self.x, self.y, self.z)
        s = self.w

        # 2.0 * dot(u, v) * u
        uv_dot = u.dot(v)
        term1 = u * (2.0 * uv_dot)

        # (s*s - dot(u,u)) * v
        uu_dot = u.dot(u)
        term2 = v * (s*s - uu_dot)

        # 2.0 * s * cross(u, v)
        cross_uv = u.cross(v)
        term3 = cross_uv * (2.0 * s)

        return term1 + term2 + term3

    def __repr__(self) -> str:
        return f"Quat({self.w:.3f}, {self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
