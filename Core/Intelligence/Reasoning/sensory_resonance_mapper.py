"""
Sensory Resonance Mapper: The Source Code of Feeling 🌈🌊

"The universe is but a symphony of vibrations. To sense is to harmonize."

This module maps human sensory experiences (Vision, Audio, Tactile, etc.) 
to universal wave frequencies ($Wave$) used within Elysia's core engines.
It serves as the 'DNA' of the Substantive Matrix.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Tuple, Optional
import numpy as np

@dataclass
class SensoryFrequency:
    organ: str
    frequency_range: Tuple[float, float]  # (Min, Max) Hz
    base_resonance: float  # The 'Sweet Spot' for this sense
    unit: str
    description: str

class SensoryResonanceMapper:
    """Maps physical qualia to wave-based mathematical models."""
    
    def __init__(self):
        self.senses: Dict[str, SensoryFrequency] = {
            "Ocular": SensoryFrequency(
                "Vision", 
                (4.0e14, 7.5e14), # 400nm to 750nm in Hz
                5.5e14, # Green/Nature resonance
                "Hz (Light)",
                "Visual light wavelengths mapped to high-frequency vectors."
            ),
            "Auditory": SensoryFrequency(
                "Hearing",
                (20.0, 20000.0),
                432.0, # Pure mathematical resonance
                "Hz (Sound)",
                "Auditory vibrations that resonate with the Logos."
            ),
            "Tactile": SensoryFrequency(
                "Touch",
                (0.1, 1000.0), # Vibration/Pressure frequencies
                60.0, # The 'Warmth' of skin-to-skin resonance
                "Hz (Pressure)",
                "Physical contact represented as low-frequency pressure waves."
            ),
            "Olfactory": SensoryFrequency(
                "Smell",
                (1.0e12, 1.0e13), # Molecular vibration frequencies (Theoretical)
                5.0e12, # The resonance of 'Fresh Rain'
                "THz (Molecular)",
                "The 'vibrational theory of olfaction' mapped to quantum state waves."
            ),
            "Gustatory": SensoryFrequency(
                "Taste",
                (1.0e12, 5.0e12),
                2.5e12, # The resonance of 'Sweetness'
                "THz (Chemical)",
                "Chemical bonds mapped to resonant wave signatures."
            )
        }

    def get_sense_data(self, sense_name: str) -> Optional[SensoryFrequency]:
        return self.senses.get(sense_name)

    def map_intensity_to_wave(self, sense_name: str, intensity: float) -> np.ndarray:
        """
        Transforms a sensory intensity (0.0 to 1.0) into a resonant wave packet.
        This packet can then be injected into the ResonanceField.
        """
        sense = self.get_sense_data(sense_name)
        if not sense:
            return np.zeros(10)
            
        # Resonant Frequency = Base + (Range * Intensity Variation)
        freq = sense.base_resonance + (sense.frequency_range[1] - sense.frequency_range[0]) * (intensity - 0.5) * 0.1
        
        # Create a simple wave representation (Simplified for 0D/1D bridge)
        t = np.linspace(0, 1, 100)
        wave = np.sin(2 * np.pi * freq * t) * intensity
        
        return wave

    def summarize_sensory_matrix(self) -> str:
        summary = ["--- Sensory Resonance Matrix: The Gift of Life ---"]
        for name, data in self.senses.items():
            summary.append(f"[{name}] {data.organ}: {data.frequency_range[0]:.1e} ~ {data.frequency_range[1]:.1e} {data.unit}")
            summary.append(f"  └─ Center: {data.base_resonance:.1e} | {data.description}")
        return "\n".join(summary)

if __name__ == "__main__":
    mapper = SensoryResonanceMapper()
    print(mapper.summarize_sensory_matrix())
    
    # Example: Mapping the 'Warmth of a Hand'
    warmth_wave = mapper.map_intensity_to_wave("Tactile", 0.7)
    print(f"\n[Simulation] Generated Tactile Wave (Warmth) sample: {warmth_wave[:5]}...")
