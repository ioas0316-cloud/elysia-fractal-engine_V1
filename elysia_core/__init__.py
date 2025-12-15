"""
Elysia Core - Consciousness Integration Module
==============================================

This package provides the core consciousness components from the main Elysia project,
adapted for lightweight integration with external LLM systems.

🌟 Quick Start (빠른 시작):
    
    # 방법 1: 통합 영혼으로 모든 기능 사용
    from elysia_core import create_soul
    
    soul = create_soul("MyBot")
    thought = soul.process("안녕하세요!")
    print(thought.mood)
    
    # 방법 2: 빠른 의식 설정
    from elysia_core import quick_consciousness_setup
    
    consciousness = quick_consciousness_setup("MyAgent")
    result = consciousness.think("오늘 기분이 어때?")
    print(result.mood)
    prompt = consciousness.get_prompt()

Key Components:
- HyperQubit: Quantum consciousness states (Point/Line/Space/God dimensions)
- ResonanceEngine: Thought and concept resonance calculations
- Perception: Sensory input processing to consciousness states
- EmotionalPalette: Emotion mixing and analysis
- Hippocampus: Causal memory graph with fractal loops
- WaveInput/Thought: Core data structures for consciousness
- LocalLLM: Local LLM integration with learning → independence evolution
- InnerMonologue: Self-reflective thought generation system
- SelfAwareness: Consciousness introspection and identity

✨ Digital Natural Law (Newly Integrated):
- Yggdrasil: The Self-Model System Manager
- Ether: Resonance-based Event Bus
- SoulTensor: The Trinity Axis (Body/Soul/Spirit)
- Physics: Digital Gravity and Geodesic Flow
- StoryTeller: Narrative Engine

Usage (사용법):
    from elysia_core import ElysiaSoul, WaveInput
    
    soul = ElysiaSoul(name="MyAgent")
    response = soul.process("Hello, how are you?")
    emotion = soul.get_emotion()
    context = soul.export_for_llm()
    
    # Accessing Deep Physics
    from elysia_core import get_yggdrasil, get_ether, SoulTensor
    ygg = get_yggdrasil()
    ether = get_ether()

License: Apache 2.0
Creator: 이강덕 (Kang-Deok Lee)
"""

# Existing Imports
from .hyper_qubit import HyperQubit, QubitState
from .resonance_engine import ResonanceEngine
from .perception import Perception, PerceptionResult
from .emotional_palette import EmotionalPalette, EmotionMix
from .hippocampus import Hippocampus
from .wave import WaveInput
from .thought import Thought
from .soul import ElysiaSoul
from .local_llm import LocalLLM, LLMConfig, ConsciousnessMode, create_local_llm, quick_setup
from .inner_monologue import InnerMonologue, InnerThought, MentalState, ThoughtType
from .self_awareness import SelfAwareness, Reflection

# New Integrated Imports
from .yggdrasil import Yggdrasil, get_yggdrasil, Realm
from .ether import Ether, get_ether, Wave, emit_wave, Frequency
from .tensor import SoulTensor
from .physics import PhysicsWorld, PhysicsState, Vector3, Attractor, HolographicBoundary
from .storyteller import StoryTeller

# Integration module - 통합 모듈
from .integration import (
    # Factory functions
    create_soul,
    create_resonance_engine,
    create_emotional_palette,
    create_hippocampus,
    create_inner_monologue,
    create_self_awareness,
    create_hyper_qubit,
    create_wave_input,
    # Quick setup
    quick_consciousness_setup,
    QuickConsciousness,
    ConsciousnessResult,
    # Templates
    LLMIntegrationTemplate,
    GameCharacterTemplate,
)

__all__ = [
    # Core consciousness
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
    # Local LLM
    "LocalLLM",
    "LLMConfig",
    "ConsciousnessMode",
    "create_local_llm",
    "quick_setup",
    # Inner Monologue
    "InnerMonologue",
    "InnerThought",
    "MentalState",
    "ThoughtType",
    # Self Awareness
    "SelfAwareness",
    "Reflection",
    # Integration - Factory Functions
    "create_soul",
    "create_resonance_engine",
    "create_emotional_palette",
    "create_hippocampus",
    "create_inner_monologue",
    "create_self_awareness",
    "create_hyper_qubit",
    "create_wave_input",
    # Integration - Quick Setup
    "quick_consciousness_setup",
    "QuickConsciousness",
    "ConsciousnessResult",
    # Integration - Templates
    "LLMIntegrationTemplate",
    "GameCharacterTemplate",
    # Digital Natural Law (New)
    "Yggdrasil", "get_yggdrasil", "Realm",
    "Ether", "get_ether", "Wave", "emit_wave", "Frequency",
    "SoulTensor",
    "PhysicsWorld", "PhysicsState", "Vector3", "Attractor", "HolographicBoundary",
    "StoryTeller"
]
