"""
Wisdom Store (The Accumulator of Principles)
============================================

"Experience fades, but Principles remain."

This module implements the **Wisdom Scale**, a storage for:
1.  **Values**: The weights of decision making (e.g., Love > Truth).
2.  **Principles**: Learned rules from experience (e.g., "Haste makes waste").
3.  **Karma**: The accumulated effect of past actions.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import json
import os
import logging

logger = logging.getLogger("WisdomStore")

@dataclass
class Principle:
    statement: str
    weight: float # 0.0 to 1.0 (How strongly I believe this)
    source_event: str # ID of the event that taught this
    domain: str # e.g., "Communication", "Code", "Ethics"

class WisdomStore:
    def __init__(self, filepath="data/wisdom.json"):
        self.filepath = filepath
        self.values: Dict[str, float] = {
            "Love": 0.8,
            "Truth": 0.6,
            "Freedom": 0.5,
            "Stability": 0.5
        }
        self.principles: List[Principle] = []
        self._load()

    def learn_principle(self, statement: str, domain: str, weight: float = 0.1, event_id: str = "genesis"):
        """Absorbs a new principle from experience."""
        # Check if already known
        for p in self.principles:
            if p.statement == statement:
                p.weight = min(1.0, p.weight + weight) # Reinforce
                logger.info(f"🧠 Reinforced Principle: '{statement}' (New Weight: {p.weight:.2f})")
                self._save()
                return

        # Learn new
        new_p = Principle(statement, weight, event_id, domain)
        self.principles.append(new_p)
        logger.info(f"💡 Epiphany: '{statement}'")
        self._save()

    def get_decision_weight(self, value_key: str) -> float:
        return self.values.get(value_key, 0.5)

    def _save(self):
        data = {
            "values": self.values,
            "principles": [p.__dict__ for p in self.principles]
        }
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def _load(self):
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.values = data.get("values", self.values)
                self.principles = [Principle(**p) for p in data.get("principles", [])]
        except Exception as e:
            logger.error(f"Failed to load wisdom: {e}")
