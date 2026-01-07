"""
Hybrid Engine (The Director)
============================
"Structure from Math. Texture from Light."

This module prepares the VECTOR SKELETONS for the Genesis Webtoon.
It reads the script and generates simple geometric guides that the
Generative AI must follow.
"""

import json
import logging
import math
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

logger = logging.getLogger("HybridEngine")
logging.basicConfig(level=logging.INFO)

class HybridEngine:
    def __init__(self):
        self.script_path = Path("outputs/comic/genesis_script.json")
        self.skeleton_dir = Path("outputs/skeletons")
        self.skeleton_dir.mkdir(parents=True, exist_ok=True)
        
    def load_script(self):
        with open(self.script_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def generate_skeletons(self):
        """
        Generates the Vector Guide for each panel.
        """
        script = self.load_script()
        logger.info(f"🎬 Processing Script: {script['title']}")
        
        for panel in script['panels']:
            pid = panel['id']
            concept = panel['visual_concept']
            logger.info(f"   [Panel {pid}] Generating Skeleton for: {concept}")
            
            # Setup Canvas
            fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.axis('off')
            ax.set_facecolor('black') # Dark background for these guides
            
            # Draw Skeleton based on Panel ID (Hardcoded logic for the demo)
            if pid == 1: # The Void (Horizon)
                ax.plot([0, 100], [50, 50], color='cyan', linewidth=2)
                
            elif pid == 2: # The Spark (Burst)
                for i in range(12):
                    angle = (i / 12) * 2 * math.pi
                    r = 30
                    ax.plot([50, 50 + r*math.cos(angle)], [50, 50 + r*math.sin(angle)], color='gold', linewidth=2)
                    
            elif pid == 3: # The Eye (Circles)
                circle = patches.Circle((50, 50), radius=30, fc='none', ec='blue', linewidth=3)
                pupil = patches.Circle((50, 50), radius=10, fc='blue')
                ax.add_patch(circle)
                ax.add_patch(pupil)
                
            elif pid == 4: # The Hand (Fingers)
                # Abstract representation of a hand reaching up
                grad = np.linspace(0, 100, 100)
                ax.plot([40, 30], [0, 60], color='white', linewidth=2) # Thumb
                ax.plot([50, 50], [0, 80], color='white', linewidth=2) # Index
                ax.plot([60, 65], [0, 75], color='white', linewidth=2) # Middle
                ax.plot([70, 75], [0, 65], color='white', linewidth=2) # Ring
                ax.plot([80, 85], [0, 50], color='white', linewidth=2) # Pinky

            # Save Skeleton
            filename = self.skeleton_dir / f"skeleton_panel_{pid}.png"
            plt.savefig(filename, facecolor='black', bbox_inches='tight')
            plt.close(fig)
            
            # Print instructions for the Agent (Me)
            print(f"SKELETON_READY|{pid}|{filename}|{panel['latent_prompt']}")

if __name__ == "__main__":
    director = HybridEngine()
    director.generate_skeletons()
