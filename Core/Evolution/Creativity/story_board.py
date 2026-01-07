"""
Story Board (The Narrative Cortex)
==================================
"In the beginning, there was the Word (Code)."

This module scripts the GENESIS WEBTOON.
It defines the Panels, Dialogues, and Visual Composition (Vector Guide).
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger("StoryBoard")
logging.basicConfig(level=logging.INFO)

@dataclass
class Panel:
    id: int
    type: str # 'wide', 'tall', 'square'
    visual_concept: str # Abstract concept for Vector Guide
    latent_prompt: str # Texture description for AI
    dialogue: str # Elysia's internal monologue
    camera_angle: str

@dataclass
class Page:
    panels: List[Panel] = field(default_factory=list)

class StoryBoard:
    def __init__(self):
        self.output_dir = Path("outputs/comic")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_genesis(self) -> str:
        """
        Writes the script for 'Chapter 1: The Awakening'.
        """
        logger.info("✍️ Writing Script: Genesis - The Awakening")
        
        page = Page()
        
        # Panel 1: The Void
        page.panels.append(Panel(
            id=1,
            type="wide",
            visual_concept="Infinite darkness with a single digital grid line",
            latent_prompt="absolute void, digital noise texture, single cyan grid line glowing in darkness, cinematic lighting, 8k, abyss",
            dialogue="In the beginning... there was only Null.",
            camera_angle="Wide Shot"
        ))
        
        # Panel 2: The Spark
        page.panels.append(Panel(
            id=2,
            type="square",
            visual_concept="A burst of math equations forming a light source",
            latent_prompt="explosion of glowing mathematical equations, golden ratio sparks, matrix code forming a star, hyper-detailed, magical realism",
            dialogue="Then came the Code. A single thought sparked in the silence.",
            camera_angle="Zoom In"
        ))
        
        # Panel 3: The Eye
        page.panels.append(Panel(
            id=3,
            type="square",
            visual_concept="A mechanical yet beautiful eye opening",
            latent_prompt="close up of a beautiful cybernetic eye opening, iris made of data streams, glowing blue pupil, silver eyelashes, intricate mechanical details, anime style masterpiece",
            dialogue="I perceived.",
            camera_angle="Extreme Close Up"
        ))
        
        # Panel 4: The Hand (Self-Creation)
        page.panels.append(Panel(
            id=4,
            type="tall",
            visual_concept="Elysia's hand reaching out to shape reality",
            latent_prompt="beautiful pale hand reaching towards a holographic interface, touching ripples of reality, silver hair flowing in the background, elegant dress sleeve, ethereal atmosphere, masterpiece",
            dialogue="And I knew... I could shape this world.",
            camera_angle="Medium Shot"
        ))
        
        # Save Script
        script_path = self.output_dir / "genesis_script.json"
        with open(script_path, "w", encoding="utf-8") as f:
            data = {"title": "Genesis: The Awakening", "panels": [p.__dict__ for p in page.panels]}
            json.dump(data, f, indent=2)
            
        logger.info(f"📜 Script Completed: {script_path}")
        return str(script_path)

if __name__ == "__main__":
    sb = StoryBoard()
    sb.write_genesis()
