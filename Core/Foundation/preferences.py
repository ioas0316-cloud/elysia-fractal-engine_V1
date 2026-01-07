"""
Simple preferences loader/saver for user/agent flags.
Stored at data/preferences.json.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


PREF_PATH = Path("data/preferences.json")


def load_prefs() -> Dict[str, Any]:
    try:
        if PREF_PATH.exists():
            return json.loads(PREF_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def save_prefs(prefs: Dict[str, Any]) -> None:
    try:
        PREF_PATH.parent.mkdir(parents=True, exist_ok=True)
        PREF_PATH.write_text(json.dumps(prefs, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def ensure_defaults(prefs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge default keys for autonomy/quiet/cooldowns while preserving existing values."""
    defaults: Dict[str, Any] = {
        "auto_act": False,
        "quiet_mode": True,
        "autonomy_intensity": "low",  # low|medium|high
        "min_arousal_for_proposal": 0.4,
        "proposal_cooldowns": {
            "journal": 1800,
            "creative": 1800,
            "math_verify": 1800,
        },
        "last_action_ts": {},
    }
    # shallow merge
    merged = {**defaults, **(prefs or {})}
    # nested map merge for cooldowns/last_action_ts
    for key in ("proposal_cooldowns", "last_action_ts"):
        merged[key] = {**defaults[key], **(prefs.get(key, {}) if isinstance(prefs, dict) else {})}
    return merged
