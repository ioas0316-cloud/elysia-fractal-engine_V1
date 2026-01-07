import json
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass
class JoyEpisode:
    """
    A value-bearing process slice around a positive signal.

    This is not just "it was joyful", but:
    - what happened shortly before/after,
    - who was involved,
    - at which signal peak.
    """

    signal_type: str
    signal_intensity: float
    timestamp_peak: int
    timestamp_start: int
    timestamp_end: int
    actors: List[str]
    events: List[Dict]
    # Optional need snapshots (by actor_id) at the start/end of the window.
    needs_before: Dict[str, Dict[str, float]] | None = None
    needs_after: Dict[str, Dict[str, float]] | None = None

    def to_dict(self) -> Dict:
        return {
            "signal_type": self.signal_type,
            "signal_intensity": float(self.signal_intensity),
            "timestamp_peak": int(self.timestamp_peak),
            "timestamp_start": int(self.timestamp_start),
            "timestamp_end": int(self.timestamp_end),
            "actors": list(self.actors),
            "events": self.events,
        }


class JoyEpisodeBuilder:
    """
    Builds JoyEpisodes by looking at Elysia signals and the raw world events
    around them.

    Law-over-rule:
    - We do not try to interpret meaning here; we simply gather
      local process slices (before/after windows) that ElysiaMind
      or higher META layers can read as "value-bearing branches".
    """

    def __init__(
        self,
        world_events_path: str = "logs/world_events.jsonl",
        signal_log_path: str = "logs/elysia_signals.jsonl",
        needs_log_path: str = "logs/human_needs.jsonl",
        window_ticks: int = 8,
    ):
        self.world_events_path = world_events_path
        self.signal_log_path = signal_log_path
        self.needs_log_path = needs_log_path
        self.window_ticks = int(window_ticks)

    def _load_world_events(self) -> Dict[int, List[Dict]]:
        """
        Load raw world events into a dict keyed by timestamp.
        This is intentionally simple; if logs become huge, consider
        streaming/segmenting instead of loading everything at once.
        """
        events_by_tick: Dict[int, List[Dict]] = {}
        if not os.path.exists(self.world_events_path):
            return events_by_tick
        with open(self.world_events_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = int(ev.get("timestamp", 0))
                events_by_tick.setdefault(t, []).append(ev)
        return events_by_tick

    def _iter_signals(self) -> Iterable[Dict]:
        if not os.path.exists(self.signal_log_path):
            return []
        with open(self.signal_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    sig = json.loads(line)
                except json.JSONDecodeError:
                    continue
                yield sig

    def _load_needs(self) -> Dict[int, Dict[str, Dict[str, float]]]:
        """
        Load per-tick human needs snapshots from a JSONL log.

        Each line is expected to look like:
        { "timestamp": int, "cell_id": "human_...", "needs": { ... } }
        """
        needs_by_tick: Dict[int, Dict[str, Dict[str, float]]] = {}
        if not os.path.exists(self.needs_log_path):
            return needs_by_tick
        with open(self.needs_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = int(rec.get("timestamp", 0))
                cid = rec.get("cell_id")
                needs = rec.get("needs") or {}
                if not isinstance(cid, str) or not isinstance(needs, dict):
                    continue
                needs_by_tick.setdefault(t, {})[cid] = needs
        return needs_by_tick

    def build_episodes(self) -> List[JoyEpisode]:
        """
        Build joy/creation/care episodes around positive signals.

        For each signal of type JOY_GATHERING, LIFE_BLOOM, CARE_ACT:
        - collect raw events in [t - window, t + window]
        - gather actors from the signal and those events
        """
        events_by_tick = self._load_world_events()
        if not events_by_tick:
            return []

        needs_by_tick = self._load_needs()

        episodes: List[JoyEpisode] = []
        positive_types = {"JOY_GATHERING", "LIFE_BLOOM", "CARE_ACT"}

        for sig in self._iter_signals():
            stype_raw: Optional[str] = sig.get("signal_type")
            if not stype_raw:
                continue
            stype = stype_raw.upper()
            if stype not in positive_types:
                continue

            t_peak = int(sig.get("timestamp", 0))
            intensity = float(sig.get("intensity", 0.0))
            if intensity <= 0.0:
                continue

            t_start = t_peak - self.window_ticks
            t_end = t_peak + self.window_ticks

            # Collect events in the window.
            window_events: List[Dict] = []
            actors: List[str] = []
            for t in range(t_start, t_end + 1):
                evs = events_by_tick.get(t)
                if not evs:
                    continue
                for ev in evs:
                    window_events.append(ev)
                    data = ev.get("data", {}) or {}
                    for key in ("cell_id", "actor_id", "target_id", "caster_id"):
                        cid = data.get(key)
                        if isinstance(cid, str):
                            actors.append(cid)

            # Merge with actors mentioned in the signal itself.
            sig_actors = sig.get("actors") or []
            for cid in sig_actors:
                if isinstance(cid, str):
                    actors.append(cid)

            # Deduplicate while preserving order.
            seen = set()
            uniq_actors: List[str] = []
            for cid in actors:
                if cid in seen:
                    continue
                seen.add(cid)
                uniq_actors.append(cid)

            # Needs snapshots (if available) for actors at the edges of the window.
            needs_before: Dict[str, Dict[str, float]] = {}
            needs_after: Dict[str, Dict[str, float]] = {}
            if needs_by_tick:
                if t_start in needs_by_tick:
                    for cid in uniq_actors:
                        n = needs_by_tick[t_start].get(cid)
                        if isinstance(n, dict):
                            needs_before[cid] = n
                if t_end in needs_by_tick:
                    for cid in uniq_actors:
                        n = needs_by_tick[t_end].get(cid)
                        if isinstance(n, dict):
                            needs_after[cid] = n

            episodes.append(
                JoyEpisode(
                    signal_type=stype,
                    signal_intensity=intensity,
                    timestamp_peak=t_peak,
                    timestamp_start=t_start,
                    timestamp_end=t_end,
                    actors=uniq_actors,
                    events=window_events,
                    needs_before=needs_before or None,
                    needs_after=needs_after or None,
                )
            )

        return episodes
