from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from .math_utils import Vector3, Quaternion
from .physics import PhysicsState, Attractor


@dataclass
class CoilStructure:
    """
    A 3D Tensor Coil that creates a helical vector field.
    This represents the 'Railgun' or 'accelerator' topology.
    """
    axis: Vector3 = field(default_factory=lambda: Vector3(0, 0, 1))  # The main direction of the flow
    center: Vector3 = field(default_factory=lambda: Vector3(0, 0, 0))
    radius: float = 5.0
    frequency: float = 1.0  # How tightly it spirals
    strength: float = 10.0  # Acceleration magnitude

    def get_field_vector(self, position: Vector3) -> Vector3:
        """
        Calculates the flow vector at a given position.
        The field spirals around the central axis.
        Respects the arbitrary 'axis' of the coil.
        """
        # 1. Calculate rotation to align Z-axis (0,0,1) to self.axis
        # We use standard "from_to_rotation" logic.
        default_axis = Vector3(0, 0, 1)
        target_axis = self.axis.normalize()

        # If already aligned
        if abs(default_axis.dot(target_axis)) > 0.999:
             if default_axis.dot(target_axis) > 0:
                 rotation = Quaternion.identity()
             else:
                 # 180 flip around X
                 rotation = Quaternion.from_axis_angle(Vector3(1, 0, 0), math.pi)
        else:
            rot_axis = default_axis.cross(target_axis).normalize()
            angle = math.acos(default_axis.dot(target_axis))
            rotation = Quaternion.from_axis_angle(rot_axis, angle)

        # Inverse rotation to bring world position into coil's local space (where axis is Z)
        # Quaternion conjugate is inverse for unit quaternions
        inv_rotation = Quaternion(rotation.w, -rotation.x, -rotation.y, -rotation.z)

        rel_pos_world = position - self.center
        local_pos = inv_rotation.rotate(rel_pos_world)

        # 2. Calculate Helical Field in Local Space (Z-aligned)
        angle = math.atan2(local_pos.y, local_pos.x)

        # Tangent in XY plane, plus Z component (frequency)
        local_tangent = Vector3(
            -math.sin(angle),
            math.cos(angle),
            self.frequency
        ).normalize()

        xy_dist = math.sqrt(local_pos.x**2 + local_pos.y**2)
        dist_diff = abs(xy_dist - self.radius)

        intensity = self.strength * math.exp(-dist_diff)
        local_field = local_tangent * intensity

        # 3. Rotate field vector back to World Space
        world_field = rotation.rotate(local_field)

        return world_field

    def railgun_accelerate(self, state: PhysicsState, dt: float) -> None:
        """
        Applies the coil field force to the physics state.
        """
        force = self.get_field_vector(state.position)
        state.apply_force(force, dt)

    def superconduct(self, state: PhysicsState, target: Attractor) -> bool:
        """
        Attempts to perform a 'Hyperdrive' jump (Zero Resistance).
        Returns True if jump occurred.
        """
        # Condition for superconductivity:
        # 1. Alignment: Velocity is roughly aligned with vector to target?
        # 2. Energy: High momentum?
        # 3. Proximity: Within the coil's effective range?

        to_target = target.position - state.position
        dist = to_target.magnitude

        if dist == 0:
            return False

        # Check alignment (Cos similarity)
        if state.velocity.magnitude > 0:
            alignment = state.velocity.normalize().dot(to_target.normalize())
        else:
            alignment = 0.0

        # Thresholds for "Intuition" / Hyperdrive
        # If we are moving fast enough in the right direction...
        # AND we are getting closer (dist < some_horizon)
        # AND alignment is good enough
        if alignment > 0.8 and state.velocity.magnitude > 10.0 and dist < 300.0:
            # FLASH STEP!
            # Move directly to target (minus a small offset to avoid singularity)
            offset = to_target.normalize() * (target.radius * 1.1)
            state.position = target.position - offset
            state.velocity = Vector3(0, 0, 0) # Stop upon arrival? or keep momentum?
            # Let's say we arrive with zero velocity, "Settled".
            return True

        return False
