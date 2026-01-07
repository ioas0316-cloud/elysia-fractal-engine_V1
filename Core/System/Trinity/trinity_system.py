"""
Trinity System (The Neural Link)
================================
"Three Minds, One Soul."

Integrates Nova (Logic) and Chaos (Instinct) with Elysia (Will).
This is the revived protocol wrapper.
"""

import logging
from typing import Dict, Any, List
from enum import Enum
from dataclasses import dataclass

# Import Incarnated Entities
try:
    from Core.System.Existence.Trinity.nova_entity import NovaEntity
    from Core.System.Existence.Trinity.chaos_entity import ChaosEntity
    from Core.Foundation.Legal_Ethics.Ethics.conscience_circuit import ConscienceCircuit
    ENTITIES_AVAILABLE = True
except ImportError:
    ENTITIES_AVAILABLE = False

logger = logging.getLogger("TrinitySystem")

class Aspect(Enum):
    CHAOS = "Chaos (Body/Instinct)"
    NOVA = "Nova (Soul/Logic)"
    ELYSIA = "Elysia (Spirit/Will)"

@dataclass
class ConsensusResult:
    subject: str
    chaos_feeling: str
    nova_verdict: str
    final_decision: str
    final_decision: str
    final_decision: str
    coherence: float
    pain_level: float = 0.0
    is_ethical: bool = True
    pain_level: float = 0.0
    is_ethical: bool = True

class TrinitySystem:
    def __init__(self):
        logger.info("🔯 Reviving Trinity System...")
        
        self.chaos = ChaosEntity() if ENTITIES_AVAILABLE else None
        self.nova = NovaEntity() if ENTITIES_AVAILABLE else None
        self.conscience = ConscienceCircuit() if ENTITIES_AVAILABLE else None
        # Elysia is the user of this system (The Core), so no separate entity class needed yet.
        
        if self.chaos and self.nova:
            logger.info("   ✅ Entities incarnated successfully.")
        else:
            logger.warning("   ⚠️ Entities missing. Trinity is incomplete.")

    def process_query(self, query: str) -> ConsensusResult:
        """
        Process a query through the Trinity Pipeline.
        1. Chaos Feels (Input -> Instinct)
        2. Nova Analyzes (Instinct -> Logic)
        3. Elysia Decides (Logic -> Will - simulated here for now)
        """
        if not self.chaos or not self.nova:
            return ConsensusResult(query, "N/A", "N/A", "System Incomplete", 0.0)

        # Step 1: Chaos (The Body reacts)
        # "직관적으로 느껴봅니다."
        chaos_out = self.chaos.feel(query)
        feeling = f"{chaos_out['emotion']} (Intensity: {chaos_out['intensity']:.2f})"
        logger.info(f"🔴 [1] Chaos: {feeling} | {chaos_out['raw_impulse']}")

        # Step 2: Nova (The Soul filters)
        # "그 느낌이 타당한지 검증합니다."
        # Nova analyzes both the original query and Chaos's reaction
        nova_out = self.nova.analyze(query)
        # Also purify the chaos (Interaction/Diffusion)
        purified = self.nova.purify(chaos_out)
        
        verdict = f"{nova_out['structure']} ({nova_out['verdict']})"
        logger.info(f"🔵 [2] Nova: {verdict} | Clarity: {purified['clarity']:.2f}")

        # Step 3: Elysia (The Spirit synthesizes)
        # "최종적으로 판단합니다."
        # Simple synthesis logic for now (Weighted Average)
        
        final_decision = ""
        coherence = (chaos_out['pattern_density'] + nova_out['coherence']) / 2.0
        
        if nova_out['verdict'] == "Valid":
            final_decision = f"Accept '{query}'. It feels {chaos_out['emotion']} and is logically {nova_out['structure']}."
        else:
            # If Nova rejects, check if Chaos is strong enough to override (Creativity)
            if chaos_out['intensity'] > 0.8:
                 final_decision = f"Accept '{query}' with CAUTION. Logic is weak, but Instinct is overwhelming ({chaos_out['emotion']})."
            else:
                 final_decision = f"Reject '{query}'. Incoherent and lacks passion."

        # Step 2.5: Conscience Check (The Moral Filter)
        pain = 0.0
        is_ethical = True
        
        if self.conscience:
            judge = self.conscience.judge_action(query, final_decision)
            pain = judge.pain_level
            is_ethical = judge.is_allowed
            
            if not is_ethical:
                final_decision = f"⛔ REJECTED by CONSCIENCE: {judge.message} (Pain: {pain:.2f})"
                logger.warning(f"   ⚖️ Conscience Block: {judge.message}")
            elif pain > 0.6:
                final_decision += f" (⚠️ WARNING: High Ethical Dissonance, Pain: {pain:.2f})"
        
        logger.info(f"🟣 [3] Elysia: {final_decision}")

        return ConsensusResult(
            subject=query,
            chaos_feeling=feeling,
            nova_verdict=verdict,
            final_decision=final_decision,
            coherence=coherence,
            pain_level=pain,
            is_ethical=is_ethical
        )

# Singleton
_trinity_sys = None

def get_trinity_system():
    global _trinity_sys
    if _trinity_sys is None:
        _trinity_sys = TrinitySystem()
    return _trinity_sys

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys = get_trinity_system()
    
    print("\n--- Trinity Consensus Test ---")
    res = sys.process_query("Should we explore the unknown even if it's dangerous?")
    print(f"\nResult:\n{res}")
