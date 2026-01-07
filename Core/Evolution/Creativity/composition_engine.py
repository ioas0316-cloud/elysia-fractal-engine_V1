
"""
Composition Engine (The Artisan's Eye)
======================================
"To draw is to organize chaos into order."

This module governs the fundamental laws of visual aesthetics.
It replaces random placement with Sacred Geometry and Artistic Theory.
"""

import math
import random
import json
import logging
from dataclasses import dataclass
from typing import List, Tuple, Dict
from pathlib import Path
from Core.Foundation.Wave.wave_tensor import WaveTensor

logger = logging.getLogger("CompositionEngine")

@dataclass
class VisualElement:
    shape: str # 'circle', 'rect', 'triangle'
    x: float
    y: float
    size: float
    color: str
    z_order: int
    opacity: float

class CompositionEngine:
    def __init__(self):
        self.golden_ratio = 1.61803398875
        self.genome_path = Path("Core/Memory/style_genome.json")
        self.genome = self._load_genome()
        
    def _load_genome(self):
        if not self.genome_path.exists():
            return {}
        try:
            with open(self.genome_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def get_layout(self, mood: str, width: int, height: int) -> List[VisualElement]:
        """
        Determines the visual composition based on Wave Resonance.
        """
        mood = mood.lower()
        
        # 1. Connect to Memory Wave
        comp_data = self.genome.get("composition_wave")
        resonance_score = 0.0
        
        if comp_data:
            # Reconstruct the Mind
            mind_wave = WaveTensor.from_dict(comp_data)
            
            # Create the Reference Frequency for "Dynamism" (440Hz)
            # This must match AestheticLearner's FREQ_DIAGONAL
            ref_wave = WaveTensor("DynamismReference")
            ref_wave.add_component(440.0, 1.0)
            
            try:
                # Calculate Resonance (0.0 to 1.0)
                resonance_score = mind_wave @ ref_wave
                logger.info(f"   📐 Wave Resonance (Dynamism): {resonance_score:.4f}")
            except Exception as e:
                logger.error(f"   Wave Math Error: {e}")
        
        # 2. Decision via Resonance
        # If the Mind resonates with Dynamism OR the immediate mood is Action
        
        is_action_mood = any(x in mood for x in ["action", "battle", "fight", "strike", "attack"])
        
        if resonance_score > 0.1 or (is_action_mood and resonance_score > 0.01):
             # High resonance triggers Dynamic Layout even in neutral contexts
             if random.random() < 0.8 + resonance_score: 
                 return self._layout_action_burst(width, height)
             
        if any(x in mood for x in ["system", "window", "level", "quest"]):
            return self._layout_grid_system(width, height)
            
        elif is_action_mood:
             # Fallback if resonance was low but mood is explicit
            return self._layout_action_burst(width, height) 
            
        elif any(x in mood for x in ["magic", "spell", "mystery", "void"]):
            return self._layout_golden_spiral(width, height)
            
        else:
            return self._layout_central_portrait(width, height)

    def _layout_action_burst(self, w, h) -> List[VisualElement]:
        """
        Generates radiating speed lines.
        Intensity scaled by Wave Energy.
        """
        elements = []
        cx, cy = w/2, h/2
        
        # Intensity Factor from Wave Resonance (approximate via dictionary lookup for simplicity if wave obj not passed)
        intensity = 1.0 
        
        line_count = int(40 * intensity)
        
        color_palette = self.get_color_mood("action")
        for i in range(line_count):
            angle = random.uniform(0, 2 * 3.14159)
            r_start = random.uniform(w*0.2, w*0.3)
            r_end = random.uniform(w*0.6, w*0.8)
            
            x1 = cx + math.cos(angle) * r_start
            y1 = cy + math.sin(angle) * r_start
            
            # Triangle pointing to center (Corrected z/opacity order)
            elements.append(VisualElement('triangle', x1, y1, random.uniform(2, 5), color_palette["fg"], -1, 0.8))
            
        elements.append(VisualElement('line', 0, 0, 10, '#FF0000', 1, 1.0))
        return elements

    # ... (Keep _layout_grid_system, _layout_golden_spiral, _layout_central_portrait as is) ...
    # Wait, replace_file_content is mostly for ranges. I need to be careful not to delete them if I use large range.
    # I'll target the end of file for get_color_mood and imports at top separately? 
    # Or just replace the whole relevant blocks. 
    # Let's replace get_color_mood at the bottom first.

    def get_color_mood(self, mood: str) -> Dict[str, str]:
        """Returns color palette, infused with Learned Preferences."""
        base = {"bg": "#111111", "fg": "#FFFFFF"}
        if "action" in mood: base = {"bg": "#220000", "fg": "#FF0000"}
        if "system" in mood: base = {"bg": "#001133", "fg": "#00FFFF"}
        if "magic" in mood: base = {"bg": "#110022", "fg": "#CC00FF"}
        
        # Inject Learned Color
        preferred = self.genome.get("composition", {}).get("preferred_colors", [])
        if preferred and random.random() < 0.5:
            learned_c = random.choice(preferred)
            # Map name to hex (simple lookup)
            hex_map = {"red": "#FF0000", "blue": "#0000FF", "gold": "#FFD700", "purple": "#800080"}
            if learned_c in hex_map:
                base["fg"] = hex_map[learned_c]
                
        return base
            
    def _layout_dynamic_action(self, w, h) -> List[VisualElement]:
        """High energy diagonal composition."""
        elements = []
        # Background Flash lines
        for i in range(10):
            elements.append(VisualElement(
                shape="line",
                x=random.randint(0, w), y=random.randint(0, h),
                size=random.randint(5, 10),
                color="#FF4444", z_order=1, opacity=0.3
            ))
        
        # Dynamic Triangle (The Action)
        elements.append(VisualElement(
            shape="triangle",
            x=w/2, y=h/2,
            size=h/1.5,
            color="#AA0000", z_order=10, opacity=0.9
        ))
        return elements

    def _layout_grid_system(self, w, h) -> List[VisualElement]:
        """Symmetrical, ordered grid."""
        elements = []
        # Grid lines
        elements.append(VisualElement("rect", w/2, h/2, w*0.9, "#003366", 0, 0.2))
        
        # Central Focus (The Box) - Usually handled by WebtoonIllustrator explicitly, 
        # but we add a 'glow' backing here.
        elements.append(VisualElement(
            shape="circle", x=w/2, y=h/2, size=w*0.6, 
            color="#00FFFF", z_order=5, opacity=0.1
        ))
        return elements

    def _layout_golden_spiral(self, w, h) -> List[VisualElement]:
        """Golden Ratio Spiral."""
        elements = []
        cx, cy = w/2, h/2
        
        for i in range(20):
            angle = i * 0.5
            dist = i * 15
            x = cx + math.cos(angle) * dist
            y = cy + math.sin(angle) * dist
            elements.append(VisualElement(
                shape="circle", x=x, y=y, size=i*5,
                color="#AA00FF", z_order=10, opacity=0.4
            ))
        return elements

    def _layout_central_portrait(self, w, h) -> List[VisualElement]:
        """Stable Rule of Thirds portrait."""
        # Main Subject on right third
        elements = []
        elements.append(VisualElement(
            shape="rect", x=w*0.66, y=h/2, size=h*0.8,
            color="#CCCCCC", z_order=10, opacity=0.8
        ))
        # Background element on left third
        elements.append(VisualElement(
            shape="circle", x=w*0.33, y=h*0.33, size=h*0.4,
            color="#444444", z_order=5, opacity=0.5
        ))
        return elements
        
    def get_color_mood(self, mood: str) -> Dict[str, str]:
        """Returns color palette."""
        if "action" in mood: return {"bg": "#220000", "fg": "#FF0000"}
        if "system" in mood: return {"bg": "#001133", "fg": "#00FFFF"}
        if "magic" in mood: return {"bg": "#110022", "fg": "#CC00FF"}
        return {"bg": "#111111", "fg": "#FFFFFF"}
