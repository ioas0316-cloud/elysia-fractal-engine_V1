"""
THE MIRROR OF CAUSALITY: WAVE STRUCTURES
========================================

"History is not a line; it is a interference pattern of infinite waves."

This module defines the fundamental data structures for the historical simulation.
Instead of static nodes, every event, choice, and consequence is modeled as a 
'ResonanceWave' that interacts with the user's internal state (Mind Landscape).

Philosophy:
1. Events has Mass (Gravity).
2. Choices have Frequency (Intent).
3. Outcomes are Interference Patterns (Harmony or Dissonance).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import math
import random

# Import Elysia's Physics Core if available, otherwise mock for isolation testing
try:
    from Core.Foundation.hyper_quaternion import HyperQuaternion
except ImportError:
    # Fallback for standalone testing
    class HyperQuaternion:
        def __init__(self, w, x, y, z): self.w, self.x, self.y, self.z = w, x, y, z

@dataclass
class Zeitgeist:
    """
    The 'Spirit of the Age'. 
    Represents the invisible background frequency of an era.
    
    Attributes:
        conservative_inertia (float): Resistance to change (0.0 to 1.0).
        latent_desire (float): The hidden hunger of the masses (-1.0 to 1.0).
        sophistication_level (float): The complexity of culture.
        dominant_frequency (float): The core 'vibe' of the era.
    """
    name: str
    conservative_inertia: float
    latent_desire: float
    sophistication_level: float
    dominant_frequency: float

    def get_resistance(self, innovation_score: float) -> float:
        """Calculates how much the era resists a new idea."""
        # High inertia resists high innovation
        return self.conservative_inertia * innovation_score

@dataclass
class HistoricalWave:
    """
    An event or generic force represented as a Wave.
    Compatible with Elysia's HyperQuaternion.
    """
    name: str
    q: HyperQuaternion  # The 4D representation (w=Time/Mag, x=Emotional, y=Logical, z=Ethical)
    frequency: float    # The type/flavor of the event
    
    @property
    def intensity(self) -> float:
        return math.sqrt(self.q.w**2 + self.q.x**2 + self.q.y**2 + self.q.z**2)

@dataclass
class ChoiceNode:
    """
    A decision point. 
    Not just 'A or B', but a vector of intent.
    """
    id: str
    description: str
    required_role: str  # e.g., "Leader", "Peasant"
    
    # The 'Intent Vector' of this choice
    # e.g., A choice to "Fight" might have high Red(Conflict) frequency
    intent_vector: HyperQuaternion 
    
    innovation_score: float # How radical is this choice?
    risk_score: float       # How dangerous?
    empathy_score: float    # How human?

@dataclass
class Consequence:
    """
    The result of a choice colliding with the Zeitgeist.
    """
    description: str
    
    # The resulting wave that will be injected into Elysia's mind
    sensory_wave: HistoricalWave
    
    # Meaning changes based on perspective
    narrative_by_role: Dict[str, str]
    
    # The Dual Axes
    worldly_resonance: float = 0.0
    divine_resonance: float = 0.0
    is_martyrdom: bool = False 

