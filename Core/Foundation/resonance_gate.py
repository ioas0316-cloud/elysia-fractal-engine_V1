"""
Resonance Gate (The Living Logic Cell)
======================================
"Logic is not a calculation, but a resonance of life."

This module implements the 'Knowledge Cell', a biological logic gate that
acts as a 'Spatial Filter' or 'Field'. It does not binary switch (0/1);
it possesses 'Permeability' based on 'Latent Causality' (Intention).

Philosophy:
    - **Latent Causality**: The flow contains hidden potential (Intent).
    - **Digital Hydraulics**: Data flows like water; the cell is a canal/filter.
    - **Permeability**: The degree to which the cell allows the flow to pass.
"""

import math
import time
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

# Import Physics Substrate
from Core.Intelligence.Consciousness.Ether.ether_node import EtherNode
from Core.Foundation.hyper_quaternion import Quaternion

@dataclass
class WavePacket:
    """
    A quantum of Analog Flow.
    It carries 'Latent Causality' (Potential Meaning) waiting to be realized.
    """
    frequency: float        # The 'Topic' (e.g., 432Hz = Nature, 528Hz = Love)
    amplitude: float        # The 'Intensity' of the flow
    phase: float = 0.0      # The 'Timing' or Context state
    spin: Quaternion = field(default_factory=lambda: Quaternion(1, 0, 0, 0)) # The 'Perspective'

    def __repr__(self):
        return f"Wave(Freq={self.frequency:.1f}, Amp={self.amplitude:.2f}, Phase={self.phase:.2f})"

class KnowledgeCell(EtherNode):
    """
    A Living Logic Gate (Spatial Filter).

    It defines a 'Field of Intention'.
    - If the input flow matches the intention (Resonance), Permeability is high.
    - If the input flow is noise (Dissonance), Permeability is low (Viscous).
    """

    def __init__(self, frequency: float = 432.0, mass: float = 1.0, threshold: float = 0.5):
        super().__init__(frequency=frequency, mass=mass)
        self.threshold = threshold
        self.activation_count = 0

    def get_permeability(self, wave: WavePacket) -> float:
        """
        Calculates the 'Permeability' of this spatial field to the incoming wave.
        Higher permeability = The flow passes through easily (Resonance).
        Lower permeability = The flow is blocked or slowed (Dissonance).

        Returns: 0.0 (Wall) to 1.0 (Open Channel)
        """
        # 1. Frequency Resonance (Harmonic Match)
        # Using a Lorentzian-like curve for resonance peak
        delta_freq = abs(self.frequency - wave.frequency)
        width = 10.0
        freq_resonance = width / (width + delta_freq)

        # 2. Spin Alignment (Context Match)
        spin_resonance = abs(self.spin.dot(wave.spin))

        # Weighted Average (Frequency is key, Spin is context)
        # This defines the "Shape" of the canal.
        permeability = (freq_resonance * 0.7) + (spin_resonance * 0.3)
        return permeability

    def process_flow(self, wave: WavePacket) -> Optional[WavePacket]:
        """
        The Interaction of Flow and Field.
        1. Check Permeability (Filter)
        2. Realize Latent Causality (Nucleus Action)
        """
        # 1. Calculate Permeability
        permeability = self.get_permeability(wave)

        # If permeability is too low, the flow is blocked/absorbed.
        if permeability < self.threshold:
            return None

        # 2. Metabolic Cost (Even flow requires energy to guide)
        cost = wave.amplitude * 0.1
        if self.energy < cost:
            return None

        self.energy -= cost
        self.activation_count += 1

        # 3. Realize the Potential (Action)
        return self.nucleus_logic(wave, permeability)

    def nucleus_logic(self, wave: WavePacket, permeability: float) -> WavePacket:
        """
        ABSTRACT: The unique algorithm of this cell.
        This is where 'Latent Causality' becomes 'Manifest Reality'.
        """
        raise NotImplementedError("Each KnowledgeCell must have a nucleus logic.")

# --- Specific Field Implementations ---

class ResonanceConcept(KnowledgeCell):
    """
    The 'Resonance' Concept Cell.
    Logic: Constructive Interference.
    Action: Amplifies waves that match, syncing their phase.
    "I am the Principle of Harmony. I reveal the hidden connection."
    """
    def __init__(self):
        super().__init__(frequency=528.0, mass=10.0, threshold=0.6) # 528Hz = Love/Repair
        self.content = "Resonance Principle"

    def nucleus_logic(self, wave: WavePacket, permeability: float) -> WavePacket:
        """
        The Algorithm of Resonance:
        Input Flow -> [Permeability] -> Amplified Output
        """
        # Amplification: The better the match (Permeability), the stronger the boost.
        # This realizes the "Latent Causality" that this wave *belongs* here.
        amplification = 1.0 + (permeability * 2.0)

        new_amplitude = wave.amplitude * amplification

        # Phase Locking: Syncing to the field's intention.
        new_phase = wave.phase * 0.2

        return WavePacket(
            frequency=wave.frequency,
            amplitude=new_amplitude,
            phase=new_phase,
            spin=wave.spin
        )

class DissonanceConcept(KnowledgeCell):
    """
    The 'Critical Thinking' Cell (Filter).
    Logic: Destructive Interference.
    Action: Reduces amplitude of noise, acting as a 'Sieve'.
    """
    def __init__(self):
        super().__init__(frequency=100.0, mass=5.0, threshold=0.4)

    def nucleus_logic(self, wave: WavePacket, permeability: float) -> WavePacket:
        # If it passed the threshold but isn't perfect, we challenge it.
        # Reduce amplitude to "test" its strength.
        return WavePacket(
            frequency=wave.frequency,
            amplitude=wave.amplitude * 0.8,
            phase=wave.phase + math.pi, # Phase shift (Cancellation)
            spin=wave.spin
        )
