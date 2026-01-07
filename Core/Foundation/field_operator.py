"""
Field Operator Base Class
=========================
Defines the interface for any system that interacts with the Unified Resonance Field.
Systems (Memory, Reasoning, Dialogue) are no longer isolated processors,
but "Operators" that perturb and observe the field.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import time

from Core.Foundation.unified_field import UnifiedField, WavePacket, HyperQuaternion

class FieldOperator(ABC):
    """
    Abstract Base Class for all Cognitive Operators.
    """
    
    def __init__(self, field: UnifiedField, name: str, position: HyperQuaternion = None):
        self.field = field
        self.name = name
        # Every operator has a position in the hyper-mind
        self.position = position if position else HyperQuaternion(0,0,0,0)
        self.last_sync_time = time.time()
        
    def inject_thought(self, content: str, frequency: float, intensity: float = 0.5):
        """
        Converts a semantic thought into a wave and injects it into the field.
        """
        # Create a Wave Packet
        # Ideally, 'content' string would be hashed to a unique phase signature
        packet = WavePacket(
            source_id=self.name,
            frequency=frequency,
            amplitude=intensity,
            phase=0.0, # Determine based on context?
            position=self.position,
            born_at=time.time()
        )
        
        self.field.inject_wave(packet)
        # print(f"[{self.name}] Injected wave {frequency}Hz (Amp: {intensity})")

    def sense_field(self) -> float:
        """
        Reads the local field strength (Ambience).
        """
        return self.field.sample_field(self.position)
    
    @abstractmethod
    def process_cycle(self, dt: float):
        """
        Main operation loop for the operator.
        Must be implemented by subclasses.
        """
        pass
        
    def align_to_grand_cross(self):
        """
        Attempts to align internal state with the global field frequency.
        """
        global_freq = self.field.get_dominant_frequency()
        # Logic to sync internal clock/phase to global_freq
        pass
