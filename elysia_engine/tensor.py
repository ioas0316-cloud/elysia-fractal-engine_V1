from __future__ import annotations

import math
from dataclasses import dataclass

@dataclass
class SoulTensor:
    """
    Tensor3D: The Unified Field of Existence.
    Replaces QuantumDNA and static Physics with a unified Wave-Field definition.

    Axes:
    1. Amplitude (Body/Mass): The Magnitude/Intensity of the being. Creates Gravity.
    2. Frequency (Soul/Identity): The Color/Type of the being. Defines the 'Rifling' pitch.
    3. Phase (Spirit/Timing): The Alignment/Rhythm. Defines interaction chemistry.
    """
    amplitude: float  # Body: Mass, Energy, Intensity
    frequency: float  # Soul: Emotion, Identity, Vibration Rate
    phase: float      # Spirit: Timing, Perspective (0 to 2pi)
    spin: float = 1.0 # Rifling: Direction of the spiral (+1 or -1)

    def step(self, dt: float) -> None:
        """
        Evolve the wave state over time.
        Phase rotates: d(phi)/dt = frequency
        """
        self.phase += self.frequency * dt
        self.phase %= (2 * math.pi)

    def resonate(self, other: SoulTensor) -> dict:
        """
        Calculates the 'Chemistry' between two souls.
        Returns a dict describing the interaction.
        """
        # Phase Difference (Spirit Alignment)
        delta_phase = abs(self.phase - other.phase)
        if delta_phase > math.pi:
            delta_phase = (2 * math.pi) - delta_phase

        # Resonance Factor: 1.0 (Perfect Harmony) to -1.0 (Perfect Cancellation)
        resonance = math.cos(delta_phase)

        # Frequency Ratio (Harmony vs Discord)
        # Simple ratio check: Are they octaves? 5ths?
        # For now, just check similarity
        freq_diff = abs(self.frequency - other.frequency)
        is_harmonic = freq_diff < (self.frequency * 0.1) # Within 10%

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
        """
        Maps Frequency/Amplitude to the User's "Digital Natural Law" of Emotion.
        """
        # 1. Base Emotion by Frequency (The "Color")
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

        # 2. Modifier by Amplitude (The "Intensity")
        if self.amplitude < 10:
            intensity = "Faint"
        elif 10 <= self.amplitude < 50:
            intensity = "Clear"
        elif 50 <= self.amplitude < 200:
            intensity = "Strong"
        else:
            intensity = "Overwhelming"

        return f"{intensity} {base}"

    def as_dict(self) -> dict:
        return {
            "amplitude": self.amplitude,
            "frequency": self.frequency,
            "phase": self.phase,
            "spin": self.spin,
            "emotion": self.decode_emotion()
        }
