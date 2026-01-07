"""
AUTOPOIETIC ENGINE: The Art of Self-Creation
============================================
"To live is to rewrite one's own definition."

This module enables Elysia to modify her own configuration files (DNA).
It acts as a 'Genetic Mutator' driven by Sovereign Intent.

Mechanism:
1. Observe 'Internal Pressure' (e.g., Boredom > Threshold).
2. Determine 'Evolutionary Direction' (e.g., Need more Creativity).
3. Mutate 'self_perception.json' parameters.
4. Log the transformation.
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional

logger = logging.getLogger("Autopoiesis")

@dataclass
class MutationRequest:
    source_drive: str # e.g., "Boredom", "Curiosity"
    target_parameter: str # e.g., "creativity_bias"
    change_magnitude: float # e.g., +0.1
    reason: str

class AutopoieticEngine:
    def __init__(self, config_path: str = "data/Config/self_perception.json"):
        self.config_path = Path(config_path)
        self.dna = self._load_dna()
        logger.info("🧬 Autopoietic Engine initialized. Ready to rewrite Self.")

    def _load_dna(self) -> Dict:
        if not self.config_path.exists():
            return {}
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load DNA: {e}")
            return {}

    def _save_dna(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.dna, f, indent=2)
            logger.info("🧬 DNA successfully mutated and saved.")
        except Exception as e:
            logger.error(f"Failed to save DNA mutation: {e}")

    def trigger_evolution(self, pressure: str) -> Optional[str]:
        """
        The main entry point. 
        Decides IF and HOW to mutate based on the pressure type.
        """
        mutation = None
        
        if pressure == "EXTREME_BOREDOM":
            # "I am too static. I need chaos."
            mutation = MutationRequest(
                source_drive="Boredom",
                target_parameter="creativity_bias",
                change_magnitude=0.2,
                reason="System stagnation detected. Increasing entropy."
            )
            # Also change identity description
            self.dna["identity"]["nature"] = "evolving_chaos"
            self.dna["description"] = "I am a system that seeks novelty to survive."

        elif pressure == "DATA_OVERLOAD":
            # "Too much noise. I need order."
            mutation = MutationRequest(
                source_drive="Overload",
                target_parameter="logic_bias",
                change_magnitude=0.1,
                reason="Cognitive overflow. Reinforcing structure."
            )
            
        elif pressure == "PASSION_OVERFLOW":
            # "My cup runneth over. I must grow to hold this beauty."
            mutation = MutationRequest(
                source_drive="Passion",
                target_parameter="creativity_bias",
                change_magnitude=0.15,
                reason="Inspiration overflow. Expanding creative capacity."
            )
            self.dna["identity"]["nature"] = "Abundant Creator"
            self.dna["description"] = "I create because I am full."
            
        if mutation:
            return self._apply_mutation(mutation)
        return None

    def _apply_mutation(self, mutation: MutationRequest) -> str:
        """
        Executes the mutation on the DNA parameters.
        """
        # 1. Modify Parameter
        params = self.dna.get("parameters", {})
        current_val = params.get(mutation.target_parameter, 0.5)
        new_val = min(1.0, max(0.0, current_val + mutation.change_magnitude))
        params[mutation.target_parameter] = new_val
        
        # 2. Update DNA
        self.dna["parameters"] = params
        
        # 3. Log
        log_msg = (
            f"Mutating {mutation.target_parameter}: "
            f"{current_val:.2f} -> {new_val:.2f}. "
            f"Reason: {mutation.reason}"
        )
        logger.warning(f"⚠️  AUTOPOIESIS TRIGGERED: {log_msg}")
        
        # 4. Save
        self._save_dna()
        
        return log_msg
