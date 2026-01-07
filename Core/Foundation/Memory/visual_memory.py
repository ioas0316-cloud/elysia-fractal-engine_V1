import json
import os
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .joy_episode_builder import JoyEpisode


@dataclass
class VisualMemoryEpisode:
    """
    Compressed visual memory for a single episode.

    This does not store raw pixels. Instead it keeps:
    - when it happened (timestamps),
    - what kind of signal it was,
    - who was involved,
    - a salience score and level that control how much detail we keep.
    """

    id: str
    signal_type: str
    salience: float
    level: str  # "trace" | "summary" | "highlight"
    timestamp_peak: int
    timestamp_start: int
    timestamp_end: int
    actors: List[str] = field(default_factory=list)
    event_type_histogram: Dict[str, int] = field(default_factory=dict)
    feelings_snapshot: Optional[Dict[str, float]] = None
    # Optional high-detail payload for "highlight" episodes only.
    events: Optional[List[Dict]] = None
    # Optional links to rendered artefacts (thumbnail/clip).
    thumbnail_path: Optional[str] = None
    clip_path: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "signal_type": self.signal_type,
            "salience": float(self.salience),
            "level": self.level,
            "timestamp_peak": int(self.timestamp_peak),
            "timestamp_start": int(self.timestamp_start),
            "timestamp_end": int(self.timestamp_end),
            "actors": list(self.actors),
            "event_type_histogram": dict(self.event_type_histogram),
            "feelings_snapshot": dict(self.feelings_snapshot or {}),
            "thumbnail_path": self.thumbnail_path,
            "clip_path": self.clip_path,
        }


class VisualMemory:
    """
    Elysia's visual memory buffer.

    - Input: JoyEpisodes (value-bearing process slices) and optional feeling snapshots.
    - Output: a tiered set of VisualMemoryEpisode entries:
      - "trace": very light, mostly timing and stats (faint memory)
      - "summary": actors + event histogram (coarse scene)
      - "highlight": full event context and attachment points for video/frames

    The goal is to keep intense or meaningful episodes detailed, while
    compressing the rest into faint traces that can still support statistics.
    """

    def __init__(
        self,
        salience_threshold_summary: float = 0.25,
        salience_threshold_highlight: float = 0.6,
    ) -> None:
        self.salience_threshold_summary = float(salience_threshold_summary)
        self.salience_threshold_highlight = float(salience_threshold_highlight)
        self.episodes: List[VisualMemoryEpisode] = []

    def _compute_event_histogram(self, episode: JoyEpisode) -> Dict[str, int]:
        hist: Dict[str, int] = {}
        for ev in episode.events:
            etype = str(ev.get("event_type", "") or "")
            hist[etype] = hist.get(etype, 0) + 1
        return hist

    def _compute_salience(
        self,
        episode: JoyEpisode,
        feelings_snapshot: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Soft salience heuristic:
        - base: signal_intensity in [0,1]
        - bonus: stronger joy/creation/care and mortality contrasts.
        """
        base = float(max(0.0, min(1.0, episode.signal_intensity)))
        if not feelings_snapshot:
            return base

        joy = float(feelings_snapshot.get("joy", 0.0))
        creation = float(feelings_snapshot.get("creation", 0.0))
        care = float(feelings_snapshot.get("care", 0.0))
        mortality = float(feelings_snapshot.get("mortality", 0.0))

        positive = joy + 0.7 * creation + 0.5 * care
        # Mortality can increase salience (sharp contrast) but not too much.
        contrast = 0.4 * mortality

        bonus = 0.3 * positive + contrast
        return float(max(0.0, min(1.0, base + bonus)))

    def add_episode(
        self,
        episode: JoyEpisode,
        feelings_snapshot: Optional[Dict[str, float]] = None,
        thumbnail_path: Optional[str] = None,
        clip_path: Optional[str] = None,
    ) -> VisualMemoryEpisode:
        """
        Add a JoyEpisode into visual memory with salience-based compression.

        - Low salience -> "trace": only timing, histogram, short actor list.
        - Medium salience -> "summary": plus feelings and richer actor list.
        - High salience -> "highlight": also keeps full events and media links.
        """
        salience = self._compute_salience(episode, feelings_snapshot)
        hist = self._compute_event_histogram(episode)

        eid = f"{episode.signal_type}_{episode.timestamp_peak}"
        actors = list(episode.actors)

        if salience >= self.salience_threshold_highlight:
            level = "highlight"
            keep_events: Optional[List[Dict]] = list(episode.events)
            keep_actors = actors
        elif salience >= self.salience_threshold_summary:
            level = "summary"
            keep_events = None
            keep_actors = actors[:8]
        else:
            level = "trace"
            keep_events = None
            keep_actors = actors[:4]

        vm = VisualMemoryEpisode(
            id=eid,
            signal_type=episode.signal_type,
            salience=salience,
            level=level,
            timestamp_peak=episode.timestamp_peak,
            timestamp_start=episode.timestamp_start,
            timestamp_end=episode.timestamp_end,
            actors=keep_actors,
            event_type_histogram=hist,
            feelings_snapshot=feelings_snapshot or None,
            events=keep_events,
            thumbnail_path=thumbnail_path if level == "highlight" else None,
            clip_path=clip_path if level == "highlight" else None,
        )
        self.episodes.append(vm)
        return vm

    def to_dict(self) -> Dict:
        return {"episodes": [ep.to_dict() for ep in self.episodes]}

    def save_to_file(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> "VisualMemory":
        vm = cls()
        if not os.path.exists(path):
            return vm
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        episodes_raw = data.get("episodes") or []
        for rec in episodes_raw:
            vm.episodes.append(
                VisualMemoryEpisode(
                    id=str(rec.get("id", "")),
                    signal_type=str(rec.get("signal_type", "")),
                    salience=float(rec.get("salience", 0.0)),
                    level=str(rec.get("level", "trace")),
                    timestamp_peak=int(rec.get("timestamp_peak", 0)),
                    timestamp_start=int(rec.get("timestamp_start", 0)),
                    timestamp_end=int(rec.get("timestamp_end", 0)),
                    actors=list(rec.get("actors") or []),
                    event_type_histogram=dict(rec.get("event_type_histogram") or {}),
                    feelings_snapshot=rec.get("feelings_snapshot") or None,
                    thumbnail_path=rec.get("thumbnail_path"),
                    clip_path=rec.get("clip_path"),
                )
            )
        return vm

