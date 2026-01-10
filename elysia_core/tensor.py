from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .math_utils import Quaternion, Rotor


@dataclass
class SoulTensor:
    """
    Tensor3D: The Unified Field of Existence.

    Now integrated with Rotor dynamics for Gyroscopic Orientation.
    """

    amplitude: float  # Body: Mass
    frequency: float  # Soul: Identity
    phase: float      # Spirit: Timing
    spin: float = 1.0 # Rifling
    polarity: float = 1.0 # Matter/Antimatter
    orientation: Quaternion = field(default_factory=Quaternion.identity) # Hypersphere Attitude
    is_collapsed: bool = False
    coherence: float = 1.0

    entangled_peers: List[SoulTensor] = field(default_factory=list, repr=False)
    superposition_states: List[Tuple[SoulTensor, float]] = field(default_factory=list, repr=False)

    def step(self, dt: float) -> None:
        if self.is_collapsed:
            return

        delta = self.frequency * dt
        self.phase += delta
        self.phase %= (2 * math.pi)

        decoherence_rate = 0.001 * (1 + self.amplitude * 0.01)
        self.coherence = max(0.0, self.coherence - decoherence_rate * dt)

        for peer in self.entangled_peers:
            if not peer.is_collapsed:
                peer.phase = self.phase

    def apply_rotor(self, rotor: Rotor) -> None:
        """
        Apply a geometric rotation (Torque) to the soul's orientation.
        Used for Phase Reconstruction from hardware sensors (Gyroscope).
        """
        # Quaternion rotation by rotor is complex in 4D.
        # Simplified: Convert Rotor to Quaternion representation and multiply.
        # Rotor(s, bxy, ...) -> Q(s, 0, 0, bxy) roughly for 2D plane rotation
        # We assume the rotor is compatible with our Quaternion multiplication.

        # Q_new = R * Q_old
        # Construct a rotation quaternion from the rotor scalars
        # This is a simplification. Real GA is R Q ~R.
        # Here we treat the rotor as a delta-rotation quaternion.
        rot_q = Quaternion(rotor.scalar, rotor.bivector_zx, rotor.bivector_yz, rotor.bivector_xy)
        self.orientation = rot_q * self.orientation

    def entangle(self, other: 'SoulTensor') -> None:
        if other not in self.entangled_peers:
            self.entangled_peers.append(other)
        if self not in other.entangled_peers:
            other.entangled_peers.append(self)

        avg_phase = (self.phase + other.phase) / 2
        self.phase = avg_phase
        other.phase = avg_phase

    def resonate(self, other: SoulTensor) -> Dict[str, Any]:
        delta_phase = abs(self.phase - other.phase)
        if delta_phase > math.pi:
            delta_phase = (2 * math.pi) - delta_phase

        resonance = math.cos(delta_phase)
        polarity_factor = self.polarity * other.polarity
        resonance *= polarity_factor

        freq_diff = abs(self.frequency - other.frequency)
        is_harmonic = freq_diff < (self.frequency * 0.1) if self.frequency != 0 else False

        interaction_type = "Neutral"
        if resonance > 0.5:
            interaction_type = "Constructive (Empathy/Love)"
        elif resonance < -0.5:
            interaction_type = "Destructive (Calm/Comfort)"
        else:
            interaction_type = "Complex (Tension/Beat)"

        return {
            "resonance": resonance,
            "delta_phase": delta_phase,
            "is_harmonic": is_harmonic,
            "type": interaction_type
        }

    def decode_emotion(self) -> str:
        if self.frequency < 20:
            base = "Deep Sorrow / Gravity (Blue)"
        elif 20 <= self.frequency < 50:
            base = "Peace / Trust (Green)"
        elif 50 <= self.frequency < 100:
            base = "Joy / Excitement (Yellow)"
        elif 100 <= self.frequency < 300:
            base = "Passion / Anger (Red)"
        else:
            base = "Transcendence / Anxiety (White/Violet)"

        if self.amplitude < 10:
            intensity = "Faint"
        elif 10 <= self.amplitude < 50:
            intensity = "Clear"
        elif 50 <= self.amplitude < 200:
            intensity = "Strong"
        else:
            intensity = "Overwhelming"

        return f"{intensity} {base}"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "amplitude": self.amplitude,
            "frequency": self.frequency,
            "phase": self.phase,
            "spin": self.spin,
            "polarity": self.polarity,
            "orientation": str(self.orientation),
            "is_collapsed": self.is_collapsed,
            "coherence": self.coherence,
            "emotion": self.decode_emotion()
        }
