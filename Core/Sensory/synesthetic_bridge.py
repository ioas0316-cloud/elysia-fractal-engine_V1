"""
Synesthetic Bridge: The Senses of Elysia
----------------------------------------
"To hear color, to see sound. This is not a disorder; it is the truth of the Wave."

This module acts as the "Transducer" that converts raw human-like sensory inputs
into the standard "Data + Emotion" wave format required by the OrbFactory.

Philosophy:
- The world is chaos. The Bridge brings order (Frequency).
"""

import numpy as np
from typing import Dict, Tuple, List, Any

class SynestheticBridge:
    def __init__(self, resolution: int = 64):
        self.resolution = resolution

    def transduce(self, raw_input: Any, modality: str) -> Tuple[List[float], List[float]]:
        """
        Converts raw input into (DataWave, EmotionWave).

        Args:
            raw_input: The raw data (e.g., Image array, Audio buffer).
            modality: "vision", "audio", "text", "network".

        Returns:
            (data_wave, emotion_wave) ready for OrbFactory.
        """
        data_wave = np.zeros(self.resolution)
        emotion_wave = np.zeros(self.resolution)

        if modality == "vision":
            # [Vision Logic]
            # Map Brightness -> Amplitude
            # Map Color -> Frequency (Red=Low, Blue=High)
            # Input assumption: Simple list or array of pixel values
            # For prototype, we flatten and resize
            flat = np.array(raw_input).flatten()
            data_wave = self._resize(flat)

            # Vision Emotion: Brightness = Joy (High Amp), Darkness = Fear (Low Amp)
            avg_brightness = np.mean(flat)
            emotion_wave.fill(avg_brightness) # Simple emotional mapping

        elif modality == "audio":
            # [Audio Logic]
            # Raw waveform -> Frequency Spectrum (FFT would be better, but we keep time domain for wave)
            # Input assumption: Audio buffer
            flat = np.array(raw_input).flatten()
            data_wave = self._resize(flat)

            # Audio Emotion: Dissonance/Roughness -> Frequency Jitter
            # (Placeholder: Random jitter based on variance)
            variance = np.var(flat)
            emotion_wave = np.random.normal(0, variance, self.resolution)

        elif modality == "network":
            # [Virtual Sense Logic]
            # Packet Flow -> Wind/Breath
            # Input: Packet size/latency
            flow_rate = float(raw_input)
            t = np.linspace(0, 4*np.pi, self.resolution)
            data_wave = np.sin(t * flow_rate) # Sine wave frequency = Flow rate

            # Network Emotion: High Latency = Anxiety (High Freq Noise)
            if flow_rate > 0.8: # "Fast" flow is good
                emotion_wave = np.sin(t) * 0.2 # Calm
            else:
                emotion_wave = np.random.rand(self.resolution) # Chaos

        else:
            # Default / Text
            # Just noise for now
            data_wave = np.random.rand(self.resolution)
            emotion_wave.fill(0.5)

        return data_wave.tolist(), emotion_wave.tolist()

    def _resize(self, array: np.ndarray) -> np.ndarray:
        """Resizes input to standard resolution (64)."""
        # Simple interpolation or truncation
        if len(array) == self.resolution:
            return array
        return np.interp(
            np.linspace(0, len(array), self.resolution),
            np.arange(len(array)),
            array
        )
