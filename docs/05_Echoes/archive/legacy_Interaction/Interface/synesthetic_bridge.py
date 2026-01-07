"""
Synesthetic Bridge
==================
'Translating Meaning into Light'

This module is the core adapter for Semantic Rendering.
It listens to the "Sound" of a concept (WaveTensor) and translates it into "Light" (SDF Parameters).
"""

import math
import colorsys
from typing import Dict, Any, Tuple
from Core.Foundation.Wave.wave_tensor import WaveTensor

class SynestheticBridge:
    """
    The translator between the Auditory Domain (WaveTensor) and Visual Domain (SDF).
    """

    def translate(self, wave: WaveTensor) -> Dict[str, Any]:
        """
        Converts a WaveTensor into visual rendering parameters.
        """
        # 1. Analyze the Wave
        energy = wave.total_energy
        frequencies = wave.active_frequencies
        
        if not frequencies:
            return self._get_void_visuals()

        # Dominant Frequency (Pitch) -> Hue (Color)
        # We find the weighted average frequency
        weighted_freq_sum = 0.0
        total_amp = 0.0
        
        # Simple analysis of the first harmonic series for now
        # Ideally, we'd do a full FFT analysis, but we have the spectrum directly.
        for f, amp_complex in wave._spectrum.items():
            amp = abs(amp_complex)
            weighted_freq_sum += f * amp
            total_amp += amp
            
        dominant_freq = weighted_freq_sum / total_amp if total_amp > 0 else 0
        
        # 2. Map Properties
        hue = self._map_frequency_to_hue(dominant_freq)
        saturation = min(1.0, math.log(energy + 1.0) * 0.5) 
        brightness = min(1.0, energy * 0.2)
        
        # Dissonance Calculation ( Roughness / Entropy )
        # A pure sine wave is Smooth. A messy spectrum is Rough.
        dissonance = self._calculate_visual_dissonance(wave)
        
        # 3. Construct Visual Parameters (SDF World Format)
        return {
            "color": self._hsl_to_rgb(hue, 0.8, 0.5), # Base Color
            
            # Emotional SDF Parameters
            "valence": self._calculate_valence(dissonance), # -1 (Dissonant) to +1 (Consonant)
            "arousal": min(1.0, energy / 5.0),             # Energy = Excitement
            "dominance": min(1.0, total_amp / 2.0),        # Amplitude = Power
            
            # Direct Shader Controls (Overrides)
            "distortionAmount": dissonance * 2.0,          # Noise = Distortion
            "colorTemperature": (0.5 - dissonance) * 2.0,  # Harmony = Warm, Noise = Cold
            "gravityStrength": 1.0 + (energy * 0.1)        # High Meaning = High Gravity
        }

    def _map_frequency_to_hue(self, freq: float) -> float:
        """
        Maps Solfeggio/Audio frequencies to Visual Spectrum (0.0 - 1.0).
        Low Freq (Base) = Red/Warm
        High Freq (Spirit) = Violet/Cool
        """
        # Linear mapping for simplicity: 100Hz (Red) -> 1000Hz (Violet)
        # 432Hz ~ Green/Heart Chakra
        norm_freq = (freq - 100.0) / 900.0
        return max(0.0, min(1.0, norm_freq)) * 0.8 # Scale to avoid wrapping back to red too fast

    def _calculate_visual_dissonance(self, wave: WaveTensor) -> float:
        """
        Estimates visual noise based on spectral complexity.
        More frequencies = More noise (unless they are harmonic).
        """
        # Simplified: Ratio of (Total Energy / Dominant Component Energy)
        # Pure wave ratio ~ 1.0 -> Dissonance 0.0
        # White noise ratio >> 1.0 -> Dissonance 1.0
        
        if not wave._spectrum: return 0.0
        
        max_amp = 0.0
        for z in wave._spectrum.values():
            if abs(z) > max_amp: max_amp = abs(z)
            
        total = wave.total_energy # Sum of squares
        # Dissonance metric roughly
        if max_amp == 0: return 0.0
        
        # If one component dominates, ratio is low.
        complexity = len(wave._spectrum)
        dissonance = (complexity - 1) * 0.1
        return min(1.0, dissonance)

    def _calculate_valence(self, dissonance: float) -> float:
        """
        Low Dissonance = High Valence (Happy/Beautiful)
        High Dissonance = Low Valence (Sad/Ugly)
        """
        # Map 0.0 (Clean) -> 1.0
        # Map 1.0 (Noisy) -> -1.0
        return 1.0 - (dissonance * 2.0)

    def _hsl_to_rgb(self, h, s, l):
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (r, g, b)

    def _get_void_visuals(self):
        return {
            "color": (0,0,0),
            "valence": 0, "arousal": 0, "dominance": 0,
            "distortionAmount": 0, "colorTemperature": 0, "gravityStrength": 1.0
        }
