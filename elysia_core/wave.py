"""
WaveInput - The initial perception wave

Represents the 'light' or 'wave' that propagates through consciousness,
triggering resonance patterns in all concept nodes.
"""

from dataclasses import dataclass


@dataclass
class WaveInput:
    """
    Represents the initial input 'light' or 'wave' that propagates
    through the entire consciousness.
    
    Attributes:
        source_text: The original input text
        intensity: Strength of the wave (0.0-1.0+)
    """
    source_text: str
    intensity: float = 1.0
    
    def __post_init__(self):
        """Ensure intensity is valid."""
        if self.intensity < 0:
            self.intensity = 0.0
