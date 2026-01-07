from __future__ import annotations

from typing import Dict, Any, Optional, List
import os
import random
import time
import yaml

from infra.telemetry import Telemetry
from nano_core.bus import MessageBus
from nano_core.message import Message


DEFAULT_FLOW_PATH = os.path.join("data", "flows", "generic_dialog.yaml")
PROFILE_FILE = os.path.join("data", "flows", "profile.txt")


class FlowEngine:
    """
    Lightweight, LLM‑free flow orchestrator that blends soft signals to
    choose small conversational operators, then composes a response.

    Goals:
    - Keep rules as hints, not hard gates.
    - Maintain continuity via working memory and topics when available.
    - Respect values/quiet/consent (gates live higher up in Agency).
    """

    def __init__(
        self,
        bus: MessageBus,
        kg_manager=None,
        orchestrator=None,
        working_memory=None,
        topic_tracker=None,
        value_cortex=None,
        wave_mechanics=None,
        flow_path: str = DEFAULT_FLOW_PATH,
        enabled: bool = True,
    ):
        self.bus = bus
        self.kg = kg_manager
        self.orchestrator = orchestrator
        self.wm = working_memory
        self.topics = topic_tracker
        self.values = value_cortex
        self.wave = wave_mechanics
        self.enabled = enabled
        self.flow_path = flow_path
        self._flow_mtime = 0.0
        self.flow = self._load_flow(self._resolve_profile_path())
        try:
            self.telemetry = Telemetry()
        except Exception:
            self.telemetry = None

    def _load_flow(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                try:
                    self._flow_mtime = os.path.getmtime(path)
                except Exception:
                    self._flow_mtime = 0.0
                self.flow_path = path
                return data
        except FileNotFoundError:
            # Minimal defaults if no spec
            return {
                "weights": {"clarify": 0.35, "reflect": 0.4, "suggest": 0.25},
                "temperature": 0.4,
            }
        except Exception:
            return {"weights": {"clarify": 0.33, "reflect": 0.34, "suggest": 0.33}, "temperature": 0.5}

    def _resolve_profile_path(self) -> str:
        """Allow external profile switching via data/flows/profile.txt.
        If the file exists and points to an existing yaml, prefer it.
        """
        try:
            if os.path.exists(PROFILE_FILE):
                p = open(PROFILE_FILE, "r", encoding="utf-8", errors="ignore").read().strip()
                if p and os.path.exists(p):
                    return p
                # support short names like "learning"
                short = os.path.join("data", "flows", f"{p}.yaml")
                if p and os.path.exists(short):
                    return short
        except Exception:
            pass
        return self.flow_path or DEFAULT_FLOW_PATH

    def _maybe_reload_flow(self):
        try:
            # check profile redirect
            desired = self._resolve_profile_path()
            if desired != self.flow_path:
                self.flow = self._load_flow(desired)
                return
            # check mtime
            mt = os.path.getmtime(self.flow_path)
            if mt != self._flow_mtime:
                self.flow = self._load_flow(self.flow_path)
        except Exception:
            pass

    # --- Scoring helpers (bounded 0..1) ---
    def _score_clarify(self, message: str) -> float:
        msg = (message or "").strip()
        if not msg:
            return 0.0
        has_q = ("?" in msg) or ("뭐" in msg or "왜" in msg or "어떻게" in msg)
        lengthy = len(msg) >= 36
        return 0.7 if (not has_q and lengthy) else (0.35 if not has_q else 0.1)

    def _score_reflect(self, emotional_state) -> float:
        try:
            ar = getattr(emotional_state, "arousal", 0.0)
            # Higher arousal → prioritize reflection
            return max(0.2, min(1.0, 0.5 + 0.5 * ar))
        except Exception:
            return 0.3

    def _score_suggest(self, context: Dict[str, Any]) -> float:
        echo = (context or {}).get("echo", {}) or {}
        density = min(1.0, len([k for k, v in echo.items() if v > 0.2]) / 5.0)
        return 0.2 + 0.6 * density

    def respond(self, message: str, emotional_state, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        if not self.enabled:
            return None
        # hot-reload flow if profile/weights changed
        self._maybe_reload_flow()
        weights = (self.flow or {}).get("weights", {})
        w_clar = float(weights.get("clarify", 0.33))
        w_refl = float(weights.get("reflect", 0.34))
        w_sugg = float(weights.get("suggest", 0.33))
        # Signals
        s_clar = self._score_clarify(message)
        s_refl = self._score_reflect(emotional_state)
        s_sugg = self._score_suggest(context or {})
        # Weighted mixture as soft arbitration
        score = [
            ("clarify", w_clar * s_clar + random.uniform(0, 0.05)),
            ("reflect", w_refl * s_refl + random.uniform(0, 0.05)),
            ("suggest", w_sugg * s_sugg + random.uniform(0, 0.05)),
        ]
        score.sort(key=lambda x: x[1], reverse=True)

        top_choice, top_score = score[0] if score else (None, 0.0)

        # Post to nano_core bus
        if top_choice:
            # --- Gravity Well ---
            gravity_bonus = 0.0
            if self.kg:
                # Map operator to a core concept, then get its mass
                concept_map = {"reflect": "value:love", "clarify": "value:clarity", "suggest": "value:creativity"}
                concept_id = concept_map.get(top_choice)
                if concept_id:
                    node = self.kg.get_node(concept_id)
                    gravity_bonus = 0.5 * (node.get("mass", 0.0) if node else 0.0)
            final_strength = float(top_score) + gravity_bonus
            # --- End Gravity Well ---

            msg = Message(
                verb=top_choice,
                slots={"raw_message": message, "context": context},
                src="FlowEngine",
                strength=final_strength,
            )
            self.bus.post(msg)

        # Telemetry: record decision signals (no sensitive content)
        try:
            if self.telemetry:
                echo = (context or {}).get('echo', {}) or {}
                echo_sorted = [k for k, _v in sorted(echo.items(), key=lambda kv: kv[1], reverse=True)][:3]
                self.telemetry.emit(
                    'flow.decision',
                    {
                        'weights': {'clarify': w_clar, 'reflect': w_refl, 'suggest': w_sugg},
                        'signals': {'clarify': s_clar, 'reflect': s_refl, 'suggest': s_sugg},
                        'top_choice': top_choice,
                        'message_len': len(message or ''),
                        'evidence': {'echo_top': echo_sorted},
                    }
                )
        except Exception:
            pass

        # Compose via existing orchestrator for naturalness
        if self.orchestrator is None:
            return None
        try:
            text = self.orchestrator.generate(message, emotional_state, context or {}, self.wm, self.topics)
            return text
        except Exception:
            return None
