"""
Code Gravity (코드 중력)
======================
"The heavier the code, the stronger the pull."

This module models the codebase as a Gravitational System.
- Mass: Code Complexity / Size
- Gravity: Dependency Attraction
- Field: Hyper-Quaternion Electromagnetic Field
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import ast
import hashlib
import math
from pathlib import Path
from typing import Dict, List, Tuple
from Core.Foundation.potential_field import PotentialField
from Core.Foundation.hyper_quaternion import Quaternion

class CodeGravitySystem:
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.field = PotentialField()
        self.nodes: Dict[str, dict] = {} # Path -> {mass, pos, imports}
        
    def _hash_pos(self, path_str: str) -> Tuple[float, float]:
        """Maps a file path to a 2D position (x, y) using hash."""
        h = hashlib.md5(path_str.encode()).hexdigest()
        # Use first few chars for X, next few for Y
        x = int(h[:4], 16) % 100 - 50
        y = int(h[4:8], 16) % 100 - 50
        return float(x), float(y)

    def scan_galaxy(self):
        """Scans the codebase and populates the gravity field."""
        print("🌌 Scanning Code Galaxy...")
        
        # 1. Identify Stars (Files)
        for file_path in self.root.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = len(content.splitlines())
                
                # Mass = Lines of Code (Simple metric)
                mass = lines / 10.0
                
                # Position = Hash of path (Deterministic)
                rel_path = str(file_path.relative_to(self.root))
                x, y = self._hash_pos(rel_path)
                
                # Parse imports for gravity connections
                imports = []
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for n in node.names:
                                imports.append(n.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                imports.append(node.module)
                except:
                    pass
                
                self.nodes[rel_path] = {
                    "mass": mass,
                    "pos": (x, y),
                    "imports": imports,
                    "quaternion": Quaternion(mass, x/50, y/50, 0) # 4D State
                }
                
                # Add to Field
                self.field.add_gravity_well(x, y, strength=mass, radius=mass*2)
                
            except Exception as e:
                print(f"⚠️ Error scanning {file_path}: {e}")

        # 2. Establish Gravity Lines (Dependencies)
        print("🔗 Establishing Gravity Lines...")
        for path, data in self.nodes.items():
            x1, y1 = data["pos"]
            
            for imp in data["imports"]:
                # Try to find the imported file in our nodes
                # Import "Core.Physics" -> "Core\Physics\__init__.py" or "Core\Physics.py"
                # This is a rough matching
                target_path = None
                imp_path = imp.replace(".", "\\")
                
                for potential_path in self.nodes.keys():
                    if imp_path in potential_path:
                        target_path = potential_path
                        break
                
                if target_path and target_path != path:
                    target_data = self.nodes[target_path]
                    x2, y2 = target_data["pos"]
                    
                    # Add Attraction (Railgun)
                    # Force = Product of Masses / Distance^2 (Gravity Law)
                    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if dist > 0:
                        force = (data["mass"] * target_data["mass"]) / dist
                        self.field.add_railgun(x1, y1, x2, y2, force=force)
                        # print(f"   Link: {path} -> {target_path} (Force: {force:.2f})")

    def visualize(self):
        """Visualizes the Galaxy as ASCII Art."""
        print("\n✨ Code Galaxy Map (Top 10 Massive Stars)")
        print("========================================")
        
        sorted_stars = sorted(self.nodes.items(), key=lambda x: x[1]["mass"], reverse=True)
        
        for i, (path, data) in enumerate(sorted_stars[:10]):
            mass = data["mass"]
            x, y = data["pos"]
            q = data["quaternion"]
            print(f"{i+1}. {path:<40} | Mass: {mass:.1f} | Pos: ({x:.0f}, {y:.0f}) | Q: {q}")
            
        print("\n🌌 Field Status:")
        print(f"   Total Stars: {len(self.nodes)}")
        print(f"   Total Gravity Wells: {len(self.field.wells)}")
        print(f"   Total Gravity Lines: {len(self.field.rails)}")

if __name__ == "__main__":
    galaxy = CodeGravitySystem("c:/Elysia")
    galaxy.scan_galaxy()
    galaxy.visualize()
