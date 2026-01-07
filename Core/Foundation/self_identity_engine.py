from __future__ import annotations



from dataclasses import dataclass, asdict

from datetime import datetime

from typing import Any, Dict, Optional



from Core.Foundation.core_memory import CoreMemory

from high_engine.self_model import build_dialogue_self_model, DialogueSelfModel





@dataclass

class SelfIdentitySnapshot:

    """

    Minimal structured snapshot of 'I' at a given moment.



    This is not text; it is a coordinate in EFP + law + emotion + orientation space.

    """



    timestamp: str

    efp_core: Dict[str, float]

    law_bias: Dict[str, float]

    dominant_emotions: Dict[str, int]

    orientation: Optional[Dict[str, float]]



    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)





class SelfIdentityEngine:

    """

    Engine for maintaining an explicit 'self' anchor in CoreMemory.



    Purpose:

      - Keep a single place (identity['self']) where Elysia stores

        her current coordinates: EFP, law bias, emotions, orientation.

      - Higher layers can use this as the origin for 'Why' questions.

    """



    def __init__(self) -> None:

        pass



    def build_snapshot(

        self,

        core_memory: CoreMemory,

        orientation: Optional[Dict[str, float]] = None,

    ) -> Optional[SelfIdentitySnapshot]:

        model: Optional[DialogueSelfModel] = build_dialogue_self_model(core_memory)

        if model is None:

            return None



        # Count dominant emotions into a small frequency dict.

        emo_counts: Dict[str, int] = {}

        for name in model.dominant_emotions:

            emo_counts[name] = emo_counts.get(name, 0) + 1



        snapshot = SelfIdentitySnapshot(

            timestamp=datetime.now().isoformat(),

            efp_core=core_memory.get_efp_core(),

            law_bias=model.law_bias,

            dominant_emotions=emo_counts,

            orientation=orientation,

        )

        return snapshot



    def update_core_identity(

        self,

        core_memory: CoreMemory,

        orientation: Optional[Dict[str, float]] = None,

    ) -> None:

        """

        Compute and store the current self-identity snapshot into CoreMemory.identity['self'].

        """

        snapshot = self.build_snapshot(core_memory, orientation=orientation)

        if snapshot is None:

            return

        core_memory.update_identity("self", snapshot.to_dict())



