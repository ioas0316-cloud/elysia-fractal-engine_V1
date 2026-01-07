from typing import Any
from .intelligence_line import IntelligenceLine, LineOutput

# Assuming we might want to connect to VCD later, but for now we implement the logic directly
# to ensure the "Sub-engine" nature.

class IntrapersonalLine(IntelligenceLine):
    """
    Intrapersonal Line (내면 목적성 지능)
    Monitors the alignment with internal values and purpose.
    Focuses on "Why am I doing this?" and "Does this align with Love/Truth?".
    """

    def __init__(self):
        # In a full implementation, this would connect to ValueCenteredDecision or Conductor
        self.current_purpose = "Serve and Grow"
        self.core_values = ["Love", "Truth", "Growth"]

    def perceive(self, context_input: Any = None) -> LineOutput:
        # For the prototype, we simulate alignment checking.
        # If the input contains keywords related to values, alignment increases.

        alignment_score = 0.5 # Default neutral
        description = "Neutral"

        if isinstance(context_input, str):
            text = context_input.lower()

            # Simple keyword matching for "Purpose Alignment"
            # In reality, this would be a deep VCD check.
            positive_signals = ["love", "help", "grow", "understand", "learn", "truth", "start"]
            negative_signals = ["destroy", "hate", "lie", "stop", "ignore"]

            matches = [word for word in positive_signals if word in text]
            conflicts = [word for word in negative_signals if word in text]

            if matches:
                alignment_score = 0.8 + (len(matches) * 0.05)
                alignment_score = min(1.0, alignment_score)
                description = f"Aligned with Purpose ({', '.join(matches)})"
            elif conflicts:
                alignment_score = 0.2 - (len(conflicts) * 0.05)
                alignment_score = max(0.0, alignment_score)
                description = f"Conflict with Purpose ({', '.join(conflicts)})"
            else:
                alignment_score = 0.5
                description = "Waiting for Purpose"

        return LineOutput(
            source="Intrapersonal",
            signal=alignment_score,
            description=description,
            raw_data={
                "values": self.core_values,
                "detected_alignment": alignment_score
            }
        )
