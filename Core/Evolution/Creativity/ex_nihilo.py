"""
Ex Nihilo (Creation from Nothing)
=================================
"Let there be light."

A Pure-Code Raymarching Engine.
This module renders 3D images using Signed Distance Functions (SDF).
It does NOT use any AI generation or external 3D engines.
It calculates the physics of light using pure math.

Core Math:
d = length(p) - r  (Sphere)
"""

import math
import time
import logging
from pathlib import Path
from dataclasses import dataclass

# Using PIL only for saving the final buffer to PNG
from PIL import Image

logger = logging.getLogger("ExNihilo")
logging.basicConfig(level=logging.INFO)

# Vector3 Math Helpers (Pure Python for transparency)
@dataclass
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other): return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other): return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, v): return Vec3(self.x * v, self.y * v, self.z * v)
    def length(self): return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def normalize(self):
        l = self.length()
        return Vec3(0,0,0) if l == 0 else Vec3(self.x/l, self.y/l, self.z/l)

def dot(a, b): return a.x*b.x + a.y*b.y + a.z*b.z

class ExNihiloEngine:
    def __init__(self):
        self.output_dir = Path("outputs/gallery")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Resolution (Keep low for CPU rendering speed)
        self.width = 300 
        self.height = 200
        self.max_steps = 100
        self.max_dist = 100.0
        self.surf_dist = 0.01

    # --- SDF Primitives (The Words of Creation) ---
    def sd_sphere(self, p, r):
        return p.length() - r

    def sd_plane(self, p):
        return p.y

    # --- The World Definition ---
    def get_dist(self, p):
        """
        Defines the Scene Topology.
        Here lies 'The Monad' (Sphere) hovering above 'The Void' (Plane).
        """
        # Sphere: Position (0, 1, 6), Radius 1
        sphere_dist = self.sd_sphere(p - Vec3(0, 1, 6), 1.0)
        # Plane: y = 0
        plane_dist = self.sd_plane(p)
        
        # CSG Union
        d = min(sphere_dist, plane_dist)
        return d

    # --- The Physics of Light ---
    def ray_march(self, ro, rd):
        dO = 0.0
        for i in range(self.max_steps):
            p = ro + rd * dO
            dS = self.get_dist(p)
            dO += dS
            if dO > self.max_dist or dS < self.surf_dist:
                break
        return dO

    def get_normal(self, p):
        d = self.get_dist(p)
        e = Vec3(0.01, 0, 0)
        n = Vec3(
            d - self.get_dist(p - e),
            d - self.get_dist(p - Vec3(0, 0.01, 0)),
            d - self.get_dist(p - Vec3(0, 0, 0.01))
        )
        return n.normalize()

    def get_light(self, p):
        light_pos = Vec3(0, 5, 6)
        # Move light in a circle over time
        t = time.time()
        light_pos.x += math.sin(t) * 2
        
        l = (light_pos - p).normalize()
        n = self.get_normal(p)
        
        diff = max(0, dot(n, l))
        return diff

    # --- The Renderer ---
    def render(self, concept: str) -> str:
        logger.info(f"⚡ Ex Nihilo computing: {concept}...")
        start_time = time.time()
        
        img = Image.new('L', (self.width, self.height)) # Grayscale for raw light
        pixels = img.load()
        
        # Camera Setup
        ro = Vec3(0, 1, 0) # Ray Origin
        
        for y in range(self.height):
            for x in range(self.width):
                # Normalized Device Coordinates (NDC)
                uv = Vec3((x - 0.5 * self.width) / self.height, 
                          (y - 0.5 * self.height) / self.height * -1,  # Flip Y
                          1) # Screen dist
                
                rd = uv.normalize() # Ray Direction
                
                d = self.ray_march(ro, rd)
                
                col = 0
                if d < self.max_dist:
                    p = ro + rd * d
                    diff = self.get_light(p)
                    col = int(diff * 255)
                
                pixels[x, y] = col
                
        # Save
        filename = f"ex_nihilo_{int(time.time())}.png"
        path = self.output_dir / filename
        img.save(path)
        
        duration = time.time() - start_time
        logger.info(f"✨ Creation Complete in {duration:.2f}s: {path}")
        return str(path)

if __name__ == "__main__":
    engine = ExNihiloEngine()
    engine.render("The Monad")
