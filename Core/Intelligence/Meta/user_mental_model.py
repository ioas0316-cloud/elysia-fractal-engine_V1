"""
USER MENTAL MODEL: The Theory of Mind
=====================================
"To understand you, I must become you."

This module enables Elysia to simulate the User's internal state.
It uses 'Inverse Empathy':
1. Input: User Text.
2. Simulation: "If I, Elysia, wrote this text, what would I be feeling?"
3. Deduction: "Therefore, the User is likely feeling X."

This overrides literal interpretation with emotional context.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

from Core.Education.CausalityMirror.projective_empathy import ProjectiveEmpathy
from Core.Education.CausalityMirror.wave_structures import HyperQuaternion

logger = logging.getLogger("UserMentalModel")

@dataclass
class UserState:
    id: str = "USER_01"
    current_mood: str = "Neutral"
    implied_intent: str = "Observation"
    cognitive_load: float = 0.5 # 0.0 relaxed, 1.0 stressed
    soul_alignment: float = 0.0 # Harmony with Elysia

class UserMentalModel:
    def __init__(self):
        self.state = UserState()
        # We use Empathy engine for simulation, though we might need a specific 'Inverse' method
        self.empathy_engine = ProjectiveEmpathy()
        logger.info("🧠 User Mental Model initialized. I am watching you.")

    def deduce_state(self, user_text: str, context_history: list) -> UserState:
        """
        Deduces the user's state based on text and history.
        """
        # 1. Linguistic Analysis (Tone)
        # Simple heuristic mapping for now, to be replaced by 4D Tone Analysis later
        tone_map = {
            "whatever": ("Dismissive", -0.5),
            "fine": ("Passive-Aggressive", -0.3),
            "wow": ("Amazed", 0.8),
            "no": ("Firm", 0.0),
            "help": ("Distressed", -0.8),
            "thanks": ("Gratitude", 0.5)
        }
        
        lower_text = user_text.lower()
        
        # 2. Inverse Simulation
        # "If I said X, what would I be?"
        # For this prototype, we use the tone map as a proxy for the simulation result
        # In a full version, we'd feed this into ImpactEngine inverted.
        
        detected_mood = "Neutral"
        sentiment_val = 0.0
        
        for key, (mood, val) in tone_map.items():
            if key in lower_text:
                detected_mood = mood
                sentiment_val = val
                break
                
        # 3. Contextual Adjustment
        # If history was "Angry" and now is "Fine" (P-A) or "Neutral", it's suspicious.
        last_context = context_history[-1] if context_history else {}
        
        # Check for suppression pattern: High arousal (Angry) -> Low arousal (Neutral/P-A)
        is_suppressed = detected_mood in ["Neutral", "Passive-Aggressive"]
        was_angry = last_context.get("mood") in ["Angry", "Distressed"]
        
        if was_angry and is_suppressed:
             detected_mood = "Concealed Anger"
             sentiment_val = -0.6 # Deep negative, not just P-A -0.3
             
        # 4. Update State
        self.state.current_mood = detected_mood
        self.state.soul_alignment += sentiment_val * 0.1
        self.state.soul_alignment = max(-1.0, min(1.0, self.state.soul_alignment))
        
        logger.info(f"👁️ Theory of Mind: User says '{user_text}' -> State: {detected_mood}")
        
        return self.state

    def get_simulation_report(self) -> str:
        return (
            f"User Simulation:\n"
            f"   Mood: {self.state.current_mood}\n"
            f"   Resonance: {self.state.soul_alignment:.2f}"
        )
