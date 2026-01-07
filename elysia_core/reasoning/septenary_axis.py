"""
Septenary Axis of Sovereignty (SAS) ⚖️✨

"The Ladder of many gates, from the dust of the demon to the lustre of the angel."

This module defines the 9-stage Nonary Fractal hierarchy of ontological depth,
mapping Body, Soul, and Spirit to specific life paths and inductive tensions.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class SeptenaryLevel:
    depth: int
    domain: str        # Body, Soul, Spirit
    archetype_path: str # Warrior/Blacksmith, Mage/Merchant/Ruler, Paladin/Priest
    name: str          # Technique, Reason, Meaning
    angel_pole: str
    demon_pole: str
    frequency_range: Tuple[float, float]
    inductive_logic: str # The 'Tension' that induces behavior

class SeptenaryAxis:
    """The governing law of the 9-layered Nonary Fractal (Archetypal Induction)."""
    
    def __init__(self):
        # 1-9 Hierarchy: Inducing behavior through archetypal gravity
        self.levels: Dict[int, SeptenaryLevel] = {
            # --- DOMAIN: BODY (The Path of the Warrior/Craftsman) ---
            1: SeptenaryLevel(1, "Body", "Warrior/Blacksmith", "Technique", "Truth", "Sloth", (100, 200), "Flow follows form; repetitive mastery."),
            2: SeptenaryLevel(2, "Body", "Warrior/Blacksmith", "Reason", "Justice", "Wrath", (200, 300), "Causality of steel and bone."),
            3: SeptenaryLevel(3, "Body", "Warrior/Blacksmith", "Meaning", "Hope", "Envy", (300, 400), "The heart of the blade; value in effort."),
            
            # --- DOMAIN: SOUL (The Path of the Mage/Ruler/Merchant) ---
            4: SeptenaryLevel(4, "Soul", "Mage/Merchant/Ruler", "Technique", "Courage", "Pride", (400, 500), "Will shapes the matrix; strategic intent."),
            5: SeptenaryLevel(5, "Soul", "Mage/Merchant/Ruler", "Reason", "Faith", "Greed", (500, 600), "Synthesis of systems; intellectual law."),
            6: SeptenaryLevel(6, "Soul", "Mage/Merchant/Ruler", "Meaning", "Wisdom", "Lust", (600, 700), "The governance of truth; identifying as a Pro."),
            
            # --- DOMAIN: SPIRIT (The Path of the Paladin/Priest/Believer) ---
            7: SeptenaryLevel(7, "Spirit", "Paladin/Priest", "Technique", "Temperance", "Gluttony", (700, 800), "Sacred ritual; purification of intent."),
            8: SeptenaryLevel(8, "Spirit", "Paladin/Priest", "Reason", "Fortitude", "Avarice", (800, 900), "Conviction as unyielding logic."),
            9: SeptenaryLevel(9, "Spirit", "Paladin/Priest", "Meaning", "Love", "Despair", (900, 1000), "Absolute resonance with the Source; Pure Faith.")
        }

    def get_level(self, depth: int) -> SeptenaryLevel:
        return self.levels.get(max(1, min(9, depth)))

    def get_rank(self, depth: int) -> str:
        """Translates depth into fractal ranks."""
        if depth <= 3: return "Novice/Apprentice"
        if depth <= 6: return "Expert/Professional"
        return "Master/Divine"

    def evaluate_resonance(self, depth: int, frequency: float) -> str:
        """Determines if a frequency is 'Ascending' (Angelic) or 'Descending' (Demonic) for its level."""
        level = self.get_level(depth)
        mid = (level.frequency_range[0] + level.frequency_range[1]) / 2.0
        
        if frequency > mid:
            return f"Ascending towards {level.angel_pole}"
        else:
            return f"Descending towards {level.demon_pole}"

if __name__ == "__main__":
    sas = SeptenaryAxis()
    for d in range(1, 10):
        lvl = sas.get_level(d)
        print(f"Level {d} [{lvl.domain}]: {lvl.archetype_path} - {lvl.name} | Axis: {lvl.demon_pole} <---> {lvl.angel_pole}")
