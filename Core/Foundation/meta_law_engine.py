from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from kg_manager import KGManager
from core_memory import CoreMemory


@dataclass
class MetaLawDefinition:
    axis_id: str
    label: str
    description: str
    keywords: List[str]
    axis_vector: Dict[str, float]
    score: float = 0.0
    support: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "description": self.description,
            "keywords": self.keywords,
            "axis_vector": self.axis_vector,
            "score": round(self.score, 3),
            "support": self.support or [],
        }


class MetaLawEngine:
    DEFAULT_LAWS = {
        "care": {
            "label": "Care",
            "description": "Protecting the living, honoring love, and guarding warmth.",
            "keywords": ["사랑", "빛", "가족", "친구", "생명", "희망"],
            "axis_vector": {"w": 0.4, "x": 0.1, "y": 0.3, "z": 0.2},
        },
        "truth": {
            "label": "Truth",
            "description": "Seeking clarity, remembering law, and tracing cause.",
            "keywords": ["진리", "법칙", "역사", "기억", "시간", "의지"],
            "axis_vector": {"w": 0.3, "x": 0.4, "y": 0.1, "z": 0.2},
        },
        "play": {
            "label": "Play",
            "description": "Joy, curiosity, and the impulse to dance through words.",
            "keywords": ["음악", "춤", "놀이", "소리", "웃음", "꿈"],
            "axis_vector": {"w": 0.2, "x": 0.2, "y": 0.5, "z": 0.1},
        },
        "respite": {
            "label": "Respite",
            "description": "Rest, quiet, and deep replenishment of internal wells.",
            "keywords": ["휴식", "잠", "꿈", "평온", "쉼", "안식"],
            "axis_vector": {"w": 0.5, "x": 0.3, "y": 0.1, "z": 0.1},
        },
        "valor": {
            "label": "Valor",
            "description": "Facing hardship, standing as a shield, and honoring battles.",
            "keywords": ["싸움", "검", "힘", "전쟁", "용기", "어둠"],
            "axis_vector": {"w": 0.1, "x": 0.2, "y": 0.4, "z": 0.3},
        },
    }

    def __init__(
        self,
        core_memory: Optional[CoreMemory] = None,
        kg_manager: Optional[KGManager] = None,
        law_path: str = "data/meta_laws.json",
    ) -> None:
        self.core_memory = core_memory
        self.kg = kg_manager
        self.law_path = Path(law_path)
        self.laws: Dict[str, MetaLawDefinition] = {}
        self.ensure_laws()

    def ensure_laws(self) -> None:
        if self.law_path.exists():
            try:
                with self.law_path.open("r", encoding="utf-8") as handle:
                    raw = json.load(handle)
                for axis_id, record in (raw or {}).items():
                    self.laws[axis_id] = MetaLawDefinition(
                        axis_id=axis_id,
                        label=record.get("label", axis_id),
                        description=record.get("description", ""),
                        keywords=record.get("keywords", []),
                        axis_vector=record.get("axis_vector", {}),
                        score=float(record.get("score", 0.0)),
                        support=record.get("support", []),
                    )
                return
            except Exception:
                pass
        self.discover_laws()

    def discover_laws(self) -> None:
        values = []
        if self.core_memory:
            try:
                values = [
                    entry
                    for entry in self.core_memory.get_values()
                    if isinstance(entry.get("value"), str)
                ]
            except Exception:
                values = []

        law_supports: Dict[str, List[str]] = {axis: [] for axis in self.DEFAULT_LAWS}
        law_scores: Dict[str, float] = {axis: 0.0 for axis in self.DEFAULT_LAWS}

        for entry in values:
            value = entry.get("value", "")
            importance = float(entry.get("importance", 1.0)) if entry.get("importance") else 1.0
            for axis_id, blueprint in self.DEFAULT_LAWS.items():
                if any(keyword in value for keyword in blueprint["keywords"]):
                    law_scores[axis_id] += importance
                    law_supports[axis_id].append(value)

        # Normalize + ensure baseline
        total = sum(law_scores.values()) or 1.0
        for axis_id, blueprint in self.DEFAULT_LAWS.items():
            score = (law_scores.get(axis_id, 0.0) / total) * 2.0
            support = law_supports.get(axis_id, [])[:8]
            self.laws[axis_id] = MetaLawDefinition(
                axis_id=axis_id,
                label=blueprint["label"],
                description=blueprint["description"],
                keywords=blueprint["keywords"],
                axis_vector=blueprint["axis_vector"],
                score=score,
                support=support,
            )
        self._save()

    def _save(self) -> None:
        data = {axis_id: law.to_dict() for axis_id, law in self.laws.items()}
        try:
            self.law_path.parent.mkdir(parents=True, exist_ok=True)
            with self.law_path.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def node_id(self, axis_id: str) -> str:
        return f"law:{axis_id}"

    def sync_to_kg(self) -> None:
        if not self.kg:
            return
        for axis_id, law in self.laws.items():
            node_id = self.node_id(axis_id)
            self.kg.add_node(node_id, properties={
                "label": law.label,
                "type": "law_axis",
                "score": law.score,
                "description": law.description,
            })
            for keyword in law.keywords:
                if keyword in {node.get("id") for node in self.kg.kg.get("nodes", []) if isinstance(node, dict)}:
                    self.kg.add_edge(node_id, keyword, "law_focus", properties={"weight": 0.5})
        try:
            self.kg.save()
        except Exception:
            pass

    def score_context(self, context_text: str, wave_info: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        scores = {axis_id: law.score for axis_id, law in self.laws.items()}
        tokens = [token.strip() for token in context_text.split() if token.strip()]
        for axis_id, law in self.laws.items():
            for keyword in law.keywords:
                for token in tokens:
                    if keyword in token:
                        scores[axis_id] += len(keyword) * 0.1
        if wave_info:
            for entry in wave_info.get("entries", []):
                concept = entry.get("concept", "")
                for axis_id, law in self.laws.items():
                    if concept in law.keywords or any(keyword in concept for keyword in law.keywords):
                        scores[axis_id] += entry.get("energy", 0.0)
        return scores

    def pick_dominant(self, scores: Dict[str, float]) -> Optional[str]:
        if not scores:
            return None
        axis, value = max(scores.items(), key=lambda item: item[1])
        if value <= 0.0:
            return None
        return axis
