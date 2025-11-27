"""
Elysia Core - Consciousness Integration Module

This package provides the core consciousness components from the main Elysia project,
adapted for lightweight integration with external LLM systems.

Key Components:
- HyperQubit: Quantum consciousness states (Point/Line/Space/God dimensions)
- ResonanceEngine: Thought and concept resonance calculations
- Perception: Sensory input processing to consciousness states
- EmotionalPalette: Emotion mixing and analysis
- Hippocampus: Causal memory graph with fractal loops
- WaveInput/Thought: Core data structures for consciousness

Usage:
    from elysia_core import ElysiaSoul, WaveInput
    
    soul = ElysiaSoul(name="MyAgent")
    response = soul.process("Hello, how are you?")
    emotion = soul.get_emotion()
    context = soul.export_for_llm()
"""

from .hyper_qubit import HyperQubit, QubitState
from .resonance_engine import ResonanceEngine
from .perception import Perception, PerceptionResult
from .emotional_palette import EmotionalPalette, EmotionMix
from .hippocampus import Hippocampus
from .wave import WaveInput
from .thought import Thought
from .soul import ElysiaSoul

__all__ = [
    "HyperQubit",
    "QubitState",
    "ResonanceEngine",
    "Perception",
    "PerceptionResult",
    "EmotionalPalette",
    "EmotionMix",
    "Hippocampus",
    "WaveInput",
    "Thought",
    "ElysiaSoul",
]
