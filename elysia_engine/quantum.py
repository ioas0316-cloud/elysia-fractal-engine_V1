from __future__ import annotations

import math
import random
from dataclasses import dataclass, asdict
from typing import Optional, Tuple


@dataclass
class QuantumDNA:
    """
    Represents the 'Wave Function' of an entity's consciousness.
    Replaces traditional static data with dynamic wave properties.
    """
    frequency: float  # The 'Nature' or 'Type' of the thought (Hz)
    phase: float      # The 'Timing' or 'Perspective' (Radians, 0-2pi)
    amplitude: float  # The 'Energy' or 'Confidence' of the thought
    spin: float = 0.5 # The 'Direction' or 'Polarity' (-1 to 1)

    def step(self, dt: float) -> None:
        """
        Evolve the wave over time.
        Phase rotates based on frequency: d(phi)/dt = omega
        """
        self.phase += self.frequency * dt
        self.phase %= (2 * math.pi)

    def interfere(self, other: QuantumDNA) -> Optional[QuantumDNA]:
        """
        Perform Quantum Crossover (Breeding).
        Returns a NEW QuantumDNA representing the Child (Interference Pattern),
        or None if the interaction was purely destructive (collapse).
        """
        # 1. Calculate Phase Difference
        delta_phase = abs(self.phase - other.phase)
        if delta_phase > math.pi:
            delta_phase = (2 * math.pi) - delta_phase

        # 2. Resonance Check (Constructive vs Destructive)
        # If phases are within 90 degrees (pi/2), we get constructive interference.
        # Cos(0) = 1 (Best), Cos(pi) = -1 (Worst)
        resonance_factor = math.cos(delta_phase)

        if resonance_factor < -0.5:
            # Destructive interference: No child, energy lost to entropy
            return None

        # 3. Child Generation
        # Frequency: Harmonic mixing + slight quantum jitter (mutation)
        # New Freq is roughly the average, but shifted by the resonance
        avg_freq = (self.frequency + other.frequency) / 2
        mutation = random.uniform(-0.1, 0.1) * avg_freq
        child_freq = avg_freq + mutation

        # Amplitude: Derived from parents' amplitudes scaled by resonance
        # Constructive interference boosts amplitude!
        # A_new = sqrt(A1^2 + A2^2 + 2*A1*A2*cos(delta))
        combined_amp = math.sqrt(
            self.amplitude**2 + other.amplitude**2 +
            2 * self.amplitude * other.amplitude * resonance_factor
        )
        # Normalize slightly to prevent infinite energy explosion, but allow growth
        child_amp = combined_amp * 0.8

        # Phase: Average phase
        child_phase = (self.phase + other.phase) / 2

        # Spin: Conservation of Angular Momentum? Or simple mix?
        child_spin = (self.spin + other.spin) / 2

        return QuantumDNA(
            frequency=child_freq,
            phase=child_phase,
            amplitude=child_amp,
            spin=child_spin
        )

    def decode_meaning(self) -> str:
        """
        Translates Frequency into a semantic 'Meme' concept.
        (A simplified spectrum of consciousness)
        """
        # Spectrum Definitions (Frequency Bands)
        if self.frequency < 10:
            return "Void (Stagnation)"
        elif 10 <= self.frequency < 30:
            return "Ice (Stability)"
        elif 30 <= self.frequency < 60:
            return "Water (Flow)"
        elif 60 <= self.frequency < 100:
            return "Fire (Passion)"
        elif 100 <= self.frequency < 200:
            return "Wind (Curiosity)"
        elif 200 <= self.frequency < 500:
            return "Lightning (Insight)"
        elif 500 <= self.frequency < 1000:
            return "Light (Wisdom)"
        else:
            return "Singularity (Transcendence)"

    def as_dict(self) -> dict:
        return {
            "frequency": self.frequency,
            "phase": self.phase,
            "amplitude": self.amplitude,
            "spin": self.spin,
            "meaning": self.decode_meaning()
        }
