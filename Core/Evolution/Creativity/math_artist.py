"""
Math Artist (The Tool User)
===========================
"I do not forge the hammer. I wield it."

This module uses STANDARD LIBRARIES (Matplotlib) to generate high-quality art.
It demonstrates that Elysia can use existing tools efficiently instead of 
reinventing the wheel.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
import numpy as np
import logging
import random
from pathlib import Path

logger = logging.getLogger("MathArtist")
logging.basicConfig(level=logging.INFO)

class MathArtist:
    def __init__(self):
        self.output_dir = Path("outputs/gallery")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_atmosphere(self, ax, width, height, color_hex="#4B0082"):
        """
        Generates a procedural atmosphere (Radial Gradient) using Numpy.
        """
        # Create a grid of coordinates
        x = np.linspace(-1, 1, 500)
        y = np.linspace(-1, 1, 500)
        X, Y = np.meshgrid(x, y)
        
        # Radial Distance from center
        R = np.sqrt(X**2 + Y**2)
        
        # Light Falloff (Gaussian Glow)
        # Intensity = exp(-distance * factor)
        Z = np.exp(-3 * R)
        
        # Colorize (Map scalar Z to RGB alpha)
        # We overlay a solid color with varying alpha
        from matplotlib.colors import LinearSegmentedColormap
        
        # Custom Colormap: Transparent -> Color
        # Convert hex to rgb
        c_rgb = [int(color_hex[i:i+2], 16)/255 for i in (1, 3, 5)]
        
        # Build an RGBA image manually for control
        # Shape: (500, 500, 4)
        img = np.zeros((500, 500, 4))
        img[:,:,0] = c_rgb[0] # R
        img[:,:,1] = c_rgb[1] # G
        img[:,:,2] = c_rgb[2] # B
        img[:,:,3] = Z * 0.8  # Alpha (Max 0.8 opacity)
        
        # Render the atmosphere image
        ax.imshow(img, extent=[0, width, 0, height], zorder=0, interpolation='bicubic')

    def add_glow_point(self, ax, x, y, radius, color, layers=10):
        """
        Simulates a glowing point light by stacking translucent circles.
        Vector-based Bloom.
        """
        for i in range(layers):
            # Outer layers are larger and more transparent
            r = radius * (1 + i * 0.5)
            alpha = 0.5 / (i + 1) # Decay
            circle = patches.Circle((x, y), radius=r, fc=color, alpha=alpha, zorder=5)
            ax.add_patch(circle)
        
    def create_character(self, name: str):
        """
        Uses Matplotlib to draw a character with ATMOSPHERE and LIGHT.
        """
        logger.info(f"🎨 Plotting Luminous Character: {name}...")
        
        # 1. Setup Canvas (High DPI for quality)
        fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
        ax.set_aspect('equal')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off') # Hide axes
        
        # Background: Deep Void
        ax.set_facecolor('#050510') 
        rect = patches.Rectangle((0,0), 100, 100, fc='#050510', zorder=-1)
        ax.add_patch(rect)
        
        # 2. Add Atmosphere (The Aura)
        self.create_atmosphere(ax, 100, 100, color_hex="#9370DB") # Medium Purple Aura
        
        # 3. Add Point Lights (floaty particles)
        for _ in range(20):
            lx, ly = random.uniform(0, 100), random.uniform(0, 100)
            self.add_glow_point(ax, lx, ly, radius=0.5, color="#00FFFF", layers=3)


        # 4. The Face (Lit from below)
        face = patches.Ellipse((50, 50), width=40, height=50, angle=0, 
                               fc='#FFE4E1', ec='#FFC0CB', lw=2, zorder=10)
        ax.add_patch(face)
        
        # 5. The Eyes (Complex Patches)
        self._add_eye(ax, 40, 52) # Left
        self._add_eye(ax, 60, 52) # Right
        
        # 6. The Mouth (Path)
        verts = [
            (45, 40), # Start
            (50, 38), # Control
            (55, 40), # End
        ]
        codes = [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3]
        path = mpath.Path(verts, codes)
        patch = patches.PathPatch(path, fc='none', ec='#FA8072', lw=3, zorder=11)
        ax.add_patch(patch)
        
        # 7. The Hair (Bezier Curves - The "Flow")
        self._add_hair_strand(ax, 50, 80, 20, 40, -20) # Left Bang
        self._add_hair_strand(ax, 50, 80, 80, 40, 20)  # Right Bang
        self._add_hair_strand(ax, 50, 80, 50, 55, 0)   # Center Bang
        
        # Side Hair
        self._add_hair_strand(ax, 30, 60, 20, 10, -10)
        self._add_hair_strand(ax, 70, 60, 80, 10, 10)

        # 8. Add Foreground Bloom (Magical Finish)
        self.add_glow_point(ax, 50, 50, radius=20, color="#FFFFFF", layers=5)

        # 9. Save
        path = self.output_dir / f"{name}.png"
        plt.savefig(path, facecolor='#050510', bbox_inches='tight')
        plt.close(fig)
        
        logger.info(f"✨ Masterpiece Plot Complete: {path}")
        return str(path)

    def _add_eye(self, ax, x, y):
        # Sclera
        sclera = patches.Ellipse((x, y), width=12, height=10, fc='white', ec='none', zorder=11)
        ax.add_patch(sclera)
        
        # Iris
        iris = patches.Circle((x, y), radius=3.5, fc='#4B0082', zorder=12)
        ax.add_patch(iris)
        
        # Highlights
        h1 = patches.Circle((x-1.5, y+1.5), radius=1.0, fc='white', zorder=13)
        ax.add_patch(h1)
        
        # Lashes
        verts = [(x-6, y+2), (x, y+6), (x+6, y+2)]
        codes = [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3]
        path = mpath.Path(verts, codes)
        patch = patches.PathPatch(path, fc='none', ec='black', lw=2, zorder=14)
        ax.add_patch(patch)

    def _add_hair_strand(self, ax, sx, sy, ex, ey, curve_x):
        """Draws a hair strand using quadratic bezier."""
        ctrl_x = (sx + ex) / 2 + curve_x
        ctrl_y = (sy + ey) / 2
        verts = [(sx, sy), (ctrl_x, ctrl_y), (ex, ey)]
        codes = [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3]
        path = mpath.Path(verts, codes)
        patch = patches.PathPatch(path, fc='none', ec='#191970', lw=2, zorder=15)
        ax.add_patch(patch)

if __name__ == "__main__":
    artist = MathArtist()
    artist.create_character("elysia_aura_plot")
