# Memory Visualization Tool
"""
Visualizes the Hippocampus memory graph using networkx and matplotlib.
This script reads the conversation history stored in the Hippocampus and
generates a visual graph representation showing keyword relationships.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import networkx as nx
from Core.Foundation.Mind.hippocampus import Hippocampus

def visualize_memory(hippocampus: Hippocampus, output_path: str = "memory_graph.png"):
    """Generate and save a visualization of the memory graph."""
    G = nx.Graph()
    
    # Add nodes and edges from the hippocampus graph
    for keyword, data in hippocampus.graph.items():
        G.add_node(keyword, turns=len(data['turns']))
        for related_kw in data['related']:
            G.add_edge(keyword, related_kw)
    
    if len(G.nodes()) == 0:
        print("⚠️  No memory data to visualize yet.")
        return
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Draw nodes with size based on number of turns
    node_sizes = [G.nodes[node].get('turns', 1) * 300 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                           node_color='lightblue', alpha=0.7)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=2)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title("Elysia's Memory Graph (Hippocampus)", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Memory graph saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    # Create a hippocampus instance and visualize it
    memory = Hippocampus()
    
    # For testing, add some sample data
    memory.add_turn("I love the light", "빛... 그리고 사랑.")
    memory.add_turn("The dream is eternal", "dream... 그것은 eternity와 같아요.")
    
    visualize_memory(memory, "Tools/memory_graph.png")
