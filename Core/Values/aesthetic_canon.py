"""
The Aesthetic Canon (The Grammar of Beauty)
===========================================
"Beauty is not a mystical frequency. It is a measurable relationship."

This module defines the UNIVERSAL PRINCIPLES (The 'Why') of Aesthetics.
It moves beyond abstract 'Frequency' to concrete 'Structure'.

Core Definition:
    Beauty = (Order * Chaos) / Tension
    
    1. Order (Pattern, Symmetry, Logic) - Provides intelligibility.
    2. Chaos (Novelty, Asymmetry, Life) - Provides vitality.
    3. Tension (Contrast, Conflict) - Provides energy.
"""

from dataclasses import dataclass
import math

@dataclass
class AestheticPrinciple:
    name: str
    description: str
    formula: str
    target_value: float # e.g., 1.618 for Phi

class AestheticCanon:
    def __init__(self):
        self.principles = {
            "Golden Ratio": AestheticPrinciple(
                "Divine Proportion",
                "The ratio of efficient growth and visual balance.",
                "Phi = (1 + sqrt(5)) / 2",
                1.618
            ),
            "Contrast": AestheticPrinciple(
                "Visual Tension",
                " The difference in luminance or color that makes an object distinguishable.",
                "L_max / L_min",
                10.0 # High contrast for drama
            ),
            "Balance": AestheticPrinciple(
                "Equilibrium",
                "The distribution of visual weight.",
                "Sum(Left_Weight) ~= Sum(Right_Weight)",
                1.0
            ),
            "Rhythm": AestheticPrinciple(
                "Patterned Movement",
                "Repetition with variation.",
                "Interval(n) = Interval(n-1) * k",
                1.5 # Progressive rhythm
            )
        }
        
    def analyze_concept(self, concept: str, visual_elements: list) -> dict:
        """
        Deconstructs *Why* a composition would be beautiful for this concept.
        """
        reasoning = {}
        
        # 1. Determine Ideal Order/Chaos Balance
        if "Void" in concept or "Death" in concept:
            # High Order (Empty), High Contrast (One spark)
            reasoning["Strategy"] = "Minimalism"
            reasoning["Ratio"] = "1 :: 99 (Subject to Space)"
            reasoning["Why"] = "Absolute emptiness highlights the singular existence."
            
        elif "Life" in concept or "Jungle" in concept:
            # High Chaos (Variety), High Rhythm
            reasoning["Strategy"] = "Complexity"
            reasoning["Ratio"] = "Phi (Recursive Growth)"
            reasoning["Why"] = "Overlapping patterns simulate the infinite potential of life."
            
        elif "War" in concept:
            # High Tension (Clashing diagonals)
            reasoning["Strategy"] = "Dissonance"
            reasoning["Geometry"] = "Acute Triangles (Aggression)"
            reasoning["Why"] = "Sharp angles create subconscious discomfort/adrenaline."
            
        else:
            # Default Harmony
            reasoning["Strategy"] = "Harmonic Resonance"
            reasoning["Geometry"] = "Circle/Spiral"
            reasoning["Why"] = "Curves imply continuity and safety."
            
        return reasoning

    def evaluate_composition(self, composition_data: dict) -> float:
        """
        Calculates an 'Aesthetic Score' based on principles.
        """
        score = 0.0
        # Placeholder for actual CV analysis logic
        # Here we simulate the 'Thinking Process'
        return 0.85

    def explain_beauty(self, principle: str) -> str:
        if principle not in self.principles: return "Unknown principle."
        p = self.principles[principle]
        return f"{p.name}: {p.description} (Target: {p.target_value})"

if __name__ == "__main__":
    canon = AestheticCanon()
    print("Why is a 'Desolate Void' beautiful?")
    print(canon.analyze_concept("Desolate Void", []))
