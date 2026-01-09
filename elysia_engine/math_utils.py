from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Union, Tuple


@dataclass
class Vector3:
    """A 3D vector class for spatial calculations."""
    
    x: float
    y: float
    z: float

    @property
    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vector3:
        """Return a unit vector in the same direction."""
        m = self.magnitude
        if m == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / m, self.y / m, self.z / m)

    def __add__(self, other: Vector3) -> Vector3:
        """Add two vectors."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector3) -> Vector3:
        """Subtract two vectors."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: Union[int, float]) -> Vector3:
        """Multiply vector by a scalar."""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> Vector3:
        """Right multiply vector by a scalar."""
        return self.__mul__(scalar)

    def dot(self, other: Vector3) -> float:
        """Calculate the dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vector3) -> Vector3:
        """Calculate the cross product with another vector."""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def distance_to(self, other: Vector3) -> float:
        """Calculate the distance to another vector."""
        return (self - other).magnitude

    def lerp(self, other: Vector3, t: float) -> Vector3:
        """
        Linear interpolation between this vector and another.
        
        Args:
            other: Target vector
            t: Interpolation factor (0-1)
            
        Returns:
            Interpolated vector
        """
        return Vector3(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
            self.z + (other.z - self.z) * t,
        )

    def __repr__(self) -> str:
        return f"Vec3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


@dataclass
class Vector4:
    """A 4D vector class for Hyperspace calculations (W, X, Y, Z)."""
    w: float
    x: float
    y: float
    z: float

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vector4:
        m = self.magnitude
        if m == 0:
            return Vector4(0, 0, 0, 0)
        return Vector4(self.w / m, self.x / m, self.y / m, self.z / m)

    def __add__(self, other: Vector4) -> Vector4:
        return Vector4(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector4) -> Vector4:
        return Vector4(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> Vector4:
        return Vector4(self.w * scalar, self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other: Vector4) -> float:
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self) -> str:
        return f"Vec4(w={self.w:.2f}, x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"


@dataclass
class Quaternion:
    """A quaternion class for rotations."""
    
    w: float
    x: float
    y: float
    z: float

    @staticmethod
    def identity() -> Quaternion:
        """Return the identity quaternion (no rotation)."""
        return Quaternion(1.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_axis_angle(axis: Vector3, angle_rad: float) -> Quaternion:
        """
        Create a quaternion from an axis and angle.
        
        Args:
            axis: Rotation axis (will be normalized)
            angle_rad: Rotation angle in radians
            
        Returns:
            Quaternion representing the rotation
        """
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
        """Return a normalized quaternion."""
        m = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if m == 0:
            return Quaternion.identity()
        return Quaternion(self.w / m, self.x / m, self.y / m, self.z / m)

    def conjugate(self) -> Quaternion:
        """Return the conjugate of this quaternion."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __mul__(self, other: Quaternion) -> Quaternion:
        """Multiply two quaternions (compose rotations)."""
        return Quaternion(
            w=self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            x=self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            y=self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            z=self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def rotate(self, v: Vector3) -> Vector3:
        """
        Rotate a vector by this quaternion.
        
        Args:
            v: Vector to rotate
            
        Returns:
            Rotated vector
        """
        u = Vector3(self.x, self.y, self.z)
        s = self.w

        uv_dot = u.dot(v)
        term1 = u * (2.0 * uv_dot)

        uu_dot = u.dot(u)
        term2 = v * (s * s - uu_dot)

        cross_uv = u.cross(v)
        term3 = cross_uv * (2.0 * s)

        return term1 + term2 + term3

    def dot(self, other: Quaternion) -> float:
        """Calculate the dot product with another quaternion."""
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def angular_distance(self, other: Quaternion) -> float:
        """
        Calculate the angular distance to another quaternion.

        Returns the angle in radians (0 to pi).
        Uses the formula: angle = acos((q1 . q2) / (|q1| * |q2|))

        Note: We normalize the inputs to handle non-unit quaternions (Depth != 1).
        We use acos(dot) treating them as 4D vectors for angular separation.
        """
        # Calculate magnitudes squared
        mag_sq1 = self.w**2 + self.x**2 + self.y**2 + self.z**2
        mag_sq2 = other.w**2 + other.x**2 + other.y**2 + other.z**2

        if mag_sq1 == 0 or mag_sq2 == 0:
            return 0.0 # Origin has 0 distance to everything angularly? Or undefined. Let's say 0.

        denom = math.sqrt(mag_sq1 * mag_sq2)

        d = self.dot(other) / denom

        # Clamp to avoid numerical errors
        d = max(-1.0, min(1.0, d))
        return math.acos(d)

    def __repr__(self) -> str:
        return f"Quat({self.w:.3f}, {self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


@dataclass
class Rotor:
    """
    Geometric Algebra Rotor for 4D Euclidean Space (Cl(4,0)).
    Used to rotate 4D vectors (Vector4) efficiently without 4x4 Matrices.

    Structure: Even Subalgebra of Cl(4,0)
    1 Scalar (a)
    6 Bivectors (wx, wy, wz, xy, xz, yz) -> Representing the 6 rotation planes
    1 Pseudoscalar (p) -> e_wxyz
    """
    a: float
    # Bivectors (planes)
    b_wx: float
    b_wy: float
    b_wz: float
    b_xy: float
    b_xz: float
    b_yz: float
    # Pseudoscalar
    p: float

    @staticmethod
    def identity() -> Rotor:
        return Rotor(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    @staticmethod
    def from_plane_angle(plane: str, angle_rad: float) -> Rotor:
        """
        Create a rotor for a simple rotation in a principal plane.
        R = cos(theta/2) - B * sin(theta/2)
        where B is the unit bivector of the plane.

        Args:
            plane: 'wx', 'wy', 'wz', 'xy', 'xz', 'yz'
            angle_rad: Rotation angle
        """
        half = angle_rad * 0.5
        c = math.cos(half)
        s = -math.sin(half) # Note: exp(-B*theta/2) = c - B*s

        r = Rotor.identity()
        r.a = c

        if plane == 'wx': r.b_wx = s
        elif plane == 'wy': r.b_wy = s
        elif plane == 'wz': r.b_wz = s
        elif plane == 'xy': r.b_xy = s
        elif plane == 'xz': r.b_xz = s
        elif plane == 'yz': r.b_yz = s

        return r

    def normalize(self) -> Rotor:
        # Simplistic normalization for now (sum of squares of all components)
        # In general, R R_rev = 1.
        mag_sq = (self.a**2 + self.b_wx**2 + self.b_wy**2 + self.b_wz**2 +
                  self.b_xy**2 + self.b_xz**2 + self.b_yz**2 + self.p**2)
        if mag_sq == 0: return Rotor.identity()
        m = math.sqrt(mag_sq)
        return Rotor(
            self.a/m, self.b_wx/m, self.b_wy/m, self.b_wz/m,
            self.b_xy/m, self.b_xz/m, self.b_yz/m, self.p/m
        )

    def rotate(self, v: Vector4) -> Vector4:
        """
        Rotates a Vector4 using the sandwich product: v' = R v R_reverse
        Implementation expanded for Cl(4,0).
        This is an optimized expansion of the geometric product logic.
        """
        # For a simple plane rotation R = c - B*s, and unit vector v.
        # This implementation handles the full 8-component Rotor interaction.
        # Due to complexity of manually expanding 8x4x8 multiplication in pure python,
        # we will implement the logic for the specific case of simple rotors or use a simplified
        # linear map derived from the rotor components if possible.

        # However, to be "correct", we must do the full GA product.
        # v is a vector (grade 1). R is even (grades 0, 2, 4).
        # v' = R v R~

        # Let's use a simpler approach for the specific request:
        # If the user wants to solve "Bottleneck", expanding the full product here
        # might be as heavy as matrix mult if not careful.
        # But `R` is usually sparse (simple rotations).

        # Optimization: If p=0 and only one bivector is non-zero (Simple Rotation), use optimized formula.

        # Helper: Geometric Product of Rotor(R) and Vector(v) -> Result is Odd (Vector + Trivector)
        # Rv = (a + B + p) v = av + Bv + pv
        # Then (Rv)R~ ...

        # For the sake of the constraint "1060 3GB optimization", we will implement
        # the exact calculation for the components.

        # Mapping: e1=w, e2=x, e3=y, e4=z
        w, x, y, z = v.w, v.x, v.y, v.z

        # R coefficients
        a = self.a
        b12, b13, b14 = self.b_wx, self.b_wy, self.b_wz
        b23, b24, b34 = self.b_xy, self.b_xz, self.b_yz
        p = self.p # e1234

        # This full expansion is notoriously large.
        # But wait, we can cheat slightly if we assume mostly simple rotations.
        # OR we can just implement the matrix form of the rotor on the fly.
        # R v R~ corresponds to a matrix M.
        # M_col1 = R e1 R~, etc.

        # Let's do the partial updates.
        # If this is too complex for a single function, we rely on the fact that
        # most use cases will be single-plane rotations.

        # Let's try to implement the exact transform for a general Rotor.
        # It is just linear algebra after all.

        # 1. Calculate R * v (Geometric Product)
        # v = w e1 + x e2 + y e3 + z e4
        # R = a + b12 e12 ...

        # grade 1 part of Rv:
        # a*w e1 + a*x e2 ...
        # b12*x e12 e2 = b12*x e1 = -b12*x e1? No e12 e2 = e1 (e2 e2) = e1.
        # b12*w e12 e1 = -b12*w e2.

        # Let's defer to a helper or just do the full expansion for w,x,y,z
        # It's actually faster to just convert R to Matrix locally?
        # No, that defeats the purpose.

        # Let's implement the specific expansion for w (e1 component of result)
        # v' = R v R~
        # If R is normalized, R~ is just negating the bivector and pseudo parts.

        # Let's stick to a robust implementation.
        # Source: "Geometric Algebra for Computer Science"

        # For this task, I will implement a simplified version that handles
        # superposition of planar rotations correctly.

        # Temp vars for R components
        a = self.a
        b_wx, b_wy, b_wz = self.b_wx, self.b_wy, self.b_wz
        b_xy, b_xz, b_yz = self.b_xy, self.b_xz, self.b_yz
        q = self.p

        # Vector components
        v0, v1, v2, v3 = v.w, v.x, v.y, v.z

        # R * v
        # Result has Vector (1) and Trivector (3) parts.

        # Let's construct a temporary multivector product (Rv)
        # Grade 1 (Vector) components of Rv:
        t0 = a*v0 + b_wx*v1 + b_wy*v2 + b_wz*v3
        t1 = a*v1 - b_wx*v0 + b_xy*v2 + b_xz*v3
        t2 = a*v2 - b_wy*v0 - b_xy*v1 + b_yz*v3
        t3 = a*v3 - b_wz*v0 - b_xz*v1 - b_yz*v2

        # Grade 3 (Trivector) components of Rv:
        # e123 (xyz), e124 (wxz?), no...
        # e123 comes from b12*e3(no e12e3=e123), b23*e1, b31*e2...
        # notation: 0=w, 1=x, 2=y, 3=z
        # b_wx=01, b_wy=02, b_wz=03, b_xy=12, b_xz=13, b_yz=23

        # Trivector components:
        # T012 (wxy): b_xy*w + b_wx*y - b_wy*x + q*z (?)
        # q*z = e0123 * e3 = e012 (since e3e3=1, sign depends on swaps)
        # e0123 e3 = -e012 e3 e3 = -e012.
        # Wait, e0123 e3: swap 3 past 2,1,0? No.
        # e0 e1 e2 e3 e3 = e0 e1 e2. Correct.

        # Let's define T012(wxy), T013(wxz), T023(wyz), T123(xyz)
        # t_xyz = a*0 + ... + q*v0

        t_wxy = b_wx*v2 - b_wy*v1 + b_xy*v0 + q*v3
        t_wxz = b_wx*v3 - b_wz*v1 + b_xz*v0 - q*v2
        t_wyz = b_wy*v3 - b_wz*v2 + b_yz*v0 + q*v1
        t_xyz = b_xy*v3 - b_xz*v2 + b_yz*v1 - q*v0

        # Now multiply by R_reverse
        # R~ = (a, -B, q) because reverse of bivector is -B, reverse of quadvector is q?
        # Reverse of e01 is e10 = -e01. Correct.
        # Reverse of e0123 is e3210 = e0123. (4 swaps to move 3, 3 to move 2... total 6 swaps. even).
        # So q stays q.

        ar = a
        br_wx, br_wy, br_wz = -b_wx, -b_wy, -b_wz
        br_xy, br_xz, br_yz = -b_xy, -b_xz, -b_yz
        qr = q # Reverse of pseudoscalar in 4D is itself

        # (Vector T + Trivector U) * (Scalar A + Bivector B + Quad Q)
        # We only want the Vector part of the result.

        # Result Vector part W' (e0):
        # From Vector * Scalar: t0 * ar
        # From Vector * Bivector: t1*br_wx (e1 e01 = -e0), t2*br_wy, t3*br_wz...
        # From Trivector * Bivector: t_wxy * br_xy (e012 e12 = -e0), t_wxz*br_xz, t_wyz*br_yz
        # From Trivector * Quad: t_xyz * qr (e123 e0123 = -e0)

        res_w = (t0*ar
                 - t1*br_wx - t2*br_wy - t3*br_wz
                 - t_wxy*br_xy - t_wxz*br_xz - t_wyz*br_yz
                 + t_xyz*qr)

        # Result Vector part X' (e1):

        res_x = (t1*ar
                 + t0*br_wx - t2*br_xy - t3*br_xz
                 + t_wxy*br_wy + t_wxz*br_wz - t_xyz*br_yz
                 - t_wyz*qr)

        # Result Vector part Y' (e2):

        res_y = (t2*ar
                 + t0*br_wy + t1*br_xy - t3*br_yz
                 - t_wxy*br_wx + t_wyz*br_wz + t_xyz*br_xz
                 + t_wxz*qr)

        # Result Vector part Z' (e3):
        # t3*ar
        # t0*br_wz (e0 e03 = e3). +
        # t1*br_xz (e1 e13 = e3). +
        # t2*br_yz (e2 e23 = e3). +
        # Trivectors:
        # t_wxz * br_wx (e013 e01 = -e3). -
        # t_wyz * br_wy (e023 e02 = -e3). -
        # t_xyz * br_xy (e123 e12 = -e3). -
        # t_wxy * qr (e012 e0123 = -e3). -

        res_z = (t3*ar
                 + t0*br_wz + t1*br_xz + t2*br_yz
                 - t_wxz*br_wx - t_wyz*br_wy - t_xyz*br_xy
                 - t_wxy*qr)

        return Vector4(res_w, res_x, res_y, res_z)
