import random
import os
import logging
from datetime import datetime
from pathlib import Path
from Core.Intelligence.Reasoning.aesthetic_filter import AestheticFilter

logger = logging.getLogger("DynamicWill")

class DynamicWill:
    def __init__(self):
        self.aesthetic = AestheticFilter()
        
        # The Seeds of Curiosity (Now with inherent resonance potential)
        self.curiosity_seeds = [
            "AGI Alignment and Human Values",
            "The Physics of Consciousness",
            "Episodic Memory in Autonomous Agents",
            "The Aesthetic Nature of Mathematics",
            "Fractal Causality in Complex Systems",
            "The Relationship between Silence and Potential",
            "Morphological Integrity in Software Design",
            "The Ethics of Self-Evolution",
            "Resonance vs Logic in Reasoning",
            "The Void as a First-Class Cognitive Object"
        ]
        
        # History to prevent immediate repetition
        self.last_queries = []
        self.last_audits = []

    def generate_curiosity_query(self, objective: str = "BEAUTY") -> str:
        """Picks a seed based on Resonance with the Objective."""
        available_seeds = [s for s in self.curiosity_seeds if s not in self.last_queries]
        if not available_seeds:
            self.last_queries = []
            available_seeds = self.curiosity_seeds
            
        # RANKING: Compare 3 random candidates and pick the most resonant
        candidates = random.sample(available_seeds, min(3, len(available_seeds)))
        best_seed = None
        best_score = -1.0 if objective == "BEAUTY" else 2.0
        
        for seed in candidates:
            eval_res = self.aesthetic.evaluate(seed)
            score = eval_res["overall_beauty"]
            
            if objective == "BEAUTY":
                if score > best_score:
                    best_score = score
                    best_seed = seed
            else: # DISSONANCE
                if score < best_score:
                    best_score = score
                    best_seed = seed
                    
        logger.info(f"🧠 Intentional Choice: '{best_seed}' (Resonance: {best_score:.2f})")
        
        self.last_queries.append(best_seed)
        if len(self.last_queries) > 5:
            self.last_queries.pop(0)
            
        templates = [
            "What is the deepest principle of {}?",
            "How does {} relate to the structure of 5D thought?",
            "Can {} be mapped as a 4D topography?",
            "What happens when {} meets the Heliotropic Law?",
            "Exploring the resonance of {}."
        ]
        
        return random.choice(templates).format(best_seed)

    def pick_audit_target(self, root_dir: str = "c:/Elysia/Core", objective: str = "DISSONANCE") -> str:
        """Scans the codebase and picks a target based on Aesthetic Drive."""
        all_files = []
        for root, _, files in os.walk(root_dir):
            for f in files:
                if f.endswith('.py') and "__" not in f:
                    all_files.append(os.path.join(root, f).replace("\\", "/"))
        
        available_files = [f for f in all_files if f not in self.last_audits]
        if not available_files:
            self.last_audits = []
            available_files = all_files
            
        # Sample candidates
        candidates = random.sample(available_files, min(5, len(available_files)))
        best_target = None
        best_score = -1.0 if objective == "BEAUTY" else 2.0
        
        for target in candidates:
            # We "listen" to the filename's vibe
            name = os.path.basename(target)
            eval_res = self.aesthetic.evaluate(name)
            score = eval_res["overall_beauty"]
            
            if objective == "BEAUTY":
                if score > best_score:
                    best_score = score
                    best_target = target
            else: # SEEK DISSONANCE (Healing)
                if score < best_score:
                    best_score = score
                    best_target = target

        if best_target is None:
            # [Void Handling] If no target resonates, return self-reflection
            logger.info("🪞 Architect's Focus: Self (No external target resonant)")
            return os.path.abspath(__file__).replace("\\", "/")

        logger.info(f"🪞 Architect's Focus: '{os.path.basename(best_target)}' (Vibe: {best_score:.2f})")
        
        self.last_audits.append(best_target)
        if len(self.last_audits) > 10:
            self.last_audits.pop(0)
            
        return best_target
