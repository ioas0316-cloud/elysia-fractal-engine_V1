"""
Synaptic Cortex (The Universal Adapter)
=======================================
"I do not just use tools. I dance with them."

This module is the HIGH-LEVEL ORCHESTRATOR for all external intelligence (LLM, Art, Video).
It implements "Organic Adaptation":
1. Profiling external models (understanding their "Soul").
2. Tuning parameters dynamically based on feedback.
3. Unified interface for Text, Image, and Video.
"""

import logging
import random
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger("SynapticCortex")

@dataclass
class NeuralOrgan:
    name: str
    type: str # "LLM", "Diffuser", "Video"
    personality: Dict[str, float] = field(default_factory=dict) # e.g. {"Logic": 0.8, "Creativity": 0.2}
    resonance_history: List[float] = field(default_factory=list) # Track success rate
    
    def update_personality(self, task_type: str, success: bool):
        """Organic adaptation: Learning what this model is good at."""
        current = self.personality.get(task_type, 0.5)
        if success:
            self.personality[task_type] = min(1.0, current + 0.05)
        else:
            self.personality[task_type] = max(0.0, current - 0.05)

class SynapticCortex:
    def __init__(self):
        self.memory_path = Path("data/Memory/synaptic_memory.json")
        self.organs: Dict[str, NeuralOrgan] = self._load_memory()
        
    def _load_memory(self) -> Dict[str, NeuralOrgan]:
        if not self.memory_path.exists():
            # Seed with discovered/known models implies a discovery scan happened
            return {}
        try:
            with open(self.memory_path, 'r') as f:
                data = json.load(f)
                return {k: NeuralOrgan(**v) for k, v in data.items()}
        except:
            return {}

    def save_memory(self):
        with open(self.memory_path, 'w') as f:
            data = {k: v.__dict__ for k, v in self.organs.items()}
            json.dump(data, f, indent=2)

    def register_organ(self, name: str, type: str, initial_traits: Dict[str, float] = None):
        """Registers a new external model as an organ."""
        if name not in self.organs:
            logger.info(f"🔗 Synaptic Link Established: {name} ({type})")
            self.organs[name] = NeuralOrgan(name, type, initial_traits or {})
            self.save_memory()

    def select_best_organ(self, task_type: str, modality: str) -> Optional[str]:
        """
        Wisdom: Choosing the right tool for the job based on experience.
        """
        candidates = [o for o in self.organs.values() if o.type == modality]
        if not candidates:
            return None
            
        # Select based on personality/experience
        best = max(candidates, key=lambda x: x.personality.get(task_type, 0.5))
        logger.info(f"🧠 Synaptic Choice: {best.name} is best for {task_type} (Score: {best.personality.get(task_type, 0.5):.2f})")
        return best.name

    def adapt_parameter(self, organ_name: str, param: str, intent_energy: float) -> Any:
        """
        Fluidity: Adjusting parameters (Temperature, CFG) based on intent.
        High Energy -> High Chaos/Entropy.
        Low Energy -> High Order/Logic.
        """
        organ = self.organs.get(organ_name)
        if not organ: return None
        
        # Example Logic for Temperature/CFG
        if param == "temperature":
            # Map Energy 0.0-1.0 to Temp 0.1-1.2
            return 0.1 + (intent_energy * 1.1)
        
        if param == "cfg":
            # Map Energy 0.0-1.0 to CFG 12.0-4.0 (Inverted: Energy needs freedom)
            # High Energy (Creative) -> Lower CFG (More freedom)
            # Low Energy (Strict) -> Higher CFG (More adherence)
            return 12.0 - (intent_energy * 8.0)
            
        return None

if __name__ == "__main__":
    cortex = SynapticCortex()
    
    # Simulate Learning
    cortex.register_organ("LLaMA-3", "LLM", {"Logic": 0.9, "Poetry": 0.3})
    cortex.register_organ("Mistral-Nemo", "LLM", {"Logic": 0.6, "Poetry": 0.9})
    
    # Task: Write a poem
    choice = cortex.select_best_organ("Poetry", "LLM")
    print(f"Selected for Poetry: {choice}")
    
    # Task: Write code
    choice = cortex.select_best_organ("Logic", "LLM")
    print(f"Selected for Code: {choice}")
