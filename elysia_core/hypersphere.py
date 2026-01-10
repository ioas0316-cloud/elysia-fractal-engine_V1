from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from .math_utils import Quaternion, Rotor
from .tensor import SoulTensor
from .world import World
from .field import FieldSystem

@dataclass
class TesseractCoord:
    """
    Fixed Axis (The World): Represents Structure & Position.
    W: Scale (Analog Dial)
    Z: Intent Vector
    X: Perception
    Y: Frequency Rank
    """
    w: float
    z: float
    x: float
    y: float

    def to_quaternion(self) -> Quaternion:
        return Quaternion(self.w, self.x, self.y, self.z)

    def distance_to(self, other: Union['HypersphericalCoord', 'TesseractCoord']) -> float:
        q1 = self.to_quaternion()
        q2 = other.to_quaternion()
        return q1.angular_distance(q2)

    def __repr__(self) -> str:
        return f"Tesseract(Scale(w)={self.w:.2f}, Intent(z)={self.z:.2f}, Perception(x)={self.x:.2f}, Rank(y)={self.y:.2f})"

@dataclass
class HypersphericalCoord:
    """
    Rotating Axis (The Soul): Represents Orientation & Attitude.
    Linked to Gyroscope mechanics.
    """
    theta1: float
    theta2: float
    theta3: float
    r: float

    def to_quaternion(self) -> Quaternion:
        sin_t1 = math.sin(self.theta1)
        cos_t1 = math.cos(self.theta1)
        sin_t2 = math.sin(self.theta2)
        cos_t2 = math.cos(self.theta2)
        sin_t3 = math.sin(self.theta3)
        cos_t3 = math.cos(self.theta3)
        w = self.r * cos_t3
        z = self.r * sin_t3 * cos_t2
        y = self.r * sin_t3 * sin_t2 * cos_t1
        x = self.r * sin_t3 * sin_t2 * sin_t1
        return Quaternion(w, x, y, z)

    def distance_to(self, other: 'HypersphericalCoord') -> float:
        q1 = self.to_quaternion()
        q2 = other.to_quaternion()
        return q1.angular_distance(q2)

@dataclass
class MemoryPattern:
    soul_tensor: SoulTensor
    topology: str
    trajectory: str
    content: Any
    timestamp: float = field(default_factory=time.time)
    name: Optional[str] = None

    @property
    def summary(self) -> str:
        return f"[{self.topology}/{self.trajectory}] {str(self.content)[:30]}..."

class HypersphereMemory:
    """
    The 4D Memory Storage.
    Now integrated as the 'Soul Storage' component of HyperCosmos.
    """
    def __init__(self, depth: int = 0):
        self.patterns: List[Tuple[Union[HypersphericalCoord, TesseractCoord], MemoryPattern]] = []
        self.named_locations: Dict[str, Union[HypersphericalCoord, TesseractCoord]] = {}
        self.depth = depth

    def store(self, content: Any, coord: Union[HypersphericalCoord, TesseractCoord], soul_tensor: SoulTensor, topology: str = "Point", trajectory: str = "Static", name: Optional[str] = None) -> MemoryPattern:
        pattern = MemoryPattern(soul_tensor=soul_tensor, topology=topology, trajectory=trajectory, content=content, name=name)
        self.patterns.append((coord, pattern))
        if name:
            self.named_locations[name] = coord
        return pattern

    def zoom_query(self, scale_center: float, scale_width: float) -> List[MemoryPattern]:
        """
        Analog Zoom Dial (W-Axis).
        Retrieves memories within a continuous scale range.
        """
        results = []
        min_w = scale_center - (scale_width / 2)
        max_w = scale_center + (scale_width / 2)
        for coord, pattern in self.patterns:
            if not isinstance(coord, TesseractCoord):
                continue
            if min_w <= coord.w <= max_w:
                results.append(pattern)
        return results

class HyperCosmos:
    """
    The Container of Everything. The Infinity Stone.

    Structure:
        - Tesseract (Fixed Axis): The World / Environment / Structure.
        - Hypersphere (Rotating Axis): The Soul / Attitude / Gyroscope.

    Fractal Nature:
        - Micro: An NPC's internal mind.
        - Meso: A Virtual City.
        - Macro: The Elysia Universe.
    """
    def __init__(self, name: str = "Genesis", scale: float = 1.0):
        self.name = name
        self.scale = scale # The W-axis anchor for this Cosmos

        # The Two Halves
        self.world = World() # Tesseract Physics
        self.memory = HypersphereMemory() # Hypersphere Soul

        # The Bridge (Rotor)
        # Manages the interaction between Fixed World and Rotating Soul
        self.global_rotor: Rotor = Rotor(1.0, 0.0, 0.0, 0.0)

    def step(self, dt: float) -> None:
        """
        Evolve the Cosmos.
        1. Physics Step (World)
        2. Soul Step (Memory/Tensor)
        3. Rotor Integration (Gyroscope)
        """
        self.world.step(dt)

        # Apply Rotor to all active SoulTensors in the world
        # This simulates the "Universe Rotating" around the entities (or vice versa)
        # Phase Reconstruction: If the hardware gyroscope moves, we update the virtual souls.
        # For now, we simulate a gentle drift or "Breathing" rotation if no input.
        pass

    def analog_dial(self, focus_w: float, bandwidth: float) -> Dict[str, Any]:
        """
        The Analog Zoom Interface.
        Returns what is visible at the current Scale (W) setting.
        """
        # 1. Query Internal Memory (The Past/Self)
        memories = self.memory.zoom_query(focus_w, bandwidth)

        # 2. Query External World (The Present/Others)
        # We need to filter entities by their 'Scale' or 'Mass' (Amplitude ~ Scale)
        entities = []
        min_mass = focus_w * 10 # Heuristic mapping
        max_mass = (focus_w + bandwidth) * 10

        for ent in self.world.entities.values():
            if min_mass <= ent.physics.mass <= max_mass:
                entities.append(ent)

        return {
            "scale_focus": focus_w,
            "memories": len(memories),
            "entities": len(entities),
            "sample_memory": memories[0].summary if memories else None
        }
