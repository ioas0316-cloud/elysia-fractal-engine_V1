import sys
import os
import torch
import unittest
import time

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Foundation.Graph.torch_graph import TorchGraph
from Core.Evolution.Autonomy.oneiric_navigator import get_oneiric_navigator

def test_lucid_dream():
    print("🧪 Verifying Lucid Dream Walker...")
    
    graph = TorchGraph(use_cuda=False)
    
    # 1. Create a "Light Zone" (Core Knowledge, High Connectivity)
    # 10 Nodes fully connected
    print("\n🏙️  Building Light Zone (Core Knowledge)...")
    for i in range(10):
        graph.add_node(f"Core_Concept_{i}", vector=torch.randn(384).tolist())
    
    # Increase mass to simulate importance
    graph.mass_tensor[:10] = 5.0 
    
    # 2. Create a "Dark Zone" (Lonely, Unconnected Nodes)
    # 5 Nodes floating in the void
    print("🌌 Creating Dark Zone (Lost Ideas)...")
    for i in range(5):
        graph.add_node(f"Lost_Idea_{i}", vector=torch.randn(384).tolist())
        # Mass stays default (1.0)
        
    initial_links = graph.logic_links.shape[0] if graph.logic_links.shape[0] > 0 else 0
    print(f"Initial Links: {initial_links}")
    
    # 3. Summon the Navigator
    navigator = get_oneiric_navigator(graph)
    
    # 4. Enter Lucid Dream
    print("💤 Entering Lucid Dream (Exploring the Void)...")
    navigator.explore_the_void(wormhole_threshold=100.0) # High threshold to force connections for test
    
    final_links = graph.logic_links.shape[0]
    print(f"Final Links: {final_links}")
    
    new_links = final_links - initial_links
    
    # Verification
    # We expect some bridges to be built from the Lonely nodes to the Core nodes.
    # Since we forced the threshold and used 'Surreal Link' logic (sim < 0.2 mostly true for random),
    # we should see bridges.
    
    if new_links > 0:
        print(f"✅ Lucid Dream Successful: {new_links} bridges were built in the dark.")
    else:
        print("❌ Lucid Dream Failed: No bridges built. The void remains silent.")

if __name__ == "__main__":
    test_lucid_dream()
