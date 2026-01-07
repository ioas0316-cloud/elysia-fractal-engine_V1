from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Union

from .feeling_buffer import ElysiaFeelingBuffer, FeelingState
from .needs_model import HumanNeeds
from .value_climate import ValueClimate


FeelingsInput = Union[None, Mapping[str, float], FeelingState, ElysiaFeelingBuffer]
NeedsInput = Union[None, Mapping[str, float], HumanNeeds]
ClimateInput = Union[None, Mapping[str, float], ValueClimate]


@dataclass
class RelationState:
    """
    Soft relation snapshot for one counterpart (for now, at least "creator").

    Values are in [0,1] where higher ~ stronger / more intense.
    """

    trust: float = 0.0
    closeness: float = 0.0
    playfulness: float = 0.0
    awe: float = 0.0

    def as_dict(self) -> Dict[str, float]:
        return {
            "trust": float(self.trust),
            "closeness": float(self.closeness),
            "playfulness": float(self.playfulness),
            "awe": float(self.awe),
        }


@dataclass
class SoulProject:
    """
    Minimal representation of an inner project Elysia is pursuing.

    Example IDs:
    - "worldtree_unification"
    - "invite_creator"
    - "refine_language"
    """

    id: str
    label: str
    progress: float = 0.0  # [0,1]
    importance: float = 1.0  # relative weight, typically [0,1] or [0,2]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "progress": float(self.progress),
            "importance": float(self.importance),
        }


@dataclass
class SoulState:
    """
    Reference shape for Elysia's "soul" snapshot.

    This is a soft state vector intended to be read by other engines
    (language, decision, visualization). It is not a rigid rule table.
    """

    mood: str = "neutral"
    feelings: Dict[str, float] = field(default_factory=dict)
    needs: Dict[str, float] = field(default_factory=dict)
    value_climate: Dict[str, float] = field(default_factory=dict)
    relations: Dict[str, RelationState] = field(default_factory=dict)
    projects: List[SoulProject] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "mood": self.mood,
            "feelings": {k: float(v) for k, v in self.feelings.items()},
            "needs": {k: float(v) for k, v in self.needs.items()},
            "value_climate": {k: float(v) for k, v in self.value_climate.items()},
            "relations": {name: rel.as_dict() for name, rel in self.relations.items()},
            "projects": [p.as_dict() for p in self.projects],
        }


def _feelings_to_dict(feelings: FeelingsInput, squash: bool = True) -> Dict[str, float]:
    """
    Normalize different feeling sources into a simple dict.
    """
    if feelings is None:
        return {}

    if isinstance(feelings, ElysiaFeelingBuffer):
        # Use squashed values by default so downstream consumers get [0,1].
        return feelings.squashed_state() if squash else feelings.current_state().as_dict()

    if isinstance(feelings, FeelingState):
        return feelings.as_dict()

    return {str(k): float(v) for k, v in dict(feelings).items()}


def _needs_to_dict(needs: NeedsInput) -> Dict[str, float]:
    if needs is None:
        return {}
    if isinstance(needs, HumanNeeds):
        return needs.as_dict()
    return {str(k): float(v) for k, v in dict(needs).items()}


def _climate_to_dict(climate: ClimateInput) -> Dict[str, float]:
    if climate is None:
        return {}
    if isinstance(climate, ValueClimate):
        return climate.as_dict()
    return {str(k): float(v) for k, v in dict(climate).items()}


def _infer_mood_from_feelings(feelings: Mapping[str, float]) -> str:
    """
    Very small heuristic to derive a mood key from analogue feelings.

    This is deliberately soft and should be treated as a hint, not a law.
    """
    if not feelings:
        return "neutral"

    joy = float(feelings.get("joy", 0.0))
    creation = float(feelings.get("creation", 0.0))
    care = float(feelings.get("care", 0.0))
    mortality = float(feelings.get("mortality", 0.0))

    # Simple ranking by dominant axis with a few named buckets.
    axes = {
        "joy": joy,
        "creation": creation,
        "care": care,
        "mortality": mortality,
    }
    dominant = max(axes.items(), key=lambda kv: kv[1])[0]

    if axes[dominant] <= 0.05:
        return "neutral"

    if dominant == "joy":
        return "joy"
    if dominant == "creation":
        return "curious"
    if dominant == "care":
        return "warm"
    if dominant == "mortality":
        # Could map to "blue" / "sad"; name is free for higher layers.
        return "blue"

    return "neutral"


def _relations_to_map(relations: Optional[Mapping[str, Mapping[str, float]]]) -> Dict[str, RelationState]:
    result: Dict[str, RelationState] = {}
    if relations:
        for name, raw in relations.items():
            r = RelationState(
                trust=float(raw.get("trust", 0.0)),
                closeness=float(raw.get("closeness", 0.0)),
                playfulness=float(raw.get("playfulness", 0.0)),
                awe=float(raw.get("awe", 0.0)),
            )
            result[str(name)] = r
    # Ensure a creator node exists at least with defaults.
    if "creator" not in result:
        result["creator"] = RelationState()
    return result


def _projects_to_list(projects: Optional[Iterable[Mapping[str, Any]]]) -> List[SoulProject]:
    result: List[SoulProject] = []
    if not projects:
        return result
    for p in projects:
        pid = str(p.get("id", "")).strip()
        label = str(p.get("label", "")).strip() or pid
        if not pid and not label:
            continue
        result.append(
            SoulProject(
                id=pid or label,
                label=label,
                progress=float(p.get("progress", 0.0)),
                importance=float(p.get("importance", 1.0)),
            )
        )
    return result


def build_soul_state(
    *,
    mood: Optional[str] = None,
    feelings: FeelingsInput = None,
    needs: NeedsInput = None,
    value_climate: ClimateInput = None,
    relations: Optional[Mapping[str, Mapping[str, float]]] = None,
    projects: Optional[Iterable[Mapping[str, Any]]] = None,
    squash_feelings: bool = True,
) -> SoulState:
    """
    Construct a SoulState from existing CORE vectors and optional extras.

    Typical usage:
    - Pass in an ElysiaFeelingBuffer (or squashed dict) for `feelings`.
    - Pass in a HumanNeeds instance for `needs` if a body/world is present.
    - Derive `value_climate` once using `compute_value_climate` and feed it here.
    - Optionally supply relation and project snapshots from higher layers.
    """
    feelings_dict = _feelings_to_dict(feelings, squash=squash_feelings)
    needs_dict = _needs_to_dict(needs)
    climate_dict = _climate_to_dict(value_climate)

    mood_key = mood or _infer_mood_from_feelings(feelings_dict)

    rel_map = _relations_to_map(relations)
    proj_list = _projects_to_list(projects)

    return SoulState(
        mood=mood_key,
        feelings=feelings_dict,
        needs=needs_dict,
        value_climate=climate_dict,
        relations=rel_map,
        projects=proj_list,
    )

