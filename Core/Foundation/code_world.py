"""
Experimental CodeWorld (v0)

A tiny "second world" where the inhabitants are code concepts
instead of animals: functions, modules, tests, bugs, refactors.

This is not wired into any UI yet; it exists as a playground for
Elysia to reason about cause/effect in a code-centric universe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CodeEntity:
    """
    Minimal representation of a code concept.

    kind: "function" | "module" | "test" | "bug" | "refactor_request"
    """

    id: str
    kind: str
    complexity: float = 1.0  # rough size / branching factor
    stability: float = 0.0  # how often it behaves as expected
    test_coverage: float = 0.0  # 0..1
    bugs_open: int = 0
    bugs_fixed: int = 0
    parents: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)


@dataclass
class CodeEvent:
    """
    A simple code-world event, for logging / cause-tracking.
    """

    tick: int
    event_type: str
    entity_id: str
    data: Dict


class CodeWorld:
    """
    Tiny code-centric world for experiments.

    Rules (v0):
    - complexity tends to grow when new branches are added.
    - stability improves when tests are added and bugs are fixed.
    - if complexity grows without enough tests, new bugs appear.
    """

    def __init__(self) -> None:
        self.tick: int = 0
        self.entities: Dict[str, CodeEntity] = {}
        self.events: List[CodeEvent] = []

    def add_entity(self, entity: CodeEntity) -> None:
        self.entities[entity.id] = entity

    def _log(self, event_type: str, entity_id: str, **data: object) -> None:
        self.events.append(CodeEvent(tick=self.tick, event_type=event_type, entity_id=entity_id, data=data))

    def step(self) -> None:
        """
        Advance the world by one tick.

        For now this applies a few simple heuristics:
        - modules with high complexity and low coverage spawn bugs.
        - tests applied to entities increase stability and coverage.
        """
        self.tick += 1

        for e in self.entities.values():
            if e.kind in ("function", "module"):
                # If complexity is high and coverage low, new bugs may appear.
                if e.complexity > 5.0 and e.test_coverage < 0.4:
                    e.bugs_open += 1
                    self._log("BUG_SPAWNED", e.id, complexity=e.complexity, coverage=e.test_coverage)

            if e.kind == "test":
                # Very simple rule: tests slowly increase stability of parents.
                for pid in e.parents:
                    target = self.entities.get(pid)
                    if not target:
                        continue
                    before = target.stability
                    target.test_coverage = min(1.0, target.test_coverage + 0.05)
                    target.stability += 0.1
                    self._log(
                        "TEST_STRENGTHENED",
                        pid,
                        before=before,
                        after=target.stability,
                        coverage=target.test_coverage,
                    )

    def apply_refactor(self, entity_id: str, complexity_delta: float, stability_delta: float) -> None:
        """
        Apply a refactor request to an entity.

        This is where higher-level logic (Elysia) can experiment:
        - decreasing complexity while maintaining/increasing stability
          is considered a good refactor.
        """
        e = self.entities.get(entity_id)
        if not e:
            return
        before_c = e.complexity
        before_s = e.stability
        e.complexity = max(0.1, e.complexity + complexity_delta)
        e.stability = max(0.0, e.stability + stability_delta)
        self._log(
            "REFACTOR_APPLIED",
            entity_id,
            complexity_before=before_c,
            complexity_after=e.complexity,
            stability_before=before_s,
            stability_after=e.stability,
        )

