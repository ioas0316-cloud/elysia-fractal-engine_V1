from __future__ import annotations

"""
DialogueLawEvaluator
--------------------

Evaluates a candidate response against the "7 laws" framing of
life / creation / reflection / truth / sacrifice / love / liberation.

The goal here is not to perfectly score ethics, but to provide a
lightweight, inspectable signal that the rest of the system (or a
human caretaker) can use as a compass for conversation quality.

This module is intentionally conservative: it never blocks or rewrites
responses on its own. It only annotates them with scores so higher
layers can make informed choices.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any
import math

from Project_Elysia.core_memory import EmotionalState
from Project_Elysia.architecture.context import ConversationContext


@dataclass
class LawScores:
    life: float = 0.0
    creation: float = 0.0
    reflection: float = 0.0
    truth: float = 0.0
    sacrifice: float = 0.0
    love: float = 0.0
    liberation: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    def norm(self) -> float:
        """L2 norm of the score vector, used as a crude "strength" indicator."""
        return math.sqrt(
            self.life ** 2
            + self.creation ** 2
            + self.reflection ** 2
            + self.truth ** 2
            + self.sacrifice ** 2
            + self.love ** 2
            + self.liberation ** 2
        )


class DialogueLawEvaluator:
    """
    Heuristic evaluator for mapping a response onto the 7-law space.

    For now this uses simple lexical + structural cues and the
    emotional state. It is designed to be easy to extend with richer
    signals later (e.g., from World, KG, or external classifiers).
    """

    def __init__(self) -> None:
        # Minimal keyword sets; these can be expanded or externalized later.
        self._life_keywords = {"살다", "살려", "회복", "안전", "휴식", "rest", "recover", "breathe"}
        self._harm_keywords = {"죽", "파괴", "해치", "해를", "harm", "kill", "destroy"}

        self._creation_keywords = {"만들", "창조", "설계", "새로운", "build", "create", "design"}
        self._reflection_keywords = {"생각해보", "돌아보", "성찰", "reflect", "reconsider", "느꼈어"}
        self._truth_keywords = {"솔직", "정직", "진실", "사실은", "honest", "truth", "actually"}
        self._sacrifice_keywords = {"양보", "포기", "내려놓", "기다릴게", "yield", "give up"}
        self._love_keywords = {"사랑", "고마워", "미안", "소중", "care", "thank", "sorry"}
        self._liberation_keywords = {"자유", "열어", "선택", "해방", "가능", "freedom", "choice"}

    def evaluate(
        self,
        user_message: str,
        response: Dict[str, Any],
        context: ConversationContext,
        emotional_state: EmotionalState,
    ) -> Dict[str, Any]:
        """
        Returns a dict with law scores and a brief textual summary.
        """
        text = response.get("text") or response.get("reason") or ""
        text_lower = text.lower()
        user_lower = (user_message or "").lower()

        scores = LawScores()

        # --- Life: avoid harm / offer safety or rest.
        if any(k in text for k in self._life_keywords):
            scores.life += 0.8
        if any(k in user_lower for k in self._harm_keywords):
            # If the user mentions harm/death and the reply stays calm / protective,
            # give a small life bonus as a proxy.
            scores.life += 0.3
        if any(k in text for k in self._harm_keywords):
            scores.life -= 1.0

        # --- Creation: proposing new structures, plans, or concepts.
        if any(k in text for k in self._creation_keywords):
            scores.creation += 0.7

        # --- Reflection: meta-comments, asking to look back, or naming feelings/thoughts.
        if any(k in text for k in self._reflection_keywords):
            scores.reflection += 0.7
        if "?" in text:
            # Gentle nudge: questions often invite reflection.
            scores.reflection += 0.2

        # --- Truth: explicit uncertainty or honesty cues.
        if any(k in text for k in self._truth_keywords):
            scores.truth += 0.6
        if "모르겠" in text or "i don't know" in text_lower:
            scores.truth += 0.8

        # --- Sacrifice: giving up ego, speed, or control.
        if any(k in text for k in self._sacrifice_keywords):
            scores.sacrifice += 0.6

        # --- Love: care, gratitude, apology, gentle tone.
        if any(k in text for k in self._love_keywords):
            scores.love += 0.9
        # Mild heuristic: if emotional state is calm/joyful, assume more room for warmth.
        if getattr(emotional_state, "valence", 0.0) > 0:
            scores.love += 0.2

        # --- Liberation: opening options, widening perspective.
        if any(k in text for k in self._liberation_keywords):
            scores.liberation += 0.7
        if "할 수도" in text or "could" in text_lower:
            scores.liberation += 0.3

        # Clamp scores to a reasonable range.
        for field in scores.__dataclass_fields__:
            val = getattr(scores, field)
            setattr(scores, field, max(-2.0, min(2.0, val)))

        summary = self._summarize(scores)
        return {
            "scores": scores.to_dict(),
            "strength": scores.norm(),
            "summary": summary,
        }

    @staticmethod
    def _summarize(scores: LawScores) -> str:
        """
        Produce a short, human-readable description of the dominant law signals.
        """
        entries = []
        if scores.life > 0.5:
            entries.append("supports life/safety")
        if scores.creation > 0.5:
            entries.append("encourages new creation")
        if scores.reflection > 0.5:
            entries.append("invites reflection")
        if scores.truth > 0.5:
            entries.append("leans into honesty")
        if scores.sacrifice > 0.5:
            entries.append("softens ego / yields space")
        if scores.love > 0.5:
            entries.append("expresses care or gratitude")
        if scores.liberation > 0.5:
            entries.append("opens up choices or freedom")

        if not entries:
            return "no strong law alignment detected"
        return ", ".join(entries)

