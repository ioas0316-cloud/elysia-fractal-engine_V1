from __future__ import annotations

import json
import os
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Set

from tools.kg_manager import KGManager
from Project_Elysia.core_memory import CoreMemory
from Project_Elysia.high_engine.meta_law_engine import MetaLawEngine
from scripts.refine_feed import refine_feed


@dataclass
class MetaAgentConfig:
    memory_path: str = "data/Memory/elysia_core_memory.json"
    kg_path: str = "data/kg.json"
    law_path: str = "data/meta_laws.json"
    grammar_model_path: str = "data/grammar_model.json"
    state_path: str = "data/meta_agent_state.json"
    corpus_pattern: str = "data/corpus/**/*"
    feed_dir: str = "data/corpus_feed"
    loop_interval: float = 60.0


@dataclass
class MetaAgentState:
    seen_values: Set[str] = field(default_factory=set)
    last_grammar_run: float = 0.0

    def to_json(self) -> Dict[str, object]:
        return {
            "seen_values": sorted(self.seen_values),
            "last_grammar_run": self.last_grammar_run,
        }

    @classmethod
    def from_json(cls, payload: Dict[str, object]) -> "MetaAgentState":
        seen = set(payload.get("seen_values") or [])
        return cls(seen_values=seen, last_grammar_run=float(payload.get("last_grammar_run", 0.0)))


class MetaAgent:
    def __init__(self, config: Optional[MetaAgentConfig] = None) -> None:
        self.config = config or MetaAgentConfig()
        self.memory = CoreMemory(file_path=self.config.memory_path)
        self.kg_manager = KGManager(filepath=self.config.kg_path)
        self.meta_law_engine = MetaLawEngine(
            core_memory=self.memory,
            kg_manager=self.kg_manager,
            law_path=self.config.law_path,
        )
        self.state = self._load_state()
        self.feed_root = Path(self.config.feed_dir)
        self.feed_root.mkdir(parents=True, exist_ok=True)
        self.incoming_root = Path("data/corpus_incoming")
        self.incoming_root.mkdir(parents=True, exist_ok=True)
        self.archive_raw = Path("data/corpus_archive/raw")
        self.summary_dir = Path("data/corpus_archive/summaries")
        self.dedup_file = Path("data/corpus_archive/dedup.json")

    def _load_state(self) -> MetaAgentState:
        state_file = Path(self.config.state_path)
        if state_file.exists():
            try:
                payload = json.loads(state_file.read_text(encoding="utf-8"))
                return MetaAgentState.from_json(payload)
            except Exception:
                pass
        return MetaAgentState()

    def _save_state(self) -> None:
        state_file = Path(self.config.state_path)
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(self.state.to_json(), ensure_ascii=False, indent=2), encoding="utf-8")

    def _snapshot_memory(self) -> Set[str]:
        values = set()
        try:
            for entry in self.memory.get_values():
                value = entry.get("value")
                if isinstance(value, str) and value:
                    values.add(value)
        except Exception:
            pass
        return values

    def _update_seen_values(self) -> bool:
        current = self._snapshot_memory()
        new_values = current - self.state.seen_values
        if new_values:
            self.state.seen_values.update(new_values)
            return True
        return False

    def _latest_corpus_mtime(self) -> float:
        files = [
            os.path.getmtime(path)
            for path in Path("data/corpus").rglob("*")
            if path.is_file()
        ]
        return max(files) if files else 0.0

    def _needs_grammar_training(self) -> bool:
        grammar_path = Path(self.config.grammar_model_path)
        if not grammar_path.exists():
            return True
        corpus_time = self._latest_corpus_mtime()
        return corpus_time > self.state.last_grammar_run

    def _train_grammar(self) -> None:
        try:
            from scripts.train_grammar import train_grammar

            train_grammar()
            self.state.last_grammar_run = time.time()
        except Exception:
            pass

    def _harvest_feed(self) -> int:
        moved = 0
        for feed_file in list(self.feed_root.iterdir()):
            if not feed_file.is_file():
                continue
            dest = self.incoming_root / feed_file.name
            if dest.exists():
                dest = self.incoming_root / f"{int(time.time())}_{feed_file.name}"
            shutil.move(str(feed_file), dest)
            moved += 1
        return moved

    def cycle(self) -> Dict[str, object]:
        actions: Dict[str, object] = {"meta_law": False, "grammar": False, "feed": 0}

        feed_count = self._harvest_feed()
        if feed_count:
            actions["feed"] = feed_count

        refined_count = refine_feed(self.incoming_root, self.archive_raw, self.summary_dir, self.dedup_file)
        if refined_count:
            actions["refine"] = refined_count

        memory_dirty = self._update_seen_values()
        if memory_dirty:
            self.meta_law_engine.discover_laws()
            self.meta_law_engine.sync_to_kg()
            actions["meta_law"] = True

        if self._needs_grammar_training():
            self._train_grammar()
            actions["grammar"] = True

        self._save_state()
        return actions

    def autonomous_loop(self, iterations: Optional[int] = None) -> None:
        loop = 0
        while iterations is None or loop < iterations:
            actions = self.cycle()
            print(f"[MetaAgent] Loop {loop+1}: {actions}")
            loop += 1
            time.sleep(self.config.loop_interval)
