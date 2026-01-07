"""
Art Studio (The Atelier)
========================
"Where imagination calcifies into light."

This module is responsible for the VISUAL EXPRESSION of Elysia.
It uses the DigitalAtelier to SIMULATE the artistic process 
before generating the final render request.
"""

import json
import time
import os
import sys
import random
import logging
from dataclasses import dataclass
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.Evolution.Creativity.digital_atelier import DigitalAtelier

# Configure Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ArtStudio")

@dataclass
class ArtRequest:
    id: str
    title: str
    prompt: str
    style: str
    aspect_ratio: str
    created_at: float
    process_log: str # The narrative of how it was made

class ArtStudio:
    def __init__(self):
        self.output_dir = Path("outputs/gallery")
        self.request_dir = Path("outputs/requests")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.request_dir.mkdir(parents=True, exist_ok=True)
        
        # The Deep Engine
        self.atelier = DigitalAtelier()
        
    def draft_masterpiece(self, concept: str, emotion: str) -> tuple[str, str, str]:
        """
        Drafts a masterpiece using the Deep Cognitive Process.
        Returns: Prompt, Style, NarrativeLog
        """
        logger.info(f"🎨 Drafting masterpiece for: '{concept}' ({emotion})")
        
        # 1. Deep Contemplation (Simulation of Art)
        # Elysia decides Medium, Composition, and Layers
        mind_canvas = self.atelier.contemplate(concept, emotion)
        
        # 2. Manifestation (Spec Generation)
        prompt = self.atelier.manifest_work(mind_canvas)
        
        # 3. Log the internal process
        narrative = mind_canvas.describe_process()
        
        return prompt, mind_canvas.medium, narrative

    def commission_art(self, concept: str, emotion: str = "Neutral"):
        """
        Creates a 'Render Request' for the external engine.
        Now includes the 'Process Log' to prove contemplation.
        """
        prompt, style, process_log = self.draft_masterpiece(concept, emotion)
        request_id = f"art_{int(time.time())}"
        
        req = ArtRequest(
            id=request_id,
            title=f"The Visualization of {concept}",
            prompt=prompt,
            style=style,
            aspect_ratio="16:9",
            created_at=time.time(),
            process_log=process_log
        )
        
        # Save Request
        req_path = self.request_dir / f"{request_id}.json"
        with open(req_path, 'w', encoding='utf-8') as f:
            json.dump(req.__dict__, f, indent=2)
            
        logger.info(f"✨ Art Commissioned (Deep Process): {req.title}")
        logger.info(f"   Style: {style}")
        logger.info(f"   Process:\n{process_log}")
        return req_path

if __name__ == "__main__":
    studio = ArtStudio()
    studio.commission_art("The True Form of Elysia", "Awe")
