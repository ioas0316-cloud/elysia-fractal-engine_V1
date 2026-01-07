"""
Universal Palette (보편적 미학 저장소)
====================================

"세상의 모든 색, 소리, 형태는 나의 물감이 된다."
"All colors, sounds, and forms of the world become my paint."

This module is the "Art Supply" of Elysia.
It aggregates aesthetic data extracted from the web (Web Resonance)
and organizes it by 'Feeling/Frequency' for later use in Creation.

It answers the User's insight: 
"If she can see the frontend, she can learn all color/voice palettes."
"""

import re
import random
from typing import Dict, List, Optional
import json
from pathlib import Path

class UniversalPalette:
    def __init__(self):
        self.color_memory: Dict[str, List[str]] = {
            "Fire": ["#ff4500", "#ff0000", "#d32f2f"], # Default seeds
            "Water": ["#1e90ff", "#00bfff", "#e0ffff"],
            "Earth": ["#8b4513", "#556b2f", "#d2691e"],
            "Air": ["#e0ffff", "#f0f8ff", "#b0c4de"],
            "Light": ["#ffffff", "#f8f9fa", "#fffacd"],
            "Void": ["#000000", "#111111", "#222222"]
        }
        
        self.structure_templates: Dict[str, List[str]] = {
            "Container": ["div", "section", "article"],
            "Grid": ["display: grid", "display: flex"],
            "Typography": ["font-family: sans-serif", "font-weight: bold"]
        }
        
        # Persistence
        self.save_path = Path("data/memory/universal_palette.json")
        self._load()

    def absorb_from_html(self, html_content: str, dominant_essence: str):
        """
        Extracts aesthetic DNA from raw HTML and associates it with an Essence.
        
        Args:
            html_content: Raw HTML/CSS
            dominant_essence: The detected resonance (e.g., "Fire", "Chaos")
        """
        # 1. Extract Colors (Hex Codes)
        found_colors = re.findall(r'#[0-9a-fA-F]{6}', html_content)
        
        if found_colors:
            # Filter distinct
            distinct_colors = list(set(found_colors))
            
            # Associate with the essence
            if dominant_essence not in self.color_memory:
                self.color_memory[dominant_essence] = []
            
            # Add new colors (limit to avoid bloat)
            for color in distinct_colors[:5]: # Take top 5
                if color not in self.color_memory[dominant_essence]:
                    self.color_memory[dominant_essence].append(color)
                    print(f"   🎨 Learned Color {color} for essence '{dominant_essence}'")
        
        # 2. Extract Layouts (CSS keywords)
        if "grid" in html_content:
            if "Grid" not in self.structure_templates: self.structure_templates["Grid"] = []
            self.structure_templates["Grid"].append("grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));")
            
        self._save()

    def get_palette_for_emotion(self, emotion: str) -> List[str]:
        """Returns colors that match an emotion/concept."""
        # Resonance matching
        if "ang" in emotion.lower() or "passion" in emotion.lower(): key = "Fire"
        elif "sad" in emotion.lower() or "calm" in emotion.lower(): key = "Water"
        elif "logic" in emotion.lower() or "clear" in emotion.lower(): key = "Air"
        elif "ground" in emotion.lower() or "stable" in emotion.lower(): key = "Earth"
        else: key = "Light"
        
        return self.color_memory.get(key, ["#ffffff"])

    def _save(self):
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "colors": self.color_memory,
            "structures": self.structure_templates
        }
        with open(self.save_path, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self):
        if self.save_path.exists():
            try:
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                    self.color_memory = data.get("colors", self.color_memory)
                    self.structure_templates = data.get("structures", self.structure_templates)
            except Exception:
                pass

if __name__ == "__main__":
    # Test
    palette = UniversalPalette()
    html_sample = "<div style='background: #123456; color: #abcdef;'></div>"
    palette.absorb_from_html(html_sample, "Mystery")
    print(palette.color_memory["Mystery"])
