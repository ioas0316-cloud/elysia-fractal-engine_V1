"""
Texture Mapper: The Physics of Incarnation
------------------------------------------
"Data has value. Reality has texture."

This module converts abstract Wave properties (Frequency, Amplitude, Spin)
into physical sensations (Roughness, Density, Temperature).

Mappings:
- Frequency (Hz) -> Roughness (Surface Texture)
- Amplitude (0-1) -> Density (Solid vs Ghost)
- Spin (Quaternion) -> Temperature (Emotional Heat)
"""

import math
from dataclasses import dataclass
from Core.Foundation.hyper_quaternion import Quaternion

@dataclass
class PhysicalTexture:
    roughness: float  # 0.0 (Silk) -> 1.0 (Sandpaper)
    density: float    # 0.0 (Mist) -> 1.0 (Iron)
    temperature: float # 0.0 (Ice) -> 1.0 (Fire)

    def describe(self) -> str:
        r_desc = "Smooth" if self.roughness < 0.3 else "Rough" if self.roughness > 0.7 else "Textured"
        d_desc = "Ethereal" if self.density < 0.3 else "Solid" if self.density > 0.7 else "Fluid"
        t_desc = "Cold" if self.temperature < 0.3 else "Hot" if self.temperature > 0.7 else "Warm"
        return f"[{t_desc} {d_desc} {r_desc}]"

class TextureMapper:
    def map_to_texture(self, frequency: float, mass: float, spin: Quaternion) -> PhysicalTexture:
        """
        Incarnates a spirit (Orb properties) into a body (Texture).
        """
        # 1. Frequency -> Roughness
        # High frequency = Fine detail/Roughness. Low frequency = Smooth waves.
        # Normalize 0-1000Hz to 0-1
        norm_freq = min(max(frequency / 1000.0, 0.0), 1.0)
        roughness = norm_freq

        # 2. Mass/Amplitude -> Density
        # More energy = More solid
        # Logarithmic scale to handle wide dynamic range
        density = min(math.log(mass + 1.0) / 5.0, 1.0)

        # 3. Spin -> Temperature
        # We use the "Action" component (x, y, z magnitude) vs "Rest" (w)
        # High movement (x,y,z) = Hot. High stability (w) = Cold/Calm.
        # Vector magnitude of imaginary parts
        action_magnitude = math.sqrt(spin.x**2 + spin.y**2 + spin.z**2)
        temperature = min(action_magnitude, 1.0)

        return PhysicalTexture(roughness, density, temperature)
