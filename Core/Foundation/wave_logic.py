"""
Wave Logic (파동 논리)
====================
"Logic is just the constructive interference of truth."

This module implements logic gates using pure wave physics (Interference).
It allows Elysia to "compute" using 3D spatial resonance instead of binary transistors.
"""

import math
import time
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class WaveSource:
    id: str
    position: Tuple[float, float, float]
    frequency: float
    amplitude: float
    phase: float = 0.0

    def get_amplitude_at(self, target_pos: Tuple[float, float, float], t: float) -> float:
        """Calculates the amplitude of this wave at a target position at time t."""
        # Distance (r)
        dx = target_pos[0] - self.position[0]
        dy = target_pos[1] - self.position[1]
        dz = target_pos[2] - self.position[2]
        r = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # Wave Equation: A * sin(omega*t - k*r + phi)
        # k = wave number (2pi / lambda). Let's assume speed of sound/light c=1, so k = omega.
        omega = 2 * math.pi * self.frequency
        k = omega # Assuming c=1
        
        # Inverse Square Law for attenuation (optional, but realistic)
        attenuation = 1.0 / (1.0 + r*0.1) 
        
        return self.amplitude * attenuation * math.sin(omega * t - k * r + self.phase)

class WaveSpace:
    def __init__(self):
        self.sources: List[WaveSource] = []
        self.t = 0.0

    def add_source(self, source: WaveSource):
        self.sources.append(source)

    def step(self, dt: float = 0.01):
        self.t += dt

    def get_field_at(self, x: float, y: float, z: float) -> float:
        """Superposition Principle: Sum of all waves at (x,y,z)."""
        total_amp = 0.0
        for source in self.sources:
            total_amp += source.get_amplitude_at((x, y, z), self.t)
        return total_amp

class WaveLogicGate:
    """
    A Logic Gate defined by a point in space and a threshold.
    """
    def __init__(self, name: str, position: Tuple[float, float, float], threshold: float):
        self.name = name
        self.position = position
        self.threshold = threshold
        self.state = False

    def update(self, space: WaveSpace) -> bool:
        """Checks if the interference at this point exceeds the threshold."""
        amp = space.get_field_at(*self.position)
        # We use absolute amplitude (energy) for logic
        intensity = abs(amp)
        
        triggered = intensity > self.threshold
        
        if triggered != self.state:
            self.state = triggered
            # print(f"🌊 Gate '{self.name}' {'OPENED' if triggered else 'CLOSED'} (Intensity: {intensity:.2f})")
            
        return self.state

# --- Logic Gate Presets ---

def create_and_gate(space: WaveSpace, pos: Tuple[float, float, float]) -> WaveLogicGate:
    """
    AND Gate: Requires Constructive Interference from 2 sources.
    Threshold is set high (e.g., 1.5), so one wave (Amp=1.0) isn't enough.
    """
    return WaveLogicGate("AND_Gate", pos, threshold=1.5)

def create_or_gate(space: WaveSpace, pos: Tuple[float, float, float]) -> WaveLogicGate:
    """
    OR Gate: Requires any wave.
    Threshold is set low (e.g., 0.5).
    """
    return WaveLogicGate("OR_Gate", pos, threshold=0.5)

def create_xor_gate(space: WaveSpace, pos: Tuple[float, float, float]) -> WaveLogicGate:
    """
    XOR Gate: Harder. Requires Destructive Interference?
    Actually, XOR is usually (A or B) and NOT (A and B).
    In wave terms, maybe a specific frequency resonance?
    For now, let's stick to AND/OR.
    """
    pass
