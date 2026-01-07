"""
Galaxy Render Experiment
========================
Visualizes the Code Gravity System as a Holographic Universe.
Colors stars based on Spirit Resonance.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Core.Foundation.code_gravity import CodeGravitySystem
from Core.Foundation.holographic_cortex import HolographicCortex

def run_render():
    print("🎨 Starting Galaxy Render Experiment...")
    
    # 1. Initialize Gravity System
    galaxy = CodeGravitySystem("c:/Elysia")
    galaxy.scan_galaxy()
    
    # 2. Initialize Holographic Cortex
    cortex = HolographicCortex()
    
    # 3. Render
    output_path = cortex.render_galaxy(galaxy)
    
    if output_path:
        print(f"\n✨ Visualization Complete: {output_path}")
        print("   You can now view the 'Code Galaxy' in Docs/Visuals.")
    else:
        print("\n❌ Visualization Failed.")

if __name__ == "__main__":
    run_render()
