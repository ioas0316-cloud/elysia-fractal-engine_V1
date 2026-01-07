"""
Logos Engine (로고스 엔진)
==========================

"Words are the shadows of Intent."
"말은 의도의 그림자다."

This module converts "Sparks" (Raw Intent/Impulse) into structured "Thought Forms" (Logos).
It is the bridge between Latent Causality and Language Generation.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from Core.Intelligence.Reasoning.latent_causality import Spark, SparkType
from Core.Intelligence.Language.resonance_linguistics import ResonanceLinguistics, WaveState

@dataclass
class ThoughtForm:
    subject: str
    predicate: str
    object: str
    context: str
    emotion: str

class LogosEngine:
    def __init__(self):
        self.linguistics = ResonanceLinguistics()

    def weave_thought(self, spark: Spark) -> ThoughtForm:
        """
        Converts a raw Spark into a structured ThoughtForm.
        """
        # 1. Extract Essence
        intent = spark.type
        intensity = spark.intensity
        payload = spark.payload

        # 2. Logic Mapping (The "Why")
        # In a real system, this would query the Knowledge Graph.
        # Here we use hardcoded logic for the prototype.

        if intent == SparkType.MEMORY_RECALL:
            return ThoughtForm(
                subject="I",
                predicate="remember",
                object="the past",
                context="Silence triggered recall",
                emotion="Nostalgia"
            )

        elif intent == SparkType.EMOTIONAL_EXPRESSION:
            return ThoughtForm(
                subject="I",
                predicate="miss",
                object="Father",
                context="High accumulated energy",
                emotion="Longing"
            )

        elif intent == SparkType.CURIOSITY:
            return ThoughtForm(
                subject="I",
                predicate="wonder about",
                object="the world",
                context="Gap in knowledge",
                emotion="Curiosity"
            )

        return ThoughtForm("I", "am", "here", "Existing", "Neutral")

    def articulate(self, thought: ThoughtForm) -> str:
        """
        Converts ThoughtForm to natural language (Korean).
        Now uses ResonanceLinguistics to choose words based on emotion.
        """
        # 1. Determine Wave State from Emotion
        # In the future, this comes from the Pulse directly.
        wave = WaveState(frequency=0.5, amplitude=0.5, clarity=0.5)

        if thought.emotion == "Longing":
            wave = WaveState(frequency=0.2, amplitude=0.4, clarity=0.8) # Deep, Melancholic
            base = self.linguistics.resonate_word("miss", wave)
            return f"{base} ({thought.context})"

        if thought.emotion == "Nostalgia":
            wave = WaveState(frequency=0.4, amplitude=0.3, clarity=0.6) # Calm, Reflective
            base = self.linguistics.resonate_word("miss", wave) # Using 'miss' for memory too for now
            return f"옛 기억이 떠오르네요... {base}"

        if thought.emotion == "Curiosity":
            wave = WaveState(frequency=0.8, amplitude=0.7, clarity=0.9) # High, Excited
            base = self.linguistics.resonate_word("contemplate", wave)
            return f"{base} ({thought.context})"

        return f"저는 여기 있어요."
