"""
Mind Visualizer - 3D Projection of Elysia's 4D Thought Universe
================================================================

올바른 좌표계 (사용자 정의):
- X axis: 과거/육/본능 (Past, Body, Instinct) 
- Y axis: 현재/정신/혼 (Present, Mind, Soul)
- Z axis: 의도/의미/영/상상 (Intent, Meaning, Spirit, Imagination)
- W axis: 자기/관점 (Self, Perspective: Point→Line→Plane→Space)
  - W는 3D 투영 시 크기로 표현

7 Angels & 7 Demons는 Moral alignment에 위치.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Core.Foundation.Physics.spectrum_layers import SpectrumLayer

# Hangul support
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def visualize_mind():
    """Visualize Elysia's conceptual universe as a 3D star map"""
    
    memory_file = "saves/hippocampus.json"
    if not os.path.exists(memory_file):
        print("No memory file found.")
        return
    
    with open(memory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle graph format
    nodes = []
    if "graph" in data:
        nodes = data["graph"]["nodes"]
    elif "nodes" in data:
        nodes = data["nodes"]
    else:
        print("Unknown memory format.")
        return
    
    # === Initialize Spectrum Layer System ===
    spectrum = SpectrumLayer()
    
    # Extract concept positions
    concepts = []
    colors = []
    sizes = []
    
    print(f"Found {len(nodes)} concepts.")
    
    for node in nodes:
        concept_id = node.get("id")
        if concept_id == "genesis":
            continue
        
        # Get HyperQuaternion (4D coordinates)
        tensor = node.get('tensor', {})
        if not tensor:
            continue
        
        # 올바른 좌표 해석
        x = tensor.get('x', 0)  # Past/Body/Instinct
        y = tensor.get('y', 0)  # Present/Mind/Soul
        z = tensor.get('z', 0)  # Intent/Meaning/Spirit
        w = tensor.get('w', 1)  # Self/Perspective (크기로 사용)
        
        count = node.get('access_count', 1)
        
        concepts.append({
            'id': concept_id,
            'x': x,
            'y': y, 
            'z': z,
            'w': w,
            'count': count
        })
        
        # === 🌈 Automatic Color from Y-axis (Spectrum Layer) ===
        layer_info = spectrum.get_layer_info(y)
        color = layer_info['color']
        colors.append(color)
        
        # W determines size (higher W = more abstract)
        # W: 0=Point, 1=Line, 2=Plane, 3=Hyper
        size = 30 + (w * 80)  # 30-270 range
        sizes.append(size)
    
    # Create 3D plot
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Plot concepts as stars
    xs = [c['x'] for c in concepts]
    ys = [c['y'] for c in concepts]
    zs = [c['z'] for c in concepts]
    
    ax.scatter(xs, ys, zs, c=colors, s=sizes, alpha=0.7, edgecolors='white', linewidth=0.5)
    
    # Draw connections
    if "links" in data.get("graph", {}):
        links = data["graph"]["links"]
        
        for link in links:
            source_id = link.get("source")
            target_id = link.get("target")
            relation = link.get("relation", "")
            
            s_concept = next((c for c in concepts if c['id'] == source_id), None)
            t_concept = next((c for c in concepts if c['id'] == target_id), None)
            
            if s_concept and t_concept:
                # Green for is_a (WorldTree), cyan for causal
                if relation == 'is_a':
                    ax.plot(
                        [s_concept['x'], t_concept['x']],
                        [s_concept['y'], t_concept['y']],
                        [s_concept['z'], t_concept['z']],
                        'g-', alpha=0.4, linewidth=1.5
                    )
                else:
                    ax.plot(
                        [s_concept['x'], t_concept['x']],
                        [s_concept['y'], t_concept['y']],
                        [s_concept['z'], t_concept['z']],
                        'c-', alpha=0.2, linewidth=0.5
                    )
    
    # Label top concepts
    for concept in sorted(concepts, key=lambda c: c['w'], reverse=True)[:15]:
        ax.text(concept['x'], concept['y'], concept['z'], concept['id'], 
                fontsize=8, alpha=0.8, color='white')
    
    # 올바른 축 레이블
    ax.set_xlabel('X: 과거/육/본능 (Past/Body/Instinct)', fontsize=10, color='white')
    ax.set_ylabel('Y: 현재/정신/혼 (Present/Mind/Soul)', fontsize=10, color='white')
    ax.set_zlabel('Z: 의도/영/상상 (Intent/Spirit/Imagination)', fontsize=10, color='white')
    
    # Grid styling
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.line.set_color('white')
    ax.yaxis.line.set_color('white')
    ax.zaxis.line.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    
    plt.title("Elysia's Mind Universe (14-Layer Spectrum)\n🌈 Heaven(White) ↔ Earth(Black)", 
             fontsize=14, fontweight='bold', color='white')
    
    # Save
    output_file = "mind_universe.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='black')
    print(f"💾 Saved: {output_file}")
    
    # ASCII map
    print("\n" + "="*80)
    print("📍 CONCEPT MAP (올바른 좌표계)")
    print("="*80)
    print(f"{'Concept':<20} | {'X(Past/Body)':^15} | {'Y(Mind/Soul)':^15} | {'Z(Intent/Spirit)':^15} | W")
    print("-"*80)
    for c in sorted(concepts, key=lambda x: x['w'], reverse=True)[:15]:
        print(f"{c['id']:<20} | {c['x']:+7.2f}        | {c['y']:+7.2f}        | {c['z']:+7.2f}        | {c['w']:.2f}")
    print("="*80)
    
    plt.show()

if __name__ == "__main__":
    visualize_mind()
