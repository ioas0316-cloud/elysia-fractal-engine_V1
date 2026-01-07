from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .context_weaver import ContextPlane

@dataclass
class InsightPattern:
    name: str
    conditions: List[Dict[str, Any]]
    result_insight: str
    result_action: str
    result_reason_template: str

class InsightJump:
    """
    The Jump.
    Derives a 3D Insight from the 2D Context Plane using Pattern Matching.
    Now supports Dynamic Intelligence Lines via generic matching.
    """

    def __init__(self):
        self.patterns = [
            # Standard Patterns
            InsightPattern(
                name="Flow State",
                conditions=[
                    {"source": "Kinesthetic", "min": 0.5},
                    {"source": "Emotional", "min": 0.6},
                    {"source": "Intrapersonal", "min": 0.6}
                ],
                result_insight="Flow State Detected",
                result_action="Accelerate",
                result_reason_template="Body, Heart, and Soul are aligned."
            ),
             InsightPattern(
                name="Burnout Risk",
                conditions=[
                    {"source": "Kinesthetic", "min": 0.8},
                ],
                result_insight="Burnout Risk",
                result_action="Rest & Reflect",
                result_reason_template="Physical stress is critical."
            ),
            InsightPattern(
                name="Creative Spark",
                conditions=[
                    {"source": "Imagination", "min": 0.7},
                    {"source": "Emotional", "min": 0.5}
                ],
                result_insight="Creative Spark",
                result_action="Brainstorm",
                result_reason_template="High imaginative potential."
            ),
            # New: Dynamic Domain Patterns
            # Instead of hardcoding "Cooking", we look for "Any Domain High Signal"
            # This is handled by logic inside jump() for universal adaptability.
        ]

    def jump(self, plane: ContextPlane) -> Dict[str, Any]:
        """
        Analyzes the plane and returns the best matching Insight.
        """
        # 1. Check Specific Registered Patterns
        best_match = None
        best_score = 0.0

        for pattern in self.patterns:
            conditions_met = 0

            for condition in pattern.conditions:
                source = condition["source"]
                line_output = plane.lines.get(source)

                if not line_output: continue

                score = 0
                if "min" in condition and line_output.signal >= condition["min"]: score = 1
                elif "max" in condition and line_output.signal <= condition["max"]: score = 1

                if score > 0: conditions_met += 1

            if conditions_met == len(pattern.conditions):
                if conditions_met > best_score:
                    best_score = conditions_met
                    best_match = pattern

        # 2. Check for Dynamic Domain Dominance (The "Universal" Jump)
        # If no specific system pattern matches, but a Universal Line (Cooking, Music) is screaming.
        if not best_match:
            # Find any non-standard line with high signal
            standard_lines = {"Kinesthetic", "Intrapersonal", "Emotional", "Logical", "Imagination", "Metacognition"}

            dominant_dynamic = None
            highest_dynamic_sig = 0.0

            for source, output in plane.lines.items():
                if source not in standard_lines and output.signal > 0.6:
                    if output.signal > highest_dynamic_sig:
                        highest_dynamic_sig = output.signal
                        dominant_dynamic = output

            if dominant_dynamic:
                return {
                    "insight": f"{dominant_dynamic.source} Context Detected",
                    "action": f"Activate {dominant_dynamic.source} Protocol",
                    "reason": f"High resonance with {dominant_dynamic.source} material ({dominant_dynamic.description}).",
                    "plane_summary": plane.overall_mood
                }

        # Return Best Match or Default
        if best_match:
            return {
                "insight": best_match.result_insight,
                "action": best_match.result_action,
                "reason": best_match.result_reason_template,
                "plane_summary": plane.overall_mood
            }
        else:
            return {
                "insight": "Observe",
                "action": "Wait",
                "reason": "No specific pattern matched.",
                "plane_summary": plane.overall_mood
            }
