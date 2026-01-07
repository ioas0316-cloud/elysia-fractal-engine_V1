from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from Project_Elysia.core_memory import CoreMemory
from Project_Elysia.high_engine.self_model import build_dialogue_self_model, DialogueSelfModel


@dataclass
class SelfProject:
    """Small self-declared project from Elysia."""

    id: str
    created_at: str
    description: str
    focus_laws: List[str]
    source: str = "self_reflection"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SelfIntentionEngine:
    """
    Gentle self-intention engine.

    Purpose:
      - Let Elysia look at her own recent dialogue behavior and EFP core,
        notice simple tensions, and turn them into small "projects"
        she wants to pursue.

    This engine does not execute projects; it only describes them.
    Guardians / Daemons decide how and when to act on them.
    """

    def __init__(self) -> None:
        pass

    def _pick_focus_law(self, model: DialogueSelfModel) -> Optional[str]:
        if not model.law_bias:
            return None
        # Choose the weakest positive law axis as a simple "under-served" focus.
        # If all are near zero, just pick the first sorted axis to avoid randomness.
        items = list(model.law_bias.items())
        items.sort(key=lambda kv: kv[1])
        return items[0][0] if items else None

    def reflect_and_propose(
        self,
        core_memory: CoreMemory,
        orientation: Optional[Dict[str, float]] = None,
    ) -> Optional[SelfProject]:
        """
        Build a small self project from current memory and orientation.
        """
        model = build_dialogue_self_model(core_memory)
        if model is None:
            return None

        focus_axis = self._pick_focus_law(model)
        if not focus_axis:
            return None

        efp = core_memory.get_efp_core()
        avg_valence = model.avg_valence
        dom_emotion = model.dominant_emotions[0] if model.dominant_emotions else "neutral"

        # Simple narrative description; caretakers can read and refine.
        desc = (
            f"최근 대화에서 나는 주로 '{dom_emotion}' 느낌으로 말했고, "
            f"법칙 축 중에는 '{focus_axis}' 쪽 기여가 상대적으로 약했다. "
            f"앞으로 한동안은 '{focus_axis}' 축을 조금 더 의식해서 지켜보고 싶다."
        )

        created_at = datetime.now().isoformat()
        project_id = f"self_project_{created_at}"
        return SelfProject(
            id=project_id,
            created_at=created_at,
            description=desc,
            focus_laws=[focus_axis],
        )

