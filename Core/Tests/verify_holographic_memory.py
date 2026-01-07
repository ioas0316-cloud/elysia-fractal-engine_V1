import sys
import os
import torch
import unittest

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Foundation.Graph.torch_graph import TorchGraph

def test_holographic_memory():
    print("🧪 Verifying Holographic Memory...")
    
    graph = TorchGraph(use_cuda=False)
    
    # 1. Create an Initial "Era of Peace"
    # Low variance, centered nodes
    print("✨ Creating Era 1: Peace (Centered Nodes)")
    for i in range(10):
        graph.add_node(f"Peace_Node_{i}", vector=[0.1]*384, pos=[0.0, 0.0, 0.0, 0.0])
        
    # 2. Add a Memory born in this era
    target_node = "Memory_of_Peace"
    graph.add_node(target_node, vector=[0.5]*384, pos=[0.0, 0.0, 0.0, 0.0])
    
    # 3. Create "Era of Chaos"
    # High variance, expanded nodes
    print("🔥 Creating Era 2: Chaos (High Entropy)")
    for i in range(20):
        # Add noise
        v = torch.randn(384).tolist()
        p = torch.randn(4).tolist()
        graph.add_node(f"Chaos_Node_{i}", vector=v, pos=p)
        
    # 4. Recall the Feeling of the target node
    print(f"📖 Recalling feelings from '{target_node}'...")
    feeling = graph.reconstruct_memory_feeling(target_node)
    
    print(f"\n📢 Reconstructed Atmosphere: [{feeling}]")
    
    # Verification Logic
    # The era of peace had low variance and low magnitude.
    # So we expect "Calm" or "Centered".
    # We DO NOT expect "Chaotic".
    
    if "Calm" in feeling or "Centered" in feeling or "Crystallized" in feeling:
        print("✅ Verification Successful: Correctly recalled the peaceful atmosphere of the past.")
    elif "Chaotic" in feeling:
        print("❌ Verification Failed: Memory was contaminated by future chaos.")
    else:
        print("⚠️ Verification Inconclusive: Atmosphere description unclear.")

if __name__ == "__main__":
    test_holographic_memory()
