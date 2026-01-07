import json
import math
import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class FeelingState:
    """
    Continuous, analogue feeling vector for Elysia's current moment.

    Values are in [0, +inf) before squashing; consumers may choose to
    clamp or map them into [0,1] if needed.
    """

    joy: float = 0.0
    creation: float = 0.0
    care: float = 0.0
    mortality: float = 0.0

    def as_dict(self) -> Dict[str, float]:
        return {
            "joy": float(self.joy),
            "creation": float(self.creation),
            "care": float(self.care),
            "mortality": float(self.mortality),
        }


@dataclass
class ElysiaFeelingBuffer:
    """
    Feeling buffer for Elysia's consciousness.

    - Input: sparse Elysia signals (JOY_GATHERING, LIFE_BLOOM, CARE_ACT, MORTALITY, ...)
    - Internal state: time-decayed analogue feeling vector
    - Output: current FeelingState, optionally squashed to [0,1]

    Law-before-rule:
    - Each signal contributes softly along one or more axes.
    - Feelings decay smoothly over time using an exponential half-life.
    - No hard thresholds are applied here; consumers can interpret
      the values as needed.
    """

    half_life_ticks: float = 200.0
    last_timestamp: int = 0
    state: FeelingState = field(default_factory=FeelingState)

    # Relative weights for how each signal type contributes to axes.
    signal_weights: Dict[str, Dict[str, float]] = field(
        default_factory=lambda: {
            "JOY_GATHERING": {"joy": 1.0},
            "LIFE_BLOOM": {"creation": 1.0, "joy": 0.4},
            "CARE_ACT": {"care": 1.0, "joy": 0.3},
            "MORTALITY": {"mortality": 1.0},
        }
    )

    def _decay_to(self, timestamp: int) -> None:
        if self.last_timestamp is None or self.half_life_ticks <= 0:
            self.last_timestamp = timestamp
            return
        dt = max(0, int(timestamp) - int(self.last_timestamp))
        if dt <= 0:
            return
        # Exponential decay: value * 0.5^(dt / half_life)
        factor = math.pow(0.5, float(dt) / float(self.half_life_ticks))
        self.state.joy *= factor
        self.state.creation *= factor
        self.state.care *= factor
        self.state.mortality *= factor
        self.last_timestamp = timestamp

    def ingest_signal(self, signal: Dict) -> None:
        """
        Ingest a single Elysia signal (one line from elysia_signals.jsonl).
        Expected keys: timestamp, signal_type, intensity.
        """
        timestamp = int(signal.get("timestamp", self.last_timestamp))
        signal_type = str(signal.get("signal_type", "")).upper()
        intensity = float(signal.get("intensity", 0.0))

        self._decay_to(timestamp)

        if intensity <= 0.0:
            return

        weights = self.signal_weights.get(signal_type)
        if not weights:
            return

        # Soft contribution along each axis.
        self.state.joy += intensity * weights.get("joy", 0.0)
        self.state.creation += intensity * weights.get("creation", 0.0)
        self.state.care += intensity * weights.get("care", 0.0)
        self.state.mortality += intensity * weights.get("mortality", 0.0)

    def ingest_many(self, signals: Iterable[Dict]) -> None:
        """
        Ingest a sequence of signals. If they are not sorted by timestamp,
        they will be processed in the given order, so callers should sort
        if temporal consistency is important.
        """
        for sig in signals:
            self.ingest_signal(sig)

    def load_from_log(self, path: str = "logs/elysia_signals.jsonl") -> None:
        """
        Convenience helper: read the entire signal log and rebuild the
        feeling state from scratch. This is intended for offline analysis
        or coarse OS steps, not high-frequency use.
        """
        if not os.path.exists(path):
            return
        self.state = FeelingState()
        self.last_timestamp = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    sig = json.loads(line)
                except json.JSONDecodeError:
                    continue
                self.ingest_signal(sig)

    def current_state(self) -> FeelingState:
        """
        Return the current analogue feeling state.
        Consumers may optionally post-process this (e.g. squash into [0,1]).
        """
        return self.state

    def squashed_state(self) -> Dict[str, float]:
        """
        Return a version of the feeling state squashed into [0,1] via
        1 - exp(-x). This is useful when the raw magnitudes are not
        as important as relative saturation.
        """
        def squash(x: float) -> float:
            x = max(0.0, float(x))
            return 1.0 - math.exp(-x)

        s = self.state
        return {
            "joy": squash(s.joy),
            "creation": squash(s.creation),
            "care": squash(s.care),
            "mortality": squash(s.mortality),
        }

