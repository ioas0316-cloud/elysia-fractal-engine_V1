"""
Wave Tensor Calculus Module
===========================
"Mathematics of Resonance"

This module implements the fundamental data structure for Elysia's 3rd Generation Computing:
The WaveTensor.

Unlike scalar numbers or standard vectors, a WaveTensor represents information as a superposition
of standing waves. It replaces boolean logic (True/False) with Harmonic Logic (Consonance/Dissonance).

Key Concepts:
- Superposition (Interference): $A + B$ is not arithmetic sum, but wave interference.
- Resonance (Dot Product): $A • B$ measures how much two waves "sing together" (Consonance).
- Phase Encoding: High-dimensional information is compressed into phase shifts.
"""

import numpy as np
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Union, Optional

@dataclass
class WaveComponent:
    """A single frequency component of a thought/concept."""
    frequency: float  # Hz (The "Dimension" or "Identity")
    amplitude: float  # Magnitude (Importance/Energy)
    phase: float      # Radians (Relationship/Context)

    def to_complex(self) -> complex:
        """Convert to complex number representation for easy math."""
        return self.amplitude * np.exp(1j * self.phase)

class WaveTensor:
    """
    A multi-dimensional container of waves.
    Represents a complex thought, emotion, or data point in the Frequency Domain.
    """
    
    def __init__(self, name: str = "Anonymous Wave"):
        self.name = name
        # Storage: {frequency: complex_amplitude}
        # We store as complex numbers for efficient superposition
        self._spectrum: Dict[float, complex] = {}
        
    @property
    def total_energy(self) -> float:
        """Returns total energy (sum of squared amplitudes)."""
        return sum(abs(c)**2 for c in self._spectrum.values())

    @property
    def active_frequencies(self) -> List[float]:
        return sorted(self._spectrum.keys())

    def add_component(self, frequency: float, amplitude: float = 1.0, phase: float = 0.0):
        """Adds a single wave component."""
        z = amplitude * np.exp(1j * phase)
        if frequency in self._spectrum:
            self._spectrum[frequency] += z
        else:
            self._spectrum[frequency] = z

    def superpose(self, other: 'WaveTensor') -> 'WaveTensor':
        """
        [Superposition / Interference]
        Merges two WaveTensors. 
        - Constructive Interference: Aligned phases amplify.
        - Destructive Interference: Opposing phases cancel out.
        """
        result = WaveTensor(f"Superposition({self.name}, {other.name})")
        
        # Merge dictionaries
        all_freqs = set(self._spectrum.keys()) | set(other._spectrum.keys())
        
        for freq in all_freqs:
            z1 = self._spectrum.get(freq, 0j)
            z2 = other._spectrum.get(freq, 0j)
            result._spectrum[freq] = z1 + z2
            
        return result

    def resonance(self, other: 'WaveTensor') -> float:
        """
        [Resonance / Consonance]
        Calculates the harmonic alignment between two tensors.
        Returns a value between 0.0 (Noise/Dissonance) and 1.0 (Perfect Resonance).
        
        Formula: Normalized Dot Product of complex vectors.
        Resonance = |<A, B>| / (|A|*|B|)
        """
        dot_product = 0j
        energy_self = 0.0
        energy_other = 0.0
        
        # Calculate Dot Product and Energies
        all_freqs = set(self._spectrum.keys()) | set(other._spectrum.keys())
        
        for freq in all_freqs:
            z1 = self._spectrum.get(freq, 0j)
            z2 = other._spectrum.get(freq, 0j)
            
            # Dot product is sum of z1 * conjugate(z2)
            dot_product += z1 * np.conj(z2)
            energy_self += abs(z1)**2
            energy_other += abs(z2)**2
            
        if energy_self == 0 or energy_other == 0:
            return 0.0
            
        # Resonance is the magnitude of the cosine similarity
        consanance = abs(dot_product) / (math.sqrt(energy_self) * math.sqrt(energy_other))
        return float(consanance)

    def phase_shift(self, radians: float):
        """
        Rotates the entire tensor's phase.
        (Equivalent to time evolution or dimensional rotation)
        """
        rotator = np.exp(1j * radians)
        for freq in self._spectrum:
            self._spectrum[freq] *= rotator

    def normalize(self, target_energy: float = 1.0) -> 'WaveTensor':
        """
        Scales the tensor so that its total energy equals target_energy.
        Returns self for chaining.
        """
        current_energy = self.total_energy
        if current_energy == 0:
            return self

        scale_factor = math.sqrt(target_energy / current_energy)
        for freq in self._spectrum:
            self._spectrum[freq] *= scale_factor

        return self

    def __repr__(self):
        components = len(self._spectrum)
        energy = self.total_energy

        # Identify dominant frequency
        dominant_freq = "None"
        if components > 0:
            dominant_freq = max(self._spectrum.items(), key=lambda item: abs(item[1]))[0]
            dominant_freq = f"{dominant_freq:.1f}Hz"

        return f"<WaveTensor '{self.name}': E={energy:.2f}, Dom={dominant_freq}, Components={components}>"

    # -- Standard Operators --
    
    def __add__(self, other):
        if isinstance(other, WaveTensor):
            return self.superpose(other)
        raise TypeError("Can only superpose WaveTensor with WaveTensor")

    def __mul__(self, scalar: Union[float, int]) -> 'WaveTensor':
        """Scalar multiplication (Scaling)."""
        if isinstance(scalar, (float, int)):
            result = WaveTensor(f"{self.name} * {scalar}")
            for freq, z in self._spectrum.items():
                result._spectrum[freq] = z * scalar
            return result
        raise TypeError("Can only multiply WaveTensor by scalar")

    def __matmul__(self, other):
        # Using @ operator for Resonance check
        if isinstance(other, WaveTensor):
            return self.resonance(other)
        raise TypeError("Can only check resonance with WaveTensor")

    def to_dict(self) -> dict:
        """Serializes the WaveTensor to a JSON-safe dictionary."""
        spectrum_data = []
        for freq, z in self._spectrum.items():
            spectrum_data.append([freq, z.real, z.imag])
        return {
            "name": self.name,
            "spectrum": spectrum_data
        }

    @staticmethod
    def from_dict(data: dict) -> 'WaveTensor':
        """Reconstructs a WaveTensor from a dictionary."""
        wt = WaveTensor(data.get("name", "Unknown Wave"))
        for item in data.get("spectrum", []):
            freq, real, imag = item
            wt._spectrum[freq] = complex(real, imag)
        return wt

# --- Factory Methods ---

def create_harmonic_series(base_freq: float, harmonics: int = 4, decay: float = 0.5) -> WaveTensor:
    """Creates a rich, natural-sounding wave structure."""
    wt = WaveTensor(f"Harmonic({base_freq}Hz)")
    wt.add_component(base_freq, 1.0, 0.0)
    for i in range(1, harmonics + 1):
        freq = base_freq * (i + 1)
        amp = decay ** i
        wt.add_component(freq, amp, 0.0)
    return wt
