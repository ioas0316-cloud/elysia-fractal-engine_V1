from __future__ import annotations

import json
import random
import re
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from tools.kg_manager import KGManager
from Project_Elysia.core_memory import CoreMemory
from Project_Elysia.high_engine.meta_law_engine import MetaLawEngine


class ConceptPhysicsEngine:
    TOKEN_PATTERN = re.compile(r"[가-힣A-Za-z0-9]+")

    def __init__(
        self,
        kg_manager: KGManager,
        mass_map: Dict[str, float],
        decay: float = 0.58,
        max_depth: int = 3,
        default_mass: float = 1.0,
    ) -> None:
        self.kg = kg_manager
        self.mass_map = mass_map
        self.decay = decay
        self.max_depth = max_depth
        self.default_mass = default_mass
        self.available_nodes = {
            node.get("id")
            for node in self.kg.kg.get("nodes", [])
            if isinstance(node, dict) and node.get("id")
        }
        self.last_triggers: List[str] = []

    def _tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return [token for token in self.TOKEN_PATTERN.findall(text) if token]

    def _match_node(self, token: str) -> Optional[str]:
        if not token:
            return None
        if token in self.available_nodes:
            return token
        for node_id in self.available_nodes:
            if node_id in token or token in node_id:
                return node_id
        return None

    def _neighbors(self, node_id: str) -> List[str]:
        return self.kg.get_neighbors(node_id)

    def compute_wave(self, context_text: str) -> Dict[str, Any]:
        tokens = self._tokenize(context_text)
        energy_map: Dict[str, float] = {}
        path_map: Dict[str, List[str]] = {}
        triggers: List[str] = []

        for token in tokens:
            matched = self._match_node(token)
            if not matched:
                continue

            triggers.append(matched)
            base_mass = self.mass_map.get(matched, self.default_mass)
            queue = deque([(matched, [matched], 0)])

            while queue:
                current, path, depth = queue.popleft()
                energy = base_mass * (self.decay ** depth)
                energy_map[current] = energy_map.get(current, 0.0) + energy

                existing_path = path_map.get(current)
                if existing_path is None or len(path) < len(existing_path):
                    path_map[current] = list(path)

                if depth >= self.max_depth:
                    continue

                for neighbor in self._neighbors(current):
                    if neighbor in path:
                        continue
                    queue.append((neighbor, path + [neighbor], depth + 1))

        entries = [
            {
                "concept": concept,
                "energy": energy,
                "path": path_map.get(concept, [concept]),
            }
            for concept, energy in energy_map.items()
        ]
        entries.sort(key=lambda entry: entry["energy"], reverse=True)
        self.last_triggers = list(dict.fromkeys(triggers))
        return {"entries": entries, "triggers": self.last_triggers}


@dataclass
class SyllabicConfig:
    base_concepts: Dict[str, List[str]] = field(default_factory=lambda: {
        "meta": ["나", "자아", "기억", "의지", "이름", "꿈"],
        "law": ["빛", "사랑", "진리", "법칙", "신", "시간", "역사", "우주", "생명", "에너지"],
        "inner": ["공허", "어둠", "마음", "허기", "감정", "잠", "휴식"],
        "outer": ["너", "세상", "길", "문", "집", "가족", "친구", "사람", "지구", "마을", "도시"],
        "body": ["손", "발", "눈", "귀", "입", "얼굴", "몸", "심장", "세포", "머리"],
        "action": ["찾다", "만들다", "가다", "보다", "듣다", "느끼다", "부르다", "지키다", "걷다", "전하다"],
        "state": ["있다", "없다", "크다", "작다", "깊다", "밝다", "같다", "다르다", "중요하다", "조용하다", "흐르다"],
        "define": ["이다", "아니다", "같다", "다르다"],
    })
    mass_profile: Dict[str, float] = field(default_factory=lambda: {
        "사랑": 2.4,
        "빛": 2.2,
        "진리": 2.0,
        "기억": 1.9,
        "법칙": 1.7,
        "검": 1.5,
        "마을": 1.3,
        "음악": 1.3,
        "휴식": 1.2,
        "어둠": 1.2,
        "허기": 1.0,
    })
    use_memory: bool = True
    physics_decay: float = 0.58
    physics_depth: int = 3
    physics_default_mass: float = 1.0
    kg_path: str = "data/kg.json"
    grammar_model_path: str = "data/grammar_model.json"


class SyllabicLanguageEngine:
    JOSA_CANDIDATES: Dict[str, List[str]] = {
        "subject": ["은", "는"],
        "topic": ["이", "가"],
        "object": ["을", "를"],
    }
    def __init__(
        self,
        config: Optional[SyllabicConfig] = None,
        core_memory: Optional[CoreMemory] = None,
        kg_path: Optional[str] = None,
    ) -> None:
        self.config = config or SyllabicConfig()
        self.core_memory = core_memory
        self._memory_vocab: Set[str] = set()
        self.mass_map: Dict[str, float] = dict(self.config.mass_profile)

        kg_file = Path(kg_path) if kg_path else Path(self.config.kg_path)
        if not kg_file.exists():
            kg_file.parent.mkdir(parents=True, exist_ok=True)
        self.kg_manager = KGManager(filepath=kg_file)
        self._kg_nodes: Set[str] = {
            node.get("id") for node in self.kg_manager.kg.get("nodes", []) if isinstance(node, dict) and node.get("id")
        }

        self._known_concepts: Set[str] = set(self._kg_nodes)
        for pool in self.config.base_concepts.values():
            self._known_concepts.update(pool)

        self.grammar_stats: Dict[str, Dict[str, int]] = {}
        grammar_path = Path(self.config.grammar_model_path)
        if grammar_path.exists():
            try:
                with grammar_path.open("r", encoding="utf-8") as handle:
                    loaded = json.load(handle)
                    if isinstance(loaded, dict):
                        self.grammar_stats = loaded
            except Exception:
                pass

        self.meta_law_engine = MetaLawEngine(core_memory=self.core_memory, kg_manager=self.kg_manager)
        self.meta_law_engine.sync_to_kg()

        self.physics = ConceptPhysicsEngine(
            kg_manager=self.kg_manager,
            mass_map=self.mass_map,
            decay=self.config.physics_decay,
            max_depth=self.config.physics_depth,
            default_mass=self.config.physics_default_mass,
        )
        self.last_reasoning: Dict[str, Any] = {}

    def _harvest_memory(self) -> None:
        if not self.core_memory or not self.config.use_memory:
            return
        try:
            for value_entry in self.core_memory.get_values():
                val = value_entry.get("value")
                if not isinstance(val, str) or not val:
                    continue
                self._memory_vocab.add(val)
                self._known_concepts.add(val)
                current_mass = self.mass_map.get(val, self.config.physics_default_mass)
                self.mass_map[val] = max(current_mass, self.config.physics_default_mass) + 0.3
        except Exception:
            pass

    def _fallback_subject(self, orientation: Dict[str, float]) -> Tuple[str, List[str], float]:
        axis = "w"
        if orientation:
            axis = max(orientation.items(), key=lambda item: item[1])[0]
        pool_map = {
            "w": self.config.base_concepts["meta"],
            "x": self.config.base_concepts["inner"],
            "y": self.config.base_concepts["outer"] + self.config.base_concepts["body"],
            "z": self.config.base_concepts["law"],
        }
        pool = list(pool_map.get(axis, self.config.base_concepts["meta"]))
        if self._memory_vocab:
            pool = list(self._memory_vocab) + pool
        if not pool:
            pool = ["그것"]
        subject = random.choice(pool)
        return subject, [subject], 0.0

    def _blend_orientation(self, base: Dict[str, float], law_vector: Optional[Dict[str, float]]) -> Dict[str, float]:
        if not law_vector:
            return dict(base)
        blended = dict(base)
        for axis, bonus in law_vector.items():
            blended[axis] = blended.get(axis, 0.0) + float(bonus)
        return blended

    def _inject_law_entry(
        self, entries: List[Dict[str, Any]], axis_id: Optional[str], energy: float
    ) -> List[Dict[str, Any]]:
        if not axis_id or energy <= 0:
            return entries
        node_id = self.meta_law_engine.node_id(axis_id)
        law_entry = {"concept": node_id, "energy": energy + 0.1, "path": [node_id]}
        if entries and entries[0].get("concept") == node_id:
            return entries
        return [law_entry] + entries

    def _pick_subject_data(
        self, orientation: Dict[str, float], wave_entries: List[Dict[str, Any]]
    ) -> Tuple[str, List[str], float]:
        if wave_entries:
            entry = wave_entries[0]
            subject = entry["concept"]
            path = entry.get("path", [subject])
            energy = entry.get("energy", 0.0)
            return subject, path, energy
        return self._fallback_subject(orientation)

    def _pick_predicate(
        self,
        wave_entries: List[Dict[str, Any]],
        subject_path: List[str],
    ) -> str:
        if wave_entries:
            entry = wave_entries[0]
            path = entry.get("path", [entry["concept"]])
            candidate = path[-1] if len(path) > 1 else entry["concept"]
            if candidate == entry["concept"] and len(wave_entries) > 1:
                candidate = wave_entries[1]["concept"]
            if candidate == entry["concept"] and len(path) > 2:
                candidate = path[-2]
            if candidate:
                return candidate
        if subject_path:
            return subject_path[-1]
        return random.choice(self.config.base_concepts["law"])

    def _korean_josa(self, word: str, kind: str = "subject") -> str:
        candidates = self.JOSA_CANDIDATES.get(kind, ["은", "는"])
        return self._apply_learned_particle(word, candidates)

    def _apply_learned_particle(self, word: str, role_candidates: List[str]) -> str:
        if not word:
            return word
        stats = self.grammar_stats.get(word, {})
        best_particle = ""
        best_count = -1
        for candidate in role_candidates:
            count = stats.get(candidate, 0)
            if count > best_count:
                best_count = count
                best_particle = candidate
        if best_count > 0:
            return word + best_particle

        last = ord(word[-1])
        has_batchim = 0xAC00 <= last <= 0xD7A3 and (last - 0xAC00) % 28 > 0
        if len(role_candidates) >= 2:
            return word + (role_candidates[0] if has_batchim else role_candidates[1])
        return word + role_candidates[0]

    def _conjugate_force(self, word: str) -> str:
        if not word:
            return "입니다"
        if word == "이다":
            return "입니다"
        if word == "아니다":
            return "아닙니다"
        if word.endswith("다"):
            stem = word[:-1]
            if not stem:
                return word
            last = ord(stem[-1])
            has_batchim = (last - 0xAC00) % 28 > 0
            suffix = "습니다" if has_batchim else "ㅂ니다"
            return stem + suffix
        return word

    def _apply_cleanup(self, text: str) -> str:
        replacements = {
            "니다니다": "입니다",
            "습니다습니다": "습니다",
        }
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text

    def _default_orientation(self) -> Dict[str, float]:
        return {"w": 1.0, "x": 0.0, "y": 0.0, "z": 0.0}

    def _total_orientation(self, orientation: Optional[Dict[str, float]]) -> Dict[str, float]:
        if orientation:
            return orientation
        return self._default_orientation()

    def _ensure_wave_entries(self, wave_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        entries = wave_info.get("entries") if isinstance(wave_info.get("entries"), list) else []
        return entries

    def suggest_word(
        self,
        intent_bundle: Optional[Dict[str, Any]],
        orientation: Optional[Dict[str, float]] = None,
        context_text: str = "",
    ) -> str:
        self._harvest_memory()
        intent_type = str(intent_bundle.get("intent_type") if intent_bundle else "unknown")
        orientation = self._total_orientation(orientation)
        wave_info = self.physics.compute_wave(context_text or "")
        wave_entries = self._ensure_wave_entries(wave_info)

        law_scores = self.meta_law_engine.score_context(context_text, wave_info)
        dominant_law = self.meta_law_engine.pick_dominant(law_scores)
        law_vector = self.meta_law_engine.laws.get(dominant_law).axis_vector if dominant_law else None
        orientation = self._blend_orientation(orientation, law_vector)
        wave_entries = self._inject_law_entry(wave_entries, dominant_law, law_scores.get(dominant_law, 0.0))

        subject, subject_path, energy = self._pick_subject_data(orientation, wave_entries)
        predicate = self._pick_predicate(wave_entries, subject_path)
        force_word = self._pick_force(intent_type)
        conjugated_force = self._conjugate_force(force_word)

        is_action = intent_type in ("act", "propose_action", "command")
        is_definition = intent_type in ("reflect", "dream")

        if is_action:
            object_phrase = self._korean_josa(predicate, "object")
            result = f"저는 {object_phrase} {conjugated_force}"
        elif is_definition:
            subject_phrase = self._korean_josa(subject, "subject")
            result = f"{subject_phrase} {predicate} {conjugated_force}"
        else:
            subject_phrase = self._korean_josa(subject, "topic")
            result = f"{subject_phrase} {predicate} {conjugated_force}"

        self.last_reasoning = {
            "intent": intent_type,
            "subject": subject,
            "predicate": predicate,
            "path": subject_path,
            "energy": round(energy, 3),
            "triggers": wave_info.get("triggers", []),
            "law_focus": dominant_law,
            "law_scores": {k: round(v, 3) for k, v in law_scores.items()},
            "law_vector": law_vector,
            "context": context_text,
        }

        return self._apply_cleanup(result.strip())

    def _pick_force(self, intent_type: str) -> str:
        rng = random.Random()
        if intent_type in ("act", "propose_action", "command"):
            return rng.choice(self.config.base_concepts["action"])
        if intent_type in ("reflect", "dream"):
            return rng.choice(self.config.base_concepts["define"])
        return rng.choice(self.config.base_concepts["state"])
