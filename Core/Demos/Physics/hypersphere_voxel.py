"""
Hyper-Sphere Voxel (Omni-Voxel) Prototype
=========================================

"Memory is not storage; it is a state of rotation."

This script implements the mathematical foundation of the Omni-Voxel:
1. Quaternion Algebra (for S^3 Hypersphere)
2. Phase Rotation (Zoom In/Out via Angle)
3. Stereographic Projection (4D -> 3D Visualization)
"""

import numpy as np
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
logger = logging.getLogger("OmniVoxel")

class Quaternion:
    """
    A 4D Number representing a point on the S^3 Hypersphere.
    q = w + xi + yj + zk
    """
    def __init__(self, w, x, y, z):
        self.q = np.array([w, x, y, z], dtype=np.float64)

    @property
    def w(self): return self.q[0]
    @property
    def x(self): return self.q[1]
    @property
    def y(self): return self.q[2]
    @property
    def z(self): return self.q[3]

    def __repr__(self):
        return f"Q({self.w:.3f}, {self.x:.3f}i, {self.y:.3f}j, {self.z:.3f}k)"

    def norm(self):
        return np.sqrt(np.sum(self.q**2))

    def normalize(self):
        n = self.norm()
        if n > 0:
            self.q /= n
        return self

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def __mul__(self, other):
        """Hamilton Product"""
        w1, x1, y1, z1 = self.q
        w2, x2, y2, z2 = other.q

        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

class OmniVoxel:
    """
    The Omni-Voxel.
    A single unit of intelligence that exists on the Hypersphere.
    """
    def __init__(self, data_seed: float = 1.0):
        # Initialize as Identity (North Pole of S^3)
        # w=1 means "Pure Potential" (No Spin)
        self.state = Quaternion(data_seed, 0, 0, 0).normalize()
        logger.info(f"⚪ OmniVoxel Born: {self.state}")

    def rotate_phase(self, theta: float, axis: tuple = (1, 0, 0)):
        """
        Applies Phase Rotation (The Act of Thinking).
        theta: The angle of thought (Intensity).
        axis: The direction of thought (x, y, z).
        """
        # Create Rotation Quaternion: r = cos(theta/2) + sin(theta/2) * axis
        half_theta = theta / 2.0
        sin_t = np.sin(half_theta)

        # Normalize axis
        ax, ay, az = axis
        axis_norm = np.sqrt(ax**2 + ay**2 + az**2)
        if axis_norm > 0:
            ax, ay, az = ax/axis_norm, ay/axis_norm, az/axis_norm

        rotator = Quaternion(
            np.cos(half_theta),
            sin_t * ax,
            sin_t * ay,
            sin_t * az
        )

        # Apply Rotation: q' = r * q (Left multiplication = Local rotation)
        old_state = self.state
        self.state = rotator * self.state
        self.state.normalize() # Ensure we stay on S^3 surface

        logger.info(f"🔄 Phase Shift ({theta:.2f} rad): {old_state} -> {self.state}")

    def project_to_3d(self):
        """
        Stereographic Projection (4D -> 3D).
        Projects the 4D state onto 3D space to visualize the 'Shape' of the thought.
        Formula: (2x, 2y, 2z) / (1 - w)  (South Pole Projection)
        Or: (2x, 2y, 2z) / (1 + w) (North Pole Projection)
        """
        w, x, y, z = self.state.q

        # Using North Pole Projection (Singularity at w = -1)
        denom = 1 + w
        if abs(denom) < 1e-6: denom = 1e-6

        px = (2 * x) / denom
        py = (2 * y) / denom
        pz = (2 * z) / denom # In 3D S^3 projection, the 3rd dim comes from z

        return np.array([px, py, pz])

    def get_zoom_level(self):
        """
        Interprets the 'w' component as the Zoom/Scale.
        w near 1: Point (Micro)
        w near 0: Expanded Sphere (Meso)
        w near -1: Infinite Field (Macro)
        """
        # w goes from 1 to -1.
        # Map to 0% to 100% expansion
        return (1.0 - self.state.w) / 2.0

if __name__ == "__main__":
    # 1. Genesis
    voxel = OmniVoxel()

    # 2. The Thought Process (Rotation)
    print("\n--- Thinking Process (Phase Rotation) ---")

    # Small thought (Zoom In)
    voxel.rotate_phase(0.5, axis=(1, 0, 0))
    p3d = voxel.project_to_3d()
    print(f"  > Projected 3D: {p3d} | Zoom: {voxel.get_zoom_level():.2f}")

    # Deep thought (Expansion)
    voxel.rotate_phase(1.5, axis=(0, 1, 0)) # Rotate on different axis
    p3d = voxel.project_to_3d()
    print(f"  > Projected 3D: {p3d} | Zoom: {voxel.get_zoom_level():.2f}")

    # Full Cycle (Return to Origin?)
    voxel.rotate_phase(4.28, axis=(0, 0, 1)) # Approx complete 2*pi
    p3d = voxel.project_to_3d()
    print(f"  > Projected 3D: {p3d} | Zoom: {voxel.get_zoom_level():.2f}")
