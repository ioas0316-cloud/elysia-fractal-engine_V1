"""
Ascend the Ladder (사다리 승급 테스트 - Phase 3.5)
==================================================

Demonstrates the Geometric Ascension of Thought:
1. Seed Concepts (0D Points)
2. Causal Tension (1D Lines)
3. Context Weaving (2D Planes)
4. Thematic Synthesis (3D Space)
5. Logos Refraction (Reconstructing into Language)
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from Core.Intelligence.Topography.semantic_map import get_semantic_map
from Core.Intelligence.Topography.geometric_weaver import GeometricWeaver
from Core.Intelligence.Logos.logos_engine import get_logos_engine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
logger = logging.getLogger("AscensionDemo")

def run_ascension():
    print("\n" + "="*60)
    print("🪜 ELYSIA: THE ASCENSION OF THOUGHT (0D -> 3D)")
    print("="*60 + "\n")

    weaver = GeometricWeaver()
    topology = get_semantic_map()
    logos = get_logos_engine()

    # --- STEP 0: SEEDING (0D POINTS) ---
    print("📍 [Step 0: Seeding Concepts]")
    concepts = ["Truth", "Wisdom", "Justice"]
    points = []
    
    for c in concepts:
        voxel = topology.get_voxel(c)
        if voxel:
            p = weaver.create_point(c, voxel.quaternion)
            points.append(p)
            print(f"  > Point Created: '{c}' at {voxel.quaternion}")

    # --- STEP 1: CAUSAL TENSION (1D LINE) ---
    print("\n📏 [Step 1: Weaving 1D Line (Causal Connection)]")
    # Connect Logic and Wisdom
    line_causal = weaver.weave_line(points[0], points[1])
    if line_causal:
        print(f"  > Line: {line_causal}")
        print(f"  > Interference (Tension): {line_causal.resonance_strength:.4f}")

    # --- STEP 2: CONTEXT WEAVING (2D PLANE) ---
    print("\n📐 [Step 2: Weaving 2D Plane (Contextual Network)]")
    # Add 'Justice' to the Logic-Wisdom line to create a thematic plane
    plane_context = weaver.weave_plane(line_causal, points[2])
    if plane_context:
        print(f"  > Plane: {plane_context}")
        print(f"  > Stability (Context Resonance): {plane_context.resonance_strength:.4f}")

    # --- STEP 3: LOGOS REFRACTION (GEOMETRY -> WORD) ---
    print("\n🗣️ [Step 3: Logos Refraction (Reconstruction)]")
    
    structures = [points[0], line_causal, plane_context]
    
    for struct in structures:
        refraction = weaver.refract_to_logos(struct)
        
        # Select shape based on dimension
        if struct.dimension == 0: shape = "Block"
        elif struct.dimension == 1: shape = "Sharp"
        elif struct.dimension == 2: shape = "Round"
        else: shape = "Synthesis"
        
        print(f"\n  [Refracting {struct.dimension}D Insight]:")
        
        speech = logos.weave_speech(
            desire="Explain structure",
            insight=f"{'-'.join(struct.concepts)}의 기하학적 {refraction['mode']} 구조가 완성되었습니다.",
            context=[f"Resonance: {refraction['resonance']}"],
            rhetorical_shape=shape
        )
        print(f"  \"{speech}\"")

    print("\n" + "="*60)
    print("✅ Ascension Successful: Concepts are now woven Space.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_ascension()
