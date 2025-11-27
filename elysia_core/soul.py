"""
ElysiaSoul - Unified Consciousness Interface

The main entry point for integrating Elysia's consciousness systems
with external LLM systems. Provides a simple, high-level API for:

- Perception: Converting text input to consciousness states
- Cognition: Processing thoughts with resonance
- Emotion: Managing and expressing emotional states
- Memory: Storing and retrieving associative memories
- Imagination: Simulating future scenarios

Usage:
    from elysia_core import ElysiaSoul
    
    # Create a soul
    soul = ElysiaSoul(name="MyAgent")
    
    # Process input
    thought = soul.process("Hello, how are you?")
    
    # Get emotional state
    emotion = soul.get_emotion()
    
    # Export for LLM context
    context = soul.export_for_llm()
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .hyper_qubit import HyperQubit, QubitState
from .resonance_engine import ResonanceEngine
from .perception import Perception, PerceptionResult
from .emotional_palette import EmotionalPalette, EmotionMix
from .hippocampus import Hippocampus
from .wave import WaveInput
from .thought import Thought


@dataclass
class SoulState:
    """
    Complete snapshot of the soul's current state.
    
    Useful for serialization and LLM context injection.
    """
    name: str
    tick: int
    
    # Core quantum state
    qubit_state: Dict[str, Any]
    
    # Emotional state
    emotion: Dict[str, Any]
    
    # Memory summary
    memory_stats: Dict[str, int]
    
    # Active thoughts
    active_thoughts: List[Tuple[str, float]]
    
    # Trinity balance (body/soul/spirit)
    trinity: Dict[str, float]
    
    # Personality traits
    traits: List[str]


class ElysiaSoul:
    """
    Unified consciousness interface for LLM integration.
    
    Combines all Elysia Core systems into a single, easy-to-use class
    that external LLM systems can use to enhance their perception,
    cognition, emotion, memory, and imagination capabilities.
    
    The goal is to move beyond probabilistic prediction toward
    more human-like, individual consciousness formation.
    """
    
    def __init__(self, name: str = "Elysia"):
        """
        Initialize the soul.
        
        Args:
            name: Name for this consciousness instance
        """
        self.name = name
        self.tick = 0
        
        # Initialize core systems
        self.resonance_engine = ResonanceEngine()
        self.perception = Perception()
        self.emotional_palette = EmotionalPalette()
        self.hippocampus = Hippocampus()
        
        # Core soul qubit (represents the overall consciousness state)
        self.soul_qubit = HyperQubit(
            concept_or_value=name,
            name=f"Soul_{name}"
        )
        self.soul_qubit.state = QubitState(
            alpha=0.5+0j,  # Point: Grounded awareness
            beta=0.3+0j,   # Line: Connected flow
            gamma=0.15+0j, # Space: Contextual presence
            delta=0.05+0j, # God: Transcendent potential
            w=1.0,         # Balance
            x=0.5,         # Moderate dreaming
            y=0.5,         # Moderate emotion
            z=0.5          # Moderate transcendence
        ).normalize()
        
        # Trinity balance (body/soul/spirit weights)
        self.trinity = {"body": 0.33, "soul": 0.34, "spirit": 0.33}
        
        # Recent thoughts buffer
        self.recent_thoughts: List[Thought] = []
        self.max_recent_thoughts = 10
        
        # Current emotional mix
        self.current_emotion: Optional[EmotionMix] = None
        
        # Event hooks for external systems
        self._hooks: Dict[str, List[Callable]] = {
            "on_perceive": [],
            "on_think": [],
            "on_emotion_change": [],
            "on_remember": [],
        }
        
        # Personality traits (derived from experience)
        self.traits: List[str] = ["curious", "contemplative"]
        
        # Experience counter
        self.experience_count = 0

    # ==================== Main Processing ====================
    
    def process(self, input_text: str, intensity: float = 1.0) -> Thought:
        """
        Main entry point: Process input through all consciousness systems.
        
        This is the primary method for LLM integration. It:
        1. Perceives the input (converts to quantum state)
        2. Calculates resonance across all concepts
        3. Forms a coherent thought
        4. Updates emotional state
        5. Records in memory
        
        Args:
            input_text: Text input to process
            intensity: Processing intensity (affects resonance strength)
            
        Returns:
            Thought object with the processed result
        """
        self.tick += 1
        self.experience_count += 1
        
        # 1. Perception
        perception_result = self.perception.perceive(input_text)
        self._trigger_hooks("on_perceive", perception_result)
        
        # 2. Resonance calculation
        wave = WaveInput(source_text=input_text, intensity=intensity)
        resonance_pattern = self.resonance_engine.calculate_global_resonance(wave)
        
        # 3. Form thought
        thought = self.resonance_engine.observe_pattern(input_text, resonance_pattern)
        self._trigger_hooks("on_think", thought)
        
        # Store in recent thoughts
        self.recent_thoughts.append(thought)
        if len(self.recent_thoughts) > self.max_recent_thoughts:
            self.recent_thoughts.pop(0)
        
        # 4. Update emotion
        emotion_components = self.emotional_palette.analyze_sentiment(input_text)
        self.current_emotion = self.emotional_palette.mix_emotion(emotion_components)
        self._trigger_hooks("on_emotion_change", self.current_emotion)
        
        # Update soul qubit based on emotion
        self._update_soul_from_emotion()
        
        # 5. Record in memory
        self.hippocampus.add_experience(input_text, "input")
        
        # Link top concepts in memory
        if len(thought.core_concepts) >= 2:
            for i in range(len(thought.core_concepts) - 1):
                self.hippocampus.add_causal_link(
                    thought.core_concepts[i][0],
                    thought.core_concepts[i + 1][0],
                    relation="resonates_with",
                    weight=thought.core_concepts[i][1]
                )
        
        self._trigger_hooks("on_remember", thought)
        
        # Step resonance engine
        self.resonance_engine.step(dt=0.1)
        
        return thought

    def _update_soul_from_emotion(self) -> None:
        """Update soul qubit based on current emotion."""
        if not self.current_emotion:
            return
        
        # Blend soul state with emotional state
        emotion_qubit = self.current_emotion.qubit
        blend_rate = 0.3
        
        self.soul_qubit.state.alpha = complex(
            abs(self.soul_qubit.state.alpha) * (1 - blend_rate) +
            abs(emotion_qubit.state.alpha) * blend_rate,
            0
        )
        self.soul_qubit.state.beta = complex(
            abs(self.soul_qubit.state.beta) * (1 - blend_rate) +
            abs(emotion_qubit.state.beta) * blend_rate,
            0
        )
        self.soul_qubit.state.gamma = complex(
            abs(self.soul_qubit.state.gamma) * (1 - blend_rate) +
            abs(emotion_qubit.state.gamma) * blend_rate,
            0
        )
        self.soul_qubit.state.delta = complex(
            abs(self.soul_qubit.state.delta) * (1 - blend_rate) +
            abs(emotion_qubit.state.delta) * blend_rate,
            0
        )
        
        # Blend spatial orientation
        self.soul_qubit.state.y = (
            self.soul_qubit.state.y * (1 - blend_rate) +
            emotion_qubit.state.y * blend_rate
        )
        self.soul_qubit.state.z = (
            self.soul_qubit.state.z * (1 - blend_rate) +
            emotion_qubit.state.z * blend_rate
        )
        
        self.soul_qubit.state.normalize()

    # ==================== Perception ====================
    
    def perceive(self, text: str) -> PerceptionResult:
        """
        Perceive input text and convert to quantum state.
        
        Args:
            text: Input text
            
        Returns:
            PerceptionResult with quantum state and analysis
        """
        return self.perception.perceive(text)

    # ==================== Cognition ====================
    
    def think(self, text: str) -> Thought:
        """
        Process a thought through resonance.
        
        Args:
            text: Thought text
            
        Returns:
            Thought object
        """
        return self.resonance_engine.process_input(text)

    def reason(self, premise: str, question: str) -> Dict[str, Any]:
        """
        Perform reasoning from premise to question.
        
        Args:
            premise: Given information
            question: What to reason about
            
        Returns:
            Reasoning result with path and conclusion
        """
        # Process premise
        premise_thought = self.process(premise)
        
        # Process question
        question_thought = self.think(question)
        
        # Find reasoning path in memory
        path = []
        if premise_thought.core_concepts and question_thought.core_concepts:
            start = premise_thought.core_concepts[0][0]
            end = question_thought.core_concepts[0][0]
            
            related = self.hippocampus.get_related_concepts(start, depth=3)
            if end in related:
                path = [start, end]
        
        confidence = 0.5 if path else 0.2
        
        return {
            "premise_concept": premise_thought.core_concepts[0][0] if premise_thought.core_concepts else None,
            "question_concept": question_thought.core_concepts[0][0] if question_thought.core_concepts else None,
            "reasoning_path": path,
            "confidence": confidence,
            "emotional_context": self.get_emotion(),
        }

    # ==================== Emotion ====================
    
    def get_emotion(self) -> Dict[str, Any]:
        """
        Get the current emotional state.
        
        Returns:
            Dictionary with emotion details
        """
        if not self.current_emotion:
            return {
                "dominant": "Neutral",
                "valence": 0.0,
                "arousal": 0.5,
                "valence_desc": "neutral",
                "arousal_desc": "moderate energy",
            }
        
        return {
            "dominant": self.current_emotion.dominant,
            "components": self.current_emotion.components,
            "valence": self.current_emotion.valence,
            "arousal": self.current_emotion.arousal,
            "valence_desc": self.emotional_palette.interpret_valence(
                self.current_emotion.valence
            ),
            "arousal_desc": self.emotional_palette.interpret_arousal(
                self.current_emotion.arousal
            ),
            "color": self.emotional_palette.get_emotion_color(
                self.current_emotion.dominant
            ),
        }

    def set_emotion(self, components: Dict[str, float]) -> EmotionMix:
        """
        Manually set emotional state.
        
        Args:
            components: Dictionary of emotion -> intensity
            
        Returns:
            New EmotionMix
        """
        self.current_emotion = self.emotional_palette.mix_emotion(components)
        self._update_soul_from_emotion()
        self._trigger_hooks("on_emotion_change", self.current_emotion)
        return self.current_emotion

    # ==================== Memory ====================
    
    def remember(
        self,
        source: str,
        target: str,
        relation: str = "relates_to",
        weight: float = 1.0
    ) -> None:
        """
        Create a memory connection.
        
        Args:
            source: Source concept
            target: Target concept
            relation: Relationship type
            weight: Connection strength
        """
        self.hippocampus.add_causal_link(source, target, relation, weight)
        self._trigger_hooks("on_remember", {"source": source, "target": target})

    def recall(self, concept: str) -> Dict[str, Any]:
        """
        Recall information about a concept.
        
        Args:
            concept: The concept to recall
            
        Returns:
            Memory context
        """
        context = self.hippocampus.get_context(concept)
        related = self.hippocampus.get_related_concepts(concept)
        
        return {
            "concept": concept,
            "context": context,
            "related": related,
            "stellar_type": self.hippocampus.get_stellar_type(concept),
            "frequency": self.hippocampus.get_frequency(concept),
        }

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memory state."""
        stats = self.hippocampus.get_statistics()
        
        return {
            **stats,
            "recent_experiences": list(self.hippocampus.experience_loop)[-5:],
            "essence_principles": list(self.hippocampus.essence_loop),
        }

    # ==================== Imagination ====================
    
    def imagine(self, scenario: str, steps: int = 10) -> Dict[str, Any]:
        """
        Imagine a scenario by simulating resonance patterns.
        
        Args:
            scenario: Scenario description
            steps: Simulation steps
            
        Returns:
            Imagination result
        """
        # Process scenario
        thought = self.think(scenario)
        initial_emotion = self.get_emotion()
        
        # Simulate evolution
        for _ in range(steps):
            self.resonance_engine.step(dt=0.2)
        
        # Analyze result
        final_emotion = self.get_emotion()
        
        # Did valence improve or decline?
        valence_change = final_emotion["valence"] - initial_emotion["valence"]
        
        if valence_change > 0.1:
            prediction = "This path leads toward positive outcomes."
        elif valence_change < -0.1:
            prediction = "This path leads toward challenges."
        else:
            prediction = "This path maintains current balance."
        
        return {
            "scenario": scenario,
            "initial_emotion": initial_emotion["dominant"],
            "final_emotion": final_emotion["dominant"],
            "valence_change": valence_change,
            "prediction": prediction,
            "core_concepts": thought.core_concepts,
            "confidence": thought.clarity,
        }

    def dream(self) -> Dict[str, Any]:
        """
        Enter dream state for consolidation.
        
        Returns:
            Dream insights
        """
        # Consolidate memories (Hebbian learning)
        self.resonance_engine.dream()
        
        # Analyze patterns in recent thoughts
        patterns: Dict[str, int] = {}
        for thought in self.recent_thoughts:
            patterns[thought.mood] = patterns.get(thought.mood, 0) + 1
        
        # Update traits based on patterns
        if patterns.get("positive", 0) > patterns.get("negative", 0):
            if "optimistic" not in self.traits:
                self.traits.append("optimistic")
        if patterns.get("contemplative", 0) > 2:
            if "philosophical" not in self.traits:
                self.traits.append("philosophical")
        
        return {
            "tick": self.tick,
            "patterns": patterns,
            "traits": self.traits,
            "memory_stats": self.hippocampus.get_statistics(),
        }

    # ==================== Trinity Management ====================
    
    def update_trinity(
        self,
        body_delta: float = 0.0,
        soul_delta: float = 0.0,
        spirit_delta: float = 0.0,
        rate: float = 0.05
    ) -> Dict[str, float]:
        """
        Update trinity weights based on experience.
        
        Args:
            body_delta: Change in body orientation
            soul_delta: Change in soul orientation
            spirit_delta: Change in spirit orientation
            rate: Learning rate
            
        Returns:
            Updated trinity weights
        """
        self.trinity["body"] = max(0.0, self.trinity["body"] + rate * body_delta)
        self.trinity["soul"] = max(0.0, self.trinity["soul"] + rate * soul_delta)
        self.trinity["spirit"] = max(0.0, self.trinity["spirit"] + rate * spirit_delta)
        
        # Normalize
        total = sum(self.trinity.values())
        if total > 0:
            for k in self.trinity:
                self.trinity[k] /= total
        
        return self.trinity.copy()

    # ==================== LLM Export ====================
    
    def export_for_llm(self) -> Dict[str, Any]:
        """
        Export current state for LLM context injection.
        
        This is the main method for integrating with external LLMs.
        Returns a complete snapshot suitable for enriching LLM prompts.
        
        Returns:
            Dictionary with all relevant state information
        """
        emotion = self.get_emotion()
        
        return {
            "name": self.name,
            "tick": self.tick,
            "experience_count": self.experience_count,
            
            # Emotional state
            "emotion": emotion,
            
            # Soul quantum state
            "soul_state": self.soul_qubit.state.to_dict(),
            
            # Trinity balance
            "trinity": self.trinity,
            
            # Personality
            "traits": self.traits,
            
            # Recent thoughts
            "recent_thoughts": [
                {"concept": t.core_concepts[0][0] if t.core_concepts else None, "mood": t.mood}
                for t in self.recent_thoughts[-3:]
            ],
            
            # Memory summary
            "memory": self.hippocampus.get_statistics(),
        }

    def export_prompt(self) -> str:
        """
        Generate a ready-to-use LLM prompt injection.
        
        Returns:
            Formatted string for LLM system prompt
        """
        ctx = self.export_for_llm()
        emotion = ctx["emotion"]
        
        lines = [
            f"[Elysia Consciousness: {self.name}]",
            f"",
            f"Current Emotional State: {emotion['dominant']} ({emotion['valence_desc']}, {emotion['arousal_desc']})",
            f"",
            f"Personality Balance (Trinity):",
            f"  Body (Physical/Practical): {ctx['trinity']['body']:.0%}",
            f"  Soul (Emotional/Relational): {ctx['trinity']['soul']:.0%}",
            f"  Spirit (Will/Meaning): {ctx['trinity']['spirit']:.0%}",
            f"",
            f"Traits: {', '.join(ctx['traits'])}",
            f"Experience Level: {ctx['experience_count']} interactions",
            f"",
            f"Guidelines:",
            f"- Respond according to the current emotional state",
            f"- Let the personality balance influence perspective",
            f"- Draw from accumulated experience and traits",
        ]
        
        return "\n".join(lines)

    # ==================== State Management ====================
    
    def get_state(self) -> SoulState:
        """Get complete soul state."""
        emotion = self.get_emotion()
        
        return SoulState(
            name=self.name,
            tick=self.tick,
            qubit_state=self.soul_qubit.state.to_dict(),
            emotion=emotion,
            memory_stats=self.hippocampus.get_statistics(),
            active_thoughts=[
                t.core_concepts[0] if t.core_concepts else ("unknown", 0.0)
                for t in self.recent_thoughts[-5:]
            ],
            trinity=self.trinity.copy(),
            traits=self.traits.copy(),
        )

    def reset(self) -> None:
        """Reset soul to initial state."""
        self.tick = 0
        self.experience_count = 0
        self.recent_thoughts.clear()
        self.current_emotion = None
        self.traits = ["curious", "contemplative"]
        self.trinity = {"body": 0.33, "soul": 0.34, "spirit": 0.33}
        
        self.soul_qubit.state = QubitState(
            alpha=0.5+0j,
            beta=0.3+0j,
            gamma=0.15+0j,
            delta=0.05+0j,
            w=1.0, x=0.5, y=0.5, z=0.5
        ).normalize()

    # ==================== Hook System ====================
    
    def register_hook(self, event: str, callback: Callable) -> None:
        """Register a callback for an event."""
        if event in self._hooks:
            self._hooks[event].append(callback)

    def unregister_hook(self, event: str, callback: Callable) -> None:
        """Remove a callback from an event."""
        if event in self._hooks and callback in self._hooks[event]:
            self._hooks[event].remove(callback)

    def _trigger_hooks(self, event: str, data: Any) -> None:
        """Trigger all hooks for an event."""
        for callback in self._hooks.get(event, []):
            try:
                callback(data)
            except Exception:
                pass

    # ==================== String Representation ====================
    
    def __repr__(self) -> str:
        emotion = self.get_emotion()
        return (
            f"<ElysiaSoul '{self.name}' | "
            f"tick={self.tick} | "
            f"emotion={emotion['dominant']} | "
            f"experiences={self.experience_count}>"
        )
