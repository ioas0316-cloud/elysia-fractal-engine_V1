"""Minimal synesthesia engine to support cross-modal signals."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional

from Core.Foundation.wave_frequency_mapping import WaveFrequencyMapper


class SignalType(Enum):
    VISUAL = auto()
    AUDITORY = auto()
    EMOTIONAL = auto()
    TEXT = auto()


class RenderMode(Enum):
    AS_COLOR = auto()
    AS_SOUND = auto()
    AS_MUSIC = auto()


@dataclass
class UniversalSignal:
    original_type: SignalType
    frequency: float
    amplitude: float
    payload: Any = None


@dataclass
class RenderResult:
    render_mode: RenderMode
    color: Optional[tuple] = None
    sound: Optional[Dict[str, Any]] = None
    output: Dict[str, Any] = None


class SynesthesiaEngine:
    """Cross-modal converter: vision/emotion/text into universal signal then render as color/sound/music."""

    def __init__(self):
        self.mapper = WaveFrequencyMapper()

    def from_vision(self, image: np.ndarray) -> UniversalSignal:
        freq = float(np.clip(np.mean(image), 0, 255)) + 1.0
        amp = float(np.std(image)) / 255.0
        return UniversalSignal(SignalType.VISUAL, frequency=freq, amplitude=max(0.1, amp), payload=image.shape)

    def from_emotion(self, emotion: str, intensity: float = 0.5) -> UniversalSignal:
        data = self.mapper.get_emotion_frequency(emotion)
        return UniversalSignal(SignalType.EMOTIONAL, frequency=data.frequency_hz, amplitude=float(intensity), payload=data)

    def from_text(self, text: str) -> UniversalSignal:
        freq = 200.0 + (hash(text) % 400)
        return UniversalSignal(SignalType.TEXT, frequency=freq, amplitude=0.5, payload=text)

    def from_audio(self, audio_data: np.ndarray, sample_rate: int) -> UniversalSignal:
        """
        Convert audio data to widespread signal.
        - Amplitude = RMS Volume
        - Frequency = Zero Crossing Rate (approximate pitch)
        """
        # calculate RMS amplitude
        volume = np.sqrt(np.mean(audio_data**2))
        
        # calculate Zero Crossing Rate for frequency approximation
        zero_crossings = np.where(np.diff(np.signbit(audio_data)))[0]
        zcr = len(zero_crossings) / len(audio_data)
        freq_est = zcr * sample_rate / 2
        
        return UniversalSignal(
            SignalType.AUDITORY, 
            frequency=float(freq_est), 
            amplitude=float(volume), 
            payload={"volume": volume, "zcr": zcr}
        )

    def convert(self, signal: UniversalSignal, render_mode: RenderMode) -> RenderResult:
        if render_mode == RenderMode.AS_COLOR:
            color = self._freq_to_rgb(signal.frequency)
            return RenderResult(render_mode=render_mode, color=color, output={"mode": "color"})
        if render_mode == RenderMode.AS_MUSIC:
            notes = self._freq_to_notes(signal.frequency)
            chord = notes[:3]
            return RenderResult(render_mode=render_mode, output={"notes": notes, "chord": chord})
        # default: sound-like dict
        return RenderResult(render_mode=render_mode, sound={"frequency": signal.frequency}, output={"mode": "sound"})

    def _freq_to_rgb(self, freq: float) -> tuple:
        hue = (freq % 360.0) / 360.0
        s = 0.8
        v = 1.0
        # simple HSV to RGB
        i = int(hue * 6)
        f = hue * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        return (int(r * 255), int(g * 255), int(b * 255))

    def _freq_to_notes(self, freq: float):
        base_notes = ["C", "D", "E", "F", "G", "A", "B"]
        idx = int(freq) % len(base_notes)
        note = base_notes[idx]
        return [note, base_notes[(idx + 2) % len(base_notes)], base_notes[(idx + 4) % len(base_notes)]]

    # [Phase 25] TensionField → Language Nuance
    def from_tension_field(self, tension_field) -> UniversalSignal:
        """
        Convert TensionField state into a UniversalSignal.
        
        - Frequency = Average Curvature (Depth of Thought)
        - Amplitude = Total Charge (Energy Level)
        """
        if not tension_field or not tension_field.shapes:
            return UniversalSignal(SignalType.EMOTIONAL, frequency=200.0, amplitude=0.5, payload=None)
        
        # Calculate field metrics
        avg_curvature = sum(s.curvature for s in tension_field.shapes.values()) / len(tension_field.shapes)
        total_charge = sum(tension_field.charges.values())
        
        # Map to frequency (100-600 Hz range)
        frequency = 100.0 + (avg_curvature * 100.0)  # Deep thought = High frequency
        frequency = min(600.0, frequency)
        
        # Map to amplitude (0.1-1.0 range)
        amplitude = min(1.0, total_charge / 5.0)  # High charge = High energy
        amplitude = max(0.1, amplitude)
        
        return UniversalSignal(
            SignalType.EMOTIONAL,
            frequency=frequency,
            amplitude=amplitude,
            payload={"curvature": avg_curvature, "charge": total_charge}
        )

    def field_to_text_nuance(self, tension_field) -> Dict[str, Any]:
        """
        [Wave-to-Text]
        
        Translate TensionField state into language style adjustments.
        
        Returns:
            - tone: "calm", "energetic", "contemplative", "urgent"
            - formality: 0.0-1.0 (casual to formal)
            - verbosity: 0.0-1.0 (concise to elaborate)
        """
        signal = self.from_tension_field(tension_field)
        
        # Determine tone based on frequency and amplitude
        if signal.frequency > 400 and signal.amplitude > 0.7:
            tone = "urgent"
        elif signal.frequency > 300 and signal.amplitude > 0.5:
            tone = "energetic"
        elif signal.frequency > 200:
            tone = "contemplative"
        else:
            tone = "calm"
        
        # Formality correlates with curvature (Deep Wells = Mature = Formal)
        payload = signal.payload or {}
        curvature = payload.get("curvature", 0.5)
        formality = min(1.0, curvature / 3.0)
        
        # Verbosity inversely correlates with charge (High Charge = Urgent = Concise)
        charge = payload.get("charge", 0.5)
        verbosity = max(0.0, 1.0 - (charge / 5.0))
        
        return {
            "tone": tone,
            "formality": round(formality, 2),
            "verbosity": round(verbosity, 2),
            "frequency": signal.frequency,
            "amplitude": signal.amplitude
        }


__all__ = ["SynesthesiaEngine", "SignalType", "RenderMode", "UniversalSignal", "RenderResult"]
