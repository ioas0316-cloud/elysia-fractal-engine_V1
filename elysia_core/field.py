from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

from .math_utils import Vector4, Rotor
from .tensor import SoulTensor

@dataclass
class FieldNode:
    coord: Tuple[int, int, int, int]
    depth: int
    w_field: float = 1.0
    x_field: float = 0.0
    y_field: float = 0.0
    z_field: float = 0.0
    is_leaf: bool = True
    last_update: int = 0

@dataclass
class SanctuaryZone:
    radius: float = 2.0

    def apply_protection(self, position: Vector4, node: FieldNode) -> None:
        dist = position.magnitude
        if dist < self.radius:
            node.w_field = 1.0
            node.x_field = 1.0
            node.y_field = 7.0
            node.z_field = 0.0

class FractalSpatialMap:
    def __init__(self, resolution_scale: float = 1.0):
        self.nodes: Dict[Tuple[int, int, int, int, int], FieldNode] = {}
        self.resolution_scale = resolution_scale
        self.sanctuary = SanctuaryZone()

    def _hash_coord(self, position: Vector4, depth: int) -> Tuple[int, int, int, int, int]:
        cell_size = self.resolution_scale * (0.5 ** depth)
        ix = int(math.floor(position.x / cell_size))
        iy = int(math.floor(position.y / cell_size))
        iz = int(math.floor(position.z / cell_size))
        iw = int(math.floor(position.w / cell_size))
        return (depth, ix, iy, iz, iw)

    def get_node(self, position: Vector4, depth: int = 0, create_if_missing: bool = True) -> Optional[FieldNode]:
        key = self._hash_coord(position, depth)
        if key in self.nodes:
            return self.nodes[key]
        if create_if_missing:
            node = FieldNode(coord=key[1:], depth=depth)
            self.sanctuary.apply_protection(position, node)
            self.nodes[key] = node
            return node
        return None

    def sample_field(self, position: Vector4, depth: int = 0, current_tick: int = -1) -> Tuple[float, float, float, float]:
        node = self.get_node(position, depth, create_if_missing=False)
        is_fresh = True
        if node and current_tick >= 0:
            if node.last_update < current_tick:
                is_fresh = False

        if node and is_fresh:
            return (node.w_field, node.x_field, node.y_field, node.z_field)

        dist = position.magnitude
        if dist < self.sanctuary.radius:
            return (1.0, 1.0, 7.0, 0.0)

        return (1.0, 0.0, 0.0, 0.0)

class FieldSystem:
    def __init__(self):
        self.spatial_map = FractalSpatialMap()
        self.time_tick: int = 0

    def update_field(self, active_entities_pos: List[Tuple[Vector4, SoulTensor]]) -> None:
        self.time_tick += 1
        for pos, soul in active_entities_pos:
            node = self.spatial_map.get_node(pos, depth=0)
            if not node: continue

            if node.last_update < self.time_tick:
                dist = pos.magnitude
                if dist < self.spatial_map.sanctuary.radius:
                     node.w_field = 1.0
                     node.x_field = 1.0
                     node.y_field = 7.0
                     node.z_field = 0.0
                else:
                     node.w_field = 1.0
                     node.x_field = 0.0
                     node.y_field = 0.0
                     node.z_field = 0.0
                node.last_update = self.time_tick

            node.w_field += soul.amplitude * 0.01
            node.x_field += abs(soul.frequency) * 0.01
            rate = 0.1
            node.y_field = node.y_field * (1-rate) + soul.frequency * rate
            node.z_field += soul.spin * soul.polarity * 0.1

    def get_local_forces(self, position: Vector4, soul: SoulTensor) -> Tuple[Vector4, Rotor]:
        step = 0.1
        center = self.spatial_map.sample_field(position, current_tick=self.time_tick)
        val_c = center[2]

        val_x = self.spatial_map.sample_field(position + Vector4(0, step, 0, 0), current_tick=self.time_tick)[2]
        val_y = self.spatial_map.sample_field(position + Vector4(0, 0, step, 0), current_tick=self.time_tick)[2]
        val_z = self.spatial_map.sample_field(position + Vector4(0, 0, 0, step), current_tick=self.time_tick)[2]
        val_w = self.spatial_map.sample_field(position + Vector4(step, 0, 0, 0), current_tick=self.time_tick)[2]

        grad = Vector4(
            (val_w - val_c)/step,
            (val_x - val_c)/step,
            (val_y - val_c)/step,
            (val_z - val_c)/step
        )

        diff = val_c - soul.frequency
        force = grad * (-1.0 * diff)

        torque_rotor = Rotor.from_plane_angle('xy', center[3] * 0.01)

        return force, torque_rotor
