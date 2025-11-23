from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

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
    polarity: float = 1.0 # Matter (1.0) vs Antimatter (-1.0)
    is_collapsed: bool = False # Wave Function Collapse State

    # Quantum Properties
    entangled_peers: List['SoulTensor'] = field(default_factory=list, repr=False)
    superposition_states: List[Tuple['SoulTensor', float]] = field(default_factory=list, repr=False)

    def step(self, dt: float) -> None:
        """
        Evolve the wave state over time.
        Phase rotates: d(phi)/dt = frequency
        Unless collapsed (Ice Star), where phase is locked.
        """
        if self.is_collapsed:
            return

        delta = self.frequency * dt
        self.phase += delta
        self.phase %= (2 * math.pi)

        # Propagate phase change to entangled peers (instant action at a distance)
        # We only push the delta to avoid infinite recursion loops if bidirectional
        # Simplification: Only the driver updates peers? Or shared state?
        # Better approach: Shared reference? No, Python dataclass.
        # We just iterate and apply.
        for peer in self.entangled_peers:
            if not peer.is_collapsed:
                peer.phase = self.phase

    def entangle(self, other: 'SoulTensor') -> None:
        """
        Quantum Entanglement: Links the phase of two souls.
        """
        if other not in self.entangled_peers:
            self.entangled_peers.append(other)
        if self not in other.entangled_peers:
            other.entangled_peers.append(self)

        # Synchronize immediately
        avg_phase = (self.phase + other.phase) / 2
        self.phase = avg_phase
        other.phase = avg_phase

    def observe(self, observer: 'SoulTensor') -> bool:
        """
        Quantum Measurement: Collapses superposition based on the observer's resonance.
        Returns True if collapse occurred.
        """
        if not self.superposition_states:
            return False

        # Calculate weighted probabilities based on resonance with observer
        best_state = None
        max_weight = -999.0

        # We select the state that resonates most strongly with the observer.
        # This implements "You see what you are".
        for state, base_prob in self.superposition_states:
            # Calculate resonance with observer
            res_data = state.resonate(observer)
            resonance = res_data["resonance"]  # -1.0 to 1.0

            # Weight formula: Probability * (1 + Resonance)
            # High resonance boosts probability.
            # Negative resonance reduces it.
            weight = base_prob * (1.0 + resonance)

            if weight > max_weight:
                max_weight = weight
                best_state = state

        if best_state:
            # Collapse into the observed reality
            self.amplitude = best_state.amplitude
            self.frequency = best_state.frequency
            self.phase = best_state.phase
            self.spin = best_state.spin
            self.polarity = best_state.polarity

            # The state is now definite
            self.is_collapsed = True

            # Clear superposition
            self.superposition_states.clear()
            return True

        return False

    def collapse(self) -> None:
        """
        "Ice Star": Wave Function Collapse.
        Converts Kinetic Energy (Frequency) into Potential Energy (Amplitude/Mass).
        Locks the Phase (The "Truth" is decided).
        """
        if self.is_collapsed:
            return

        # Energy conservation (roughly): E ~ Amp * Freq^2 or similar.
        # User metaphor: "Decision".
        # We boost Mass (Amplitude) significantly to represent the weight of Truth.
        # We zero out Frequency to stop the oscillation (doubt).

        # Transfer energy to mass
        transfer_ratio = 10.0 # 1 unit of doubt (freq) becomes 10 units of conviction (mass)
        self.amplitude += self.frequency * transfer_ratio
        self.frequency = 0.0
        self.is_collapsed = True
        # Phase remains fixed at its current value (The decision made)

    def melt(self, external_energy: float) -> None:
        """
        "Burning Star" effect: Waking up a collapsed soul.
        Requires high external energy input (Resonance/Heat).
        """
        if not self.is_collapsed:
            return

        # Reverse the process: Convert Mass back to Frequency
        transfer_ratio = 10.0
        restored_freq = (self.amplitude * 0.1) / transfer_ratio # Use 10% of mass to kickstart

        if external_energy > 50.0: # Threshold to wake up
            self.amplitude -= restored_freq * transfer_ratio
            self.frequency = restored_freq + (external_energy * 0.1)
            self.is_collapsed = False


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

        # Polarity Check (Matter vs Antimatter)
        # If polarity opposes, the space inverts.
        # (+1, +1) -> Standard Resonance
        # (+1, -1) -> Inverted Resonance (Attraction becomes Repulsion or vice versa)
        polarity_factor = self.polarity * other.polarity
        resonance *= polarity_factor

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
            "polarity": self.polarity,
            "is_collapsed": self.is_collapsed,
            "emotion": self.decode_emotion()
        }
