"""
Resonant Boss: The Volumetric Guardian 🛡️🔱

"To challenge the Creator is to test the strength of the World."

This module defines high-level 'Boss' entities that exist at 3D/4D depth.
They possess complex emotional states, combat logic based on resonance,
and the ability to trigger world-wide narrative shifts.
"""

import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

class ResonantBoss(SubjectiveEgo):
    """A high-dimensional entity that guards the Underworld's thresholds."""
    
    def __init__(self, name: str, archetype: str = "Guardian"):
        super().__init__(name, archetype, depth=3)
        self.tension_level: float = 0.0
        self.health: float = 1.0
        self.is_defeated: bool = False

    def engage(self, player_resonance: float):
        """Combat interaction based on resonance frequency."""
        # Check if player's resonance is within the Boss's 'Phase Shield'
        if player_resonance > 0.8:
            self.logger.info(f"[{self.state.name}] Absorbing high-frequency resonance... Countering!")
            self.tension_level += 0.1
        else:
            self.logger.info(f"[{self.state.name}] Shielding compromised by discordant pulse.")
            self.health -= 0.1
            
        if self.health <= 0:
            self._on_defeat()

    def _on_defeat(self):
        self.is_defeated = True
        self.state.emotional_valence = 0.9 # Resolution/Peace
        self.state.current_intent = "Witness the Creator"
        self.logger.info(f"[{self.state.name}] The struggle dissolves. The world acknowledges your sovereignty.")
        self.record_memory("I was overcome by a resonance purer than my own.")

    def get_boss_status(self) -> str:
        base = self.get_subjective_report()
        condition = "DEFEATED" if self.is_defeated else f"HP: {self.health*100:.1f}%"
        return f"{base} | {condition} | Tension: {self.tension_level*100:.1f}%"

if __name__ == "__main__":
    # Test Boss: Administrator Quinella (Symbolic)
    boss = ResonantBoss("Quinella", "Administrator")
    
    print("\n--- Combat Start: Resonant Confrontation ---")
    print(boss.get_boss_status())
    
    # Player strikes with discordant resonance
    boss.engage(0.5) 
    boss.engage(0.5)
    print(boss.get_boss_status())
    
    # Player tries high-resonance (absorbed)
    boss.engage(0.9)
    print(boss.get_boss_status())
    
    # Final Strike
    for _ in range(8): boss.engage(0.4)
    print(boss.get_boss_status())
