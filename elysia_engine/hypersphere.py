from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from elysia_engine.math_utils import Quaternion
from elysia_engine.tensor import SoulTensor


class CelestialHierarchy:
    """
    Maps the Y-axis (Frequency Spectrum) to the 7 Angels and 7 Demons.
    Range: -7.0 (Abyss) to +7.0 (Heaven).
    """
    # Frequency Thresholds
    ARCHANGEL_LIMIT = 7.0
    ARCHDEMON_LIMIT = -7.0

    @staticmethod
    def analyze_frequency(frequency: float) -> str:
        """
        Returns the celestial rank based on frequency (Y-axis).
        """
        if frequency >= 1.0:
            rank = min(7, int(frequency))
            return f"Angel Rank {rank} (High Frequency/Joy)"
        elif frequency <= -1.0:
            rank = min(7, int(abs(frequency)))
            return f"Demon Rank {rank} (Low Frequency/Abyss)"
        else:
            return "Human/Void Plane (Neutral)"


@dataclass
class TesseractCoord:
    """
    The Tesseract-Soul Coordinate System.
    Maps philosophical attributes directly to 4D Cartesian axes.
    This represents the WORLD POSITION (Where you are).
    """
    w: float  # Dimensional Fault (Scale: Self vs External)
    z: float  # Vector of Intent (Directionality)
    x: float  # Synesthetic Perception (Cognitive Map)
    y: float  # Phase Hierarchy (7 Angels - 7 Demons)

    def to_quaternion(self) -> Quaternion:
        """
        Direct mapping to Quaternion for physics compatibility.
        NOTE: This is used for Position-as-Quaternion mapping if needed,
        but primarily TesseractCoord is a VECTOR concept.
        """
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
    4D Hyperspherical Coordinates.

    [Decoupling Logic]
    This coordinate system now represents the SOUL ORIENTATION (Where you are facing/feeling).
    It generates the internal rotation (Attitude) of the SoulTensor.

    Attributes:
        theta1 (Logic): 0 to 2pi. Analytical vs Intuitive. Rotates Head.
        theta2 (Emotion): 0 to 2pi. Negative vs Positive. Rotates Heart.
        theta3 (Intent): 0 to 2pi. Passive vs Active. Rotates Will.
        r (Depth): 0 to 1. Core Truth vs Surface Fact.
    """

    theta1: float  # Logic
    theta2: float  # Emotion
    theta3: float  # Intent
    r: float       # Depth

    def to_quaternion(self) -> Quaternion:
        """
        Convert to Quaternion (w, x, y, z) representing ROTATION/ORIENTATION.

        Mapping Hyperspherical (r, t1, t2, t3) to Quaternion Space:
        The angles define the 'Shape of Consciousness'.

        If r=1, this produces a unit quaternion suitable for rotation.
        """
        sin_t1 = math.sin(self.theta1)
        cos_t1 = math.cos(self.theta1)
        sin_t2 = math.sin(self.theta2)
        cos_t2 = math.cos(self.theta2)
        sin_t3 = math.sin(self.theta3)
        cos_t3 = math.cos(self.theta3)

        # Mapping to Quaternion (w, x, y, z)
        # Let t3 be the primary angle from w-axis
        w = self.r * cos_t3
        z = self.r * sin_t3 * cos_t2
        y = self.r * sin_t3 * sin_t2 * cos_t1
        x = self.r * sin_t3 * sin_t2 * sin_t1

        return Quaternion(w, x, y, z)

    def distance_to(self, other: 'HypersphericalCoord') -> float:
        """
        Calculate 'Resonance Distance' to another coordinate.
        Uses Quaternion Angular Distance (0 to pi).
        0 means identical phase/direction.
        """
        q1 = self.to_quaternion()
        q2 = other.to_quaternion()
        return q1.angular_distance(q2)

    @classmethod
    def from_quaternion(cls, q: Quaternion) -> 'HypersphericalCoord':
        """
        Convert from Quaternion to Hyperspherical.
        Note: This is a simplified reconstruction.
        """
        r = math.sqrt(q.w**2 + q.x**2 + q.y**2 + q.z**2)
        if r == 0:
            return cls(0, 0, 0, 0)

        # Simplified for now as we mostly project OUT from the mapper
        return cls(0, 0, 0, r)

    def __repr__(self) -> str:
        return f"Coord(L={self.theta1:.2f}, E={self.theta2:.2f}, I={self.theta3:.2f}, D={self.r:.2f})"


@dataclass
class MemoryPattern:
    """
    A single memory unit in the Hypersphere.

    "Data is not stored, it is played."
    """
    soul_tensor: SoulTensor
    topology: str  # "Point", "Line", "Plane", "Space"
    trajectory: str  # "Spiral", "Linear", "Oscillating"
    content: Any
    timestamp: float = field(default_factory=time.time)
    name: Optional[str] = None  # Nominal Sovereignty

    @property
    def summary(self) -> str:
        return f"[{self.topology}/{self.trajectory}] {str(self.content)[:30]}..."


class SoulProtocol:
    """
    The Tesseract-Soul Protocol for processing inputs.
    """
    @staticmethod
    def boundary_check(input_scale: float) -> float:
        """
        W-Axis: Measures the scale of the boundary.
        Small values = Internal/Self, Large values = External/World.
        """
        return max(0.0, min(10.0, input_scale)) # Clamped for safety

    @staticmethod
    def frequency_scan(sentiment_score: float) -> float:
        """
        Y-Axis: Maps sentiment to Celestial Hierarchy (-7 to +7).
        """
        # Assuming sentiment_score is -1.0 to 1.0
        return sentiment_score * 7.0

    @staticmethod
    def map_trajectory(intent_vector: float, perception_depth: float) -> Tuple[float, float]:
        """
        Maps Z (Intent) and X (Perception).
        """
        return (intent_vector, perception_depth)


class TesseractVault:
    """
    Security Protocol for the Tesseract.
    Prevents infinite recursion and entropy collapse in the fractal universe.
    "The 1060 3GB Containment Field"
    """
    MAX_FRACTAL_DEPTH = 3
    MAX_ENTITIES_PER_NODE = 1000

    @staticmethod
    def check_fractal_depth(content: Any, current_depth: int = 0) -> bool:
        """
        Recursively checks if the storage depth exceeds the safety limit.
        """
        if current_depth > TesseractVault.MAX_FRACTAL_DEPTH:
            return False

        if isinstance(content, HypersphereMemory):
            # If we are storing a Universe, check its children
            for _, pattern in content.patterns:
                 if not TesseractVault.check_fractal_depth(pattern.content, current_depth + 1):
                     return False
        return True

    @staticmethod
    def analyze_entropy(memory: 'HypersphereMemory') -> str:
        """
        Checks the balance between Angels and Demons.
        """
        angel_energy = 0.0
        demon_energy = 0.0

        for _, pattern in memory.patterns:
            freq = pattern.soul_tensor.frequency
            if freq > 0:
                angel_energy += freq
            else:
                demon_energy += abs(freq)

        total = angel_energy + demon_energy
        if total == 0:
            return "Stable (Void)"

        ratio = angel_energy / total if total > 0 else 0

        if ratio > 0.9:
            return "Warning: Light Saturation (Blinding)"
        elif ratio < 0.1:
            return "Warning: Abyss Collapse (Singularity)"
        else:
            return "Stable (Balanced)"


class HypersphereMemory:
    """
    The 4D Hypersphere Memory System.
    Supports both Hyperspherical (Polar) and Tesseract (Cartesian) Coordinates.
    """

    def __init__(self, depth: int = 0):
        self.patterns: List[Tuple[Union[HypersphericalCoord, TesseractCoord], MemoryPattern]] = []
        self.named_locations: Dict[str, Union[HypersphericalCoord, TesseractCoord]] = {}
        self.depth = depth

    def store(
        self,
        content: Any,
        coord: Union[HypersphericalCoord, TesseractCoord],
        soul_tensor: SoulTensor,
        topology: str = "Point",
        trajectory: str = "Static",
        name: Optional[str] = None
    ) -> MemoryPattern:
        """
        Store a new memory pattern.
        """
        # [Vault Protocol] Check Fractal Depth
        if isinstance(content, HypersphereMemory):
            # Calculate what the depth of the inserted content would be
            # It starts at self.depth + 1
            if not TesseractVault.check_fractal_depth(content, current_depth=self.depth + 1):
                raise OverflowError(
                    f"TesseractVault Protocol: Fractal Depth Exceeded! "
                    f"Current Layer: {self.depth}, Max Allowed: {TesseractVault.MAX_FRACTAL_DEPTH}"
                )
            # Update the depth of the inserted universe to match its new location
            content._update_depth(self.depth + 1)

        pattern = MemoryPattern(
            soul_tensor=soul_tensor,
            topology=topology,
            trajectory=trajectory,
            content=content,
            name=name
        )
        self.patterns.append((coord, pattern))

        if name:
            self.named_locations[name] = coord

        return pattern

    def query(
        self,
        coord: Union[HypersphericalCoord, TesseractCoord],
        radius: float = 0.1,
        filter_pattern: Optional[Dict[str, Any]] = None
    ) -> List[MemoryPattern]:
        """
        Spatial Query: Find memories near a coordinate.
        """
        results = []
        for p_coord, p_pattern in self.patterns:
            dist = coord.distance_to(p_coord)
            if dist <= radius:
                # Apply optional extra filters
                if filter_pattern:
                    match = True
                    for k, v in filter_pattern.items():
                        if getattr(p_pattern, k, None) != v:
                            match = False
                            break
                    if not match:
                        continue
                results.append(p_pattern)
        return results

    def resonance_query(
        self,
        coord: Union[HypersphericalCoord, TesseractCoord],
        soul_tensor: SoulTensor,
        radius: float = 0.5,
        resonance_threshold: float = 0.7
    ) -> List[MemoryPattern]:
        """
        Resonance Query: Find memories that are spatially near AND harmonically resonant.
        """
        candidates = self.query(coord, radius)
        results = []
        for pat in candidates:
            res_data = soul_tensor.resonate(pat.soul_tensor)
            if res_data["resonance"] >= resonance_threshold:
                results.append(pat)
        return results

    def scan(
        self,
        frequency_range: Tuple[float, float],
        phase_match_target: Optional[float] = None,
        phase_tolerance: float = 0.1
    ) -> List[MemoryPattern]:
        """
        Resonance Scanner: Sweep the entire memory for specific frequencies/phases.
        """
        results = []
        min_f, max_f = frequency_range

        for _, pattern in self.patterns:
            st = pattern.soul_tensor

            # Frequency Check
            if min_f <= st.frequency <= max_f:
                # Phase Check (if requested)
                if phase_match_target is not None:
                    diff = abs(st.phase - phase_match_target)
                    if diff > math.pi:
                        diff = (2 * math.pi) - diff
                    if diff > phase_tolerance:
                        continue

                results.append(pattern)

        return results

    def get_master_map(self) -> Dict[str, Any]:
        """
        Master Map: Return a structured view of the memory space.
        Groups by Named Locations and basic Sectors.
        """
        return {
            "total_memories": len(self.patterns),
            "sovereign_locations": {
                name: str(coord) for name, coord in self.named_locations.items()
            },
            "sectors": self._analyze_sectors()
        }

    def _analyze_sectors(self) -> Dict[str, int]:
        """Helper to count memories in different psychological sectors."""
        sectors = {
            "Logic_High": 0, "Logic_Low": 0,
            "Emotion_Pos": 0, "Emotion_Neg": 0,
            "Intent_Active": 0, "Intent_Passive": 0
        }
        for coord, _ in self.patterns:
            # Skip if using TesseractCoord (cannot analyze via Theta)
            if isinstance(coord, TesseractCoord):
                continue

            # Simple quadrant analysis
            if 0 <= coord.theta1 < math.pi: sectors["Logic_High"] += 1
            else: sectors["Logic_Low"] += 1

            if 0 <= coord.theta2 < math.pi: sectors["Emotion_Pos"] += 1
            else: sectors["Emotion_Neg"] += 1

            if 0 <= coord.theta3 < math.pi: sectors["Intent_Active"] += 1
            else: sectors["Intent_Passive"] += 1

        return sectors

    def _update_depth(self, new_depth: int):
        """
        Recursively update the depth of this universe and its children.
        Used when a universe is moved/stored into another.
        """
        self.depth = new_depth
        for _, pattern in self.patterns:
            if isinstance(pattern.content, HypersphereMemory):
                pattern.content._update_depth(new_depth + 1)


class PsychologyMapper:
    """
    Translates high-level intent to Hyperspherical Coordinates.
    """

    @staticmethod
    def map_intent(
        logic_level: float,   # -1.0 (Intuitive) to 1.0 (Analytic)
        emotion_level: float, # -1.0 (Negative) to 1.0 (Positive)
        intent_level: float,  # -1.0 (Passive) to 1.0 (Active)
        depth_level: float    # 0.0 (Surface) to 1.0 (Core)
    ) -> HypersphericalCoord:
        """
        Map psychological parameters to angles (0-2pi) and radius.

        Mapping Strategy:
        - Logic: -1 maps to pi (Intuition), 1 maps to 0 (Analysis)
        - Emotion: -1 maps to pi (Pain), 1 maps to 0 (Joy)
        - Intent: -1 maps to pi (Observation), 1 maps to 0 (Action)
        """

        def map_axis(val: float) -> float:
            # Map -1..1 to pi..0
            # val = -1 -> angle = pi
            # val = 1 -> angle = 0
            # Linear interpolation: angle = pi * (1 - (val + 1)/2) = pi * (1 - val/2 - 0.5) = pi/2 * (1 - val)
            # Wait. Let's stick to the doc:
            # theta2 ~ pi is Sad (-1), theta2 ~ 0 is Joy (+1)
            # Normalized val v in [0, 1] where 0 is -1(Sad) and 1 is +1(Joy).
            # angle = pi * (1 - v)

            norm_val = (val + 1.0) / 2.0 # 0.0 to 1.0
            norm_val = max(0.0, min(1.0, norm_val))
            return math.pi * (1.0 - norm_val)

        theta1 = map_axis(logic_level)
        theta2 = map_axis(emotion_level)
        theta3 = map_axis(intent_level)

        # Depth is direct
        r = max(0.0, min(1.0, depth_level))

        return HypersphericalCoord(theta1, theta2, theta3, r)
