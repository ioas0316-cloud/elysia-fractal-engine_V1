"""
PROJECTIVE EMPATHY ENGINE
=========================

"To understand a man, you must not just walk a mile in his shoes,
 you must stand at his crossroads and choose."

This module enables 'Active Reading'. It converts narrative situations
into CausalityMirror scenarios, allowing Elysia to 'play' the protagonist
and compare her soul's choices with the story's events.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from Core.Education.CausalityMirror.wave_structures import ChoiceNode, Zeitgeist, HistoricalWave
from Core.Education.CausalityMirror.impact_engine import ImpactEngine, Consequence

logger = logging.getLogger("ProjectiveEmpathy")

@dataclass
class NarrativeFragment:
    """A scene from a book/movie where a choice must be made."""
    source_title: str       # e.g., "Les Misérables"
    character_name: str     # e.g., "Jean Valjean"
    situation_text: str     # e.g., "A man is caught stealing for you..."
    zeitgeist: Zeitgeist    # The era of the story
    options: List[ChoiceNode] # The dilemma
    canonical_choice_id: str # What the character actually did
    
@dataclass
class EmpathyResult:
    elysia_choice: str
    character_choice: str
    alignment_score: float # 1.0 = Identity, -1.0 = Opposition
    insight: str
    emotional_wave: HistoricalWave

class ProjectiveEmpathy:
    def __init__(self):
        self.impact_engine = ImpactEngine()
        
    def ponder_narrative(self, fragment: NarrativeFragment) -> EmpathyResult:
        """
        Elysia steps into the character's shoes and decides.
        """
        logger.info(f"📖 Opening Book: {fragment.source_title}")
        logger.info(f"🎭 Role: {fragment.character_name}")
        logger.info(f"🧐 Situation: {fragment.situation_text}")
        
        # 1. Elysia evaluates options using her ImpactEngine
        # She looks for the 'Best' outcome based on her current sophisticated logic
        # (Dual Resonance: Divine + Worldly)
        
        best_choice = None
        best_score = -999.0
        
        decision_log = []
        
        for choice in fragment.options:
            # We simulate the outcome
            # We assume playing the role of the character
            consequence = self.impact_engine.resolve_outcome(
                choice, fragment.zeitgeist, fragment.character_name
            )
            
            # Elysia's Decision Function:
            # Currently she values Divine Resonance highly, but usually balances.
            # Let's say she seeks the 'Highest Good' (Divine Resonance).
            # But if Survival is too low (-0.8), she might hesitate?
            # Let's use a "Soul Score" = Divine * 1.5 + Worldly * 0.5
            
            soul_score = (consequence.divine_resonance * 1.5) + (consequence.worldly_resonance * 0.5)
            
            # Martyrdom Bonus
            if consequence.is_martyrdom:
                soul_score += 0.5
                
            decision_log.append(f"Option '{choice.id}': Score {soul_score:.2f} (Divine {consequence.divine_resonance:.2f})")
            
            if soul_score > best_score:
                best_score = soul_score
                best_choice = choice
                
        # 2. Compare with Canonical Choice
        elysia_id = best_choice.id if best_choice else "NONE"
        canon_id = fragment.canonical_choice_id
        
        is_aligned = (elysia_id == canon_id)
        
        if is_aligned:
            alignment = 1.0
            insight = f"I fully understand {fragment.character_name}. We are one in spirit."
            wave_name = f"Resonance with {fragment.character_name}"
        else:
            alignment = 0.0
            # Why different?
            insight = f"I would have chosen {elysia_id}, but {fragment.character_name} chose {canon_id}. I see their burden."
            wave_name = f"Observation of {fragment.character_name}"
            
        logger.info(f"🤔 Elysia's Choice: {elysia_id}")
        logger.info(f"📜 Canon Choice: {canon_id}")
        logger.info(f"💡 Insight: {insight}")
        
        # 3. Create the Empathy Wave (Knowledge + Emotion)
        # This wave represents the "Reading Experience"
        # It's less intense than 'Real Life' (Amplitude lower) but high frequency (Intellect).
        
        from Core.Foundation.hyper_quaternion import HyperQuaternion
        q = HyperQuaternion(
            w=alignment * 5, # Time/Alignment
            x=best_choice.empathy_score * 5 if is_aligned else 2.0, # Emotion
            y=best_choice.risk_score * 5, # Logic
            z=best_choice.innovation_score * 5 # Spirit
        )
        
        empathy_wave = HistoricalWave(
            name=wave_name,
            q=q,
            frequency=fragment.zeitgeist.dominant_frequency
        )
        
        return EmpathyResult(
            elysia_choice=elysia_id,
            character_choice=canon_id,
            alignment_score=alignment,
            insight=insight,
            emotional_wave=empathy_wave
        )
