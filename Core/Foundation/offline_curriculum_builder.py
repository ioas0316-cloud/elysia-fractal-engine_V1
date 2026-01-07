"""Offline curriculum builder for natural-language knowledge growth."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple
import json
import math
import re

try:  # Optional dependency; fall back to JSON for .json curriculum files.
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - exercised in environments without PyYAML
    yaml = None

from kg_manager import KGManager


StageId = str


@dataclass
class LessonParse:
    """Structured interpretation of a natural-language lesson sentence."""

    subject: Optional[str]
    verb: Optional[str]
    obj: Optional[str]


class OfflineCurriculumBuilder:
    """Converts curated offline language lessons into knowledge graph updates."""

    def __init__(
        self,
        curriculum_path: Path,
        kg_manager: Optional[KGManager] = None,
    ) -> None:
        self.curriculum_path = Path(curriculum_path)
        self.kg_manager = kg_manager or KGManager()

    def load_curriculum(self) -> Dict[str, object]:
        raw = self.curriculum_path.read_text(encoding="utf-8")
        suffix = self.curriculum_path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise ModuleNotFoundError(
                    "PyYAML is required to load .yaml curriculum files. Install PyYAML or provide a JSON curriculum."
                )
            data = yaml.safe_load(raw)
        else:
            data = json.loads(raw)
        if not isinstance(data, dict) or "stages" not in data:
            raise ValueError("Curriculum file must define a top-level 'stages' list.")
        return data

    def integrate(self, curriculum: Optional[Dict[str, object]] = None) -> Dict[str, int]:
        payload = curriculum or self.load_curriculum()
        stages = payload.get("stages", [])
        summary = {"stages": 0, "lessons": 0, "new_nodes": 0, "new_edges": 0}
        previous_stage_node: Optional[str] = None

        for stage_index, stage in enumerate(stages):
            stage_id = self._require(stage, "id")
            stage_node_id = f"curriculum_stage::{stage_id}"
            stage_position = self._stage_position(stage_index)
            new_nodes_before = self._node_count
            self.kg_manager.add_node(
                stage_node_id,
                position={"x": stage_position[0], "y": stage_position[1], "z": stage_position[2]},
                properties={
                    "type": "curriculum_stage",
                    "label": stage.get("label", stage_id),
                    "age_range": stage.get("age_range"),
                    "focus": stage.get("focus", []),
                    "narrative": stage.get("narrative"),
                },
            )
            summary["new_nodes"] += self._node_count - new_nodes_before
            summary["stages"] += 1

            if previous_stage_node:
                new_edges_before = self._edge_count
                self.kg_manager.add_edge(previous_stage_node, stage_node_id, "precedes")
                summary["new_edges"] += self._edge_count - new_edges_before
            previous_stage_node = stage_node_id

            lessons = stage.get("lessons", [])
            for lesson_index, lesson in enumerate(lessons):
                summary["lessons"] += 1
                lesson_node_id = self._lesson_node_id(stage_id, lesson)
                new_nodes_before = self._node_count
                self.kg_manager.add_node(
                    lesson_node_id,
                    position=self._lesson_position(stage_position, lesson_index),
                    properties={
                        "type": "curriculum_lesson",
                        "stage_id": stage_id,
                        "sentence": lesson.get("sentence"),
                        "keywords": lesson.get("keywords", []),
                        "affirmation": lesson.get("affirmation"),
                    },
                )
                summary["new_nodes"] += self._node_count - new_nodes_before

                summary["new_edges"] += self._add_edge(stage_node_id, lesson_node_id, "teaches")

                affirmation_text = self._clean_field(lesson.get("affirmation"))
                if affirmation_text:
                    affirmation_node_id = f"affirmation::{self._slug(lesson_node_id)}"
                    new_nodes_before = self._node_count
                    self.kg_manager.add_node(
                        affirmation_node_id,
                        properties={
                            "type": "curriculum_affirmation",
                            "lesson_id": lesson_node_id,
                            "text": affirmation_text,
                        },
                    )
                    summary["new_nodes"] += self._node_count - new_nodes_before
                    summary["new_edges"] += self._add_edge(lesson_node_id, affirmation_node_id, "offers_affirmation")

                parse = self._parse_lesson(lesson)
                summary["new_nodes"] += self._ensure_concept_node(parse.subject, "curriculum_concept")
                summary["new_nodes"] += self._ensure_concept_node(parse.obj, "curriculum_object")
                summary["new_nodes"] += self._ensure_concept_node(parse.verb, "curriculum_action")

                if parse.subject:
                    subject_node_id = self._concept_node_id(parse.subject, "concept")
                    summary["new_edges"] += self._add_edge(lesson_node_id, subject_node_id, "involves_subject")
                if parse.obj:
                    object_node_id = self._concept_node_id(parse.obj, "object")
                    summary["new_edges"] += self._add_edge(lesson_node_id, object_node_id, "involves_object")
                if parse.verb:
                    action_node_id = self._concept_node_id(parse.verb, "action")
                    summary["new_edges"] += self._add_edge(lesson_node_id, action_node_id, "reinforces_action")

                for keyword in lesson.get("keywords", []):
                    keyword_node_id = f"value::{self._slug(keyword)}"
                    new_nodes_before = self._node_count
                    self.kg_manager.add_node(
                        keyword_node_id,
                        properties={"type": "curriculum_theme", "label": keyword},
                    )
                    summary["new_nodes"] += self._node_count - new_nodes_before
                    summary["new_edges"] += self._add_edge(lesson_node_id, keyword_node_id, "highlights_theme")

        return summary

    def _parse_lesson(self, lesson: Dict[str, object]) -> LessonParse:
        subject = self._clean_field(lesson.get("subject"))
        obj = self._clean_field(lesson.get("object"))
        verb = self._clean_field(lesson.get("verb"))

        if not subject or not obj or not verb:
            fallback = self._heuristic_parse(lesson.get("sentence"))
            subject = subject or fallback.subject
            obj = obj or fallback.obj
            verb = verb or fallback.verb

        return LessonParse(subject=subject, verb=verb, obj=obj)

    def _heuristic_parse(self, sentence: Optional[str]) -> LessonParse:
        if not sentence:
            return LessonParse(None, None, None)
        clean = sentence.strip().rstrip(".!?\u3002")
        tokens = clean.split()
        subject = None
        obj = None
        verb = None
        for token in tokens:
            if token.endswith("는") or token.endswith("은") or token.endswith("이가") or token.endswith("이") or token.endswith("가"):
                candidate = token.rstrip("는은이가")
                if candidate:
                    subject = subject or candidate
                    continue
            if token.endswith("를") or token.endswith("을"):
                candidate = token.rstrip("를을")
                if candidate:
                    obj = obj or candidate
                    continue
        if tokens:
            verb = tokens[-1]
        return LessonParse(subject, verb, obj)

    def _stage_position(self, index: int) -> Tuple[float, float, float]:
        radius = 3.0
        angle = index * (math.pi / 4)
        return (radius * math.cos(angle), radius * math.sin(angle), index * 0.5)

    def _lesson_position(self, stage_position: Tuple[float, float, float], lesson_index: int) -> Dict[str, float]:
        offset_angle = lesson_index * (math.pi / 6)
        distance = 0.8 + 0.2 * lesson_index
        return {
            "x": stage_position[0] + distance * math.cos(offset_angle),
            "y": stage_position[1] + distance * math.sin(offset_angle),
            "z": stage_position[2] + 0.2 * lesson_index,
        }

    def _lesson_node_id(self, stage_id: StageId, lesson: Dict[str, object]) -> str:
        lesson_id = self._slug(lesson.get("id") or lesson.get("sentence") or "lesson")
        return f"curriculum_lesson::{stage_id}::{lesson_id}"

    def _add_edge(self, source: str, target: str, relation: str) -> int:
        before = self._edge_count
        self.kg_manager.add_edge(source, target, relation)
        return self._edge_count - before

    def _ensure_concept_node(self, label: Optional[str], concept_type: str) -> int:
        if not label:
            return 0
        node_id = self._concept_node_id(label, concept_type.split("_")[-1])
        before = self._node_count
        self.kg_manager.add_node(
            node_id,
            properties={"type": concept_type, "label": label},
        )
        return self._node_count - before

    def _concept_node_id(self, label: str, prefix: str) -> str:
        return f"{prefix}::{self._slug(label)}"

    def _slug(self, value: Optional[str]) -> str:
        if not value:
            return "unknown"
        normalized = re.sub(r"\s+", "_", value.strip())
        normalized = re.sub(r"[^\w가-힣_]", "", normalized)
        return normalized.lower() or "unknown"

    def _clean_field(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @property
    def _node_count(self) -> int:
        return len(self.kg_manager.kg.get("nodes", []))

    @property
    def _edge_count(self) -> int:
        return len(self.kg_manager.kg.get("edges", []))

    @staticmethod
    def _require(payload: Dict[str, object], key: str) -> object:
        if key not in payload:
            raise ValueError(f"Curriculum stage must define '{key}'.")
        return payload[key]


def build_offline_curriculum(curriculum_path: Path, kg_path: Optional[Path] = None) -> Dict[str, int]:
    """Convenience function to load and integrate the offline curriculum."""
    manager = KGManager(kg_path) if kg_path else KGManager()
    builder = OfflineCurriculumBuilder(curriculum_path=curriculum_path, kg_manager=manager)
    summary = builder.integrate()
    manager.save()
    return summary


__all__ = ["OfflineCurriculumBuilder", "build_offline_curriculum", "LessonParse"]
