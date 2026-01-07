from typing import Any
from .intelligence_line import IntelligenceLine, LineOutput

class LogicalLine(IntelligenceLine):
    """
    Logical Line (자연 탐구/논리 지능)
    Monitors the "Reason" and "Fact".
    Checks for logical consistency and clarity.
    """

    def __init__(self):
        self.name = "Logical"

    def perceive(self, context_input: Any = None) -> LineOutput:
        signal = 0.5
        description = "Unclear"

        if isinstance(context_input, str):
            text = context_input

            # Simple Logic Heuristics
            # 1. Length Check (Too short is often ambiguous)
            length_score = min(1.0, len(text) / 20.0)

            # 2. Structure Check (Connectives imply logic)
            connectives = ["because", "therefore", "if", "then", "so", "but", "and", "why", "how"]
            logic_density = sum(1 for word in text.lower().split() if word in connectives)

            # 3. Fact/Assertion check
            # Questions are low logic assertiveness, Statements are high
            is_question = "?" in text

            score = 0.5
            if is_question:
                score = 0.6 # Seeking logic (Increased from 0.4 based on feedback)
                description = "Inquiry (Seeking)"
            elif logic_density > 0:
                score = 0.7 + (logic_density * 0.1)
                description = "Structured Reason"
            else:
                score = 0.6
                description = "Simple Assertion"

            signal = min(1.0, score)

        return LineOutput(
            source="Logical",
            signal=signal,
            description=description,
            raw_data={
                "logic_density": signal
            }
        )
