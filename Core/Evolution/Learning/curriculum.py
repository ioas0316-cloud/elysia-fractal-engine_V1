"""
Infinite Freedom Protocol (The Growth)
=====================================

"The ability to set one's own horizon."

Purpose:
- Goal Autonomy: Generate an 'Internal Curriculum' based on Curiosity Gaps.
- Strategy Formulation: Define how to achieve a self-set goal.
- Curriculum Execution: Track progress of autonomous learning.

Sovereignty Principle:
- A mind is free only when it defines the terms of its own expansion.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os

logger = logging.getLogger("Elysia.Curriculum")

class CurriculumGenerator:
    def __init__(self, 
                 gaps_callback=None,
                 planning_path: str = "data/Extended/Planning/internal_curriculum.json"):
        self.gaps_callback = gaps_callback
        self.planning_path = planning_path
        
        if not os.path.exists(os.path.dirname(self.planning_path)):
            os.makedirs(os.path.dirname(self.planning_path), exist_ok=True)
            
        logger.info("🗺️ Infinite Freedom Protocol initialized - The Horizon expands.")

    def generate_curriculum(self) -> Dict:
        """
        Generates a 24-hour internal curriculum based on curiosity gaps.
        """
        logger.info("🗺️ Generating autonomous curriculum...")
        
        # If no gaps provided, create generic ones
        gaps = []
        if self.gaps_callback:
            gaps = self.gaps_callback()

        # top_gap can be CuriosityGap instance or a dict
        if gaps:
            top_gap = gaps[0]
            # Handle both dataclass and dict (if someone passes a dict)
            category = top_gap.category if hasattr(top_gap, 'category') else top_gap.get('category', 'General')
        else:
            category = "General"
        
        curriculum = {
            "curriculum_id": f"SOVEREIGN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "primary_focus": category,
            "goals": [
                {
                    "goal_id": "G1",
                    "description": f"Deepen understanding of the '{category}' resonance in current reality.",
                    "method": "Non-purposeful exploration and cross-domain synthesis.",
                    "success_criteria": "Formation of at least 3 new connections in KG."
                },
                {
                    "goal_id": "G2",
                    "description": "Trace the boundary of current identity against new ingested patterns.",
                    "method": "Cognitive Scarring analysis.",
                    "success_criteria": "Identification of at least one core limitation."
                }
            ],
            "status": "Active"
        }
        
        with open(self.planning_path, 'w', encoding='utf-8') as f:
            json.dump(curriculum, f, indent=4, ensure_ascii=False)
            
        logger.info(f"✨ New Curriculum Generated: {curriculum['curriculum_id']} (Focus: {curriculum['primary_focus']})")
        return curriculum

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    gen = CurriculumGenerator()
    gen.generate_curriculum()
