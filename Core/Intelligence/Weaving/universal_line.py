from typing import Any, List, Dict
from .intelligence_line import IntelligenceLine, LineOutput

class UniversalLine(IntelligenceLine):
    """
    Universal Intelligence Line.
    A generic vessel that becomes specific intelligence by injecting
    'Material' (Keywords/Patterns) and 'Logic' (Processing Rule).
    """

    def __init__(self, name: str, keywords: List[str], patterns: Dict[str, float] = None, logic_type: str = "keyword_density"):
        self.name = name
        self.keywords = [k.lower() for k in keywords]
        self.patterns = patterns or {} # e.g. {"salt": 0.8, "sugar": 0.6} for weighted scoring
        self.logic_type = logic_type

    def perceive(self, context_input: Any = None) -> LineOutput:
        signal = 0.0
        description = "Dormant"
        details = {}

        if isinstance(context_input, str):
            text = context_input.lower()

            # --- Logic A: Simple Keyword Density ---
            if self.logic_type == "keyword_density":
                match_count = sum(1 for k in self.keywords if k in text)

                # Check for weighted patterns if available
                pattern_score = 0.0
                for pat, weight in self.patterns.items():
                    if pat in text:
                        pattern_score += weight
                        match_count += 1 # Count it as a match too

                if match_count > 0:
                    # Normalize: A few keywords shouldn't max out immediately, but strong pattern should
                    raw_score = (match_count * 0.1) + pattern_score
                    signal = min(1.0, raw_score)

                    if signal > 0.8:
                        description = f"High Resonance ({match_count} hits)"
                    elif signal > 0.4:
                        description = f"Active ({match_count} hits)"
                    else:
                        description = "Low Activity"

                    details = {"hits": match_count, "score": raw_score}
                else:
                    signal = 0.05 # Baseline hum
                    description = "Silent"

            # --- Logic B: Concept Association (Placeholder) ---
            # Future: Vector similarity using embeddings

        return LineOutput(
            source=self.name,
            signal=signal,
            description=description,
            raw_data=details
        )
