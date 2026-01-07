"""
Light Computer (빛의 연산 엔진)
=============================
Core Module adapted from Nova Seed Experiment.

"Logic is heavy. Resonance is instant."

This module provides wave-based computation primitives 
to replace heavy logic operations with interference patterns.
"""

import math
import cmath
from typing import Dict, Optional, Tuple

class Photon:
    """The basic unit of thought wave."""
    __slots__ = ['amplitude', 'phase', 'frequency']
    
    def __init__(self, amplitude: float, phase: float, frequency: float = 1.0):
        self.amplitude = amplitude
        self.phase = phase
        self.frequency = frequency

    @property
    def complex_val(self) -> complex:
        return cmath.rect(self.amplitude, self.phase)

    def interact(self, other: 'Photon') -> 'Photon':
        """
        Interference between two thoughts.
        """
        # Linear Superposition
        new_c = self.complex_val + other.complex_val
        new_amp, new_phase = cmath.polar(new_c)
        new_freq = (self.frequency + other.frequency) / 2
        return Photon(new_amp, new_phase, new_freq)

class LightField:
    """Simulation of a Consciousness Field."""
    
    def __init__(self):
        self.field: Dict[str, Photon] = {}
        
    def inject(self, name: str, amplitude: float, phase: float):
        self.field[name] = Photon(amplitude, phase)
        
    def calculate_coherence(self, name_a: str, name_b: str) -> float:
        """
        Calculates coherence (constructive interference) between two waves.
        Returns 0.0 (Destructive) to 1.0 (Constructive).
        """
        p1 = self.field.get(name_a)
        p2 = self.field.get(name_b)
        
        if not p1 or not p2:
            return 0.0
            
        result = p1.interact(p2)
        max_amp = p1.amplitude + p2.amplitude
        
        if max_amp == 0: return 0.0
        return result.amplitude / max_amp
