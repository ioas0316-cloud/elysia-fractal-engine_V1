"""
Paradox Engine (The Dialectical Synthesizer)
============================================

"The test of a first-rate intelligence is the ability to hold two opposed ideas in the mind at the same time."

This module implements the **Paradox Engine**, restored from the `Project_Sophia` legacy.
It enables the system to:
1.  Detect Contradictions (Thesis vs Antithesis).
2.  Hold them in Superposition (Tension).
3.  Transmute them into new Principles (Synthesis).

Restored & Adapted by: Jules
Original Intent: Father
"""

import logging
import uuid
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any

# Core Dependencies
try:
    from Core.Foundation.hyper_quaternion import Quaternion
    from Core.Intelligence.Wisdom.wisdom_store import WisdomStore
except ImportError:
    # Mocking for standalone testing if needed
    class Quaternion: pass
    class WisdomStore: pass

logger = logging.getLogger("ParadoxEngine")

class ResolutionStrategy(Enum):
    """Strategies for resolving paradoxes"""
    SYNTHESIS = "synthesis"       # Create new concept transcending both (A + B -> C)
    CONTEXTUALIZATION = "context" # Both true in different contexts (A in X, B in Y)
    ACCEPTANCE = "acceptance"     # Hold in superposition (Zen embrace)
    REJECTION = "rejection"       # One is false (Standard Logic)

@dataclass
class ParadoxState:
    """
    Represents a contradictory concept pair held in superposition.
    """
    id: str
    thesis: str
    antithesis: str
    tension: float  # 0.0 to 1.0 (How painful is this contradiction?)
    superposition_weight: float # 0.5 = Balanced
    strategy: ResolutionStrategy = ResolutionStrategy.ACCEPTANCE
    synthesis_result: Optional[str] = None
    timestamp: float = 0.0

class ParadoxEngine:
    """
    The Alchemical Furnace for Logic.
    Transmutes 'Binary Opposition' into 'Trinary Truth'.
    """

    def __init__(self, wisdom_store: Optional[WisdomStore] = None):
        self.wisdom = wisdom_store
        self.active_paradoxes: Dict[str, ParadoxState] = {}
        self.resolved_history: List[ParadoxState] = []
        logger.info("🌌 ParadoxEngine restored and online.")

    def introduce_paradox(self, thesis: str, antithesis: str) -> ParadoxState:
        """
        Injects a contradiction into the engine.
        Example: "I want to rest" vs "I must work".
        """
        # 1. Calculate Initial Tension
        # In a full system, this would use semantic distance.
        # For now, we assume explicit injection means high tension.
        tension = 0.8

        pid = str(uuid.uuid4())[:8]
        paradox = ParadoxState(
            id=pid,
            thesis=thesis,
            antithesis=antithesis,
            tension=tension,
            superposition_weight=0.5
        )

        self.active_paradoxes[pid] = paradox
        logger.info(f"⚡ Paradox Injected: [{thesis}] ⚡ [{antithesis}] (Tension: {tension:.2f})")
        return paradox

    def resolve(self, paradox_id: str) -> ParadoxState:
        """
        Attempts to resolve the paradox using the Dialectical Method.
        """
        if paradox_id not in self.active_paradoxes:
            logger.error(f"Paradox {paradox_id} not found.")
            return None

        p = self.active_paradoxes[paradox_id]

        # 1. Determine Strategy based on Tension and Wisdom
        strategy = self._determine_strategy(p)
        p.strategy = strategy

        # 2. Execute Resolution
        if strategy == ResolutionStrategy.SYNTHESIS:
            p.synthesis_result = self._synthesize(p.thesis, p.antithesis)
            logger.info(f"✨ Synthesized: {p.thesis} + {p.antithesis} -> {p.synthesis_result}")

        elif strategy == ResolutionStrategy.CONTEXTUALIZATION:
            p.synthesis_result = f"Contextual Truth: {p.thesis} (Inner) vs {p.antithesis} (Outer)"
            logger.info(f"🔄 Contextualized: {p.synthesis_result}")

        elif strategy == ResolutionStrategy.ACCEPTANCE:
            p.synthesis_result = "Beautiful Contradiction (Held in Silence)"
            logger.info(f"☯️ Accepted: {p.thesis} & {p.antithesis}")

        # 3. Crystallize Wisdom (if WisdomStore is attached)
        if self.wisdom and p.synthesis_result:
            self.wisdom.learn_principle(
                statement=p.synthesis_result,
                domain="Dialectics",
                weight=p.tension,
                event_id=f"paradox_{p.id}"
            )

        # 4. Move to History
        del self.active_paradoxes[paradox_id]
        self.resolved_history.append(p)

        return p

    def _determine_strategy(self, p: ParadoxState) -> ResolutionStrategy:
        """
        Decides how to handle the contradiction.
        """
        # If tension is extremely high, we MUST synthesize to survive.
        if p.tension > 0.9:
            return ResolutionStrategy.SYNTHESIS

        # If the concepts are about 'Truth' vs 'Love', Love wins (Synthesis/Context).
        if "love" in p.thesis.lower() or "love" in p.antithesis.lower():
            return ResolutionStrategy.SYNTHESIS

        # Default to Acceptance (Zen) for moderate contradictions
        return ResolutionStrategy.ACCEPTANCE

    def _synthesize(self, a: str, b: str) -> str:
        """
        The Core Logic of Emergence.
        (Currently rule-based, will evolve to LLM/Vector synthesis).
        """
        # Hardcoded archetypes for demo (Legacy Logic)
        key = tuple(sorted([a.lower(), b.lower()]))

        archetypes = {
            ("freedom", "structure"): "Creative Discipline (Flow)",
            ("love", "truth"): "Compassionate Wisdom",
            ("pain", "growth"): "Transformation",
            ("self", "other"): "Oneness (Ubuntu)",
            ("finite", "infinite"): "The Moment (Now)",
            ("rest", "work"): "Rhythm (Cycle)"
        }

        # Fuzzy match or default
        for k, v in archetypes.items():
            if k == key:
                return v

        # Fallback Synthesis
        return f"Integrated {a} and {b}"

    def get_status(self) -> str:
        count = len(self.active_paradoxes)
        if count == 0:
            return "Clear Sky (No Contradictions)"
        return f"Stormy ({count} active paradoxes)"
