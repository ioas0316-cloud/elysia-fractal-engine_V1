from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from elysia_engine.math_utils import Quaternion


@dataclass
class SoulTensor:
    """
    Tensor3D: The Unified Field of Existence.
    Replaces QuantumDNA and static Physics with a unified Wave-Field definition.

    Axes:
        1. Amplitude (Body/Mass): The Magnitude/Intensity of the being. Creates Gravity.
        2. Frequency (Soul/Identity): The Color/Type of the being. Defines the 'Rifling' pitch.
        3. Phase (Spirit/Timing): The Alignment/Rhythm. Defines interaction chemistry.
    
    New Axis (Hypersphere Decoupling):
        4. Orientation (Hypersphere): The 'Attitude' or 'Facing' of the soul.
           Determines the Intent Vector (Volition) separate from Position.

    Additional Properties:
        - Coherence: Quantum coherence (0-1), how "quantum" vs "classical" the state is
        - Temperature: Derived from frequency, used for thermodynamic calculations
    
    Attributes:
        amplitude: Body/Mass - Energy intensity (float)
        frequency: Soul/Identity - Vibration rate (float)
        phase: Spirit/Timing - Phase angle in radians (0 to 2π)
        spin: Direction of spiral (+1 or -1)
        polarity: Matter (1.0) vs Antimatter (-1.0)
        orientation: The facing direction of the soul (Quaternion)
        is_collapsed: Wave function collapse state
        coherence: Quantum coherence (1.0 = pure quantum, 0.0 = classical)
    """
    
    amplitude: float  # Body: Mass, Energy, Intensity
    frequency: float  # Soul: Emotion, Identity, Vibration Rate
    phase: float      # Spirit: Timing, Perspective (0 to 2pi)
    spin: float = 1.0 # Rifling: Direction of the spiral (+1 or -1)
    polarity: float = 1.0 # Matter (1.0) vs Antimatter (-1.0)
    orientation: Quaternion = field(default_factory=Quaternion.identity) # Hypersphere Orientation
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
            self.orientation = best_state.orientation

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


    def resonate(self, other: SoulTensor) -> Dict[str, Any]:
        """
        Calculates the 'Chemistry' between two souls.
        
        Args:
            other: The other SoulTensor to resonate with
            
        Returns:
            Dictionary describing the interaction with keys:
                - resonance: float (-1.0 to 1.0)
                - delta_phase: float
                - is_harmonic: bool
                - type: str
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

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert the tensor to a dictionary representation.
        
        Returns:
            Dictionary with all tensor properties
        """
        return {
            "amplitude": self.amplitude,
            "frequency": self.frequency,
            "phase": self.phase,
            "spin": self.spin,
            "polarity": self.polarity,
            "orientation": str(self.orientation),
            "is_collapsed": self.is_collapsed,
            "coherence": self.coherence,
            "temperature": self.temperature,
            "energy": self.total_energy,
            "emotion": self.decode_emotion()
        }

    # ==================== Energy & Temperature Properties ====================

    @property
    def temperature(self) -> float:
        """
        Calculate temperature from frequency.
        
        Temperature represents the internal kinetic energy of the soul.
        Higher frequency = higher temperature = more active state.
        
        Returns:
            Temperature value (conceptual, not physical units)
        """
        # Base temperature from frequency
        base_temp = self.frequency * 10.0
        
        # Collapsed souls have reduced temperature
        if self.is_collapsed:
            base_temp *= 0.1
        
        # Amplitude adds some heat (more mass = more potential energy)
        base_temp += self.amplitude * 0.5
        
        return max(0.0, base_temp)

    @property
    def total_energy(self) -> float:
        """
        Calculate total energy of the soul.
        
        E = amplitude * frequency^2 (analogous to kinetic energy)
        Plus potential energy from amplitude (mass-energy equivalence)
        
        Returns:
            Total energy value
        """
        kinetic = 0.5 * self.amplitude * (self.frequency ** 2) * 0.01
        potential = self.amplitude * 10.0  # Mass-energy
        return kinetic + potential

    @property
    def spiritual_buoyancy(self) -> float:
        """
        Calculate spiritual buoyancy (tendency to rise or sink).
        
        High frequency = rise (ethereal, light)
        Low frequency = sink (grounded, heavy)
        
        Returns:
            Buoyancy value (-1 to 1, negative = sinks, positive = rises)
        """
        # Frequency determines base buoyancy
        if self.frequency > 500:
            base = 1.0  # Transcendent, rising
        elif self.frequency > 200:
            base = 0.5  # Elevated
        elif self.frequency > 100:
            base = 0.0  # Neutral
        elif self.frequency > 50:
            base = -0.3  # Slight gravity
        else:
            base = -0.7  # Heavy, sinking
        
        # Amplitude affects buoyancy (more mass = harder to rise)
        mass_factor = 1.0 / (1.0 + self.amplitude * 0.01)
        
        # Collapsed souls are heavier
        if self.is_collapsed:
            mass_factor *= 0.5
        
        return base * mass_factor

    # ==================== State Transition Methods ====================

    def sublime(self) -> None:
        """
        Sublimation: Direct transition from solid (collapsed) to gas (plasma).
        
        Requires significant energy input.
        Opposite of crystallization.
        """
        if not self.is_collapsed:
            return
        
        # Convert mass to energy (frequency)
        energy_release = self.amplitude * 0.3
        self.frequency = energy_release
        self.amplitude *= 0.7
        self.is_collapsed = False
        self.coherence = 0.8  # Partially restore quantum properties

    def crystallize(self) -> None:
        """
        Crystallization: Form a permanent, stable structure.
        
        Like collapse but more permanent.
        Represents achieving a final form/truth.
        """
        if self.is_collapsed:
            # Already collapsed, just strengthen
            self.coherence = 0.0  # Fully classical
            return
        
        # Full collapse with enhanced stability
        self.collapse()
        self.coherence = 0.0  # Fully classical (permanent)

    def harmonize(self, target_phase: float, rate: float = 0.1) -> None:
        """
        Gradually align phase toward a target.
        
        Used for synchronization without full entanglement.
        
        Args:
            target_phase: The phase to align toward
            rate: How fast to align (0-1)
        """
        if self.is_collapsed:
            return
        
        # Calculate shortest path to target phase
        diff = target_phase - self.phase
        if diff > math.pi:
            diff -= 2 * math.pi
        elif diff < -math.pi:
            diff += 2 * math.pi
        
        # Move toward target
        self.phase += diff * rate
        self.phase %= (2 * math.pi)

    def absorb(self, other: 'SoulTensor', ratio: float = 0.5) -> None:
        """
        Absorb energy from another soul.
        
        The absorber gains amplitude/frequency, donor loses.
        
        Args:
            other: The soul to absorb from
            ratio: Fraction of energy to transfer (0-1)
        """
        # Calculate transfer amounts
        amp_transfer = other.amplitude * ratio
        freq_transfer = other.frequency * ratio
        
        # Apply transfer
        self.amplitude += amp_transfer * 0.8  # 80% efficiency
        self.frequency = (self.frequency + freq_transfer) / 2  # Average
        
        # Donor loses energy
        other.amplitude *= (1 - ratio)
        other.frequency *= (1 - ratio)

    def split(self) -> Optional['SoulTensor']:
        """
        Split the soul into two parts.
        
        Creates a new soul with half the energy.
        Used for replication without a partner.
        
        Returns:
            The new split-off soul, or None if insufficient energy
        """
        # Minimum amplitude required for splitting
        MIN_SPLIT_AMPLITUDE = 20
        
        # Child inherits fraction of parent's properties
        CHILD_AMPLITUDE_RATIO = 0.4
        PARENT_AMPLITUDE_AFTER_SPLIT = 0.6
        # Child inherits half coherence because quantum state is partially disrupted by splitting
        CHILD_COHERENCE_RATIO = 0.5
        
        if self.amplitude < MIN_SPLIT_AMPLITUDE:
            return None  # Not enough energy to split
        
        # Create child with inherited properties
        child = SoulTensor(
            amplitude=self.amplitude * CHILD_AMPLITUDE_RATIO,
            frequency=self.frequency,
            phase=(self.phase + math.pi) % (2 * math.pi),  # Opposite phase
            spin=self.spin * -1,  # Opposite spin (conservation)
            polarity=self.polarity,
            orientation=self.orientation, # Inherit orientation
            coherence=self.coherence * CHILD_COHERENCE_RATIO
        )
        
        # Parent loses energy
        self.amplitude *= PARENT_AMPLITUDE_AFTER_SPLIT
        
        return child

    # ==================== Harmonic Analysis ====================

    def harmonic_distance(self, other: 'SoulTensor') -> float:
        """
        Calculate harmonic distance between two souls.
        
        Based on frequency ratios (musical harmony).
        
        Args:
            other: Soul to compare with
            
        Returns:
            Distance value (0 = perfect harmony, higher = more dissonant)
        """
        if self.frequency <= 0 or other.frequency <= 0:
            return 1.0
        
        # Calculate frequency ratio
        ratio = max(self.frequency, other.frequency) / min(self.frequency, other.frequency)
        
        # Perfect harmonic ratios from music theory:
        # - 1:1 = Unison (same pitch)
        # - 2:1 = Octave (doubling frequency)
        # - 3:2 = Perfect Fifth (1.5)
        # - 4:3 = Perfect Fourth (1.333...)
        # - 5:4 = Major Third (1.25)
        HARMONIC_RATIOS = [1.0, 2.0, 1.5, 1.333, 1.25]
        
        # Find closest perfect ratio
        min_distance = float('inf')
        for pr in HARMONIC_RATIOS:
            dist = abs(ratio - pr) / pr
            if dist < min_distance:
                min_distance = dist
        
        return min(1.0, min_distance)

    def is_octave(self, other: 'SoulTensor') -> bool:
        """
        Check if two souls are in octave relationship.
        
        Octaves are 2:1 frequency ratios.
        """
        if self.frequency <= 0 or other.frequency <= 0:
            return False
        
        ratio = max(self.frequency, other.frequency) / min(self.frequency, other.frequency)
        
        # Check if ratio is close to a power of 2
        log_ratio = math.log2(ratio)
        return abs(log_ratio - round(log_ratio)) < 0.1
