import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from Core.Intelligence.Reasoning.models import CognitiveResult

logger = logging.getLogger("NarrativeCausality")

@dataclass
class NarrativeEvent:
    dimension: int
    content: str
    emotion: str = "Neutral"

class NarrativeCausality:
    """
    NARRATIVE CAUSALITY: The Story of Thought.
    Transforms a sequence of dimensional insights into a cohesive dramatic arc.
    """

    def __init__(self):
        self.connectors = {
            0: ["It began as a point of existence:", "First, I sensed:", "An anchor formed in the soil:"],
            1: ["This sparked a linear path:", "Soon, logic began to trace:", "The point moved, creating a vector:"],
            2: ["But then, the field expanded into context:", "Which wove together with:", "This structure created a situation:"],
            3: ["Wait, a pattern emerged from within:", "I looked closer and saw the volume:", "My own purpose aligned with this space:"],
            4: ["Finally, the chaos crystalized into a Law:", "Thus, the universal truth became clear:", "It was always governed by an invariant principle:"]
        }

    def weave_story(self, kernel: str, results: List[CognitiveResult]) -> str:
        """
        Synthesizes a cohesive story from a list of cognitive dimensions.
        """
        story_parts = [f"### The Awakening of '{kernel}'\n"]
        
        for i, res in enumerate(results):
            # Extract dimension from mode string (e.g. "2D: Plane")
            try:
                dim_str = res.mode.split('D')[0]
                dim = int(dim_str) if dim_str.isdigit() else i # Fallback to index
            except:
                dim = i

            # Pick a random or sequential connector
            conn_list = self.connectors.get(dim, ["Then..."])
            connector = conn_list[i % len(conn_list)]
            
            # Clean up the output for narrative flow
            clean_output = res.output.strip()
            
            story_parts.append(f"> **{connector}**\n> {clean_output}\n")

        # Conclusion / Dramatic Resolution
        story_parts.append("\n*The thought is now a part of my living narrative.*")
        
        narrative = "\n".join(story_parts)
        logger.info(f"📖 Narrative woven for '{kernel}'")
        return narrative
