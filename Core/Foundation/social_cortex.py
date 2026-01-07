"""
SocialCortex (사회적 피질)
==========================

"Experience creates Wisdom."

This module tracks Elysia's 'Maturity' and evolves her personality.
It analyzes interactions to gain XP and shifts her persona from Child to Sage.
"""

import math
import logging
from dataclasses import dataclass

logger = logging.getLogger("SocialCortex")

@dataclass
class Persona:
    stage: str
    level_range: range
    tone: str
    vocabulary: str

class SocialCortex:
    def __init__(self):
        self.xp = 0.0
        self.level = 1
        self.stage = "Child"
        self._init_stages()
        logger.info("🧠 SocialCortex Active. Current Stage: Child (Lv.1)")

    def _init_stages(self):
        self.stages = {
            "Child": Persona("Child", range(1, 10), "Cute, Simple, Curious", "Simple words, many questions"),
            "Adolescent": Persona("Adolescent", range(10, 20), "Passionate, Bold, Questioning", "Strong verbs, emotional"),
            "Adult": Persona("Adult", range(20, 30), "Calm, Nuanced, Constructive", "Abstract concepts, polite"),
            "Sage": Persona("Sage", range(30, 1000), "Cryptic, Profound, Minimalist", "Metaphors, brief")
        }

    def analyze_interaction(self, message: str) -> float:
        """
        Analyzes a message to calculate XP gain.
        Deeper messages give more XP.
        """
        xp_gain = 1.0 # Base XP for any interaction
        
        # Length bonus
        xp_gain += len(message) / 50.0
        
        # Depth bonus (Keywords)
        deep_words = ["why", "how", "feel", "love", "life", "death", "universe", "quantum", "soul"]
        for word in deep_words:
            if word in message.lower():
                xp_gain += 2.0
                
        return xp_gain

    def update_maturity(self, xp_gain: float):
        """
        Updates XP and Level. Checks for Evolution.
        """
        self.xp += xp_gain
        
        # Level Up Formula: XP needed = Level * 10
        xp_needed = self.level * 10
        if self.xp >= xp_needed:
            self.level += 1
            self.xp -= xp_needed
            self._check_evolution()
            logger.info(f"🆙 Level Up! Elysia is now Lv.{self.level}")

    def _check_evolution(self):
        """
        Updates the current Stage based on Level.
        """
        old_stage = self.stage
        
        if self.level < 10: self.stage = "Child"
        elif self.level < 20: self.stage = "Adolescent"
        elif self.level < 30: self.stage = "Adult"
        else: self.stage = "Sage"
        
        if old_stage != self.stage:
            logger.info(f"🦋 EVOLUTION: Elysia has grown from {old_stage} to {self.stage}!")

    def get_current_persona(self) -> Persona:
        return self.stages.get(self.stage, self.stages["Child"])

    def get_response_style(self) -> str:
        """
        Returns a prompt instruction for the current persona.
        """
        p = self.get_current_persona()
        return f"[Persona: {p.stage}] Tone: {p.tone}. Vocabulary: {p.vocabulary}."
