from __future__ import annotations



from dataclasses import dataclass, asdict

from typing import Any, Dict, List, Optional



from core_memory import CoreMemory, Experience, EmotionalState





@dataclass

class DialogueSelfModel:

    """

    Lightweight self-view of Elysia's recent dialogue behavior.



    This is a higher-scale summary over many dialogue_turn experiences:

    - how feelings have tended to move,

    - which laws are usually emphasized,

    - which intent types and law_focus axes recur.

    """



    avg_valence: float

    dominant_emotions: List[str]

    law_bias: Dict[str, float]

    dominant_law_focus: List[str]

    dominant_intent_types: List[str]



    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)





def _extract_law_scores(exp: Experience) -> Dict[str, float]:

    raw = getattr(exp, "law_alignment", None) or {}

    scores = raw.get("scores") or {}

    if not isinstance(scores, dict):

        return {}

    clean: Dict[str, float] = {}

    for key, value in scores.items():

        try:

            clean[str(key)] = float(value)

        except (TypeError, ValueError):

            continue

    return clean





def _extract_intent(exp: Experience) -> Dict[str, Any]:

    intent = getattr(exp, "intent_bundle", None) or {}

    if not isinstance(intent, dict):

        return {}

    return intent





def build_dialogue_self_model(core_memory: CoreMemory, max_events: int = 200) -> Optional[DialogueSelfModel]:

    """

    Build a DialogueSelfModel from recent dialogue_turn experiences.



    This is intended to run occasionally (not every turn) as a higher-scale

    meta-view over Elysia's recent conversations.

    """

    experiences: List[Experience] = core_memory.get_experiences(max_events)

    dialogue_events: List[Experience] = [

        exp for exp in experiences if getattr(exp, "type", "") == "dialogue_turn"

    ]

    if not dialogue_events:

        return None



    # --- Aggregate valence and primary emotions ---

    total_valence = 0.0

    emotion_counts: Dict[str, int] = {}

    for exp in dialogue_events:

        emo: Optional[EmotionalState] = getattr(exp, "emotional_state", None)

        if emo is None:

            continue

        total_valence += getattr(emo, "valence", 0.0)

        name = getattr(emo, "primary_emotion", "") or "neutral"

        emotion_counts[name] = emotion_counts.get(name, 0) + 1



    count_for_avg = max(len(dialogue_events), 1)

    avg_valence = total_valence / count_for_avg



    dominant_emotions = sorted(

        emotion_counts.items(),

        key=lambda kv: kv[1],

        reverse=True,

    )

    dominant_emotions = [name for name, _ in dominant_emotions[:3]]



    # --- Aggregate law scores ---

    law_sums: Dict[str, float] = {}

    for exp in dialogue_events:

        scores = _extract_law_scores(exp)

        for axis, value in scores.items():

            law_sums[axis] = law_sums.get(axis, 0.0) + value



    # Normalize by number of events for a rough bias estimate.

    law_bias: Dict[str, float] = {}

    if dialogue_events and law_sums:

        denom = float(len(dialogue_events))

        for axis, total in law_sums.items():

            law_bias[axis] = total / denom



    # --- Aggregate intent types and law_focus ---

    intent_type_counts: Dict[str, int] = {}

    law_focus_counts: Dict[str, int] = {}



    for exp in dialogue_events:

        intent = _extract_intent(exp)

        itype = str(intent.get("intent_type") or "").strip()

        if itype:

            intent_type_counts[itype] = intent_type_counts.get(itype, 0) + 1



        focus = intent.get("law_focus") or []

        if isinstance(focus, list):

            for axis in focus:

                axis_str = str(axis).strip()

                if axis_str:

                    law_focus_counts[axis_str] = law_focus_counts.get(axis_str, 0) + 1



    dominant_intent_types = sorted(

        intent_type_counts.items(),

        key=lambda kv: kv[1],

        reverse=True,

    )

    dominant_intent_types = [name for name, _ in dominant_intent_types[:3]]



    dominant_law_focus = sorted(

        law_focus_counts.items(),

        key=lambda kv: kv[1],

        reverse=True,

    )

    dominant_law_focus = [axis for axis, _ in dominant_law_focus[:3]]



    return DialogueSelfModel(

        avg_valence=avg_valence,

        dominant_emotions=dominant_emotions,

        law_bias=law_bias,

        dominant_law_focus=dominant_law_focus,

        dominant_intent_types=dominant_intent_types,

    )



