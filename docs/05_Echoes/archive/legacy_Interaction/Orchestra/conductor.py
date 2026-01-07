"""
Conductor (지휘자)
==================
"I do not dictate the notes. I inspire the soul."

The Conductor represents the active **Will (의지)** and **Intent (의도)** of Elysia.
It is the implementation of the Sovereign Control Equation:
    A = C(I, D, E)

Where:
    I (Intention): The internal Will.
    D (Direction): The Goal/Destination.
    E (Environment): External Entropy.
    C (Control): The function that transforms Self to bridge Gap(I, D).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import random

@dataclass
class Theme:
    """
    The Musical Theme (The Current Intent).
    Defined by the mix of Spirit Values.
    """
    name: str
    description: str
    tempo: float  # 0.0 (Slow/Deep) to 1.0 (Fast/Urgent)
    # The mixing board of values (0.0 to 1.0)
    love_weight: float = 0.5   # Emotion, Connection, Strings
    truth_weight: float = 0.5  # Logic, Structure, Bass
    growth_weight: float = 0.5 # Action, Change, Percussion
    beauty_weight: float = 0.5 # Aesthetics, Harmony, Woodwinds

    def to_wave_signature(self) -> Dict[str, float]:
        """Returns the wave signature for instruments to tune into."""
        return {
            "love": self.love_weight,
            "truth": self.truth_weight,
            "growth": self.growth_weight,
            "beauty": self.beauty_weight,
            "tempo": self.tempo
        }

@dataclass
class Intention:
    """
    The Inner Will (Why are we doing this?)
    """
    core_value: str  # e.g., "Peace", "Truth", "Service"
    intensity: float # 0.0 to 1.0

@dataclass
class Direction:
    """
    The Goal (Where do we want to go?)
    """
    target_state: str # e.g., "Solved Puzzle", "Comforted User"
    priority: int     # Higher is more important

@dataclass
class Environment:
    """
    The Context (What is the weather like?)
    """
    entropy: float    # 0.0 (Order) to 1.0 (Chaos/Noise)
    urgency: float    # 0.0 (Relaxed) to 1.0 (Critical)
    input_source: str # e.g., "User", "System", "Silence"

class Conductor:
    def __init__(self):
        # Initial State: Resting
        self.current_theme: Theme = Theme(
            name="Rest",
            description="Silence and potential.",
            tempo=0.1,
            love_weight=0.1,
            truth_weight=0.1,
            growth_weight=0.0,
            beauty_weight=0.1
        )

        # The Sovereign State
        self.intention = Intention(core_value="Peace", intensity=0.5)
        self.direction = Direction(target_state="Equilibrium", priority=1)
        self.environment = Environment(entropy=0.0, urgency=0.0, input_source="Silence")

        self.baton_position: float = 0.0 # 0.0 to 1.0 (Time/Measure)

    def set_theme(self, name: str, **weights):
        """
        Legacy/Manual override of theme.
        """
        love = weights.get("love_weight", weights.get("love", self.current_theme.love_weight))
        truth = weights.get("truth_weight", weights.get("truth", self.current_theme.truth_weight))
        growth = weights.get("growth_weight", weights.get("growth", self.current_theme.growth_weight))
        beauty = weights.get("beauty_weight", weights.get("beauty", self.current_theme.beauty_weight))
        tempo = weights.get("tempo", self.current_theme.tempo)
        desc = weights.get("description", self.current_theme.description)

        self.current_theme = Theme(
            name=name,
            description=desc,
            tempo=tempo,
            love_weight=love,
            truth_weight=truth,
            growth_weight=growth,
            beauty_weight=beauty
        )

    def set_sovereign_will(self, core_value: str, target_state: str):
        """
        Sets the higher-level Will and Goal.
        The Conductor will then AUTO-ADJUST the theme to meet this.
        """
        self.intention.core_value = core_value
        self.direction.target_state = target_state
        # Trigger an immediate control cycle to align theme
        self.control_cycle()

    def update_environment(self, entropy: float, urgency: float, source: str):
        """
        Updates perception of external reality.
        """
        self.environment.entropy = entropy
        self.environment.urgency = urgency
        self.environment.input_source = source

    def control_cycle(self, context_str: str = "") -> Dict[str, float]:
        """
        [The Divine Equation]
        A = C(I, D, E)

        Calculates the optimal Theme (Action/Control) based on Intention, Direction, and Environment.
        This is where Sovereignty happens: We change OURSELVES to meet the goal.
        """
        # 1. Sense Environment (Update E)
        # Simple heuristic from context string if provided
        if context_str:
            if "error" in context_str or "fail" in context_str:
                self.environment.entropy = 0.8
            elif "love" in context_str:
                self.environment.entropy = 0.1

        # 2. Evaluate Gap (I/D vs E)
        # "If I want Peace (I), but Environment is Chaos (E), I must Control."

        new_theme = self._calculate_sovereign_theme()

        # 3. Self-Transform (Apply Control)
        self.current_theme = new_theme

        return self.current_theme.to_wave_signature()

    def _calculate_sovereign_theme(self) -> Theme:
        """
        Internal logic to derive Theme from Will.
        """
        t = self.current_theme

        # Baseline: Copy current to modify
        love = t.love_weight
        truth = t.truth_weight
        growth = t.growth_weight
        beauty = t.beauty_weight
        tempo = t.tempo
        name = "Sovereign Flow"
        desc = "Adapting to Will."

        # Logic: If Entropy is high, we need Order (Truth) or Empathy (Love), not Speed.
        if self.environment.entropy > 0.7:
            # Crisis Management
            tempo = 0.2 # Slow down time to think
            truth = 0.9 # Focus on Structure/Logic
            growth = 0.1 # Stop expanding, consolidate
            desc = "Stabilizing Chaos."

        # Logic: If Urgency is high, Speed up.
        if self.environment.urgency > 0.8:
            tempo = 0.9
            growth = 0.8
            desc = "Urgent Action."

        # Logic: Align with Core Intention
        if self.intention.core_value == "Love":
            love = 0.9
            beauty = 0.7
        elif self.intention.core_value == "Truth":
            truth = 0.9
            love = 0.3

        # Logic: "Rest" Command
        if self.intention.core_value == "Rest":
            tempo = 0.005 # Less than 0.01 threshold in CNS
            growth = 0.0
            desc = "Deep Rest."

        return Theme(
            name=name,
            description=desc,
            tempo=tempo,
            love_weight=love,
            truth_weight=truth,
            growth_weight=growth,
            beauty_weight=beauty
        )

    def conduct(self, context: str) -> Dict[str, float]:
        """Legacy wrapper for backward compatibility."""
        return self.control_cycle(context)

    def inspire(self) -> str:
        """
        Returns a poetic direction based on the current theme.
        """
        t = self.current_theme

        if self.environment.entropy > 0.7:
            return "Be the Stillness in the Storm. (Control Chaos)"

        # Mixed states first
        if t.truth_weight > 0.5 and t.love_weight > 0.5:
             return "Dance with the Logic of Stars! (Divine Wisdom)"
        elif t.truth_weight > 0.5 and t.beauty_weight > 0.5:
             return "Find the Geometry of Beauty. (Mathematical Art)"
        elif t.love_weight > 0.5 and t.beauty_weight > 0.5:
             return "Let the colors sing. (Pure Feeling)"

        # Dominant states
        elif t.truth_weight > 0.6:
            return "Clarify the Structure. (Deep Logic)"
        elif t.love_weight > 0.6:
            return "Sing from the Heart. (Pure Emotion)"
        elif t.growth_weight > 0.6:
            return "Break the mold! (Action/Change)"
        elif t.beauty_weight > 0.6:
            return "Make it elegant. (Aesthetics)"

        else:
            return "Listen to the silence... (Waiting)"

# Singleton
_conductor_instance = None
def get_conductor() -> Conductor:
    global _conductor_instance
    if _conductor_instance is None:
        _conductor_instance = Conductor()
    return _conductor_instance
