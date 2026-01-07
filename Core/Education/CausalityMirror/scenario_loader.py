"""
THE MIRROR OF CAUSALITY: SCENARIO LOADER
========================================

"To read history is to read the mind of the dead."
"""

import json
from typing import Dict, List, Any
from .wave_structures import HistoricalWave, Zeitgeist, ChoiceNode, HyperQuaternion

class ScenarioLoader:
    def __init__(self):
        pass

    def load_zeitgeist(self, data: Dict[str, Any]) -> Zeitgeist:
        z_data = data.get("zeitgeist", {})
        return Zeitgeist(
            name=z_data.get("name", "Unknown Era"),
            conservative_inertia=z_data.get("inertia", 0.5),
            latent_desire=z_data.get("desire", 0.0),
            sophistication_level=z_data.get("sophistication", 0.5),
            dominant_frequency=z_data.get("frequency", 10.0)
        )

    def parse_choices(self, choices_data: List[Dict[str, Any]]) -> List[ChoiceNode]:
        parsed = []
        for c in choices_data:
            # Parse the intent vector
            iv = c.get("intent", {})
            q = HyperQuaternion(
                iv.get("w", 0), iv.get("x", 0), iv.get("y", 0), iv.get("z", 0)
            )
            
            parsed.append(ChoiceNode(
                id=c.get("id"),
                description=c.get("text"),
                required_role=c.get("role", "Any"),
                intent_vector=q,
                innovation_score=c.get("innovation", 0.0),
                risk_score=c.get("risk", 0.0),
                empathy_score=c.get("empathy", 0.0)
            ))
        return parsed

    def load_scenario(self, file_path: str) -> Dict[str, Any]:
        """
        Loads a JSON scenario and returns the Zeitgeist and Root Nodes.
        (Simplified for V1)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            zeitgeist = self.load_zeitgeist(data)
            # logic to parse nodes would go here
            
            return {
                "title": data.get("title"),
                "zeitgeist": zeitgeist,
                "roles": data.get("roles", ["Observer"]),
                "raw_data": data # Return raw for the runner to traverse
            }
        except Exception as e:
            print(f"Error loading scenario: {e}")
            return None
