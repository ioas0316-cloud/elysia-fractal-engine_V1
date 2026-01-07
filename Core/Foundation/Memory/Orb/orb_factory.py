"""
OrbFactory: The Alchemy of Memory
---------------------------------
"To freeze a moment is not to kill it, but to seal its soul."

This module implements the "Quantum Cycle" (Wave <-> Particle Transformation).
It synthesizes three ancient technologies:
1. Fractal Quantization (Noise Filtering)
2. Holographic Embedding (Data Binding)
3. Tesseract Geometry (Dimensional Folding)
"""

import math
import numpy as np
from typing import Tuple, Dict, Any, List, Optional
import logging

from Core.Foundation.Memory.holographic_embedding import HolographicEmbedder as HolographicEmbedding
from Core.Foundation.hyper_quaternion import Quaternion as HyperQuaternion
from Core.Foundation.Memory.Orb.hyper_resonator import HyperResonator

# Configure logger
logger = logging.getLogger("OrbFactory")

class OrbFactory:
    def __init__(self):
        # Tools
        self.hologram = HolographicEmbedding(compressed_dim=64)
        logger.info("🔮 OrbFactory initialized: Ready to crystallize moments.")

    def analyze_wave(self, wave: List[float]) -> float:
        """
        Calculates the dominant frequency of a wave vector.
        """
        arr = self._normalize_vector(wave, 64)
        # FFT
        spectrum = np.abs(np.fft.fft(arr))
        # Weighted average of indices
        total_energy = np.sum(spectrum)
        if total_energy > 0:
            freq_center = np.average(np.arange(len(spectrum)), weights=spectrum)
            # Map 0-64 index to 400-800Hz audible range
            return 400.0 + (freq_center * 6.0)
        return 0.0

    def freeze(self, name: str, data_wave: List[float], emotional_wave: List[float]) -> HyperResonator:
        """
        [Wave -> Particle]
        Compresses a temporal experience into a static Memory Orb.
        """
        # 1. Validation & Preprocessing
        if not data_wave:
            data_wave = [0.0] * 64
        if not emotional_wave:
            emotional_wave = [0.0] * 64

        clean_data = self._normalize_vector(data_wave, 64)
        clean_emotion = self._normalize_vector(emotional_wave, 64)

        # 2. Holographic Binding (Synthesis)
        bound_essence = self.hologram.encode(clean_data, clean_emotion)

        # 3. Dimensional Folding (Spin Calculation)
        mass = float(np.sum(np.abs(bound_essence)))

        # Calculate Frequency
        # Philosophy Update: The Orb's frequency should match the EMOTIONAL KEY that unlocks it.
        # If we use the bound essence frequency, we can only unlock it if we guess the bound frequency (which depends on data).
        # But we want to recall "Sad memories" (Key=Sadness) regardless of the data content.
        # So, the Orb's broadcast frequency should be dominated by the Emotion Wave.

        # spectrum = np.abs(bound_essence)
        # INSTEAD, we analyze the clean_emotion directly to set the "Listening Channel"
        emotion_spectrum = np.abs(np.fft.fft(clean_emotion))
        if np.sum(emotion_spectrum) > 0:
            freq_center = np.average(np.arange(len(emotion_spectrum)), weights=emotion_spectrum)
            frequency = 400.0 + (freq_center * 6.0)
        else:
            frequency = 0.0

        coeffs = np.abs(bound_essence)[:4]
        if len(coeffs) < 4:
            coeffs = np.pad(coeffs, (0, 4-len(coeffs)))

        spin = HyperQuaternion(
            w=float(coeffs[0]),
            x=float(coeffs[1]),
            y=float(coeffs[2]),
            z=float(coeffs[3])
        )
        spin.normalize()

        # 4. Crystallization
        orb = HyperResonator(
            name=name,
            frequency=frequency,
            mass=mass,
            quaternion=spin
        )

        orb.memory_content["hologram"] = bound_essence.tolist()
        orb.memory_content["raw_data"] = clean_data.tolist()

        logger.debug(f"❄️ Frozen '{name}': Freq={frequency:.1f}Hz, Mass={mass:.2f}")
        return orb

    def melt(self, orb: HyperResonator, trigger_key: List[float]) -> Dict[str, Any]:
        """
        [Particle -> Wave]
        Resurrects the memory using a "Key" (Trigger).
        """
        if "hologram" not in orb.memory_content:
            return {"error": "Orb is empty", "resonance_intensity": 0.0}

        bound_essence = np.array(orb.memory_content["hologram"])
        key_wave = self._normalize_vector(trigger_key, 64)

        decoded_wave = self.hologram.decode(bound_essence, key_wave)

        return {
            "recalled_wave": decoded_wave.tolist(),
            "resonance_intensity": orb.state.amplitude
        }

    def _normalize_vector(self, vec: List[float], target_len: int) -> np.ndarray:
        """Helper to pad/trim/normalize vectors."""
        arr = np.array(vec)
        current_len = len(arr)

        if current_len < target_len:
            arr = np.pad(arr, (0, target_len - current_len))
        elif current_len > target_len:
            arr = arr[:target_len]

        return arr
