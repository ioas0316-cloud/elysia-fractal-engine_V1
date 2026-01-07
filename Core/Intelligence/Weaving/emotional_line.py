from typing import Any
from .intelligence_line import IntelligenceLine, LineOutput

class EmotionalLine(IntelligenceLine):
    """
    Emotional Line (감정 유추 지능)
    Monitors the "Heart" of the interaction.
    Reads the emotional tone of the input (User or Environment).
    """

    def __init__(self):
        self.name = "Emotional"

    def perceive(self, context_input: Any = None) -> LineOutput:
        signal = 0.5 # Neutral
        description = "Calm"

        if isinstance(context_input, str):
            text = context_input.lower()

            # Simple heuristic for emotional tone
            # High Energy / Positive
            joy_markers = ["!", "happy", "great", "love", "good", "thanks", "wow", "amazing"]
            # Low Energy / Negative
            sad_markers = ["sad", "sorry", "bad", "fail", "pain", "error", "grief", "cry"]
            # Anxiety / Tension
            anxiety_markers = ["urgent", "hurry", "worry", "scared", "fear", "panic"]
            # Curiosity / Interest (Positive Tension)
            curiosity_markers = ["?", "wonder", "curious", "interesting", "why", "how"]

            joy_score = sum(1 for m in joy_markers if m in text)
            sad_score = sum(1 for m in sad_markers if m in text)
            anxiety_score = sum(1 for m in anxiety_markers if m in text)
            curiosity_score = sum(1 for m in curiosity_markers if m in text)

            if joy_score > sad_score and joy_score > anxiety_score:
                signal = 0.8 + (joy_score * 0.05)
                signal = min(1.0, signal)
                description = "Joyful/Resonant"
            elif sad_score > joy_score:
                signal = 0.2 - (sad_score * 0.05)
                signal = max(0.0, signal)
                description = "Melancholic/Dissonant"
            elif anxiety_score > 0:
                signal = 0.3
                description = "Tense/Anxious"
            elif curiosity_score > 0:
                # Curiosity is a positive, active state (0.6 ~ 0.7)
                signal = 0.65
                description = "Curious/Engaged"
            else:
                signal = 0.5
                description = "Neutral/Stable"

        return LineOutput(
            source="Emotional",
            signal=signal,
            description=description,
            raw_data={
                "tone_analysis": description
            }
        )
