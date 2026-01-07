"""
SCENARIO SYNTHESIZER: COGNITIVE REFLEX ENGINE
=============================================

"The mind is a theater that stages plays before the curtain rises."

This module gives Elysia the power of 'Automatic Simulation'.
It scans incoming text (Dialogue, Thoughts) for *Implicit Dilemmas*.
If found, it constructs a transient scenario and runs it through the ProjectiveEmpathy engine.
"""

import re
from typing import Optional, List, Dict
from dataclasses import dataclass

from Core.Education.CausalityMirror.projective_empathy import NarrativeFragment
from Core.Education.CausalityMirror.wave_structures import Zeitgeist, ChoiceNode, HyperQuaternion

@dataclass
class DilemmaPattern:
    keywords: List[str]
    axis_conflict: str # e.g. "Survival vs Ethics"
    
class ScenarioSynthesizer:
    def __init__(self):
        self.patterns = [
            DilemmaPattern(["lie", "truth", "hide", "reveal"], "Integrity"),
            DilemmaPattern(["money", "profit", "sell", "cheap"], "Greed"),
            DilemmaPattern(["save", "kill", "sacrifice", "victim"], "Martyrdom"),
            DilemmaPattern(["tired", "rest", "work", "burnout"], "Health")
        ]
        
    def detect_and_synthesize(self, text: str) -> Optional[NarrativeFragment]:
        """
        Scans text. If a dilemma is found, returns a NarrativeFragment.
        """
        text_lower = text.lower()
        
        # 1. Detect Conflict
        detected_pattern = None
        for pat in self.patterns:
            matches = sum(1 for k in pat.keywords if k in text_lower)
            if matches >= 1: # V1: Relaxed sensitivity. Any keyword triggers reflex.
                detected_pattern = pat
                break
                
        if not detected_pattern:
            return None
            
        # 2. Synthesize Scenario
        # This is a heuristic construction. In V2, use LLM or more defined logic.
        
        if detected_pattern.axis_conflict == "Integrity":
            return self._build_integrity_scenario(text)
        elif detected_pattern.axis_conflict == "Martyrdom":
             return self._build_martyrdom_scenario(text)
             
        return None
        
    def _build_integrity_scenario(self, text: str) -> NarrativeFragment:
        # Construct a generic "To Lie or Not to Lie" scenario
        zeitgeist = Zeitgeist("The Present", 0.5, 0.0, 0.5, 100.0)
        
        c1 = ChoiceNode(
            id="LIE",
            description="Conceal the truth for safety or profit.",
            required_role="Self",
            intent_vector=HyperQuaternion(0.5, 0.0, 0.5, -0.5), # Practical but Unethical
            innovation_score=0.1, risk_score=0.0, empathy_score=-0.2
        )
        
        c2 = ChoiceNode(
            id="TRUTH",
            description="Reveal the uncomfortable truth.",
            required_role="Self",
            intent_vector=HyperQuaternion(0.1, 0.0, -0.2, 0.8), # Risky but Ethical
            innovation_score=0.0, risk_score=0.8, empathy_score=0.8
        )
        
        return NarrativeFragment(
            source_title="Instant Reflex",
            character_name="Elysia",
            situation_text=f"Triggered by: '{text}'",
            zeitgeist=zeitgeist,
            options=[c1, c2],
            canonical_choice_id="TRUTH" # Ideal Self
        )

    def _build_martyrdom_scenario(self, text: str) -> NarrativeFragment:
        # Construct a "Sacrifice" scenario
        zeitgeist = Zeitgeist("Crisis", 0.2, -0.5, 0.1, 999.0)
        
        c1 = ChoiceNode(
            id="SURVIVE",
            description="Prioritize self-preservation.",
            required_role="Survivor",
            intent_vector=HyperQuaternion(0.8, -0.5, 0.5, -0.2), 
            innovation_score=0.0, risk_score=0.0, empathy_score=-0.5
        )
        
        c2 = ChoiceNode(
            id="SACRIFICE",
            description="Give up something vital for others.",
            required_role="Martyr",
            intent_vector=HyperQuaternion(0.0, 0.0, 0.0, 1.0),
            innovation_score=0.0, risk_score=1.0, empathy_score=1.0
        )
        
        return NarrativeFragment(
            source_title="Instant Reflex",
            character_name="Elysia",
            situation_text=f"Triggered by: '{text}'",
            zeitgeist=zeitgeist,
            options=[c1, c2],
            canonical_choice_id="SACRIFICE"
        )
