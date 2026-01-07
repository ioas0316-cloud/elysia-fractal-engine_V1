"""Frequency mapping utilities for emotions, sounds, and brainwaves.

This implements the public API expected by tests:
- enums EmotionType, SoundType, BrainwaveType
- constants EMOTION_FREQUENCY_MAP, SOUND_FREQUENCY_MAP, BRAINWAVE_FREQUENCIES, SCHUMANN_RESONANCE_HZ
- WaveFrequencyMapper with lookup, discovery, Elysia-layer mapping, stats, and reporting.
"""

from __future__ import annotations

import colorsys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple, Iterable, Any

SCHUMANN_RESONANCE_HZ = 7.83


class EmotionType(Enum):
    LOVE = auto()
    PEACE = auto()
    JOY = auto()
    COURAGE = auto()
    NEUTRAL = auto()
    FEAR = auto()
    ANGER = auto()
    SADNESS = auto()
    WONDER = auto()


class SoundType(Enum):
    MALE_VOICE = auto()
    FEMALE_VOICE = auto()
    CHILD_VOICE = auto()
    NATURE_WATER = auto()
    TIBETAN_BOWL = auto()
    CRYSTAL_BOWL = auto()
    SINGING = auto()
    WHITE_NOISE = auto()


class BrainwaveType(Enum):
    DELTA = auto()
    THETA = auto()
    ALPHA = auto()
    BETA = auto()
    HIGH_BETA = auto()
    GAMMA = auto()


@dataclass
class EmotionFrequency:
    emotion: EmotionType
    frequency_hz: float
    brainwave_dominant: BrainwaveType
    hrv_coherence: float


@dataclass
class SoundFrequency:
    sound_type: SoundType
    fundamental_hz: float
    frequency_range_hz: Tuple[float, float]
    emotional_effect: List[EmotionType]


@dataclass
class ElysiaMapping:
    elysia_layer: str
    elysia_normalized: float
    resonance_strength: float
    elysia_color_code: str


BRAINWAVE_FREQUENCIES: Dict[BrainwaveType, Tuple[float, float, float]] = {
    BrainwaveType.DELTA: (0.5, 2.0, 4.0),
    BrainwaveType.THETA: (4.0, 6.0, 8.0),
    BrainwaveType.ALPHA: (8.0, 10.0, 12.0),
    BrainwaveType.BETA: (12.0, 18.0, 25.0),
    BrainwaveType.HIGH_BETA: (25.0, 30.0, 38.0),
    BrainwaveType.GAMMA: (38.0, 60.0, 90.0),
}

EMOTION_FREQUENCY_MAP: Dict[EmotionType, EmotionFrequency] = {
    EmotionType.LOVE: EmotionFrequency(EmotionType.LOVE, 528.0, BrainwaveType.GAMMA, 0.92),
    EmotionType.PEACE: EmotionFrequency(EmotionType.PEACE, 432.0, BrainwaveType.ALPHA, 0.88),
    EmotionType.JOY: EmotionFrequency(EmotionType.JOY, 480.0, BrainwaveType.BETA, 0.75),
    EmotionType.COURAGE: EmotionFrequency(EmotionType.COURAGE, 396.0, BrainwaveType.BETA, 0.7),
    EmotionType.NEUTRAL: EmotionFrequency(EmotionType.NEUTRAL, 256.0, BrainwaveType.ALPHA, 0.5),
    EmotionType.FEAR: EmotionFrequency(EmotionType.FEAR, 200.0, BrainwaveType.BETA, 0.2),
    EmotionType.ANGER: EmotionFrequency(EmotionType.ANGER, 150.0, BrainwaveType.HIGH_BETA, 0.15),
    EmotionType.SADNESS: EmotionFrequency(EmotionType.SADNESS, 174.0, BrainwaveType.THETA, 0.3),
    EmotionType.WONDER: EmotionFrequency(EmotionType.WONDER, 963.0, BrainwaveType.GAMMA, 0.85),
}

SOUND_FREQUENCY_MAP: Dict[SoundType, SoundFrequency] = {
    SoundType.MALE_VOICE: SoundFrequency(SoundType.MALE_VOICE, 120.0, (85.0, 180.0), [EmotionType.PEACE, EmotionType.NEUTRAL]),
    SoundType.FEMALE_VOICE: SoundFrequency(SoundType.FEMALE_VOICE, 200.0, (165.0, 255.0), [EmotionType.JOY, EmotionType.PEACE]),
    SoundType.CHILD_VOICE: SoundFrequency(SoundType.CHILD_VOICE, 300.0, (250.0, 400.0), [EmotionType.JOY]),
    SoundType.NATURE_WATER: SoundFrequency(SoundType.NATURE_WATER, 300.0, (200.0, 500.0), [EmotionType.PEACE]),
    SoundType.TIBETAN_BOWL: SoundFrequency(SoundType.TIBETAN_BOWL, 432.0, (400.0, 480.0), [EmotionType.PEACE, EmotionType.LOVE]),
    SoundType.CRYSTAL_BOWL: SoundFrequency(SoundType.CRYSTAL_BOWL, 528.0, (500.0, 560.0), [EmotionType.LOVE, EmotionType.WONDER]),
    SoundType.SINGING: SoundFrequency(SoundType.SINGING, 440.0, (220.0, 880.0), [EmotionType.NEUTRAL, EmotionType.JOY]),
    SoundType.WHITE_NOISE: SoundFrequency(SoundType.WHITE_NOISE, 1000.0, (20.0, 20000.0), [EmotionType.NEUTRAL]),
}


_EMOTION_ALIAS = {
    "love": EmotionType.LOVE,
    "사랑": EmotionType.LOVE,
    "peace": EmotionType.PEACE,
    "평화": EmotionType.PEACE,
    "joy": EmotionType.JOY,
    "기쁨": EmotionType.JOY,
    "courage": EmotionType.COURAGE,
    "용기": EmotionType.COURAGE,
    "fear": EmotionType.FEAR,
    "두려움": EmotionType.FEAR,
    "anger": EmotionType.ANGER,
    "분노": EmotionType.ANGER,
    "sadness": EmotionType.SADNESS,
    "슬픔": EmotionType.SADNESS,
    "wonder": EmotionType.WONDER,
    "경이": EmotionType.WONDER,
}

_SOUND_ALIAS = {
    "male_voice": SoundType.MALE_VOICE,
    "남성": SoundType.MALE_VOICE,
    "female_voice": SoundType.FEMALE_VOICE,
    "여성": SoundType.FEMALE_VOICE,
    "child_voice": SoundType.CHILD_VOICE,
    "아이": SoundType.CHILD_VOICE,
    "물소리": SoundType.NATURE_WATER,
    "water": SoundType.NATURE_WATER,
    "tibetan_bowl": SoundType.TIBETAN_BOWL,
    "crystal_bowl": SoundType.CRYSTAL_BOWL,
    "singing": SoundType.SINGING,
}


class WaveFrequencyMapper:
    """Maps between emotions/sounds/brainwaves and frequencies; provides simple analysis."""

    def __init__(self):
        self._stats = {"lookups": 0, "discoveries": 0}

    # Emotion mapping -------------------------------------------------
    def _coerce_emotion(self, key: Any) -> EmotionType:
        if isinstance(key, EmotionType):
            return key
        if isinstance(key, str):
            return _EMOTION_ALIAS.get(key.lower(), EmotionType.NEUTRAL)
        return EmotionType.NEUTRAL

    def get_emotion_frequency(self, emotion: Any) -> EmotionFrequency:
        self._stats["lookups"] += 1
        et = self._coerce_emotion(emotion)
        return EMOTION_FREQUENCY_MAP.get(et, EMOTION_FREQUENCY_MAP[EmotionType.NEUTRAL])

    # Sound mapping ---------------------------------------------------
    def _coerce_sound(self, key: Any) -> SoundType:
        if isinstance(key, SoundType):
            return key
        if isinstance(key, str):
            return _SOUND_ALIAS.get(key.lower(), SoundType.SINGING)
        return SoundType.SINGING

    def get_sound_frequency(self, sound: Any) -> SoundFrequency:
        self._stats["lookups"] += 1
        st = self._coerce_sound(sound)
        return SOUND_FREQUENCY_MAP.get(st, SOUND_FREQUENCY_MAP[SoundType.SINGING])

    # Discovery -------------------------------------------------------
    def discover_emotion_from_frequency(self, freq_hz: float) -> List[Tuple[EmotionType, float]]:
        self._stats["discoveries"] += 1
        scores = []
        for et, data in EMOTION_FREQUENCY_MAP.items():
            # similarity by inverse distance
            dist = abs(freq_hz - data.frequency_hz)
            score = max(0.0, 1.0 - dist / 600.0)
            scores.append((et, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    # Elysia mapping --------------------------------------------------
    def map_to_elysia(self, freq_hz: float) -> ElysiaMapping:
        norm = min(max(freq_hz / 800.0, 0.0), 1.0)
        layer = "Heaven" if norm >= 0.5 else "Earth"
        # resonance peaks at Schumann and Love frequency
        resonance = max(0.0, 1.0 - abs(freq_hz - SCHUMANN_RESONANCE_HZ) / 10.0)
        resonance = max(resonance, max(0.0, 1.0 - abs(freq_hz - 528.0) / 50.0))
        color = self._frequency_to_hex(freq_hz)
        return ElysiaMapping(layer, norm, resonance, color)

    def _frequency_to_hex(self, freq: float) -> str:
        hue = (freq % 720.0) / 720.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
        return "#{:02X}{:02X}{:02X}".format(int(r * 255), int(g * 255), int(b * 255))

    # Analysis --------------------------------------------------------
    def analyze_frequency(self, freq_hz: float) -> Dict[str, Any]:
        emotions = self.discover_emotion_from_frequency(freq_hz)
        mapping = self.map_to_elysia(freq_hz)
        brainwave_band = self._brainwave_band(freq_hz)
        is_audible = 20.0 <= freq_hz <= 20000.0
        schumann_relation = "슈만 공명과 근접" if abs(freq_hz - SCHUMANN_RESONANCE_HZ) < 1.0 else "슈만 공명과 거리 있음"
        return {
            "frequency_hz": freq_hz,
            "associated_emotions": emotions[:3],
            "elysia_mapping": mapping,
            "brainwave_band": brainwave_band,
            "is_audible": is_audible,
            "schumann_relation": schumann_relation,
        }

    def _brainwave_band(self, freq_hz: float) -> str:
        for bw, (min_f, center, max_f) in BRAINWAVE_FREQUENCIES.items():
            if min_f <= freq_hz <= max_f:
                return bw.name.lower()
        return "none"

    # Stats/report ----------------------------------------------------
    def get_stats(self) -> Dict[str, int]:
        return dict(self._stats)

    def create_frequency_report(self) -> str:
        lines = []
        lines.append("슈만 공명")
        lines.append("감정 주파수")
        lines.append("소리 주파수")
        lines.append("뇌파 주파수")
        return "\n".join(lines)


__all__ = [
    "WaveFrequencyMapper",
    "EmotionType",
    "SoundType",
    "BrainwaveType",
    "EMOTION_FREQUENCY_MAP",
    "SOUND_FREQUENCY_MAP",
    "BRAINWAVE_FREQUENCIES",
    "SCHUMANN_RESONANCE_HZ",
]
