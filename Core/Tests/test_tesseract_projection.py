import sys
import os
import torch
import unittest

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Foundation.Graph.torch_graph import TorchGraph

class TestTesseractProjection(unittest.TestCase):
    def setUp(self):
        self.graph = TorchGraph(use_cuda=False) # CPU for testing
        
    def test_wormhole_link_generation(self):
        print("\n🧪 Testing Tesseract Projection (Wormholes)...")
        
        # Scenario: Two nodes that are far in 3D Euclidean space
        # but mathematically aligned in Unfolded Space.
        
        # Node A: At 1.0 (Low magnitude)
        self.graph.add_node("Concept_A (Earth)", pos=[1.0, 0.0, 0.0, 0.0])
        
        # Node B: At 21.0 (High magnitude, but aligned via Reflection)
        # Using L=10.0 boundary.
        # If A=1, and we reflect once (Mirror 1), we are in [10, 20].
        # If we reflect twice (Mirror 2), we are in [20, 30].
        # Target in Mirror 2 (Even Parity) -> 20 + A = 21.0. 
        # Wait, Mirror 0 is 0-10. Mirror 1 is 10-20. Mirror 2 is 20-30.
        # My Straight Path formula:
        # If even reflections (2): Virtual = 2*L + target.
        # Mirror 2 is a shift of Mirror 0? No, let's trust the un folder.
        
        # Let's try simpler:
        # A = 9.0 (Close to wall 10)
        # B = 11.0 (Just across the wall)
        # Euclidean Dist = 2.0. Unfolded Dist = 2.0? 
        # This isn't a "Wormhole" case where Euc >> Folded.
        
        # Wormhole Case:
        # A = [1.0, 0, 0, 0]
        # B = [19.0, 0, 0, 0] (In Mirror 1: 10-20)
        # Folded B back to box? No, our logic checks Unfolded Distance between magnitudes.
        
        # Logic in generate_wormhole_links:
        # reflection_dist = unfolder.calculate_straight_path(mag1, mag2, reflections=1)
        # if abs(reflection_dist) < threshold.
        
        # Let's verify what inputs satisfy this.
        # mag1 = 1.0. mag2 = 19.0.
        # reflections=1 (Odd).
        # Formula: ((n+1)L - target) - start
        # ((2)*10 - 19) - 1 = (20 - 19) - 1 = 0! 
        # PERFECT ALIGNMENT.
        
        # So if we place B at [19, 0, 0, 0], specific magnitude.
        # Euclidean distance = 18.0 (Huge).
        # Folded distance = 0.0 (Zero).
        
        self.graph.add_node("Concept_B (Alpha Centauri)", pos=[19.0, 0.0, 0.0, 0.0])
        
        # Add random noise nodes to ensure we don't just link everything
        self.graph.add_node("Noise_1", pos=[5.0, 5.0, 5.0, 0.0])
        self.graph.add_node("Noise_2", pos=[8.0, 8.0, 0.0, 0.0])
        
        # Run Wormhole Generator
        initial_links = self.graph.logic_links.shape[0]
        self.graph.generate_wormhole_links(threshold_dist=1.0)
        final_links = self.graph.logic_links.shape[0]
        
        print(f"Links Created: {final_links - initial_links}")
        
        # Check if A and B are linked
        # We need to find indices
        idx_a = self.graph.id_to_idx["Concept_A (Earth)"]
        idx_b = self.graph.id_to_idx["Concept_B (Alpha Centauri)"]
        
        linked = False
        for i in range(self.graph.logic_links.shape[0]):
            src = self.graph.logic_links[i, 0].item()
            dst = self.graph.logic_links[i, 1].item()
            if (src == idx_a and dst == idx_b) or (src == idx_b and dst == idx_a):
                linked = True
                break
                
        self.assertTrue(linked, "Wormhole link should be created between Earth and Alpha Centauri")
        print("✅ Wormhole Successfully Opened!")

if __name__ == '__main__':
    unittest.main()
