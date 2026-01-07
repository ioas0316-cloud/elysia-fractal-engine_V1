```python

import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

from Core.Intelligence.Topography.void_perceiver import VoidPerceiver
from Core.Intelligence.Topography.resonance_sphere import ResonanceSphere, ReflectionResult, ReflectionModality
from Core.Intelligence.Wisdom.wisdom_store import WisdomStore

logger = logging.getLogger("ReflectionLoop")

@dataclass
class ActionIntent:
    content: str
    modality: str = "text"
    target: str = "user"

@dataclass
class ReflectionVerdict:
    approved: bool
    reason: str
    adjusted_content: Optional[str] = None
    curiosity_score: float = 0.0

class ReflectionLoop:
    """
    The 'Conscience' of Elysia.
    Before any action is taken, it is projected onto the MirrorSurface.
    If the reflection is too distorted (High Tension), the action is paused or corrected.
    """

    def __init__(self, mirror: MirrorSurface):
        self.mirror = mirror
        # Golden Ratio of Tension: Not too boring (0.0), not too chaotic (1.0).
        self.min_tension = 0.05
        self.max_tension = 0.85

    def contemplate(self, intent: ActionIntent) -> ReflectionVerdict:
        """
        Reflects on the intended action before execution.
        """
        logger.info(f"🤔 Contemplating action: '{intent.content[:30]}...'")

        # 1. Project onto Mirror
        reflection: ReflectionResult = self.mirror.reflect(intent.content)

        # 2. Evaluate the Reflection
        return self._judge_reflection(reflection, intent)

    def _judge_reflection(self, reflection: ReflectionResult, intent: ActionIntent) -> ReflectionVerdict:
        score = reflection.curiosity_score

        # Case A: High Tension (Dissonance / Danger?)
        if score > self.max_tension:
            logger.warning(f"🛑 High Tension detected ({score:.2f}). Pausing action.")
            return ReflectionVerdict(
                approved=False,
                reason=f"The action creates too much dissonance ({score:.2f}) against my principles. {reflection.description}",
                curiosity_score=score
            )

        # Case B: Healthy Tension (Resonance / Curiosity)
        elif self.min_tension <= score <= self.max_tension:
            logger.info(f"✅ Action resonates well (Score: {score:.2f}).")
            return ReflectionVerdict(
                approved=True,
                reason=f"The action is balanced. {reflection.description}",
                curiosity_score=score
            )

        # Case C: Low Tension (Boredom / Repetition)
        else:
            # We approve it, but maybe note it's a bit "safe"
            logger.info(f"⚠️ Low Tension ({score:.2f}). Is this meaningful?")
            return ReflectionVerdict(
                approved=True,
                reason="The action is safe, perhaps too safe.",
                curiosity_score=score
            )
