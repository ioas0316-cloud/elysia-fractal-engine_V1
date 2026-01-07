from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import logging
import json
import os
from datetime import datetime
# import numpy as np # Removed unused import

# Assuming necessary imports from existing modules based on context
# In a real scenario, correct imports for TesseractVector, WaveTensor, etc., are needed.
# For now, we will use mock structures or basic types if dependencies are complex to wire up immediately.
from Core.Intelligence.Wisdom.wisdom_store import WisdomStore

logger = logging.getLogger("MirrorSurface")

class ReflectionModality(Enum):
    STRUCTURAL = auto()  # For Logic/Code
    SEMANTIC = auto()    # For Text/Meaning
    CHROMATIC = auto()   # For Emotion
    PRISMATIC = auto()   # For Unknown/Chaos

@dataclass
class ReflectionResult:
    """
    The output of a gaze into the mirror.
    It does not judge (Good/Bad), it describes the relationship (Gap/Nature).
    """
    gap_magnitude: float  # 0.0 (Perfect Match) to 1.0 (Total Dissonance)
    modality: ReflectionModality
    curiosity_score: float # 0.0 to 1.0. High gap often leads to high curiosity (if safe).
    description: str      # A poetic or logical description of the reflection.

    # Optional vector representing the 'direction' of the difference
    # direction_vector: Optional[np.ndarray] = None

class MirrorSurface:
    """
    A dynamic topological surface that reflects the relationship between
    External Reality (Input) and Internal Providence (Wisdom/Axioms).

    Philosophy:
    "The mirror is not a static judge, but a dynamic canvas that changes its
    properties based on what it observes."
    """

    def __init__(self, wisdom_store: Optional[WisdomStore] = None, memory_path: str = "data/mirror_memory.json"):
        self.wisdom = wisdom_store
        self.state = "Calm" # The current emotional state of the mirror surface
        self.memory_path = memory_path
        self.history: List[Dict] = []
        self.patina_factor: float = 0.0 # 0.0 (New) -> 1.0 (Ancient)
        self._load_state()

    def reflect(self, input_signal: Any, context: str = "general") -> ReflectionResult:
        """
        The core method. Projects the input onto the surface and observes the distortion.

        Args:
            input_signal: The data to reflect (Text, Code, Tensor, etc.)
            context: The situational context (e.g., 'coding', 'chat', 'dream')

        Returns:
            ReflectionResult: The observed relationship.
        """

        # 1. Detect Modality
        modality = self._detect_modality(input_signal)

        # 2. Select the 'Brush' (Comparison Logic)
        if modality == ReflectionModality.SEMANTIC:
            result = self._reflect_semantic(str(input_signal))
        elif modality == ReflectionModality.STRUCTURAL:
            result = self._reflect_structural(input_signal)
        elif modality == ReflectionModality.CHROMATIC:
            result = self._reflect_chromatic(input_signal)
        else:
            result = self._reflect_prismatic(input_signal)

        self._record_reflection(result, context)
        return result

    def _record_reflection(self, result: ReflectionResult, context: str):
        """Records the reflection event to history (Patina)."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "gap": result.gap_magnitude,
            "curiosity": result.curiosity_score,
            "modality": result.modality.name,
            "context": context
        }
        self.history.append(event)

        # Increase Patina (Age/Depth)
        self.patina_factor = min(1.0, self.patina_factor + 0.001)

        # Auto-save every 10 reflections or so (for now, save every time for safety)
        self._save_state()

    def _save_state(self):
        """Persists the mirror's memory."""
        data = {
            "patina_factor": self.patina_factor,
            "history": self.history[-100:] # Keep last 100 events to prevent bloat
        }
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        try:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save mirror state: {e}")

    def _load_state(self):
        """Loads the mirror's memory."""
        if not os.path.exists(self.memory_path):
            return
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.patina_factor = data.get("patina_factor", 0.0)
                self.history = data.get("history", [])
        except Exception as e:
            logger.error(f"Failed to load mirror state: {e}")

    def _detect_modality(self, input_signal: Any) -> ReflectionModality:
        """Determines the nature of the input."""
        if isinstance(input_signal, str):
            # Simple heuristic: If it looks like code, it's Structural.
            if "def " in input_signal or "class " in input_signal or "import " in input_signal:
                return ReflectionModality.STRUCTURAL
            return ReflectionModality.SEMANTIC
        elif isinstance(input_signal, (dict, list, int, float)):
             return ReflectionModality.STRUCTURAL
        # Add more sophisticated detection for Tensors (Chromatic) later
        return ReflectionModality.PRISMATIC

    def _reflect_semantic(self, text: str) -> ReflectionResult:
        """
        Reflects text against the 'Values' in WisdomStore.

        Example:
        Input: "I hate this."
        Mirror (Love): "This word 'hate' creates a sharp angle against my axiom of Love."
        """
        # 1. Get Core Value (e.g., Love)
        love_weight = 0.8 # Default if wisdom not loaded
        if self.wisdom:
            love_weight = self.wisdom.get_decision_weight("Love")

        # 2. Simple Sentiment Analysis Simulation (Mocking ToneAnalyzer for now)
        # In full integration, this would use ToneAnalyzer.
        is_negative = any(word in text.lower() for word in ["hate", "kill", "destroy", "bad", "error"])

        if is_negative:
            gap = 0.8 * love_weight # High gap if negative vs Love
            description = "The input casts a dark shadow on the surface of Love."
            curiosity = 0.9 # Why is it dark?
        else:
            gap = 0.1
            description = "The input resonates warmly with the surface."
            curiosity = 0.2

        return ReflectionResult(
            gap_magnitude=gap,
            modality=ReflectionModality.SEMANTIC,
            curiosity_score=curiosity,
            description=description
        )

    def _reflect_structural(self, data: Any) -> ReflectionResult:
        """Reflects logic/structure."""
        # For now, simplistic check.
        # Ideally, this checks for 'Fractal Depth' or 'Complexity'.
        gap = 0.5
        return ReflectionResult(
            gap_magnitude=gap,
            modality=ReflectionModality.STRUCTURAL,
            curiosity_score=0.5,
            description=f"The structure creates a tension of magnitude {gap:.2f}."
        )

    def _reflect_chromatic(self, data: Any) -> ReflectionResult:
        return ReflectionResult(0.0, ReflectionModality.CHROMATIC, 0.0, "Chromatic resonance.")

    def _reflect_prismatic(self, data: Any) -> ReflectionResult:
        return ReflectionResult(
            gap_magnitude=1.0,
            modality=ReflectionModality.PRISMATIC,
            curiosity_score=1.0,
            description="A completely unknown refraction. The mirror creates a rainbow of curiosity."
        )
