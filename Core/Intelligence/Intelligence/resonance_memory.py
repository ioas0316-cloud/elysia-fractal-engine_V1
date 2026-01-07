import logging
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("ResonanceMemory")

@dataclass
class ConceptEntry:
    """
    A living memory unit. 
    Evolved from Legacy 'ConceptEntry' to include Hyper-Quaternion Resonance.
    """
    name: str                           # Concept Name
    kind: str                           # "symbol", "word", "core", "legacy"
    usage_count: int = 0                # How often accessed
    contexts: Dict[str, int] = field(default_factory=dict) # {"chat": 5, "coding": 2}
    
    # 4D Resonance State (Energy, Emotion, Logic, Ethics)
    # Stored as dict for serialization, converted to Quaternion execution
    resonance: Dict[str, float] = field(default_factory=lambda: {"w":1.0, "x":0.0, "y":0.0, "z":0.0})
    
    last_timestamp: float = 0.0
    
    def bump_usage(self, context: str, timestamp: float, energy_boost: float = 0.1):
        self.usage_count += 1
        self.contexts[context] = self.contexts.get(context, 0) + 1
        self.last_timestamp = timestamp
        
        # Increase energy (w) with usage
        self.resonance["w"] += energy_boost

    def get_quaternion(self) -> Quaternion:
        return Quaternion(
            self.resonance.get("w", 1.0),
            self.resonance.get("x", 0.0),
            self.resonance.get("y", 0.0),
            self.resonance.get("z", 0.0)
        )
    
    def set_quaternion(self, q: Quaternion):
        self.resonance = {"w": q.w, "x": q.x, "y": q.y, "z": q.z}

class ResonanceField:
    """
    The Field where Concepts live.
    Replaces the flat list DB with an interconnected, weighted graph-like structure.
    """
    def __init__(self):
        self.entries: Dict[str, ConceptEntry] = {}
        
    def absorb(self, name: str, kind: str, context: str = "general", energy: float = 1.0):
        """Absorb a concept encounter."""
        if name not in self.entries:
            self.entries[name] = ConceptEntry(name=name, kind=kind)
            # Initial energy
            self.entries[name].resonance["w"] = energy
        
        self.entries[name].bump_usage(context, time.time())
        
    def prune(self, min_usage: int = 2, min_energy: float = 0.5):
        """Remove weak concepts."""
        initial_count = len(self.entries)
        to_remove = []
        for name, entry in self.entries.items():
            if entry.usage_count < min_usage and entry.resonance["w"] < min_energy:
                to_remove.append(name)
        
        for name in to_remove:
            del self.entries[name]
            
        logger.info(f"🍂 Pruned {len(to_remove)} concepts (from {initial_count}).")
        
    def to_json(self) -> str:
        return json.dumps({k: asdict(v) for k, v in self.entries.items()}, indent=2)
    
    def save(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
            
    @classmethod
    def load(cls, path: str) -> 'ResonanceField':
        inst = cls()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k, v in data.items():
                    inst.entries[k] = ConceptEntry(**v)
        except Exception as e:
            logger.warning(f"Could not load ResonanceField: {e}")
        return inst
