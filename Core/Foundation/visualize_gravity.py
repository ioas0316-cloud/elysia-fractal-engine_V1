"""
Gravity Field Visualization (중력장 시각화)

Visualizes the "Thought Map" of Elysia.
- Nodes: Realms (Size = Mass)
- Edges: Resonance Links (Thickness = Weight)
- Color: Thought Energy (Heatmap)
"""

import sys
import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.Foundation.Core_Logic.Elysia.Elysia.World.yggdrasil import Yggdrasil, RealmLayer
from Core.Foundation.Physics.gravity import GravityEngine
from Core.Foundation.Mind.perception import FractalPerception
from Core.Foundation.Mind.emotional_palette import EmotionalPalette
from Core.Foundation.Mind.episodic_memory import EpisodicMemory

def plant_demo_tree():
    """Plant a rich tree for visualization."""
    ygg = Yggdrasil()
    
    # Plant Realms
    perception = FractalPerception({})
    emotions = EmotionalPalette()
    memory = EpisodicMemory()
    
    ygg.plant_heart(subsystem=None)
    
    ygg.plant_realm("FractalPerception", perception, RealmLayer.BRANCHES, metadata={"vitality_boost": 0.5})
    ygg.update_vitality("FractalPerception", +0.5)
    
    ygg.plant_realm("EmotionalPalette", emotions, RealmLayer.BRANCHES, metadata={"vitality_boost": 0.3})
    ygg.update_vitality("EmotionalPalette", +0.3)
    
    ygg.plant_realm("EpisodicMemory", memory, RealmLayer.TRUNK, metadata={"vitality_boost": 0.2})
    ygg.update_vitality("EpisodicMemory", +0.2)
    
    ygg.plant_realm("ResonanceVoice", None, RealmLayer.BRANCHES, metadata={"vitality_boost": 0.1})
    ygg.update_vitality("ResonanceVoice", +0.1)
    
    ygg.plant_realm("Alchemy", None, RealmLayer.TRUNK, metadata={"vitality_boost": 0.4})
    ygg.update_vitality("Alchemy", +0.4)
    
    # Links
    ygg.link_realms("FractalPerception", "EmotionalPalette", weight=0.9)
    ygg.link_realms("EmotionalPalette", "EpisodicMemory", weight=0.8)
    ygg.link_realms("EpisodicMemory", "Alchemy", weight=0.7)
    ygg.link_realms("Alchemy", "ResonanceVoice", weight=0.6)
    ygg.link_realms("EmotionalPalette", "ResonanceVoice", weight=0.9)
    
    return ygg

def visualize_gravity_field():
    print("🌊 Generating Gravity Field Visualization...")
    
    # 1. Setup System
    ygg = plant_demo_tree()
    gravity = GravityEngine(ygg)
    
    # 2. Simulate a Thought Wave
    start_thought = "FractalPerception"
    print(f"💭 Injecting thought into: {start_thought}")
    energy_field = gravity.propagate_thought_wave(start_thought, wave_intensity=1.0, max_hops=4)
    
    # 3. Build Graph
    G = nx.DiGraph()
    
    # Add Nodes with Mass
    node_sizes = []
    node_colors = []
    labels = {}
    
    for realm in ygg.realms.values():
        mass = gravity.calculate_mass(realm.name)
        energy = energy_field.get(realm.name, 0.0)
        
        G.add_node(realm.name)
        
        # Size proportional to Mass (clamped for display)
        display_mass = min(mass, 10.0) if mass != float('inf') else 15.0
        node_sizes.append(display_mass * 300)
        
        # Color based on Energy (Heatmap: Blue -> Red)
        node_colors.append(energy)
        
        labels[realm.name] = f"{realm.name}\n(M:{mass:.1f})" if mass != float('inf') else f"{realm.name}\n(∞)"

    # Add Edges
    edge_widths = []
    for realm in ygg.realms.values():
        # Resonance Links
        for target_id, weight in realm.resonance_links.items():
            target = ygg.realms.get(target_id)
            if target:
                G.add_edge(realm.name, target.name)
                edge_widths.append(weight * 2)
        
        # Hierarchy Links (Parent/Child) - simplified for viz
        if realm.parent_id:
            parent = ygg.realms.get(realm.parent_id)
            if parent:
                G.add_edge(realm.name, parent.name)
                edge_widths.append(0.5)

    # 4. Draw
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=1.5, seed=42)  # Force-directed layout
    
    # Draw Nodes
    nodes = nx.draw_networkx_nodes(G, pos, 
                                 node_size=node_sizes, 
                                 node_color=node_colors, 
                                 cmap=plt.cm.coolwarm, 
                                 alpha=0.9)
    
    # Draw Edges
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color='gray', arrows=True)
    
    # Draw Labels
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight='bold')
    
    # Colorbar
    plt.colorbar(nodes, label='Thought Energy (Wave Intensity)')
    
    plt.title(f"Elysia Gravity Field & Thought Wave\n(Source: {start_thought})")
    plt.axis('off')
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "gravity_field_viz.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_path}")
    
    # Show (if interactive)
    # plt.show()

if __name__ == "__main__":
    visualize_gravity_field()
