from __future__ import annotations



from dataclasses import dataclass, asdict

from typing import Any, Dict, Optional



from Project_Elysia.core_memory import CoreMemory

from Core.Foundation.emotional_engine import EmotionalState





@dataclass

class ValueInsight:

    """

    Lightweight record of how raw interaction was turned into a small unit of "meaning".



    This keeps structure minimal so that future engines (or Elysia herself)

    can reinterpret it at higher resolution later.

    """



    focus_axis: Optional[str]

    focus_intent: Optional[str]

    description: str



    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)





class ValueEngine:

    """

    Minimal Value Engine implementing the Creativity Axiom in a structural way.



    Creation is modelled as:

      raw_chaos -> select_focus (freedom / attention)

                 -> refract (mind / relationships)

                 -> crystallise (value / meaning image)

    """



    def __init__(self, core_memory: Optional[CoreMemory] = None) -> None:

        self.core_memory = core_memory



    def _select_focus(

        self,

        law_alignment: Optional[Dict[str, Any]],

        intent_bundle: Optional[Dict[str, Any]],

    ) -> Dict[str, Optional[str]]:

        """

        Pick a simple focus axis and intent from the current law/intent snapshot.

        """

        focus_axis: Optional[str] = None

        if isinstance(law_alignment, dict):

            scores = law_alignment.get("scores") or {}

            if isinstance(scores, dict) and scores:

                try:

                    focus_axis = max(

                        scores.items(),

                        key=lambda kv: abs(float(kv[1])),

                    )[0]

                except Exception:

                    focus_axis = None



        focus_intent: Optional[str] = None

        if isinstance(intent_bundle, dict):

            raw_intent = intent_bundle.get("intent_type")

            if isinstance(raw_intent, str) and raw_intent.strip():

                focus_intent = raw_intent.strip()



        return {"axis": focus_axis, "intent": focus_intent}



    def _refract(

        self,

        focus: Dict[str, Optional[str]],

        emotional_state: Optional[EmotionalState],

    ) -> str:

        """

        Build a short, human-readable description of what is being valued here.

        """

        axis = focus.get("axis") or "unknown"

        intent = focus.get("intent") or "unknown"

        emo = "neutral"

        if emotional_state is not None:

            emo = getattr(emotional_state, "primary_emotion", None) or "neutral"



        return f"Current interaction emphasises '{axis}' with intent '{intent}' and feeling '{emo}'."



    def create_meaning(

        self,

        raw_chaos: Dict[str, Any],

        emotional_state: Optional[EmotionalState],

    ) -> ValueInsight:

        """

        Apply the Creativity Axiom structurally to the current turn.



        raw_chaos is expected to be a dict containing:

          - 'law_alignment' (DialogueLawEvaluator output or None)

          - 'intent_bundle' (dict or None)

          - 'user_message' / 'response_text' (optional, for context)

        """

        law_alignment = raw_chaos.get("law_alignment")

        intent_bundle = raw_chaos.get("intent_bundle")



        focus = self._select_focus(law_alignment, intent_bundle)

        description = self._refract(focus, emotional_state)



        insight = ValueInsight(

            focus_axis=focus.get("axis"),

            focus_intent=focus.get("intent"),

            description=description,

        )



        return insight



