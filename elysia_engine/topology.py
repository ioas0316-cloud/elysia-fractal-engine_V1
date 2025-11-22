from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional

from .math_utils import Vector3
from .physics import PhysicsState


@dataclass
class GravityPath:
    """
    A 'River' or 'Pipe' of gravity.
    Entities near this path are pulled towards the center line
    and pushed forward along the tangent.
    """
    points: List[Vector3]
    radius: float = 5.0
    pull_strength: float = 10.0  # Gravity towards the center of the pipe
    flow_strength: float = 5.0   # Force pushing along the pipe

    def _get_closest_segment(self, pos: Vector3) -> tuple[Vector3, Vector3, float]:
        """
        Finds the closest segment [p1, p2] and the projection point on it.
        Returns (p1, p2, distance_sq_to_segment).
        """
        best_dist_sq = float('inf')
        best_segment = (self.points[0], self.points[1])
        best_proj = self.points[0]

        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]

            # Vector from p1 to p2
            seg_v = p2 - p1
            # Vector from p1 to pos
            pt_v = pos - p1

            # Project pt_v onto seg_v
            seg_len_sq = seg_v.dot(seg_v)
            if seg_len_sq <= 0:
                continue

            t = pt_v.dot(seg_v) / seg_len_sq

            # Clamp t to segment [0, 1]
            t = max(0.0, min(1.0, t))

            # Closest point on this segment
            closest = p1 + (seg_v * t)

            dist_sq = (pos - closest).dot(pos - closest)
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                best_segment = (p1, p2)
                best_proj = closest

        return best_segment[0], best_segment[1], best_dist_sq

    def calculate_force(self, state: PhysicsState) -> Vector3:
        if len(self.points) < 2:
            return Vector3(0, 0, 0)

        p1, p2, dist_sq = self._get_closest_segment(state.position)
        dist = math.sqrt(dist_sq)

        # If outside the "River Bank" (Radius * 2 for influence), ignore
        if dist > self.radius * 2.0:
            return Vector3(0, 0, 0)

        # 1. Centering Force (Gravity towards the line)
        # Find closest point on the line
        seg_v = p2 - p1
        pt_v = state.position - p1
        t = pt_v.dot(seg_v) / seg_v.dot(seg_v)
        t = max(0.0, min(1.0, t))
        closest_point = p1 + (seg_v * t)

        to_center = closest_point - state.position
        centering_force = to_center.normalize() * self.pull_strength

        # 2. Flow Force (Push along the tangent)
        tangent = seg_v.normalize()
        flow_force = tangent * self.flow_strength

        # Combine
        # Stronger pull if far from center?
        return centering_force + flow_force


@dataclass
class TensorGate:
    """
    A topological gate.
    If the entity meets the criteria (momentum, energy), it passes (boosts).
    If not, it is rejected (reversed/damped).
    """
    position: Vector3
    radius: float = 5.0
    required_momentum: float = 0.0
    required_energy: float = 0.0
    boost_multiplier: float = 1.5
    reject_force: float = 50.0

    def calculate_interaction(self, state: PhysicsState, efp_energy: float, efp_momentum: float) -> Vector3:
        """
        Returns the force applied by the gate.
        """
        dist = (state.position - self.position).magnitude
        if dist > self.radius:
            return Vector3(0, 0, 0)

        # Check criteria
        # We use EFP momentum (abstract) or Physics momentum (mass * velocity)?
        # Let's use Physics velocity magnitude for "Physical" momentum here.
        phys_momentum = state.velocity.magnitude * state.mass

        passed = True
        if phys_momentum < self.required_momentum:
            passed = False
        if efp_energy < self.required_energy:
            passed = False

        if passed:
            # Boost!
            # Apply force in direction of current velocity
            if state.velocity.magnitude > 0:
                return state.velocity.normalize() * (self.boost_multiplier * 10.0)
            else:
                return Vector3(0,0,0)
        else:
            # Reject!
            # Force opposite to velocity
            if state.velocity.magnitude > 0:
                return state.velocity.normalize() * -1.0 * self.reject_force
            else:
                 # If still, push away from gate center
                 push = (state.position - self.position).normalize()
                 return push * self.reject_force
