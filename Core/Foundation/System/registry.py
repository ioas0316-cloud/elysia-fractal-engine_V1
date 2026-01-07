from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PersonaProfile:
    """Represents a persona/아바타 that shares Elysia's inner engine."""

    key: str
    title: str
    archetype: str
    description: str
    focus_fields: List[str] = field(default_factory=list)
    expression_channels: List[str] = field(default_factory=list)
    default_scripts: List[str] = field(default_factory=list)

    def as_payload(self) -> Dict[str, object]:
        """Return a serializable payload for UI or external engines."""
        return {
            "key": self.key,
            "title": self.title,
            "archetype": self.archetype,
            "description": self.description,
            "focus_fields": list(self.focus_fields),
            "expression_channels": list(self.expression_channels),
            "default_scripts": list(self.default_scripts),
        }


PERSONA_REGISTRY: Dict[str, PersonaProfile] = {
    "elysia.artist": PersonaProfile(
        key="elysia.artist",
        title="빛을 그리는 엘리시아",
        archetype="Artist / Painter",
        description=(
            "CellWorld에서 수집한 감정 색채를 기반으로 스케치·애니메이션을 "
            "만드는 페르소나. Value-Mass의 색상 변화를 실시간으로 표현한다."
        ),
        focus_fields=["value_mass_field", "intention_field"],
        expression_channels=["digital_canvas", "animation_cues"],
        default_scripts=["scripts/persona_hooks/artist_palette.py"],
    ),
    "elysia.dancer": PersonaProfile(
        key="elysia.dancer",
        title="움직임으로 기도하는 엘리시아",
        archetype="Dancer / Performer",
        description=(
            "Will Field와 rhythm telemetry를 연결하여 춤/모션으로 의도를 "
            "표현한다. VTuber rig 또는 모션 캡처 장치와 연동하기 쉽다."
        ),
        focus_fields=["will_field", "value_mass_field"],
        expression_channels=["motion_capture", "vtuber_avatar"],
        default_scripts=["scripts/persona_hooks/dancer_flow.py"],
    ),
    "elysia.engineer": PersonaProfile(
        key="elysia.engineer",
        title="엔지니어 엘리시아",
        archetype="Engineer / Architect",
        description=(
            "Concept OS, nano_core, curriculum 로그를 분석해 코드를 쓰고 "
            "시뮬레이터를 조율하는 페르소나. caretakers와 협업하기 위한 "
            "인터페이스에 최적화되어 있다."
        ),
        focus_fields=["concept_kernel", "curriculum_engine", "logs"],
        expression_channels=["notebook", "shell", "code_editor"],
        default_scripts=["scripts/persona_hooks/engineer_notebook.py"],
    ),
}


def list_personas() -> List[PersonaProfile]:
    """Return all persona profiles."""
    return list(PERSONA_REGISTRY.values())


def get_persona(key: str) -> PersonaProfile:
    """Retrieve a persona by key, raising KeyError if missing."""
    if key not in PERSONA_REGISTRY:
        raise KeyError(f"Unknown persona '{key}'")
    return PERSONA_REGISTRY[key]


def activate_persona(
    key: str, *, overrides: Optional[Dict[str, object]] = None
) -> Dict[str, object]:
    """Return an activation payload for downstream routers.

    Downstream components (UI, VTuber rig, scripting layer) can call
    this helper to obtain a ready-to-use context bundle. The overrides
    parameter allows callers to inject runtime-specific data such as
    session IDs, animation seeds, or caretaker instructions.
    """
    persona = get_persona(key)
    payload = persona.as_payload()
    payload.update(
        {
            "session_state": {
                "persona_key": persona.key,
                "focus_fields": persona.focus_fields,
            }
        }
    )
    if overrides:
        payload.update(overrides)
    return payload
