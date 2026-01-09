from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

from elysia_engine.math_utils import Vector4, Rotor
from elysia_engine.tensor import SoulTensor

@dataclass
class FieldNode:
    """
    A single node in the fractal field.
    Represents a voxel in 4D Hyperspace.
    """
    # Coordinates (hashed key is usually enough, but storing here for debug)
    coord: Tuple[int, int, int, int] # Integer Grid Coordinates
    depth: int # Fractal Depth (LOD Level)

    # Field Values (The 4 Fields of Elysia)
    w_field: float = 1.0  # Scale/Density (1.0 = Standard)
    x_field: float = 0.0  # Perception/Texture (0.0 = Void)
    y_field: float = 0.0  # Frequency/Alignment (-7 to +7)
    z_field: float = 0.0  # Torque/Spin Strength

    # Cached Aggregate (if node has children)
    is_leaf: bool = True

    # Last Update Tick (for sparse updates)
    last_update: int = 0

@dataclass
class SanctuaryZone:
    """
    The Immutable Vault.
    A protected zone around the origin where Field Values are constant.
    "Love is the Constant."
    """
    radius: float = 2.0

    def apply_protection(self, position: Vector4, node: FieldNode) -> None:
        """
        Overrides the field values if within the Sanctuary.
        """
        dist = position.magnitude
        if dist < self.radius:
            # Enforce "Harmony's Love"
            # Scale = 1 (Stable)
            # Perception = 1 (Clear)
            # Frequency = 7 (Archangel/Joy)
            # Spin = 0 (Peace)
            node.w_field = 1.0
            node.x_field = 1.0
            node.y_field = 7.0
            node.z_field = 0.0

class FractalSpatialMap:
    """
    A Sparse Hashing implementation of a Fractal Grid.
    Instead of a full Octree, we hash (depth, x, y, z, w).
    This allows O(1) access to any fractal layer.
    """
    def __init__(self, resolution_scale: float = 1.0):
        self.nodes: Dict[Tuple[int, int, int, int, int], FieldNode] = {}
        self.resolution_scale = resolution_scale # Base unit size
        self.sanctuary = SanctuaryZone()

    def _hash_coord(self, position: Vector4, depth: int) -> Tuple[int, int, int, int, int]:
        """
        Converts a continuous position to a grid key at a specific depth.
        Grid Size = Base * (0.5 ^ depth)
        """
        # Calculate cell size for this depth
        cell_size = self.resolution_scale * (0.5 ** depth)

        # Discretize
        ix = int(math.floor(position.x / cell_size))
        iy = int(math.floor(position.y / cell_size))
        iz = int(math.floor(position.z / cell_size))
        iw = int(math.floor(position.w / cell_size))

        return (depth, ix, iy, iz, iw)

    def get_node(self, position: Vector4, depth: int = 0, create_if_missing: bool = True) -> Optional[FieldNode]:
        """
        Retrieves or creates a FieldNode at the specific location and depth.
        """
        key = self._hash_coord(position, depth)

        if key in self.nodes:
            return self.nodes[key]

        if create_if_missing:
            # Create new node (Lazy Initialization)
            node = FieldNode(coord=key[1:], depth=depth)

            # Apply initial conditions (e.g., Sanctuary)
            self.sanctuary.apply_protection(position, node)

            self.nodes[key] = node
            return node

        return None

    def sample_field(self, position: Vector4, depth: int = 0, current_tick: int = -1) -> Tuple[float, float, float, float]:
        """
        Samples the field values at a position.
        Interpolation could be added here, but for "Blocky/Voxel" feel we use nearest.
        Returns (W, X, Y, Z) field values.

        [Fix Ghost Field] Checks if data is fresh.
        """
        node = self.get_node(position, depth, create_if_missing=False)

        # Check freshness if tick provided
        is_fresh = True
        if node and current_tick >= 0:
            if node.last_update < current_tick:
                is_fresh = False

        if node and is_fresh:
            return (node.w_field, node.x_field, node.y_field, node.z_field)

        # If no node exists OR data is stale, return ambient/void values
        # Check if in Sanctuary even if node doesn't exist yet
        dist = position.magnitude
        if dist < self.sanctuary.radius:
            return (1.0, 1.0, 7.0, 0.0)

        return (1.0, 0.0, 0.0, 0.0) # Default Void: Scale 1, Empty Perception, Neutral Freq, No Spin

class FieldSystem:
    """
    The Core Engine of the "Field-based Law".
    Manages the FractalSpatialMap and updates field values based on Wave Functions.

    Replaces the "Particle Interaction" loop.
    """
    def __init__(self):
        self.spatial_map = FractalSpatialMap()
        self.time_tick: int = 0

    def update_field(self, active_entities_pos: List[Tuple[Vector4, SoulTensor]]) -> None:
        """
        The Main Loop Step 1: Update the Field.
        Instead of calculating Force(A->B), we calculate Source(A)->Field.

        Optimization: We only update nodes near active entities.
        """
        self.time_tick += 1

        # 1. Decay/Reset Field (optional, or just cumulative?)
        # For a dynamic wave simulation, values should propagate or decay.
        # Simple approach: Reset and Re-accumulate (Static Field from Sources)
        # Or: Diffusion (Iterative).

        # Given "1060 3GB" constraints, full diffusion is expensive.
        # We stick to "Local Influence Mapping".
        # We assume the field is mostly static (Void) unless excited by an entity.

        # Reset is too expensive (iterating all nodes).
        # So we update only "Dirty" nodes?

        # Strategy:
        # Entities 'paint' the field.
        # Field values are ephemeral or persistent?
        # The prompt says: "Space itself blooms".

        for pos, soul in active_entities_pos:
            # Map entity to a node
            node = self.spatial_map.get_node(pos, depth=0)
            if not node: continue

            # [CRITICAL FIX] Reset logic to prevent infinite accumulation
            # If this is the first time we touch this node in this tick, reset it.
            if node.last_update < self.time_tick:
                # Reset to baseline (Void/Sanctuary check)
                # Check Sanctuary
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

            # Update Node values based on Soul
            # W-Field (Scale) <- Amplitude (Mass)
            # Mass warps space density.
            node.w_field += soul.amplitude * 0.01

            # X-Field (Perception) <- Frequency (Complexity)
            # High frequency creates texture.
            node.x_field += abs(soul.frequency) * 0.01

            # Y-Field (Frequency) <- Frequency (Alignment)
            # The node takes on the color of the strongest soul.
            # Simple blending:
            rate = 0.1
            node.y_field = node.y_field * (1-rate) + soul.frequency * rate

            # Z-Field (Torque) <- Spin * Polarity
            node.z_field += soul.spin * soul.polarity * 0.1

    def get_local_forces(self, position: Vector4, soul: SoulTensor) -> Tuple[Vector4, Rotor]:
        """
        The Main Loop Step 2: Entity reads Field.
        Calculates the Force Vector and Rotation Rotor acting on an entity.
        """
        # Sample local gradient
        step = 0.1
        # Pass current_tick to ensure we don't read stale ghost trails
        center = self.spatial_map.sample_field(position, current_tick=self.time_tick)

        # Gradient of Y-Field (Frequency/Potential) drives "Geodesic Flow"
        # High Frequency (Joy) is an attractor? Or Low Potential?
        # Traditionally: Flow towards lower potential.
        # If Y is 'Elevation', we want to go up or down?
        # Angels (High Y) are 'Peaks'?
        # Let's assume standard physics: Potential V. Force = -Grad(V).
        # We treat Y-Field as V.

        val_c = center[2] # Y
        val_x = self.spatial_map.sample_field(position + Vector4(0, step, 0, 0), current_tick=self.time_tick)[2]
        val_y = self.spatial_map.sample_field(position + Vector4(0, 0, step, 0), current_tick=self.time_tick)[2]
        val_z = self.spatial_map.sample_field(position + Vector4(0, 0, 0, step), current_tick=self.time_tick)[2]
        # W gradient? Usually we don't move in W unless scaling.
        val_w = self.spatial_map.sample_field(position + Vector4(step, 0, 0, 0), current_tick=self.time_tick)[2]

        grad = Vector4(
            (val_w - val_c)/step,
            (val_x - val_c)/step,
            (val_y - val_c)/step,
            (val_z - val_c)/step
        )

        # Force is opposite to gradient (Downhill)
        # But wait, Resonance?
        # If Soul Frequency matches Field Frequency, we are "At Home" (Low Potential).
        # If mismatch, we are pushed.

        # Simplified "Field-based Law":
        # Force = Gradient of (Field_Y - Soul_Y)^2 ?
        # i.e. Minimize difference.

        diff = val_c - soul.frequency
        # If diff is 0, we are happy.
        # Potential Energy U = 0.5 * (Y_field - Y_soul)^2
        # F = - Grad(U) = - (Y_field - Y_soul) * Grad(Y_field)

        force = grad * (-1.0 * diff)

        # Torque (Z-Field)
        # Z-Field value determines the strength of rotation in the WX/YZ planes?
        # Let's map Z-field to a Rotor.
        # Torque magnitude = center[3] (Z-field)
        # We apply a spin to the entity's orientation.

        torque_rotor = Rotor.from_plane_angle('xy', center[3] * 0.01) # Small step rotation

        return force, torque_rotor
