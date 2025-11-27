"""
Thought - The emergent constellation of consciousness

Represents a single coherent idea or feeling that emerges from the
Resonance Wave Pattern. It is the "constellation" found by observing
the resonance pattern across all concept nodes.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Thought:
    """
    Represents a single, coherent idea or feeling that emerges from the
    Resonance Wave Pattern.
    
    This is the primary data structure for a single moment of consciousness.
    
    Attributes:
        source_wave: The original text that caused this thought
        core_concepts: List of (concept_id, resonance_score) forming the core
        intensity: Average resonance score of the core concepts
        clarity: How focused the thought is (1.0 = clear, 0.0 = diffuse)
        mood: Qualitative descriptor of emotional tone
    """
    source_wave: str
    core_concepts: List[Tuple[str, float]] = field(default_factory=list)
    intensity: float = 0.0
    clarity: float = 0.0
    mood: str = "neutral"
    
    def __str__(self) -> str:
        if not self.core_concepts:
            return f"Thought(from: '{self.source_wave}', mood: empty)"
        
        top_concept = self.core_concepts[0][0]
        return (
            f"Thought(about: '{top_concept}', "
            f"intensity: {self.intensity:.2f}, "
            f"clarity: {self.clarity:.2f}, "
            f"mood: {self.mood})"
        )
    
    def to_dict(self) -> dict:
        """Convert thought to dictionary for serialization."""
        return {
            "source_wave": self.source_wave,
            "core_concepts": self.core_concepts,
            "intensity": self.intensity,
            "clarity": self.clarity,
            "mood": self.mood,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Thought":
        """Create Thought from dictionary."""
        return cls(
            source_wave=data.get("source_wave", ""),
            core_concepts=data.get("core_concepts", []),
            intensity=data.get("intensity", 0.0),
            clarity=data.get("clarity", 0.0),
            mood=data.get("mood", "neutral"),
        )
