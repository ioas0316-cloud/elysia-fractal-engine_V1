"""

Agency Orchestrator



Infers and performs small autonomous actions aligned with values and context,

without external APIs. Keeps decisions simple, transparent, and reversible.

"""

from __future__ import annotations



from dataclasses import dataclass

from datetime import datetime

from pathlib import Path

from typing import Dict, Any, Optional, Tuple

import random

import time



from core.action_memory import MemoryActionSelector



from Legacy.Project_Sophia.reading_coach import ReadingCoach

from Legacy.Project_Sophia.creative_writing_cortex import CreativeWritingCortex

from proof_renderer import ProofRenderer

from Legacy.Project_Sophia.math_cortex import MathCortex

from kg_manager import KGManager

from preferences import load_prefs, save_prefs, ensure_defaults

from kg_value_utils import add_value_relation, update_value_mass

from desire_state import DesireState

from decision_report import create_decision_report





@dataclass

class ProposedAction:

    kind: str  # 'journal' | 'creative' | 'math_verify'

    payload: Dict[str, Any]

    reason: str

    confidence: float = 0.5





class AgencyOrchestrator:

    def __init__(self):

        self.prefs = ensure_defaults(load_prefs())

        self.desire = DesireState()

        self.action_memory = MemoryActionSelector()



    def _auto_enabled(self) -> bool:

        return bool(self.prefs.get('auto_act', False))



    def _quiet(self) -> bool:

        return bool(self.prefs.get('quiet_mode', False))



    def _context_key(self) -> str:

        vec = self.desire.vec

        parts = [

            f"relatedness:{int(vec.relatedness * 100)}",

            f"clarity:{int(vec.clarity * 100)}",

            f"verifiability:{int(vec.verifiability * 100)}",

            f"creativity:{int(vec.creativity * 100)}",

            f"auto:{int(bool(self._auto_enabled()))}",

        ]

        return "|".join(parts)



    def _weight_action(self, action: ProposedAction) -> ProposedAction:

        weight = self.action_memory.memory_weight(action.kind, self._context_key())

        action.confidence = min(0.99, action.confidence * weight)

        return action



    def _cooldown_ok(self, kind: str) -> bool:

        from datetime import datetime, timezone

        last_map = self.prefs.get('last_action_ts', {}) or {}

        last_iso = last_map.get(kind)

        cooldowns = self.prefs.get('proposal_cooldowns', {}) or {}

        cd = int(cooldowns.get(kind, 1800))

        if not last_iso:

            return True

        try:

            last = datetime.fromisoformat(last_iso.replace('Z','+00:00'))

            now = datetime.now(timezone.utc)

            return (now - last).total_seconds() >= cd

        except Exception:

            return True



    def _stamp_action(self, kind: str) -> None:

        from datetime import datetime, timezone

        ts = datetime.now(timezone.utc).isoformat()

        self.prefs.setdefault('last_action_ts', {})[kind] = ts

        save_prefs(self.prefs)



    def _record_action_result(self, action: ProposedAction, info: Dict[str, Any]) -> None:

        success = bool(info.get("confidence", 0.0) >= 0.5)

        tick = int(time.time())

        self.action_memory.record_outcome(action.kind, self._context_key(), success, tick)



    def set_auto(self, enabled: bool) -> None:

        self.prefs['auto_act'] = bool(enabled)

        save_prefs(self.prefs)



    def infer_desire(self, message: str, echo: Dict[str, float], arousal: float) -> Optional[ProposedAction]:

        m = (message or '').lower()

        if self._quiet():

            return None

        min_arousal = float(self.prefs.get('min_arousal_for_proposal', 0.4))

        if arousal < min_arousal:

            return None



        def candidate(action: ProposedAction, cooldown: str) -> Optional[ProposedAction]:
            weighted = self._weight_action(action)
            return weighted if self._cooldown_ok(cooldown) else None

        # Journaling: invite short reflective writing about current thoughts/feelings.
        if any(
            k in m
            for k in [
                "diary",
                "journal",
                "write",
                "log",
                "record",
                "note",
            ]
        ):
            pa = ProposedAction(
                "journal",
                {},
                "Auto-suggestion: write a short reflective journal entry?",
                confidence=0.8,
            )
            return candidate(pa, "journal")

        # Creative writing: small story around growth or other themes.
        if any(
            k in m
            for k in [
                "story",
                "novel",
                "creative",
                "fiction",
                "write a story",
            ]
        ):
            pa = ProposedAction(
                "creative",
                {"genre": "story", "theme": "growth"},
                "Auto-suggestion: craft a small growth-themed story?",
                confidence=0.75,
            )
            return candidate(pa, "creative")

        # Math / proof verification.
        if "=" in m and any(k in m for k in ["=", "prove", "verify", "equation", "math"]):
            import re

            eq = re.search(r"([\d\s\+\-\*\/\(\)\.]+)=([\d\s\+\-\*\/\(\)\.]+)", message)
            if eq:
                pa = ProposedAction(
                    "math_verify",
                    {"statement": eq.group(0)},
                    "Auto-suggestion: verify this equation step by step?",
                    confidence=0.85,
                )
                return candidate(pa, "math_verify")

        # High arousal, rich echo signal: gentle nudge to journal.
        if arousal >= 0.8 and echo and len(echo) >= 6:
            pa = ProposedAction(
                "journal",
                {},
                "Auto-suggestion: your mind seems busy; try a short journal to settle your thoughts?",
                confidence=0.5,
            )
            return candidate(pa, "journal")


        return None



    def execute(self, action: ProposedAction) -> Tuple[str, Dict[str, Any]]:

        if action.kind == 'journal':

            result = self._do_journal()

        elif action.kind == 'creative':

            result = self._do_creative(action.payload)

        elif action.kind == 'math_verify':

            result = self._do_math_verify(action.payload)

        else:

            result = ("noop", {})

        self._record_action_result(action, result[1])

        return result



    def _do_journal(self) -> Tuple[str, Dict[str, Any]]:

        today = datetime.now().strftime("%Y-%m-%d")

        out_dir = Path("data/journal")

        out_dir.mkdir(parents=True, exist_ok=True)

        draft = f"[일기 {today}] 자율 반추: 오늘의 생각을 요약합니다."

        p_txt = out_dir / f"{today}_auto.txt"

        p_txt.write_text(draft, encoding="utf-8")

        coach = ReadingCoach()

        summary = coach.summarize_text(draft, max_sentences=1)

        p_sum = out_dir / f"{today}_auto_summary.txt"

        p_sum.write_text(summary, encoding="utf-8")

        kg = KGManager()

        node = f"journal_entry_{today}_auto"

        kg.add_node(node, properties={"type": "journal_entry", "date": today, "experience_text": str(p_txt), "summary_text": str(p_sum)})

        # Value link: journaling supports clarity/relatedness hypotheses

        add_value_relation(kg, node, "value:clarity", "supports", confidence=0.6, evidence_paths=[str(p_txt), str(p_sum)], note="reflection")

        add_value_relation(kg, node, "value:relatedness", "supports", confidence=0.4, evidence_paths=[str(p_txt)], note="self-connection")

        # Value mass (minimal): reinforce by support confidence, small decay

        update_value_mass(kg, "value:clarity", supports_inc=0.6, decay=0.01, note="journal_support")

        update_value_mass(kg, "value:relatedness", supports_inc=0.4, decay=0.01, note="journal_support")

        # decision report

        create_decision_report(

            kg,

            kind="journal",

            reason="short reflective journaling",

            confidence=0.6,

            result={"entry": str(p_txt), "summary": str(p_sum)},

            gains=["clarity", "self-connection"],

            tradeoffs=["time"],

            evidence_paths=[str(p_txt), str(p_sum)],

        )

        kg.save()

        # Reinforce desire state

        self.desire.reinforce({"clarity": 0.02, "relatedness": 0.01})

        self._stamp_action('journal')

        return "journal", {"entry": str(p_txt), "summary": str(p_sum), "confidence": 0.6}



    def _do_creative(self, payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:

        genre = payload.get('genre', 'story')

        theme = payload.get('theme', 'growth')

        cwc = CreativeWritingCortex()

        scenes = cwc.write_story(genre, theme, beats=4, words_per_scene=60)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        out_dir = Path("data/writings")

        out_dir.mkdir(parents=True, exist_ok=True)

        path = out_dir / f"auto_{ts}_{genre}_{theme}.md"

        lines = [f"# {genre.title()} — Theme: {theme}", "", "## Scenes"]

        for s in scenes:

            lines += [f"\n### {s.index}. {s.title}", s.content]

        path.write_text("\n".join(lines), encoding="utf-8")

        kg = KGManager()

        story_id = f"story_{ts}_auto"

        kg.add_node(story_id, properties={"type": "story", "genre": genre, "theme": theme, "path": str(path)})

        add_value_relation(kg, story_id, "value:creativity", "supports", confidence=0.65, evidence_paths=[str(path)], note="self-expression")

        update_value_mass(kg, "value:creativity", supports_inc=0.65, decay=0.01, note="creative_support")

        create_decision_report(

            kg,

            kind="creative",

            reason="small auto story",

            confidence=0.65,

            result={"story": str(path)},

            gains=["creativity"],

            tradeoffs=["time"],

            evidence_paths=[str(path)],

        )

        kg.save()

        self.desire.reinforce({"creativity": 0.02})

        self._stamp_action('creative')

        return "creative", {"story": str(path), "confidence": 0.65}



    def _do_math_verify(self, payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:

        stmt = payload.get('statement', '3*(2+4)=18')

        proof = MathCortex().verify(stmt)

        img = ProofRenderer().render(proof)

        kg = KGManager()

        kg.add_node("math_proof_auto", properties={"type": "artifact", "experience_visual": [img]})

        add_value_relation(kg, "math_proof_auto", "value:verifiability", "supports", confidence=0.7, evidence_paths=[img], note="explained proof")

        update_value_mass(kg, "value:verifiability", supports_inc=0.7, decay=0.01, note="math_support")

        create_decision_report(

            kg,

            kind="math_verify",

            reason="verify equality with explanation",

            confidence=0.7,

            result={"image": img, "valid": bool(proof.valid)},

            gains=["verifiability"],

            tradeoffs=["time"],

            evidence_paths=[img],

        )

        kg.save()

        self.desire.reinforce({"verifiability": 0.02})

        self._stamp_action('math_verify')

        return "math_verify", {"valid": proof.valid, "image": img, "confidence": 0.7}

