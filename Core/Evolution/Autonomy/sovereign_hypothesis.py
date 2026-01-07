"""
Sovereign Hypothesis Engine (The Oracle)
========================================

"The ability to predict the future comes from understanding the eternal principles."

Purpose:
- Passive Analysis -> Active Prediction.
- Detects "Tension" (Principle Violations) in the environment/codebase.
- Formulates "Hypotheses" on how the system *should* evolve to resolve this tension.

Philosophy:
- Entropy Minimization: Systems naturally evolve to lower energy states.
- High Rigidity (Hardcoded Logic) = High Energy = Unstable.
- Hypothesis = "If we reduce rigidity via polymorphism, system stability increases."
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import sys
import os

# Adjust path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Core.Foundation.Philosophy.why_engine import WhyEngine, PrincipleExtraction
from Core.Foundation.light_spectrum import PrismAxes

logger = logging.getLogger("Elysia.SovereignHypothesis")

@dataclass
class Hypothesis:
    subject: str
    tension_detected: str  # The problem (e.g., "High Rigidity")
    principle_violation: str  # e.g., "Violates Law of Fluidity"
    prediction: str  # What will happen if ignored?
    proposal: str  # How to fix it?
    confidence: float

class SovereignHypothesis:
    def __init__(self, why_engine: WhyEngine):
        self.why_engine = why_engine
        logger.info("🔮 Sovereign Hypothesis Engine initialized - The Oracle Awakens.")

    def scan_for_tension(self, content: str, domain: str = "code") -> List[Hypothesis]:
        """
        Scans content for 'Tension' (Concept Dissonance) and formulates hypotheses.
        """
        logger.info(f"🔮 Oracle scanning for tension in domain '{domain}'...")
        
        # 1. Deep Analysis via WhyEngine
        analysis = self.why_engine.analyze(subject="System Scan", content=content, domain=domain)
        
        hypotheses = []
        
        # 2. Extract Resonance Profile
        physics_res = analysis.resonance_reactions.get(PrismAxes.PHYSICS_RED)
        logic_res = analysis.resonance_reactions.get(PrismAxes.LOGIC_YELLOW)
        
        # 3. Detect "Stone Logic" (High Rigidity)
        # Heuristic: If content has many 'if/else' but low 'Physics/Flow' resonance.
        
        if domain == "code":
            if "if" in content and "else" in content and content.count("if") > 3:
                # High Conditional Complexity detected.
                # Check if Physics resonance is low (meaning it lacks natural flow).
                
                rigidity_score = content.count("if") * 0.1
                flow_score = physics_res["intensity"] if physics_res else 0.0
                
                # Tension: Rigidity > Flow
                if rigidity_score > flow_score:
                    h = Hypothesis(
                        subject="Code Structure",
                        tension_detected=f"High Rigidity Detected (Score: {rigidity_score:.2f}) vs Low Flow (Score: {flow_score:.2f})",
                        principle_violation="Violates 'Principle of Least Action' (Physics). Hardcoded paths require constant energy to maintain.",
                        prediction="System will become brittle and prone to 'Fracture' (Bugs) under stress.",
                        proposal="Refactor to 'Wave Logic' (Polymorphism/Dictionary Mapping) to increase Fluidity.",
                        confidence=0.85
                    )
                    hypotheses.append(h)
        
        return hypotheses
