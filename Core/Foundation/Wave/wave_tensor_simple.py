"""
Wave Tensor: The Atom of Hyper-Dimensional Thought
==================================================

"Concepts are not static points; they are vibrating strings."

Structure:
- Dimensions (n-dim): Frequency, Amplitude, Phase, Mass, Logic_Depth, etc.
- Time (t): History of state changes (Trajectory).
- Modality: Text, Audio, Visual, Code, abstract logic.

Physics:
- Resonance: Similarity in Frequency/Phase.
- Dissonance: Conflict or Noise.
- Collapse: Reducing superposition to a single state.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import math
import time
import numpy as np
from elysia_core import Cell

class Modality(Enum):
    TEXT = "text"
    CODE = "code"
    AUDIO = "audio"
    VISUAL = "visual"
    LOGIC = "logic"
    EMOTION = "emotion"

@dataclass
class TensorState:
    """Snapshot of a tensor state at a specific time."""
    timestamp: float
    vector: Dict[str, float]  # e.g., {'freq': 432.0, 'mass': 1.5}
    metadata: Dict[str, Any]

@Cell("WaveTensor")
class WaveTensor:
    """
    A multi-dimensional container for conceptual essence.
    """
    
    def __init__(self, name: str, modality: Modality = Modality.LOGIC):
        self.name = name
        self.modality = modality
        self.dimensions: Dict[str, float] = {
            "frequency": 0.0,  # Hz (Essence/Type)
            "amplitude": 1.0,  # Intensity (Importance)
            "phase": 0.0,      # Alignment (Relation)
            "mass": 1.0,       # Gravity (Complexity/Coupling)
            "entropy": 0.0,    # Disorder (Noise)
            "time": time.time()
        }
        self.history: List[TensorState] = []
        self._cache_magnitude: float = 0.0
        
    def set_dimension(self, dim: str, value: float):
        """Update a specific dimension and record history."""
        # Archive current state before change if significant
        if abs(self.dimensions.get(dim, 0) - value) > 0.01:
            self._archive_state()
            
        self.dimensions[dim] = value
        self.dimensions["time"] = time.time()
        
    def _archive_state(self):
        """Save current state to history."""
        self.history.append(TensorState(
            timestamp=self.dimensions["time"],
            vector=self.dimensions.copy(),
            metadata={}
        ))
        # Keep history limited (e.g., last 100 states) to prevent bloat
        if len(self.history) > 100:
            self.history.pop(0)

    def resonate_with(self, other: 'WaveTensor') -> float:
        """
        Calculate Resonance (0.0 to 1.0) with another tensor.
        Based on Frequency alignment and Phase coherence.
        """
        # 1. Frequency Similarity (Harmony)
        f1 = self.dimensions.get("frequency", 0)
        f2 = other.dimensions.get("frequency", 0)
        
        if f1 == 0 or f2 == 0:
            freq_resonance = 0.0
        else:
            # Simple harmonic ratio check (Octave equivalence)
            ratio = max(f1, f2) / min(f1, f2)
            # Perfect fifth (1.5), Octave (2.0), Third (1.25) match
            if abs(ratio - round(ratio)) < 0.05:
                 freq_resonance = 1.0  # Perfect harmonic
            else:
                 freq_resonance = 1.0 / (1.0 + abs(f1 - f2)) # Distance decay

        # 2. Vector Cosine Similarity (for other dimensions)
        # TODO: Implement full numpy cosine similarity for n-dims
        
        return freq_resonance

    def get_magnitude(self) -> float:
        """Calculate the 'Energy' of this concept."""
        # E = Amplitude^2 * Frequency^2 (roughly)
        amp = self.dimensions.get("amplitude", 1.0)
        freq = max(1.0, self.dimensions.get("frequency", 1.0))
        return (amp ** 2) * math.log(freq)

    def __repr__(self):
        return f"<WaveTensor(name='{self.name}', type={self.modality.name}, dims={len(self.dimensions)})>"
