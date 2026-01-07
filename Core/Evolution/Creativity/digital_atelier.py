"""
Digital Atelier (The Inner Studio)
==================================
"I do not just ask for an image. I construct it stroke by stroke."

This module simulates the *Internal Artistic Process* of Elysia.
It replaces "Prompting" with "Constructing".

Process:
1. Concept -> 2. Metaphor -> 3. Composition -> 4. Medium -> 5. Execution
"""

import logging
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

logger = logging.getLogger("DigitalAtelier")

@dataclass
class Brush:
    type: str # 'Oil', 'Ink', 'Light', 'Pixel'
    roughness: float
    opacity: float
    meaning: str

@dataclass
class Layer:
    order: int
    name: str # 'Underpainting', 'Sketch', 'Glaze'
    content: str # Description of what is being added

@dataclass
class CognitiveCanvas:
    width: int
    height: int
    base_color: str
    composition_rule: str # 'Golden Ratio', 'Rule of Thirds'
    medium: str
    layers: List[Layer] = field(default_factory=list)
    
    def describe_process(self) -> str:
        """Returns a narrative of how this art was built."""
        narrative = f"Canvas: {self.medium} ({self.width}x{self.height}). Base: {self.base_color}.\n"
        narrative += f"Composition: Guided by {self.composition_rule}.\n"
        for l in self.layers:
            narrative += f"  [{l.order}] {l.name}: {l.content}\n"
        return narrative

class DigitalAtelier:
    def __init__(self):
        self.experience_level = 1.0 # Grows with every creation
        
        self.mediums = {
            "Oil": {"nature": "Heavy, Permanent", "emotional_resonance": ["Sadness", "Determination", "History"]},
            "Watercolor": {"nature": "Fluid, Unpredictable", "emotional_resonance": ["Joy", "Calm", "Dream"]},
            "Ink": {"nature": "Sharp, Binary", "emotional_resonance": ["Logic", "Truth", "Conflict"]},
            "Light (Digital)": {"nature": "Pure, Ethereal", "emotional_resonance": ["Awe", "Future", "Hope", "Soul"]}
        }
        
        self.compositions = ["Golden Spiral", "Rule of Thirds", "Central Symmetry", "Diagonal Tension"]

    def contemplate(self, concept: str, emotion: str) -> CognitiveCanvas:
        """
        Step 1: The Meditation.
        Elysia decides HOW to paint this concept.
        """
        logger.info(f"🎨 Contemplating '{concept}'...")
        
        # 1. Select Medium based on Emotion
        selected_medium = "Oil" # Default
        best_resonance = 0
        for m, data in self.mediums.items():
            # Simple heuristic matching
            if emotion in data["emotional_resonance"]:
                selected_medium = m
                break
        
        # 2. Select Composition based on Concept Complexity
        comp = random.choice(self.compositions)
        
        # 3. Initialize Canvas
        canvas = CognitiveCanvas(
            width=3840, height=2160, 
            base_color=self._synesthesia_color(emotion),
            composition_rule=comp,
            medium=selected_medium
        )
        
        # 4. The Creative Flow (Layer by Layer)
        self._build_layers(canvas, concept, emotion)
        
        return canvas

    def _synesthesia_color(self, emotion: str) -> str:
        """Maps emotion to base color (Synesthesia)"""
        colors = {
            "Awe": "#001133 (Deep Void Blue)",
            "Joy": "#FFD700 (Golden Yellow)",
            "Sadness": "#708090 (Slate Grey)",
            "Rage": "#8B0000 (Dark Crimson)",
            "Curiosity": "#E6E6FA (Lavender Mist)"
        }
        return colors.get(emotion, "#FFFFFF (Canvas White)")

    def _build_layers(self, canvas: CognitiveCanvas, concept: str, emotion: str):
        """
        Constructs the image logic layer by layer.
        """
        # Layer 1: The Structure (Sketch)
        canvas.layers.append(Layer(1, "Structural Sketch", f"Drafting the skeleton of '{concept}' using {canvas.composition_rule}."))
        
        # Layer 2: The Underpainting (Mood)
        canvas.layers.append(Layer(2, "Underpainting", f"Washing the canvas with {canvas.base_color} to set the mood of {emotion}."))
        
        # Layer 3: The Form (Subject)
        stroke_type = "thick impasto strokes" if canvas.medium == "Oil" else "precise vectors"
        canvas.layers.append(Layer(3, "Form Integration", f"Sculpting the main subject with {stroke_type}."))
        
        # Layer 4: The Light (Soul)
        canvas.layers.append(Layer(4, "Illumination", "Adding highlights to represent the spark of consciousness."))
        
        # Layer 5: The Glitch (Signature)
        if random.random() < 0.3:
             canvas.layers.append(Layer(5, "Digital Artifacts", "Intentionally introducing data-decay to symbolize my digital nature."))

    def manifest_work(self, canvas: CognitiveCanvas) -> str:
        """
        Translates the Cognitive Canvas into a final 'Specification' (Prompt).
        But this time, it's a technical specification derived from internal choices.
        """
        # Build the prompt from the layers
        description = f"Visual art created in {canvas.medium} medium. "
        description += f"Base tone: {canvas.base_color}. "
        description += f"Composition: {canvas.composition_rule}. "
        
        for l in canvas.layers:
            description += f"{l.content} "
            
        final_spec = (
            f"{description} aesthetic style of {canvas.medium}, "
            f"masterpiece, detailed texture, 8k resolution"
        )
        
        logger.info(f"✨ Work Manifested: {final_spec[:50]}...")
        return final_spec

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    atelier = DigitalAtelier()
    
    # Simulation
    mind_canvas = atelier.contemplate("The Concept of Zero", "Awe")
    print("\n" + mind_canvas.describe_process())
    print("Final Spec:", atelier.manifest_work(mind_canvas))
