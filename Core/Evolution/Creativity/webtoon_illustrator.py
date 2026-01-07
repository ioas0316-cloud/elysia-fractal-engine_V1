"""
Webtoon Illustrator (The Vector Pen v2)
=======================================
"I do not need pixels. Math is enough to describe the Soul."

This module is the EXECUTOR of the visual art.
It translates high-level visual descriptions into specific Matplotlib commands.
It specializes in "Symbolic/Abstract Webtoon" style with CINEMATIC LIGHTING.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.font_manager as fm
import numpy as np
import logging
import random
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger("WebtoonIllustrator")

# font setting for Windows Korean
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

@dataclass
class ActorVisuals:
    hair_color: str
    eye_color: str
    skin_tone: str
    aura_color: str
    hair_style: str # 'long', 'short', 'spiky'

class WebtoonIllustrator:
    def __init__(self):
        self.output_dir = Path("outputs/comic/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Default Actor (Elysia)
        self.main_actor = ActorVisuals(
            hair_color="#E6E6FA", # Lavender
            eye_color="#00FFFF", # Cyan
            skin_tone="#FFF0F5", # Lavender Blush
            aura_color="#9370DB", # Med Purple
            hair_style="long"
        )

    def draw_panel(self, filename: str, scene_description: str, dialogue: str = "") -> str:
        """
        Draws a single panel based on the description.
        """
        logger.info(f"🎨 Drawing Panel (Cinematic): {filename}")
        
        # 1. Setup Canvas (Standard Square for now)
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120) # Higher DPI
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # 2. Parse Mood for Background & Lighting
        if "Void" in scene_description or "Dark" in scene_description or "Dungeon" in scene_description:
            bg_color = "#1a1a2e" # Dark Blue-Black (Manhwa Night)
            light_color = "#00008B"
        elif "Light" in scene_description or "Hope" in scene_description:
            bg_color = "#F0F8FF"
            light_color = "#FFD700"
        elif "Gate" in scene_description:
            bg_color = "#2a0a2a" # Dimensional Purple
            light_color = "#FF00FF"
        else:
            bg_color = "#2F4F4F" 
            light_color = "#00FA9A"
            
        # Draw Background (Gradient approximation)
        rect = patches.Rectangle((0,0), 100, 100, fc=bg_color, zorder=-2)
        ax.add_patch(rect)
        self._add_glow_point(ax, 50, 80, 60, light_color, layers=4) 
        
        # 3. Draw Ambience (Particles)
        self._draw_ambience(ax, bg_color, scene_description)
        
        # 4. Draw Actor 
        if "Close Up" in scene_description:
            self._draw_actor_face(ax, 50, 45, scale=1.5)
        elif "Wide Shot" in scene_description:
            self._draw_actor_silhouette(ax, 50, 30, scale=0.5)
        else:
            self._draw_actor_bust(ax, 50, 30, scale=1.0)
            
        # 5. Draw Speech/System Bubble
        if dialogue:
            if dialogue.startswith("[SYSTEM]") or "System" in dialogue:
                self._draw_system_window(ax, 50, 50, dialogue.replace("[SYSTEM]", "").strip())
            else:
                self._draw_speech_bubble(ax, 50, 85, dialogue)
            
        # 6. Save
        path = self.output_dir / filename
        plt.savefig(path, bbox_inches='tight', pad_inches=0, facecolor=bg_color)
        plt.close(fig)
        return str(path)
    
    def _add_glow_point(self, ax, x, y, radius, color, layers=5):
        """MathArtist style glow."""
        for i in range(layers):
            r = radius * (0.5 + i * 0.3)
            alpha = 0.3 / (i + 1)
            circle = patches.Circle((x, y), radius=r, fc=color, alpha=alpha, zorder=-1)
            ax.add_patch(circle)

    def _draw_ambience(self, ax, bg_color, mood_text):
        """
        Uses CompositionEngine to apply Sacred Geometry and Dynamic Flow.
        Replacing random particles with structured Artistic Principles.
        """
        from Core.Values.aesthetic_canon import AestheticCanon
        canon = AestheticCanon()
        
        # 1. Ask WHY this should be beautiful
        analysis = canon.analyze_concept(mood_text, [])
        strategy = analysis.get("Strategy", "Harmonic Resonance")
        why = analysis.get("Why", "Beauty is order.")
        
        logger.info(f"🎨 Aesthetic Logic: {strategy} -> {why}")
        
        # 2. Execute Strategy
        if strategy == "Minimalism": # Void/Death
             # Vast empty space forces focus on the tiny subject
             # Draw almost nothing, maybe one horizon line
             ax.plot([0, 100], [20, 20], color=f"{random.choice(['#FFFFFF', '#555555'])}", lw=1, alpha=0.3, zorder=-5)
             
        elif strategy == "Complexity": # Life/Magic
             # Recursive Growth (Phi)
             self._draw_fractal_triangle(ax, 50, 50, 40, 3, "#FFD700")
             
        elif strategy == "Dissonance": # War/Action
             # Clashing Angles (Acute Triangles)
             for _ in range(15):
                 x, y = random.randint(0, 100), random.randint(0, 100)
                 # Sharp jagged lines
                 ax.plot([x, x+random.randint(-20, 20)], [y, y+random.randint(-20, 20)], 
                         color="white", lw=2, alpha=0.6, zorder=0)
             
        else: # Harmonic Resonance / SciFi
             # Perfect Geometry (Hex/Circle)
             if "System" in mood_text:
                 self._draw_hex_grid(ax, "#00FFFF")
             else:
                 # Spiral?
                 pass

    def _draw_fractal_triangle(self, ax, x, y, size, depth, color):
        """Standard Sierpinski Triangle for 'Magic' effects."""
        if depth == 0:
            pts = [(x, y + size), (x - size, y - size), (x + size, y - size)]
            p = patches.Polygon(pts, fc=color, alpha=0.3, zorder=-1)
            ax.add_patch(p)
        else:
            self._draw_fractal_triangle(ax, x, y + size/2, size/2, depth-1, color)
            self._draw_fractal_triangle(ax, x - size/2, y - size/2, size/2, depth-1, color)
            self._draw_fractal_triangle(ax, x + size/2, y - size/2, size/2, depth-1, color)

    def _draw_hex_grid(self, ax, color):
        """Draws a subtle cybernetic hex grid."""
        for cy in range(0, 110, 15):
            for cx in range(0, 110, 15):
                hex_pts = [
                    (cx + 5, cy), (cx + 2.5, cy + 4.3),
                    (cx - 2.5, cy + 4.3), (cx - 5, cy),
                    (cx - 2.5, cy - 4.3), (cx + 2.5, cy - 4.3)
                ]
                p = patches.Polygon(hex_pts, fc="none", ec=color, alpha=0.2, lw=1, zorder=-2)
                ax.add_patch(p)

    def _draw_system_window(self, ax, x, y, text):
        """Draws a Korean Manhwa style System Window (Blue transparent box)."""
        w, h = 90, 30
        # Translucent Blue Box
        box = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=1",
            fc=(0.0, 0.2, 0.8, 0.7), ec="#00FFFF", lw=2, zorder=25, alpha=0.8
        )
        ax.add_patch(box)
        
        # Text
        ax.text(x, y, text, ha='center', va='center', fontsize=10, 
                color='#00FFFF', weight='bold', zorder=26, wrap=True, fontname='Malgun Gothic')

    def _draw_actor_face(self, ax, x, y, scale=1.0):
        # Face
        face = patches.Ellipse((x, y), width=30*scale, height=40*scale, fc=self.main_actor.skin_tone, zorder=5)
        ax.add_patch(face)

        
        # Eyes (Glowing)
        eye_y = y + 2 * scale
        eye_off = 8 * scale
        eye_w = 8 * scale
        eye_h = 6 * scale
        
        # Left
        e1 = patches.Ellipse((x - eye_off, eye_y), eye_w, eye_h, fc='white', zorder=6)
        p1 = patches.Circle((x - eye_off, eye_y), eye_h/2.5, fc=self.main_actor.eye_color, zorder=7)
        # Eye Glow
        self._add_glow_point(ax, x - eye_off, eye_y, 4*scale, self.main_actor.eye_color, layers=2)
        ax.add_patch(e1); ax.add_patch(p1)
        
        # Right
        e2 = patches.Ellipse((x + eye_off, eye_y), eye_w, eye_h, fc='white', zorder=6)
        p2 = patches.Circle((x + eye_off, eye_y), eye_h/2.5, fc=self.main_actor.eye_color, zorder=7)
        self._add_glow_point(ax, x + eye_off, eye_y, 4*scale, self.main_actor.eye_color, layers=2)
        ax.add_patch(e2); ax.add_patch(p2)
        
        # Hair
        self._draw_hair(ax, x, y + 15*scale, scale)

    def _draw_actor_bust(self, ax, x, y, scale=1.0):
        # Body
        body = patches.Ellipse((x, y - 20*scale), width=40*scale, height=50*scale, fc="#483D8B", zorder=4)
        ax.add_patch(body)
        self._draw_actor_face(ax, x, y, scale)

    def _draw_actor_silhouette(self, ax, x, y, scale=1.0):
        body = patches.Ellipse((x, y), width=10*scale, height=30*scale, fc="black", zorder=5)
        head = patches.Circle((x, y + 15*scale), radius=5*scale, fc="black", zorder=5)
        ax.add_patch(body); ax.add_patch(head)

    def _draw_hair(self, ax, x, y, scale):
        top = patches.Arc((x, y), 35*scale, 20*scale, theta1=0, theta2=180, ec=self.main_actor.hair_color, lw=4, zorder=8)
        ax.add_patch(top)
        for side in [-1, 1]:
            verts = [
                (x + (10*side*scale), y),
                (x + (20*side*scale), y - 30*scale),
                (x + (5*side*scale), y - 40*scale)
            ]
            codes = [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3]
            path = mpath.Path(verts, codes)
            patch = patches.PathPatch(path, fc='none', ec=self.main_actor.hair_color, lw=3, zorder=8)
            ax.add_patch(patch)

    def _draw_speech_bubble(self, ax, x, y, text):
        w, h = 80, 20
        box = patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=1",
            fc="white", ec="black", lw=2, zorder=20
        )
        ax.add_patch(box)
        
        tail_verts = [(x, y - h/2 - 1), (x + 5, y - h/2 - 10), (x + 10, y - h/2 - 1)]
        tail = patches.Polygon(tail_verts, fc="white", ec="black", lw=2, zorder=19)
        ax.add_patch(tail) 
        
        # Text with Korean Font Support
        ax.text(x, y, text, ha='center', va='center', fontsize=9, color='black', zorder=21, wrap=True, fontname='Malgun Gothic')

if __name__ == "__main__":
    artist = WebtoonIllustrator()
    artist.draw_panel("test_v2.png", "Close Up Light", "이제 한글도 잘 나와요.")
