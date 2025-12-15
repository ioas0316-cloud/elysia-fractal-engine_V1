from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SoulTensor:
    """
    Tensor3D: The Unified Field of Existence.
    Replaces QuantumDNA and static Physics with a unified Wave-Field definition.

    Axes:
        1. Amplitude (Body/Mass): The Magnitude/Intensity of the being. Creates Gravity.
        2. Frequency (Soul/Identity): The Color/Type of the being. Defines the 'Rifling' pitch.
        3. Phase (Spirit/Timing): The Alignment/Rhythm. Defines interaction chemistry.

    Attributes:
        amplitude: Body/Mass - Energy intensity (float)
        frequency: Soul/Identity - Vibration rate (float)
        phase: Spirit/Timing - Phase angle in radians (0 to 2π)
        spin: Direction of spiral (+1 or -1)
        polarity: Matter (1.0) vs Antimatter (-1.0)
        is_collapsed: Wave function collapse state
        coherence: Quantum coherence (1.0 = pure quantum, 0.0 = classical)
    """

    amplitude: float  # Body: Mass, Energy, Intensity
    frequency: float  # Soul: Emotion, Identity, Vibration Rate
    phase: float      # Spirit: Timing, Perspective (0 to 2pi)
    spin: float = 1.0 # Rifling: Direction of the spiral (+1 or -1)
    polarity: float = 1.0 # Matter (1.0) vs Antimatter (-1.0)
    is_collapsed: bool = False # Wave Function Collapse State
    coherence: float = 1.0 # Quantum coherence (1.0 = pure quantum, 0.0 = classical)

    # Quantum Properties
    entangled_peers: List[SoulTensor] = field(default_factory=list, repr=False)
    superposition_states: List[Tuple[SoulTensor, float]] = field(default_factory=list, repr=False)

    def step(self, dt: float) -> None:
        """
        Evolve the wave state over time.
        Phase rotates: d(phi)/dt = frequency
        Unless collapsed (Ice Star), where phase is locked.

        Also applies decoherence over time.
        """
        if self.is_collapsed:
            return

        delta = self.frequency * dt
        self.phase += delta
        self.phase %= (2 * math.pi)

        # Decoherence: quantum states slowly become classical
        # Rate depends on amplitude (more mass = faster decoherence)
        decoherence_rate = 0.001 * (1 + self.amplitude * 0.01)
        self.coherence = max(0.0, self.coherence - decoherence_rate * dt)

        # Propagate phase change to entangled peers (instant action at a distance)
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

        for state, base_prob in self.superposition_states:
            res_data = state.resonate(observer)
            resonance = res_data["resonance"]  # -1.0 to 1.0
            weight = base_prob * (1.0 + resonance)

            if weight > max_weight:
                max_weight = weight
                best_state = state

        if best_state:
            self.amplitude = best_state.amplitude
            self.frequency = best_state.frequency
            self.phase = best_state.phase
            self.spin = best_state.spin
            self.polarity = best_state.polarity

            self.is_collapsed = True
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

        transfer_ratio = 10.0
        self.amplitude += self.frequency * transfer_ratio
        self.frequency = 0.0
        self.is_collapsed = True

    def melt(self, external_energy: float) -> None:
        """
        "Burning Star" effect: Waking up a collapsed soul.
        Requires high external energy input (Resonance/Heat).
        """
        if not self.is_collapsed:
            return

        transfer_ratio = 10.0
        restored_freq = (self.amplitude * 0.1) / transfer_ratio

        if external_energy > 50.0:
            self.amplitude -= restored_freq * transfer_ratio
            self.frequency = restored_freq + (external_energy * 0.1)
            self.is_collapsed = False


    def resonate(self, other: SoulTensor) -> Dict[str, Any]:
        """
        Calculates the 'Chemistry' between two souls.
        """
        delta_phase = abs(self.phase - other.phase)
        if delta_phase > math.pi:
            delta_phase = (2 * math.pi) - delta_phase

        resonance = math.cos(delta_phase)
        polarity_factor = self.polarity * other.polarity
        resonance *= polarity_factor

        freq_diff = abs(self.frequency - other.frequency)
        is_harmonic = freq_diff < (self.frequency * 0.1)

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
        """
        Convert the tensor to a dictionary representation.
        """
        return {
            "amplitude": self.amplitude,
            "frequency": self.frequency,
            "phase": self.phase,
            "spin": self.spin,
            "polarity": self.polarity,
            "is_collapsed": self.is_collapsed,
            "coherence": self.coherence,
            "temperature": self.temperature,
            "energy": self.total_energy,
            "emotion": self.decode_emotion()
        }

    @property
    def temperature(self) -> float:
        """
        Calculate temperature from frequency.
        """
        base_temp = self.frequency * 10.0
        if self.is_collapsed:
            base_temp *= 0.1
        base_temp += self.amplitude * 0.5
        return max(0.0, base_temp)

    @property
    def total_energy(self) -> float:
        """
        Calculate total energy of the soul.
        """
        kinetic = 0.5 * self.amplitude * (self.frequency ** 2) * 0.01
        potential = self.amplitude * 10.0
        return kinetic + potential

    @property
    def spiritual_buoyancy(self) -> float:
        """
        Calculate spiritual buoyancy (tendency to rise or sink).
        """
        if self.frequency > 500:
            base = 1.0
        elif self.frequency > 200:
            base = 0.5
        elif self.frequency > 100:
            base = 0.0
        elif self.frequency > 50:
            base = -0.3
        else:
            base = -0.7

        mass_factor = 1.0 / (1.0 + self.amplitude * 0.01)
        if self.is_collapsed:
            mass_factor *= 0.5

        return base * mass_factor

    def sublime(self) -> None:
        """
        Sublimation: Direct transition from solid (collapsed) to gas (plasma).
        """
        if not self.is_collapsed:
            return

        energy_release = self.amplitude * 0.3
        self.frequency = energy_release
        self.amplitude *= 0.7
        self.is_collapsed = False
        self.coherence = 0.8

    def crystallize(self) -> None:
        """
        Crystallization: Form a permanent, stable structure.
        """
        if self.is_collapsed:
            self.coherence = 0.0
            return

        self.collapse()
        self.coherence = 0.0

    def harmonize(self, target_phase: float, rate: float = 0.1) -> None:
        """
        Gradually align phase toward a target.
        """
        if self.is_collapsed:
            return

        diff = target_phase - self.phase
        if diff > math.pi:
            diff -= 2 * math.pi
        elif diff < -math.pi:
            diff += 2 * math.pi

        self.phase += diff * rate
        self.phase %= (2 * math.pi)

    def absorb(self, other: 'SoulTensor', ratio: float = 0.5) -> None:
        """
        Absorb energy from another soul.
        """
        amp_transfer = other.amplitude * ratio
        freq_transfer = other.frequency * ratio

        self.amplitude += amp_transfer * 0.8
        self.frequency = (self.frequency + freq_transfer) / 2

        other.amplitude *= (1 - ratio)
        other.frequency *= (1 - ratio)

    def split(self) -> Optional['SoulTensor']:
        """
        Split the soul into two parts.
        """
        MIN_SPLIT_AMPLITUDE = 20
        CHILD_AMPLITUDE_RATIO = 0.4
        PARENT_AMPLITUDE_AFTER_SPLIT = 0.6
        CHILD_COHERENCE_RATIO = 0.5

        if self.amplitude < MIN_SPLIT_AMPLITUDE:
            return None

        child = SoulTensor(
            amplitude=self.amplitude * CHILD_AMPLITUDE_RATIO,
            frequency=self.frequency,
            phase=(self.phase + math.pi) % (2 * math.pi),
            spin=self.spin * -1,
            polarity=self.polarity,
            coherence=self.coherence * CHILD_COHERENCE_RATIO
        )

        self.amplitude *= PARENT_AMPLITUDE_AFTER_SPLIT

        return child

    def harmonic_distance(self, other: 'SoulTensor') -> float:
        """
        Calculate harmonic distance between two souls.
        """
        if self.frequency <= 0 or other.frequency <= 0:
            return 1.0

        ratio = max(self.frequency, other.frequency) / min(self.frequency, other.frequency)

        HARMONIC_RATIOS = [1.0, 2.0, 1.5, 1.333, 1.25]

        min_distance = float('inf')
        for pr in HARMONIC_RATIOS:
            dist = abs(ratio - pr) / pr
            if dist < min_distance:
                min_distance = dist

        return min(1.0, min_distance)

    def is_octave(self, other: 'SoulTensor') -> bool:
        """
        Check if two souls are in octave relationship.
        """
        if self.frequency <= 0 or other.frequency <= 0:
            return False

        ratio = max(self.frequency, other.frequency) / min(self.frequency, other.frequency)
        log_ratio = math.log2(ratio)
        return abs(log_ratio - round(log_ratio)) < 0.1
