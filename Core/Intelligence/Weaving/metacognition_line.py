from typing import Any
from .intelligence_line import IntelligenceLine, LineOutput

class MetacognitionLine(IntelligenceLine):
    """
    Metacognition Line (메타인지/자기성찰 지능)
    Monitors self-referential thought and awareness depth.
    Detects "I think", "I feel", "Why did I", "Self".
    """

    def perceive(self, context_input: Any = None) -> LineOutput:
        signal = 0.2
        description = "Surface Level"

        if isinstance(context_input, str):
            text = context_input.lower()

            self_refs = ["i think", "i feel", "my", "me", "self", "why did i", "am i"]
            reflection_markers = ["reflect", "analyze", "understand", "learn", "improve", "mistake"]

            self_count = sum(1 for m in self_refs if m in text)
            reflection_count = sum(1 for m in reflection_markers if m in text)

            total_score = (self_count * 0.1) + (reflection_count * 0.15)

            if total_score > 0.6:
                signal = 0.9
                description = "Deep Introspection"
            elif total_score > 0.3:
                signal = 0.6
                description = "Self-Aware"
            else:
                signal = 0.2
                description = "External Focus"

            signal = min(1.0, signal)

        return LineOutput(
            source="Metacognition",
            signal=signal,
            description=description,
            raw_data={
                "self_refs": self_count if 'self_count' in locals() else 0,
                "reflections": reflection_count if 'reflection_count' in locals() else 0
            }
        )
