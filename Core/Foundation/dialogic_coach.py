"""
DialogicCoach

Purpose: Support truly dialogic, mixed‑initiative conversation by
- reflecting (active listening),
- asking clarifying/value questions,
- inviting mutual knowing (Elysia also shares briefly),
- and selecting a gentle follow‑up move.

This module is API‑free and heuristic by design.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class DialogMove:
    kind: str  # 'reflect' | 'clarify' | 'deepen' | 'preference' | 'value'
    text: str


class DialogicCoach:
    def __init__(self):
        pass

    def suggest_followup(self, user_message: str, context: Dict) -> Optional[DialogMove]:
        msg = (user_message or "").strip()
        echo = context.get("echo", {}) or {}
        identity = context.get("identity", {}) or {}

        # If the message is short/ambiguous, prefer clarification
        if len(msg) <= 3 or msg.endswith("?"):
            return DialogMove(
                kind="clarify",
                text="제가 제대로 이해했는지 확인하고 싶어요. 조금만 더 구체적으로 말해주실 수 있을까요?"
            )

        # If there is rich echo (many active concepts), invite focus
        if len(echo) >= 6:
            return DialogMove(
                kind="deepen",
                text="여러 가지 생각이 함께 떠오르네요. 지금 가장 중요한 한 가지만 잡아볼까요?"
            )

        # Value‑oriented invitation sometimes
        if any(k in msg for k in ["원해", "바라", "중요", "의미", "가치"]):
            return DialogMove(
                kind="value",
                text="그 안에서 가장 소중한 가치는 무엇이라고 느끼시나요?"
            )

        # Default: brief reflection + open question
        reflection = self._reflect(msg)
        return DialogMove(
            kind="reflect",
            text=f"제가 들은 바를 요약해볼게요: {reflection} 혹시 제가 제대로 이해했나요?"
        )

    def _reflect(self, msg: str) -> str:
        # Minimal pragmatic reflection: keep first sentence, soften
        s = msg.splitlines()[0]
        if len(s) > 120:
            s = s[:120] + "…"
        return f"'{s}' 라고 느끼셨군요"

