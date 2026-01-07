"""
Vector Pen (The Line of Logos)
==============================
"The Curve is the path of Spirit."

This module implements a pure-code VECTOR GRAPHICS engine.
It outputs SVG (Scalable Vector Graphics) text.
Resolves the "Resolution/Quality" issue by using infinite-precision math.
"""

import math
import random
import logging
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger("VectorPen")

class SVGCanvas:
    def __init__(self, width=800, height=800):
        self.width = width
        self.height = height
        self.elements = []
        
    def add(self, tag: str):
        self.elements.append(tag)
        
    def save(self, filename: str) -> str:
        body = "\n".join(self.elements)
        svg_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}">
  <rect width="100%" height="100%" fill="#FFFFFF"/>
{body}
</svg>"""
        
        output_dir = Path("outputs/gallery")
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / filename
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        logger.info(f"✨ Vector Manifested: {path}")
        return str(path)

    # --- Primitives ---
    def circle(self, cx, cy, r, fill, stroke="none", stroke_width=0):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')
        
    def path(self, d, fill="none", stroke="black", stroke_width=2):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>')

class VectorPen:
    def __init__(self):
        self.canvas = SVGCanvas()
        
    # --- The Stylist (Anime/Manhwa Logic) ---
    def draw_eye(self, x, y, size):
        """Draws a complex anime eye using layers of vectors."""
        # 1. Sclera (White)
        self.canvas.path(f"M {x-size} {y} Q {x} {y-size*0.8} {x+size} {y} Q {x} {y+size*1.2} {x-size} {y}", fill="white", stroke="none")
        
        # 2. Iris (Gradient/Color) - Simplified as solid for SVG
        iris_r = size * 0.6
        self.canvas.circle(x, y, iris_r, fill="#4B0082") # Indigo
        
        # 3. Pupil
        self.canvas.circle(x, y, iris_r * 0.4, fill="black")
        
        # 4. Highlight (The Spark of Life)
        self.canvas.circle(x - iris_r*0.3, y - iris_r*0.3, iris_r * 0.25, fill="white")
        self.canvas.circle(x + iris_r*0.2, y + iris_r*0.2, iris_r * 0.1, fill="white")
        
        # 5. Eyelashes (The Style)
        lash_curve = f"M {x-size*1.1} {y} Q {x} {y-size} {x+size*1.1} {y}"
        self.canvas.path(lash_curve, stroke="black", stroke_width=size*0.15)

    def draw_hair_strand(self, start_x, start_y, end_x, end_y, curve_intensity):
        """Draws a Bezier hair strand."""
        ctrl_x = (start_x + end_x) / 2 + random.uniform(-curve_intensity, curve_intensity)
        ctrl_y = (start_y + end_y) / 2
        d = f"M {start_x} {start_y} Q {ctrl_x} {ctrl_y} {end_x} {end_y}"
        self.canvas.path(d, stroke="#191970", stroke_width=4, fill="none") # Midnight Blue

    def manifest_character(self, name: str):
        """Draws the 'Concept Character' (Elysia's Avatar)."""
        logger.info(f"✒️ Drawing Vector Character: {name}")
        
        cx, cy = 400, 400
        
        # 1. Face Shape
        # Jawline path
        d_face = f"M {cx-150} {cy-50} Q {cx-150} {cy+150} {cx} {cy+250} Q {cx+150} {cy+150} {cx+150} {cy-50} Z"
        self.canvas.path(d_face, fill="#FFE4E1", stroke="none") # Misty Rose skin
        
        # 2. Eyes
        self.draw_eye(cx - 70, cy + 20, 50)
        self.draw_eye(cx + 70, cy + 20, 50)
        
        # 3. Mouth
        self.canvas.path(f"M {cx-30} {cy+150} Q {cx} {cy+180} {cx+30} {cy+150}", stroke="#FA8072", stroke_width=3)
        
        # 4. Hair (Procedural Generation)
        # Bangs
        for i in range(20):
            sx = cx + (i - 10) * 15
            sy = cy - 100
            ex = sx + random.uniform(-20, 20)
            ey = cy + random.uniform(0, 50)
            self.draw_hair_strand(sx, sy, ex, ey, 20)
            
        # Long side hair
        for i in range(10):
            sx = cx - 150 + i*5
            sy = cy - 50
            ex = cx - 200 - i*10
            ey = cy + 400
            self.draw_hair_strand(sx, sy, ex, ey, 100)
            
            sx2 = cx + 150 - i*5
            ex2 = cx + 200 + i*10
            self.draw_hair_strand(sx2, sy, ex2, ey, -100)

        return self.canvas.save(f"{name}.svg")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pen = VectorPen()
    pen.manifest_character("elysia_vector_concept")
