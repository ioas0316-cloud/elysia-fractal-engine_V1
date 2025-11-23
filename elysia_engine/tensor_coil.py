from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional, List

from .math_utils import Vector3, Quaternion
from .physics import PhysicsState, Attractor
from .entities import Entity
from .tensor import SoulTensor

@dataclass
class CoilStructure:
    """
    A 3D Tensor Coil that creates a helical vector field.
    This represents the 'Railgun' or 'accelerator' topology.
    Acts as a 'Particle Accelerator' for Souls.
    """
    axis: Vector3 = field(default_factory=lambda: Vector3(0, 0, 1))  # The main direction of the flow
    center: Vector3 = field(default_factory=lambda: Vector3(0, 0, 0))
    radius: float = 5.0
    frequency: float = 1.0  # How tightly it spirals (Frequency match)
    strength: float = 10.0  # Acceleration magnitude

    def get_field_vector(self, position: Vector3) -> Vector3:
        """
        Calculates the flow vector at a given position.
        The field spirals around the central axis.
        """
        # 1. Calculate rotation to align Z-axis (0,0,1) to self.axis
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
        """
        to_target = target.position - state.position
        dist = to_target.magnitude

        if dist == 0:
            return False

        # Check alignment
        if state.velocity.magnitude > 0:
            alignment = state.velocity.normalize().dot(to_target.normalize())
        else:
            alignment = 0.0

        if alignment > 0.8 and state.velocity.magnitude > 10.0 and dist < 300.0:
            # FLASH STEP!
            offset = to_target.normalize() * (target.radius * 1.1)
            state.position = target.position - offset
            state.velocity = Vector3(0, 0, 0)
            return True

        return False

    def incubate(self, entities: List[Entity], world_time: float) -> List[Entity]:
        """
        Checks for entities colliding within the high-energy coil field
        and triggers Quantum Crossover (Breeding).
        Updated to use SoulTensor logic.
        """
        new_entities = []

        # 1. Filter entities effectively inside the coil's influence
        candidates = []
        for ent in entities:
            dist = (ent.physics.position - self.center).magnitude
            if dist < (self.radius + 5.0) and ent.soul is not None:
                candidates.append(ent)

        # 2. Brute-force collision check
        interaction_dist = 2.0 # Increased for field interactions
        processed = set()

        for i in range(len(candidates)):
            p1 = candidates[i]
            if p1.id in processed:
                continue

            for j in range(i + 1, len(candidates)):
                p2 = candidates[j]
                if p2.id in processed:
                    continue

                # Check distance
                d = (p1.physics.position - p2.physics.position).magnitude
                if d < interaction_dist:
                    # COLLISION! Trigger Crossover based on Soul Resonance

                    # 1. Check Resonance
                    res_data = p1.soul.resonate(p2.soul)

                    # Only breed if constructive interference (Empathy/Love)
                    if res_data['resonance'] > 0.5:

                        child_id = f"child_{world_time:.2f}_{len(new_entities)}"

                        # Create Child Soul (Average + Mutation)
                        avg_freq = (p1.soul.frequency + p2.soul.frequency) / 2
                        child_soul = SoulTensor(
                            amplitude = (p1.soul.amplitude + p2.soul.amplitude) * 0.5 * res_data['resonance'],
                            frequency = avg_freq,
                            phase = (p1.soul.phase + p2.soul.phase) / 2,
                            spin = (p1.soul.spin + p2.soul.spin) / 2
                        )

                        child = Entity(id=child_id)
                        child.soul = child_soul

                        # Position child
                        mid_pos = (p1.physics.position + p2.physics.position) * 0.5
                        child.physics.position = mid_pos

                        child.data = {"desc": f"Born from {p1.id} & {p2.id}", "harmony": res_data['resonance']}

                        new_entities.append(child)

                        # Cost
                        p1.soul.amplitude *= 0.8
                        p2.soul.amplitude *= 0.8

                        processed.add(p1.id)
                        processed.add(p2.id)

        return new_entities
