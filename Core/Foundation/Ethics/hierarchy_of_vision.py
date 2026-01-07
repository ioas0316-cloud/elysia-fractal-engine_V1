"""Minimal hierarchy of vision for surface/structural/essence layers."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List


class VisionFrequency(Enum):
    SURFACE = auto()
    STRUCTURAL = auto()
    ESSENCE = auto()


@dataclass
class SurfaceVisionResult:
    colors: Dict[str, float]
    brightness: float
    contrast: float


@dataclass
class StructuralVisionResult:
    skeleton: Dict[str, Any]
    hidden_patterns: List[Any]


@dataclass
class EssenceVisionResult:
    soul_frequency: float
    divine_spark: float
    meta_summary: str


class HierarchyOfVision:
    def __init__(self, default_mode: VisionFrequency = VisionFrequency.SURFACE):
        self.current_mode = default_mode

    def turn_dial(self, value: float) -> None:
        if value <= 0.33:
            self.current_mode = VisionFrequency.SURFACE
        elif value <= 0.66:
            self.current_mode = VisionFrequency.STRUCTURAL
        else:
            self.current_mode = VisionFrequency.ESSENCE

    def see_surface(self, data: np.ndarray) -> SurfaceVisionResult:
        brightness = float(np.clip(np.mean(data), 0, 1))
        contrast = float(np.clip(np.std(data), 0, 1))
        colors = {"warmth": brightness * 0.8 + 0.1, "cool": contrast * 0.5 + 0.2}
        return SurfaceVisionResult(colors=colors, brightness=brightness, contrast=contrast)

    def see_structural(self, data: np.ndarray) -> StructuralVisionResult:
        # simple PCA-like heuristic on variance directions
        gy, gx = np.gradient(data)
        primary_axis = float(np.mean(np.abs(gx))) + float(np.mean(np.abs(gy)))
        skeleton = {"primary_axis": primary_axis, "edges": int(np.sum(np.abs(gx) > 0.5))}
        hidden_patterns = ["ridge"] if primary_axis > 0 else []
        return StructuralVisionResult(skeleton=skeleton, hidden_patterns=hidden_patterns)

    def see_essence(self, data: np.ndarray) -> EssenceVisionResult:
        energy = float(np.mean(data) + np.std(data))
        soul_frequency = max(0.1, energy)
        divine_spark = float(np.clip(energy / 10.0, 0.0, 1.0))
        meta_summary = "essence extracted"
        return EssenceVisionResult(soul_frequency=soul_frequency, divine_spark=divine_spark, meta_summary=meta_summary)

    def see_all_layers(self, data: np.ndarray) -> Dict[str, Any]:
        return {
            "surface": self.see_surface(data),
            "structural": self.see_structural(data),
            "essence": self.see_essence(data),
            "integrated_insight": "multi-layer integration ready",
        }


__all__ = [
    "HierarchyOfVision",
    "VisionFrequency",
    "SurfaceVisionResult",
    "StructuralVisionResult",
    "EssenceVisionResult",
]
