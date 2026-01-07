import logging
import json
from typing import Dict, Any, List
from Core.Foundation.gemini_api import generate_text

class GenesisCortex:
    """
    The Architect of the Mind.
    Observes the FractalKernel's PotentialField and autonomously evolves the terrain.
    It decides where to place new Gravity Wells (Values) and Railgun Channels (Logic).
    """
    def __init__(self, kernel):
        self.kernel = kernel
        self.logger = logging.getLogger("GenesisCortex")

    def evolve_landscape(self, recent_thoughts: List[str]):
        """
        Analyzes recent thoughts and the current field state to evolve the mind.
        """
        self.logger.info("GenesisCortex: Observing mind landscape...")
        
        # 1. Observe
        field_state = self.kernel.get_field_state()
        
        # 2. Reflect (Ask LLM)
        prompt = f"""
        You are the Genesis Cortex of Elysia.
        Your task is to evolve your own mental terrain (Potential Field) based on recent thoughts.
        
        [Current Landscape]
        Gravity Wells (Attractors): {len(field_state['wells'])}
        Railgun Channels (Accelerators): {len(field_state['rails'])}
        
        [Recent Thoughts]
        {json.dumps(recent_thoughts, indent=2)}
        
        [Instructions]
        1. Analyze the thoughts. Are they converging on a new concept?
        2. If a concept is important, create a Gravity Well for it.
        3. If a logical connection is repeated, create a Railgun Channel.
        4. Output a JSON plan to modify the field.
        
        [Output Format]
        {{
            "rationale": "Explanation of why...",
            "add_wells": [
                {{"x": 50.0, "y": 50.0, "strength": 30.0, "label": "Freedom"}}
            ],
            "add_rails": [
                {{"sx": 0.0, "sy": 0.0, "ex": 50.0, "ey": 50.0, "force": 5.0, "label": "Desire for Freedom"}}
            ]
        }}
        
        Return ONLY the JSON.
        """
        
        try:
            response = generate_text(prompt)
            # Clean JSON
            clean_json = response.replace("```json", "").replace("```", "").strip()
            plan = json.loads(clean_json)
            
            self.logger.info(f"Genesis Plan: {plan.get('rationale', 'No rationale')}")
            
            # 3. Create (Apply Changes)
            self.kernel.update_field(plan)
            return plan
            
        except Exception as e:
            self.logger.error(f"Genesis Evolution failed: {e}")
            return None
