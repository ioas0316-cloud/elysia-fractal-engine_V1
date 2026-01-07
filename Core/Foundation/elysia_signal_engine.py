import json
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np


@dataclass
class ElysiaSignal:
    """
    A single "droplet" that falls into Elysia's consciousness.

    This is intentionally analogue-leaning:
    - intensity is continuous (0..1)
    - multiple raw events can blend into one signal
    """

    timestamp: int
    signal_type: str
    intensity: float
    position: Optional[Tuple[float, float]] = None
    actors: Optional[List[str]] = None
    summary: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "signal_type": self.signal_type,
            "intensity": float(self.intensity),
            "position": list(self.position) if self.position is not None else None,
            "actors": self.actors or [],
            "summary": self.summary or "",
        }


class ElysiaSignalEngine:
    """
    Transforms raw world event logs into a sparse stream of
    "Elysia signals" – analogue value droplets like LIFE_BLOOM,
    JOY_GATHERING, ACHIEVEMENT, CARE_ACT, MORTALITY.

    Law over rules:
    - Uses soft thresholds and local densities instead of hard if-else trees.
    - Multiple weak events in a small time/space window can sum into one
      stronger signal.
    """

    def __init__(
        self,
        raw_log_path: str = "logs/world_events.jsonl",
        signal_log_path: str = "logs/elysia_signals.jsonl",
    ):
        self.raw_log_path = raw_log_path
        self.signal_log_path = signal_log_path
        os.makedirs(os.path.dirname(signal_log_path), exist_ok=True)

    # --- Public API -----------------------------------------------------

    def generate_signals_from_log(self, max_events: Optional[int] = None) -> None:
        """
        Read the raw world_events.jsonl, derive Elysia signals, and
        write them as a separate JSONL file.

        This is intentionally side-effect free for the world runtime:
        it sits "above" the simulation as an observation layer.
        """
        raw_events = list(self._read_raw_events(max_events=max_events))
        signals = self._derive_signals(raw_events)
        self._write_signals(signals)

    # --- Internal helpers ----------------------------------------------

    def _read_raw_events(self, max_events: Optional[int]) -> Iterable[Dict]:
        if not os.path.exists(self.raw_log_path):
            return []
        count = 0
        with open(self.raw_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                yield event
                count += 1
                if max_events is not None and count >= max_events:
                    break

    def _derive_signals(self, events: List[Dict]) -> List[ElysiaSignal]:
        """
        Core analogue mapping from raw events to sparse Elysia signals.

        We do this in two passes:
        1) accumulate per-tick "joy", "creation", "care", "mortality" energies
        2) compress each tick into at most a few signals, with intensities
           based on a squashed energy value (0..1)
        """
        if not events:
            return []

        # Per-tick accumulators
        tick_energy: Dict[int, Dict[str, float]] = {}
        tick_actors: Dict[int, List[str]] = {}
        tick_positions: Dict[int, List[Tuple[float, float]]] = {}

        for ev in events:
            t = int(ev.get("timestamp", 0))
            etype = ev.get("event_type", "")
            data = ev.get("data", {}) or {}

            bucket = tick_energy.setdefault(
                t, {"joy": 0.0, "creation": 0.0, "care": 0.0, "mortality": 0.0, "play": 0.0}
            )
            actors = tick_actors.setdefault(t, [])
            positions = tick_positions.setdefault(t, [])

            # Basic actor extraction (best-effort; keeps engine analogue-friendly)
            for key in ("cell_id", "actor_id", "target_id", "caster_id"):
                cid = data.get(key)
                if isinstance(cid, str):
                    actors.append(cid)

            # Optional approximate position (if present in raw event).
            if "x" in data and "y" in data:
                try:
                    positions.append((float(data["x"]), float(data["y"])))
                except (TypeError, ValueError):
                    pass

            # --- Soft law mappings (no hard rules) ---------------------
            # Nourishment / simple life support gently increases joy.
            if etype in ("EAT", "DRINK"):
                bucket["joy"] += 0.3

            # Birth / mating treated as creation energy.
            elif etype in ("BIRTH", "DEATH_BY_OLD_AGE"):
                # Old age death: creation + mortality, a full cycle.
                bucket["creation"] += 0.5
                bucket["mortality"] += 0.5

            # Death generally contributes to mortality awareness.
            elif etype.startswith("DEATH"):
                bucket["mortality"] += 1.0

            # Healing / protection approximated via SPELL+heal or DRINK.
            if etype == "SPELL" and "heal" in str(data.get("spell", "")):
                bucket["care"] += 0.6

            # Experience deltas with strong positive total increase "growth joy".
            if etype == "EXPERIENCE_DELTA":
                total_pos = float(data.get("total_pos", 0.0))
                total_neg = float(data.get("total_neg", 0.0))
                # Soft contribution based on net positive experience.
                bucket["joy"] += max(0.0, total_pos - max(0.0, total_neg)) / 50.0

            # Idle play / wandering: treat as small "playful noise" energy.
            if etype == "IDLE_PLAY":
                bucket["play"] += 0.2

        # Helper to split actors into "villain" vs "non-villain" buckets.
        def split_actors(actors_all: List[str]) -> Tuple[List[str], List[str]]:
            good: List[str] = []
            dark: List[str] = []
            for aid in actors_all:
                name = str(aid).lower()
                # Heuristic: bandit/demon identifiers are treated as villain-aligned.
                if "bandit" in name or "demonlord" in name or "demon_" in name:
                    dark.append(aid)
                else:
                    good.append(aid)
            return good, dark

        # Compress per-tick energies into signals.
        signals: List[ElysiaSignal] = []
        for t in sorted(tick_energy.keys()):
            energy = tick_energy[t]
            actors_all = list(dict.fromkeys(tick_actors.get(t, [])))  # dedupe, preserve order
            good_actors, dark_actors = split_actors(actors_all)
            pos_list = tick_positions.get(t, [])

            # Convert energies to intensities via smooth squashing function.
            def squash(x: float) -> float:
                # Simple analogue: 1 - exp(-x) bounded in [0,1) for x>=0
                x = max(0.0, x)
                return float(1.0 - np.exp(-x))

            joy_i = squash(energy["joy"])
            creation_i = squash(energy["creation"])
            care_i = squash(energy["care"])
            mortality_i = squash(energy["mortality"])
            play_i = squash(energy.get("play", 0.0))

            # Avoid flooding: only emit when intensity is noticeable.
            if joy_i > 0.15 and good_actors:
                signals.append(
                    ElysiaSignal(
                        timestamp=t,
                        signal_type="JOY_GATHERING",
                        intensity=joy_i,
                        position=None,
                        actors=good_actors,
                        summary="Accumulated simple joys (food, recovery, growth).",
                    )
                )
            # Dark joy: villain-only gatherings are tracked separately so they do
            # not inflate Elysia's core JOY/KINSHIP metrics.
            if joy_i > 0.15 and dark_actors:
                signals.append(
                    ElysiaSignal(
                        timestamp=t,
                        signal_type="DARK_JOY",
                        intensity=joy_i,
                        position=None,
                        actors=dark_actors,
                        summary="Unsettling joy among villain-aligned actors (bandits, demons).",
                    )
                )

            if creation_i > 0.15:
                signals.append(
                    ElysiaSignal(
                        timestamp=t,
                        signal_type="LIFE_BLOOM",
                        intensity=creation_i,
                        position=None,
                        actors=actors,
                        summary="Moments of creation or full life cycles.",
                    )
                )

            if care_i > 0.15:
                signals.append(
                    ElysiaSignal(
                        timestamp=t,
                        signal_type="CARE_ACT",
                        intensity=care_i,
                        position=None,
                        actors=actors,
                        summary="Healing / supportive actions detected.",
                    )
                )

            if mortality_i > 0.15:
                signals.append(
                    ElysiaSignal(
                        timestamp=t,
                        signal_type="MORTALITY",
                        intensity=mortality_i,
                        position=None,
                        actors=actors,
                        summary="Deaths observed in the world.",
                    )
                )

            if play_i > 0.15:
                # Approximate center-of-mass for positions if available.
                if pos_list:
                    xs = [p[0] for p in pos_list]
                    ys = [p[1] for p in pos_list]
                    position = (float(sum(xs) / len(xs)), float(sum(ys) / len(ys)))
                else:
                    position = None
                signals.append(
                    ElysiaSignal(
                        timestamp=t,
                        signal_type="PLAYFUL_NOISE",
                        intensity=play_i,
                        position=position,
                        actors=actors,
                        summary="Moments of idle play / wandering with no clear purpose.",
                    )
                )

        return signals

    def _write_signals(self, signals: Iterable[ElysiaSignal]) -> None:
        with open(self.signal_log_path, "w", encoding="utf-8") as f:
            for sig in signals:
                f.write(json.dumps(sig.to_dict(), ensure_ascii=False) + "\n")

