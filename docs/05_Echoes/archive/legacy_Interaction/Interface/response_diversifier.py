from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import random
import re


@dataclass
class ResponseVariant:
    text: str
    style: str
    emotion_tone: float
    formality: float


class ResponseDiversifier:
    """
    Build lightweight stylistic variants for an assistant response by spotting
    common conversational concepts (greeting, gratitude, apology, encouragement)
    and weaving small narrative openers around them.  This keeps the behavior
    intentional instead of swapping tokens randomly.
    """

    CONCEPT_KEYWORDS: Dict[str, List[str]] = {
        "greeting": ["hello", "hi", "hey", "greetings", "nice to meet you"],
        "gratitude": ["thanks", "thank you", "appreciate it", "grateful"],
        "apology": ["sorry", "apologize", "my fault", "forgive me"],
        "encouragement": ["it's okay", "cheer up", "believe", "you can do it"],
    }

    FORMAL_OPENERS = {
        "default": "Greetings.",
        "gratitude": "It is a pleasure to express my gratitude.",
        "apology": "Please accept my sincere apology.",
    }

    FRIENDLY_OPENERS = {
        "default": "Hey!",
        "greeting": "Hey! It's great to see you.",
        "gratitude": "Thanks so much!",
    }

    SUPPORTIVE_TEMPLATES = [
        "I can imagine how complicated this might feel. {body}",
        "It's probably a tough moment. Even so, {body}",
    ]

    def __init__(self):
        self.recent_responses: List[str] = []
        self.max_history = 10
        self.similarity_threshold = 0.7

    def generate_variants(
        self, base_response: str, context: Optional[Dict[str, Any]] = None
    ) -> List[ResponseVariant]:
        context = context or {}
        base = base_response.strip()
        concepts = self._detect_concepts(base)
        variants: List[ResponseVariant] = []

        variants.append(
            ResponseVariant(
                text=self._ensure_sentence(base),
                style="neutral",
                emotion_tone=context.get("emotional_state", 0.0),
                formality=0.5,
            )
        )

        formal_text = self._apply_opening(
            base, concepts, template_map=self.FORMAL_OPENERS, default_key="default"
        )
        variants.append(
            ResponseVariant(
                text=self._ensure_sentence(formal_text),
                style="formal",
                emotion_tone=0.0,
                formality=0.9,
            )
        )

        friendly_text = self._apply_opening(
            base, concepts, template_map=self.FRIENDLY_OPENERS, default_key="default"
        )
        variants.append(
            ResponseVariant(
                text=self._ensure_sentence(friendly_text),
                style="friendly",
                emotion_tone=0.3,
                formality=0.2,
            )
        )

        if context.get("emotional_state", 0.0) < 0:
            supportive_text = random.choice(self.SUPPORTIVE_TEMPLATES).format(body=base)
            variants.append(
                ResponseVariant(
                    text=self._ensure_sentence(supportive_text),
                    style="supportive",
                    emotion_tone=0.6,
                    formality=0.4,
                )
            )

        if base.endswith("?"):
            clarifying = self._ensure_sentence(
                f"If I missed a nuance, let me check with you once more. {base}"
            )
            variants.append(
                ResponseVariant(
                    text=clarifying,
                    style="reflective",
                    emotion_tone=0.1,
                    formality=0.6,
                )
            )

        return variants

    def select_best_variant(
        self, variants: List[ResponseVariant], context: Optional[Dict[str, Any]] = None
    ) -> ResponseVariant:
        if not variants:
            return ResponseVariant(
                text="Even if my words stumble, know that I'm still here with you.",
                style="fallback",
                emotion_tone=0.0,
                formality=0.5,
            )

        context = context or {}
        relationship_level = context.get("relationship_level", 0.5)
        formality_preference = context.get("formality_preference", 0.5)
        emotional_state = context.get("emotional_state", 0.0)

        best_variant = variants[0]
        best_score = float("-inf")

        for variant in variants:
            formality_score = 1 - abs(formality_preference - variant.formality)
            emotion_score = 1 - abs(emotional_state - variant.emotion_tone)
            relationship_score = 1 - abs(relationship_level - (1 - variant.formality))
            total_score = (
                formality_score * 0.4 + emotion_score * 0.3 + relationship_score * 0.3
            )

            if self._is_too_similar(variant.text):
                total_score *= 0.5

            if total_score > best_score:
                best_score = total_score
                best_variant = variant

        return best_variant

    def update_history(self, response: str):
        normalized = self._normalize(response)
        if not normalized:
            return
        self.recent_responses.append(normalized)
        if len(self.recent_responses) > self.max_history:
            self.recent_responses.pop(0)

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #

    def _detect_concepts(self, text: str) -> List[str]:
        lowered = text.casefold()
        matches = [
            concept
            for concept, keywords in self.CONCEPT_KEYWORDS.items()
            if any(keyword.casefold() in lowered for keyword in keywords)
        ]
        if not matches and "?" in text:
            matches.append("question")
        return matches

    def _apply_opening(
        self,
        body: str,
        concepts: List[str],
        template_map: Dict[str, str],
        default_key: str,
    ) -> str:
        for concept in concepts:
            opener = template_map.get(concept)
            if opener:
                return f"{opener} {body}"
        opener = template_map.get(default_key, "")
        return f"{opener} {body}" if opener else body

    def _ensure_sentence(self, text: str) -> str:
        trimmed = text.strip()
        if not trimmed:
            return trimmed
        if trimmed[-1] in ".!?":
            return trimmed
        return f"{trimmed}."

    def _is_too_similar(self, response: str) -> bool:
        normalized = self._normalize(response)
        return any(
            self._calculate_similarity(normalized, previous) > self.similarity_threshold
            for previous in self.recent_responses
        )

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        words1 = {token for token in text1.split() if len(token) > 1}
        words2 = {token for token in text2.split() if len(token) > 1}
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union)

    def _normalize(self, text: str) -> str:
        letters_only = re.sub(r"[^\w\s]", " ", text).lower()
        return re.sub(r"\s+", " ", letters_only).strip()
