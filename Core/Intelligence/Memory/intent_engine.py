from dataclasses import dataclass, asdict

from typing import Any, Dict, List, Optional



from architecture.context import ConversationContext

from core_memory import CoreMemory

from emotional_engine import EmotionalState



from dialogue_law_evaluator import DialogueLawEvaluator





@dataclass

class IntentBundle:

    """

    Minimal "present intention" snapshot for one turn.



    This is not a command; it is a compact description of how

    Elysia currently orients toward the partner and the laws.

    """



    target: str

    emotion: str

    intent_type: str

    style: str

    relationship: str

    law_focus: List[str]



    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)





class IntentEngine:

    """

    Lightweight E–S–L style engine that summarizes the present

    conversational state into an IntentBundle.



    This does not change behavior on its own; it only produces a

    structured view that other modules (or caretakers) can inspect.

    """



    def __init__(

        self,

        core_memory: CoreMemory,

        dialogue_law_evaluator: Optional[DialogueLawEvaluator] = None,

    ) -> None:

        self.core_memory = core_memory

        self.dialogue_law_evaluator = dialogue_law_evaluator



    def build_intent_bundle(

        self,

        user_message: str,

        response: Dict[str, Any],

        conversation_context: ConversationContext,

        emotional_state: EmotionalState,

    ) -> IntentBundle:

        """

        Build a single-turn IntentBundle from the current message,

        response, context, and emotional state.

        """

        # --- Target / relationship (very minimal heuristics for now) ---

        target = "user"

        if getattr(conversation_context, "pending_hypothesis", None):

            target = "caretaker"



        relationship = "ally"



        # --- Emotion and style ---

        emotion = getattr(emotional_state, "primary_emotion", "") or "neutral"

        style = "conversational"



        # --- Law focus: derive from existing law_alignment if present ---

        law_info = response.get("law_alignment")

        scores: Dict[str, float] = {}

        if isinstance(law_info, dict):

            scores = law_info.get("scores", {}) or {}



        law_focus: List[str] = []

        if scores:

            # Take the top 2 positive axes as focus.

            sorted_axes = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

            for axis, score in sorted_axes:

                if score <= 0:

                    continue

                law_focus.append(f"+{axis}")

                if len(law_focus) >= 2:

                    break



        intent_type = "respond"



        return IntentBundle(

            target=target,

            emotion=emotion,

            intent_type=intent_type,

            style=style,

            relationship=relationship,

            law_focus=law_focus,

        )



