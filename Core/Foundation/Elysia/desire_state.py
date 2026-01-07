"""
DesireState

Stores a lightweight multi-criteria desire vector with decay and update.
This is intentionally simple and transparent.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict


STATE_PATH = Path("data/desire_state.json")


@dataclass
class DesireVector:
    relatedness: float = 0.3   # 관계성/돌봄
    clarity: float = 0.3       # 명료성/설명가능성
    verifiability: float = 0.3 # 검증가능성/근거성
    creativity: float = 0.3    # 창조성/표현


class DesireState:
    def __init__(self):
        self.vec = DesireVector()
        self.load()

    def load(self):
        try:
            if STATE_PATH.exists():
                data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
                self.vec = DesireVector(**data)
        except Exception:
            pass

    def save(self):
        try:
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            STATE_PATH.write_text(json.dumps(asdict(self.vec), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def decay(self, rate: float = 0.98):
        self.vec.relatedness *= rate
        self.vec.clarity *= rate
        self.vec.verifiability *= rate
        self.vec.creativity *= rate
        self.save()

    def reinforce(self, gains: Dict[str, float]):
        for k, v in gains.items():
            if hasattr(self.vec, k):
                setattr(self.vec, k, max(0.0, min(1.0, getattr(self.vec, k) + float(v))))
        self.save()

