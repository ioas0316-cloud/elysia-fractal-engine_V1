"""
Mimicry Engine (Organic SDF Sculptor)
=====================================
"Math is not rigid. It flows like water."

This module demonstrates that mathematical functions can represent
ORGANIC, SOFT, and IRREGULAR shapes using:
1. Smooth Blending (smin) - The "Clay" logic.
2. Domain Warping (sin/cos) - The "Flow" logic.
"""

import math
import time
import logging
from pathlib import Path
from dataclasses import dataclass
from PIL import Image

logger = logging.getLogger("MimicryEngine")
logging.basicConfig(level=logging.INFO)

@dataclass
class Vec3:
    x: float; y: float; z: float
    def __add__(self, o): return Vec3(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o): return Vec3(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self, v): return Vec3(self.x*v, self.y*v, self.z*v)
    def length(self): return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def normalize(self):
        l = self.length()
        return Vec3(0,0,0) if l==0 else Vec3(self.x/l, self.y/l, self.z/l)

def dot(a, b): return a.x*b.x + a.y*b.y + a.z*b.z

class MimicryEngine:
    def __init__(self):
        self.output_dir = Path("outputs/gallery")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 300
        self.height = 300
        self.max_steps = 60 # Reduced for Python speed
        self.max_dist = 10.0
        self.surf_dist = 0.01

    # --- Organic Math Operators (The Secret Sauce) ---
    
    def smin(self, a, b, k):
        """
        Smooth Minimum (Polynomial Mix).
        Blends two distances 'a' and 'b' together like liquid mercury.
        k = blending smoothness (e.g., 0.1)
        """
        h = max(0.0, min(1.0, 0.5 + 0.5 * (b - a) / k))
        return (b * h + a * (1.0 - h)) - k * h * (1.0 - h)

    def op_twist(self, p, amount=1.0):
        """Domain Twist for Hair/Organic flow."""
        c = math.cos(amount * p.y)
        s = math.sin(amount * p.y)
        # Standard rotation matrix on XZ plane
        return Vec3(c * p.x - s * p.z, p.y, s * p.x + c * p.z)

    # --- Primitives ---
    def sd_sphere(self, p, r): return p.length() - r
    def sd_box(self, p, b):
        q = Vec3(abs(p.x)-b.x, abs(p.y)-b.y, abs(p.z)-b.z)
        length_max = math.sqrt(max(q.x,0)**2 + max(q.y,0)**2 + max(q.z,0)**2)
        return length_max + min(max(q.x, max(q.y, q.z)), 0.0)

    # --- The Character Sculpt (Chibi Style) ---
    def map_scene(self, p):
        # 1. Head (Main Sphere)
        # Slightly squashed sphere for cuteness
        head_p = Vec3(p.x * 0.9, p.y * 1.0, p.z * 1.0)
        d_head = self.sd_sphere(head_p - Vec3(0, 0.2, 0), 0.6)
        
        # 2. Cheeks (Smooth Blending) - THE ORGANIC TOUCH
        # Adding spheres on sides but blending seamlessly
        cheek_l = self.sd_sphere(p - Vec3(-0.4, 0.0, 0.3), 0.35)
        cheek_r = self.sd_sphere(p - Vec3(0.4, 0.0, 0.3), 0.35)
        d_face = self.smin(d_head, cheek_l, 0.2)
        d_face = self.smin(d_face, cheek_r, 0.2)
        
        # 3. Eyes (Subtraction) - Hard Cuts
        eye_l = self.sd_sphere(p - Vec3(-0.25, 0.2, 0.55), 0.15)
        eye_r = self.sd_sphere(p - Vec3(0.25, 0.2, 0.55), 0.15)
        
        # Subtract eyes from face (d_A intersection -d_B)
        d_with_eyes = max(d_face, -eye_l)
        d_with_eyes = max(d_with_eyes, -eye_r)

        # 4. Hair (Twisted Domain) - IRREGULARITY
        # Twist the space above the head
        hair_p = p - Vec3(0, 0.6, 0)
        twisted_p = self.op_twist(hair_p, amount=3.0) 
        d_hair = self.sd_box(twisted_p, Vec3(0.65, 0.2, 0.65))
        d_hair -= 0.1 # Rounded box
        
        # Combine Hair and Head smoothly
        d_final = self.smin(d_with_eyes, d_hair, 0.05)
        
        return d_final

    # --- Raymarching Kernel ---
    def get_normal(self, p):
        d = self.map_scene(p)
        e = 0.01
        dx = self.map_scene(p - Vec3(e,0,0))
        dy = self.map_scene(p - Vec3(0,e,0))
        dz = self.map_scene(p - Vec3(0,0,e))
        return Vec3(d-dx, d-dy, d-dz).normalize()

    def render(self, output_name: str):
        logger.info(f"🎨 Sculpting Character: {output_name}...")
        img = Image.new('RGB', (self.width, self.height), "black") # Color!
        pixels = img.load()
        
        # Camera (Fixed: Moved back to -2.5 to see the object at 0,0,0)
        ro = Vec3(0, 0.5, -2.5)
        
        hit_count = 0
        for y in range(self.height):
            for x in range(self.width):
                uv = Vec3((x - 0.5*self.width)/self.height, (y - 0.5*self.height)/self.height * -1, 1.0)
                rd = uv.normalize()
                
                # March
                dO = 0.0
                hit = False
                for i in range(self.max_steps):
                    p = ro + rd * dO
                    dS = self.map_scene(p)
                    dO += dS
                    if dS < self.surf_dist:
                        hit = True
                        break
                    if dO > self.max_dist: break
                
                if hit:
                    hit_count += 1
                    p = ro + rd * dO
                    n = self.get_normal(p)
                    
                    # Lighting (Key Light + Ambient)
                    light_dir = Vec3(0.5, 1.0, 0.5).normalize()
                    diff = max(0.0, dot(n, light_dir))
                    
                    # Material Color (Simple Gradient based on Normal)
                    # Skin tone-ish + Lighting
                    base_color = Vec3(255, 200, 180) # Pale Skin
                    
                    # If normal points up/back, maybe hair color?
                    if p.y > 0.5: 
                        base_color = Vec3(100, 200, 255) # Blue Hair
                    
                    col_r = int(base_color.x * (diff * 0.8 + 0.2))
                    col_g = int(base_color.y * (diff * 0.8 + 0.2))
                    col_b = int(base_color.z * (diff * 0.8 + 0.2))
                    
                    pixels[x,y] = (col_r, col_g, col_b)
                else:
                    pixels[x,y] = (20, 20, 30) # Background
                    
        path = self.output_dir / output_name
        img.save(path)
        
        hit_pct = (hit_count / (self.width * self.height)) * 100
        logger.info(f"✨ Character Sculpted: {path} (Coverage: {hit_pct:.1f}%)")
        return str(path)

if __name__ == "__main__":
    engine = MimicryEngine()
    engine.render("mimic_character_fixed.png")
