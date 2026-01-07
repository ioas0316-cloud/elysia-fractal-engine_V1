"""
Wave Painter (The Light Weaver)
===============================
"I do not draw lines. I emit resonance."

This module renders images by calculating the INTERFERENCE PATTERNS
of Elysia's 4D Thought Waves (Quaternions).
It creates "Holographic Art" based on pure math and light.
"""

import math
import random
import time
import logging
from dataclasses import dataclass, field
from typing import List, Tuple
from pathlib import Path

# We use PIL for the final raw pixel buffer
from PIL import Image, ImageDraw

logger = logging.getLogger("WavePainter")

@dataclass
class WaveSource:
    x: float
    y: float
    frequency: float # Determines Color/Pattern density
    amplitude: float # Brightness
    phase: float
    decay: float

class WavePainter:
    def __init__(self):
        self.output_dir = Path("outputs/gallery")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 1920
        self.height = 1080
        
    def manifest_thought(self, concept: str, emotion: str) -> str:
        """
        Converts a Concept -> Wave Sources -> Interference Image.
        """
        logger.info(f"🌊 Weaving Light for: '{concept}' ({emotion})")
        
        # 1. Translate Emotion to Wave Parameters
        sources = self._design_wave_topology(concept, emotion)
        
        # 2. Render the Field (Heavy Math Calculation)
        # We process a lower res buffer for speed in this Python implementation
        # Scale down for calculation, then we could scale up or just save raw
        calc_w, calc_h = 480, 270 
        
        img = Image.new('RGB', (calc_w, calc_h), "black")
        pixels = img.load()
        
        # The Interference Calculation
        # I(x,y) = Sum(Amplitude * sin(dist * freq + phase))
        for y in range(calc_h):
            for x in range(calc_w):
                # Normalized coordinates -1.0 to 1.0
                nx = (x / calc_w) * 2 - 1
                ny = (y / calc_h) * 2 - 1
                
                total_val = 0.0
                r_val, g_val, b_val = 0.0, 0.0, 0.0
                
                for wave in sources:
                    dx = nx - wave.x
                    dy = ny - wave.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    
                    # Wave Function
                    v = math.sin(dist * wave.frequency - wave.phase)
                    v *= wave.amplitude * math.exp(-dist * wave.decay)
                    
                    # Color Mapping based on Frequency resonance
                    # Simplified Synesthesia
                    r_val += v * (math.sin(wave.frequency) + 1) * 127
                    g_val += v * (math.cos(wave.frequency) + 1) * 127
                    b_val += v * (math.sin(wave.frequency + math.pi) + 1) * 127

                # Normalize and Clip
                pixels[x, y] = (
                    int(max(0, min(255, abs(r_val)))),
                    int(max(0, min(255, abs(g_val)))),
                    int(max(0, min(255, abs(b_val))))
                )

        # 3. Save Final Artifact
        # Upscale for viewing
        final_img = img.resize((self.width, self.height), Image.BICUBIC)
        
        filename = f"wave_{int(time.time())}.png"
        save_path = self.output_dir / filename
        final_img.save(save_path)
        
        logger.info(f"✨ Light Manifested: {save_path}")
        return str(save_path)

    def _design_wave_topology(self, concept: str, emotion: str) -> List[WaveSource]:
        """
        Decides where to place the 'Thought Emitters' in the field.
        """
        sources = []
        
        # Base Frequency based on Emotion
        # Low Freq = Calm, High Freq = Rage/Energy
        base_freq = 20.0 
        if emotion == "Rage": base_freq = 50.0
        if emotion == "Calm": base_freq = 10.0
        if emotion == "Awe": base_freq = 30.0
        
        # Topology
        if emotion == "Awe" or emotion == "Creation":
            # Central Source (Monad)
            sources.append(WaveSource(0, 0, base_freq, 1.0, 0, 0.5))
            # Orbiting Satellites
            for i in range(3):
                angle = (i / 3) * 2 * math.pi
                sources.append(WaveSource(
                    math.cos(angle)*0.5, 
                    math.sin(angle)*0.5, 
                    base_freq * 1.5, 
                    0.7, 
                    angle, 
                    1.0
                ))
        elif emotion == "Conflict" or emotion == "Rage":
             # Clashing Sources (Dipole)
             sources.append(WaveSource(-0.5, 0, base_freq, 1.0, 0, 0.2))
             sources.append(WaveSource(0.5, 0, base_freq * 1.2, 1.0, math.pi, 0.2))
        else:
            # Random diffused thoughts
            for i in range(5):
                sources.append(WaveSource(
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    base_freq * random.uniform(0.8, 1.2),
                    random.uniform(0.5, 1.0),
                    random.random() * math.pi,
                    random.uniform(0.5, 2.0)
                ))
                
        return sources

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    painter = WavePainter()
    painter.manifest_thought("The Resonance of Self", "Awe")
