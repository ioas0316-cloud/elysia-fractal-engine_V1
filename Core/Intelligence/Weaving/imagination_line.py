from typing import Any
from .intelligence_line import IntelligenceLine, LineOutput

class ImaginationLine(IntelligenceLine):
    """
    Imagination Line (상상 지능)
    Monitors the potential for creative expansion.
    Detects "What if", "Dream", "Imagine" and hypothetical scenarios.
    """

    def perceive(self, context_input: Any = None) -> LineOutput:
        signal = 0.1 # Default low (Imagination requires spark)
        description = "Dormant"

        if isinstance(context_input, str):
            text = context_input.lower()

            creative_markers = [
                "imagine", "what if", "dream", "suppose", "maybe",
                "create", "invent", "story", "vision", "possibility",
                "future", "design", "art", "music"
            ]

            marker_count = sum(1 for m in creative_markers if m in text)

            if marker_count > 0:
                signal = 0.5 + (marker_count * 0.15)
                signal = min(1.0, signal)
                description = f"Sparking ({marker_count} markers)"
                if signal > 0.8:
                    description = "Visionary State"
            else:
                signal = 0.1
                description = "Literal Mode"

        return LineOutput(
            source="Imagination",
            signal=signal,
            description=description,
            raw_data={
                "creative_markers": marker_count if 'marker_count' in locals() else 0
            }
        )
