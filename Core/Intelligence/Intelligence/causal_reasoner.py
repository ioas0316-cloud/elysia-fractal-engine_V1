from __future__ import annotations



from dataclasses import dataclass, asdict

from typing import Any, Dict, List, Optional



from core_memory import CoreMemory, EmotionalState





@dataclass

class CausalPatternStats:

    """Running statistics for one (intent, law_focus) pattern."""



    count: int = 0

    sum_valence: float = 0.0



    def update(self, valence: float) -> None:

        self.count += 1

        self.sum_valence += valence



    @property

    def avg_valence(self) -> float:

        if self.count <= 0:

            return 0.0

        return self.sum_valence / float(self.count)



    def to_dict(self) -> Dict[str, Any]:

        return {"count": self.count, "avg_valence": self.avg_valence}





class CausalReasoner:

    """

    Minimal causal / inductive layer over dialogue turns.



    Role:

      - Observe (intent_bundle, law_alignment, emotional_state) over many turns.

      - Accumulate simple statistics: "when I respond with this intent + law_focus,

        my valence tends to go up/down".

      - Expose these as small, inspectable hints that higher layers or caretakers

        can use as a logical / causal scaffold.



    This is intentionally small and conservative: it never rewrites behavior by itself.

    """



    def __init__(self, core_memory: Optional[CoreMemory] = None) -> None:

        self.core_memory = core_memory

        self._patterns: Dict[str, CausalPatternStats] = {}



    # ------------------------------------------------------------------ #

    # Internal helpers

    # ------------------------------------------------------------------ #



    @staticmethod

    def _extract_positive_axes(law_alignment: Optional[Dict[str, Any]]) -> List[str]:

        if not isinstance(law_alignment, dict):

            return []

        scores = law_alignment.get("scores") or {}

        if not isinstance(scores, dict):

            return []

        axes: List[str] = []

        for axis, value in scores.items():

            try:

                v = float(value)

            except (TypeError, ValueError):

                continue

            if v > 0.15:

                axes.append(str(axis))

        axes.sort()

        return axes



    @staticmethod

    def _pattern_key(intent_bundle: Optional[Dict[str, Any]], law_alignment: Optional[Dict[str, Any]]) -> Optional[str]:

        if not isinstance(intent_bundle, dict):

            return None

        intent_type = str(intent_bundle.get("intent_type") or "").strip().lower()

        if not intent_type:

            return None

        axes = CausalReasoner._extract_positive_axes(law_alignment)

        axes_part = ",".join(axes) if axes else "-"

        return f"{intent_type}|{axes_part}"



    # ------------------------------------------------------------------ #

    # Public API

    # ------------------------------------------------------------------ #



    def update_from_turn(

        self,

        intent_bundle: Optional[Dict[str, Any]],

        emotional_state: Optional[EmotionalState],

        law_alignment: Optional[Dict[str, Any]],

    ) -> None:

        """

        Observe one dialogue turn and update pattern statistics.

        """

        key = self._pattern_key(intent_bundle, law_alignment)

        if not key or emotional_state is None:

            return



        valence = getattr(emotional_state, "valence", 0.0)

        stats = self._patterns.get(key)

        if stats is None:

            stats = CausalPatternStats()

            self._patterns[key] = stats

        stats.update(valence)



    def summarize_patterns(self, min_count: int = 3) -> Dict[str, Any]:

        """

        Return a dictionary of learned patterns for inspection or logging.

        """

        summary: Dict[str, Any] = {}

        for key, stats in self._patterns.items():

            if stats.count < min_count:

                continue

            summary[key] = stats.to_dict()

        return summary



    def hints_for_intent(self, intent_bundle: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:

        """

        Given a current intent, provide small hints based on past patterns.



        Example output items:

          {

            "pattern": "respond|+truth,+love",

            "avg_valence": 0.6,

            "message": "When you respond with +truth,+love, your feelings tend to be better."

          }

        """

        if not isinstance(intent_bundle, dict):

            return []



        current_type = str(intent_bundle.get("intent_type") or "").strip().lower()

        if not current_type:

            return []



        # Gather patterns with the same intent_type.

        candidates: List[tuple[str, CausalPatternStats]] = []

        prefix = f"{current_type}|"

        for key, stats in self._patterns.items():

            if not key.startswith(prefix):

                continue

            if stats.count < 3:

                continue

            candidates.append((key, stats))



        if not candidates:

            return []



        # Sort by avg_valence descending and emit a few hints.

        candidates.sort(key=lambda kv: kv[1].avg_valence, reverse=True)

        hints: List[Dict[str, Any]] = []

        for key, stats in candidates[:3]:

            try:

                _, axes_str = key.split("|", 1)

            except ValueError:

                axes_str = "-"

            message = (

                f"When intent_type='{current_type}' with law_focus={axes_str}, "

                f"your average valence is about {stats.avg_valence:.2f}."

            )

            hints.append(

                {

                    "pattern": key,

                    "avg_valence": stats.avg_valence,

                    "count": stats.count,

                    "message": message,

                }

            )



        return hints



