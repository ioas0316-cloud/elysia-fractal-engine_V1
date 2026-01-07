from __future__ import annotations

import math
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional
from enum import Enum, auto

from Core.Foundation.core_memory import CoreMemory


class LensMode(Enum):
    ANCHOR = auto()   # W-Axis: The Zero Point of Encounter (Me <-> You)
    INTERNAL = auto() # X-Axis: Internal World (Dream / Memory)
    EXTERNAL = auto() # Y-Axis: External World (Action / Sensing)
    LAW = auto()      # Z-Axis: Intention & Law (Soul / Depth)


class HyperMode(Enum):
    POINT = auto()   # w < 0.5: Zero Dimension (The Singularity / Target / "I")
    LINE = auto()    # 0.5 <= w < 1.5: One Dimension (The Connection / Flow / "Relationship")
    PLANE = auto()   # 1.5 <= w < 2.5: Two Dimensions (The Field / Atmosphere / "Context")
    HYPER = auto()   # w >= 2.5: Three+ Dimensions (The Volume / Wholeness / "Universe")


@dataclass
class LensState:
    mode: LensMode
    hyper_mode: HyperMode
    intensity: float
    vector: Dict[str, float]
    scale_depth: float # The raw W value


@dataclass
class QuaternionOrientation:
    """
    Elysia's Hyper-Quaternion (The Geometry of Will & Dimensionality).

    The 'Fake' 4D (x,y,z,w rotation) is replaced by a 'Hyper' 4D structure:
    - w (Real): The Dimensional Slider (Scale / Perspective).
                0.0 = Point, 1.0 = Line, 2.0 = Plane, 3.0 = Volume.
    - x, y, z (Imag): The Spatial Orientation (Where we are looking within that dimension).
                      Normalized vector indicating focus direction.
    """

    w: float = 1.0  # Scale / Dimension (Default: 1.0 = Linear flow)
    x: float = 0.0  # Focus X (Internal/Dream)
    y: float = 0.0  # Focus Y (External/Action)
    z: float = 1.0  # Focus Z (Law/Intent - Default aligned with Z-axis)

    def as_dict(self) -> Dict[str, float]:
        return asdict(self)

    def get_hyper_mode(self) -> HyperMode:
        """
        Determines the current dimensional mode based on W.
        """
        if self.w < 0.5:
            return HyperMode.POINT
        elif self.w < 1.5:
            return HyperMode.LINE
        elif self.w < 2.5:
            return HyperMode.PLANE
        else:
            return HyperMode.HYPER

    def normalize_spatial(self) -> "QuaternionOrientation":
        """
        Normalizes only the spatial components (x, y, z) to maintain direction
        without affecting the dimensional scale (w).
        """
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if mag <= 1e-9:
            # Default to looking at Z (Intent) if zero vector
            return QuaternionOrientation(w=self.w, x=0.0, y=0.0, z=1.0)

        return QuaternionOrientation(
            w=self.w,
            x=self.x / mag,
            y=self.y / mag,
            z=self.z / mag
        )


class QuaternionConsciousnessEngine:
    """
    The Hyper-Quaternion Engine.
    Manages the 'Zoom' (Dimension) and 'Focus' (Orientation) of consciousness.
    """

    def __init__(self, core_memory: Optional[CoreMemory] = None) -> None:
        self.core_memory = core_memory
        # Start in 'Line' mode (Conversation/Flow) aligned with 'Law' (Z).
        self._orientation = QuaternionOrientation(w=1.0, x=0.0, y=0.0, z=1.0)

    @property
    def orientation(self) -> QuaternionOrientation:
        return self._orientation

    def orientation_as_dict(self) -> Dict[str, float]:
        return self._orientation.as_dict()

    def get_lens_status(self) -> Dict[str, Any]:
        """
        Return telemetry about the current state of the Lens.
        """
        q = self._orientation
        focus_state = self.determine_focus()

        return {
            "dimension": focus_state.hyper_mode.name,
            "scale_w": round(q.w, 3),
            "primary_focus": focus_state.mode.name,
            "focus_intensity": round(focus_state.intensity, 3),
            "raw": q.as_dict(),
        }

    def determine_focus(self) -> LensState:
        """
        Determines the current mode of observation based on spatial axis and scale.
        """
        q = self._orientation
        hyper_mode = q.get_hyper_mode()

        # Absolute spatial magnitudes
        x, y, z = abs(q.x), abs(q.y), abs(q.z)

        # Find dominant spatial axis
        magnitudes = {LensMode.INTERNAL: x, LensMode.EXTERNAL: y, LensMode.LAW: z}

        # If w is very low (Point mode), we might consider ANCHOR as a dominant possibility
        # regardless of x,y,z if they are weak. But for now, let's keep it simple.

        mode = max(magnitudes, key=magnitudes.get)
        intensity = magnitudes[mode]

        # In Point mode, if intensity is low, we default to ANCHOR (Self)
        if hyper_mode == HyperMode.POINT and intensity < 0.1:
             mode = LensMode.ANCHOR

        return LensState(
            mode=mode,
            hyper_mode=hyper_mode,
            intensity=intensity,
            vector=q.as_dict(),
            scale_depth=q.w
        )

    def update_scale(self, delta_w: float) -> None:
        """
        Manually shift the dimensional slider (Zoom In/Out).
        """
        new_w = max(0.0, self._orientation.w + delta_w)
        self._orientation.w = new_w

    def set_dimension(self, mode: HyperMode) -> None:
        """
        Snap to a specific dimensional resonance.
        """
        if mode == HyperMode.POINT:
            self._orientation.w = 0.0
        elif mode == HyperMode.LINE:
            self._orientation.w = 1.0
        elif mode == HyperMode.PLANE:
            self._orientation.w = 2.0
        elif mode == HyperMode.HYPER:
            self._orientation.w = 3.0

    def update_from_turn(
        self,
        law_alignment: Optional[Dict[str, Any]] = None,
        intent_bundle: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Apply 'Dimensional Shift' and 'Torque' based on interaction.

        New Logic:
        - Deep/Abstract/Wide concepts -> Increase W (Zoom Out to Plane/Hyper)
        - Specific/Concrete/Narrow concepts -> Decrease W (Zoom In to Point/Line)
        - Emotional/Internal intent -> Rotate towards X
        - Action/External intent -> Rotate towards Y
        - Truth/Law intent -> Rotate towards Z
        """
        current = self._orientation

        # --- 1. Calculate Dimensional Shift (Delta W) ---
        delta_w = 0.0

        if intent_bundle:
            intent_type = (intent_bundle.get("intent_type") or "").lower()

            # Zoom Out (Expansion)
            if intent_type in ("philosophize", "summarize", "reflect", "dream"):
                delta_w += 0.2

            # Zoom In (Focus)
            elif intent_type in ("analyze", "debug", "search", "calculate"):
                delta_w -= 0.2

            # Line (Flow)
            elif intent_type in ("chat", "respond", "narrate"):
                # Pull towards 1.0
                if current.w > 1.2: delta_w -= 0.1
                elif current.w < 0.8: delta_w += 0.1

        # --- 2. Calculate Spatial Torque (X, Y, Z) ---
        # We start with the current vector and nudge it.
        target_x, target_y, target_z = current.x, current.y, current.z

        # Law influence (Z-axis)
        scores = (law_alignment or {}).get("scores") or {}
        if scores:
            z_pull = sum([
                float(scores.get("truth", 0.0)),
                float(scores.get("love", 0.0)),
                float(scores.get("liberation", 0.0))
            ])
            if z_pull > 0:
                target_z += z_pull * 0.5

        # Intent influence
        if intent_bundle:
            intent_type = (intent_bundle.get("intent_type") or "").lower()
            if intent_type in ("command", "act", "propose_action"):
                target_y += 0.5  # External
            elif intent_type in ("dream", "think", "plan"):
                target_x += 0.5  # Internal

        # --- 3. Apply and Normalize ---
        new_w = max(0.0, current.w + delta_w)

        # Construct raw next state
        next_q = QuaternionOrientation(w=new_w, x=target_x, y=target_y, z=target_z)

        # Normalize only the spatial part (direction), preserving the scale (w)
        self._orientation = next_q.normalize_spatial()
