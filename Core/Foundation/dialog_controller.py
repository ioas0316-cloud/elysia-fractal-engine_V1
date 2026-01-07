"""Multimodal dialogue controller bridging world state and resonance mappings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from Core.Foundation.wave_frequency_mapping import WaveFrequencyMapper, EmotionType, SoundType
from Core.Interaction.Interface.Perception.synesthesia_engine import SynesthesiaEngine, RenderMode
from Core.Interaction.Interface.conversation_engine import ConversationEngine


@dataclass
class DialogueOutput:
    text: str
    color_hex: str
    sound: Dict[str, Any]
    meta: Dict[str, Any]


class MultimodalDialogueController:
    """
    Lightweight controller that:
    - reads world state (valence/arousal/will/value summaries),
    - runs the Resonance-based ConversationEngine for text,
    - maps emotion ↔ frequency to produce color/sound side-channel.
    """

    def __init__(self):
        self.conv = ConversationEngine()
        self.mapper = WaveFrequencyMapper()
        self.synesthesia = SynesthesiaEngine()

    def _infer_emotion(self, world: Any) -> EmotionType:
        try:
            alive = int(world.is_alive_mask.sum())
            mean_val = float(world.valence[world.is_alive_mask].mean()) if alive > 0 else 0.5
            mean_aro = float(world.arousal[world.is_alive_mask].mean()) if alive > 0 else 0.5
        except Exception:
            mean_val, mean_aro = 0.5, 0.5
        if mean_val > 0.6:
            return EmotionType.LOVE if mean_aro < 0.7 else EmotionType.JOY
        if mean_val < 0.3:
            return EmotionType.SADNESS if mean_aro < 0.6 else EmotionType.FEAR
        return EmotionType.NEUTRAL

    def _render_multimodal(self, emotion: EmotionType, intensity: float = 0.5) -> Dict[str, Any]:
        em_data = self.mapper.get_emotion_frequency(emotion)
        # color from synesthesia (emotion -> music/color)
        signal = self.synesthesia.from_emotion(emotion.name.lower(), intensity=intensity)
        color_render = self.synesthesia.convert(signal, RenderMode.AS_COLOR)
        music_render = self.synesthesia.convert(signal, RenderMode.AS_MUSIC)
        sound_freq = em_data.frequency_hz
        sound_info = {
            "frequency_hz": sound_freq,
            "brainwave": em_data.brainwave_dominant.name,
            "hrv_coherence": em_data.hrv_coherence,
            "mode": "healing" if emotion in (EmotionType.LOVE, EmotionType.PEACE) else "stabilize",
        }
        return {
            "color_hex": self.mapper.map_to_elysia(sound_freq).elysia_color_code
            if not color_render.color
            else "#{:02X}{:02X}{:02X}".format(*color_render.color),
            "music": music_render.output,
            "sound": sound_info,
        }

    def respond(self, user_text: str, world: Optional[Any] = None) -> DialogueOutput:
        emotion = self._infer_emotion(world) if world is not None else EmotionType.NEUTRAL
        intensity = 0.5
        if world is not None:
            try:
                alive = int(world.is_alive_mask.sum())
                if alive > 0:
                    intensity = float(world.arousal[world.is_alive_mask].mean())
            except Exception:
                pass
        multimodal = self._render_multimodal(emotion, intensity=intensity)
        text = self.conv.listen(user_text)
        meta = {
            "emotion": emotion.name.lower(),
            "intensity": intensity,
        }
        return DialogueOutput(
            text=text,
            color_hex=multimodal["color_hex"],
            sound=multimodal["sound"],
            meta=meta,
        )


__all__ = ["MultimodalDialogueController", "DialogueOutput"]
