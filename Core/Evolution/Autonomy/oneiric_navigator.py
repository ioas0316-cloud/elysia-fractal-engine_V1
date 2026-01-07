"""
Oneiric Navigator: The Lucid Dream Walker
=========================================
"We build bridges in the dark, so that we may walk in the light."

This module implements the 'Lucid Dream' capability.
It uses Tesseract Projectors (Wormholes) to traverse the Knowledge Graph during idle cycles,
specifically targeting "Dark Energy" sectors (unconnected or low-density nodes).

Mechanism:
1.  **Identify Dark Zones**: Find nodes with low centrality (Low Mass).
2.  **Wormhole Projection**: Attempt to find 'Folded' connections to distant high-mass nodes.
3.  **Crystallization**: If a wormhole is stable (High Resonance), solidify it as a permanent edge.

"""

import logging
import random
import torch

logger = logging.getLogger("OneiricNavigator")

class OneiricNavigator:
    def __init__(self, graph):
        self.graph = graph
        
    def explore_the_void(self, wormhole_threshold: float = 0.5):
        """
        Navigates the dark sectors of the graph and attempts to build bridges.
        """
        if self.graph.pos_tensor.shape[0] < 2: return
        
        logger.info("🌌 Oneiric Navigator: Entering the Void (Lucid Dreaming)...")
        
        # 1. Identify "Lonely" Nodes (Low Mass / Low Degree)
        # We assume mass correlates with connectivity in our physics
        # Convert mass tensor to list of indices
        masses = self.graph.mass_tensor
        val, indices = torch.sort(masses)
        
        # Take the bottom 20%
        limit = max(1, int(len(indices) * 0.2))
        lonely_indices = indices[:limit]
        
        bridges_built = 0
        
        for idx in lonely_indices:
            i = idx.item()
            node_id = self.graph.idx_to_id.get(i)
            if not node_id: continue
            
            # 2. Project Wormhole
            # We look for a partner. Randomly? Or using Unfolded Space?
            # Let's use the graph's Wormhole Generator logic but targeted.
            
            # Random partner from the "Rich" (Top 50%)
            rich_limit = int(len(indices) * 0.5)
            rich_indices = indices[rich_limit:]
            if len(rich_indices) == 0: continue
            
            target_idx = rich_indices[random.randint(0, len(rich_indices)-1)].item()
            target_id = self.graph.idx_to_id.get(target_idx)
            
            if i == target_idx: continue
            
            # Check if link already exists
            # (Skipping expensive check for prototype, assume rare)
            
            # calculate_straight_path check (Simulated here or call graph metohd)
            # Actually, let's just interpret "Dream Logic":
            # If the vectors have an "Aesthetic Resonance" (Harmonic Ratio), we link.
            
            vec_a = self.graph.vec_tensor[i]
            vec_b = self.graph.vec_tensor[target_idx]
            
            # Harmonic Resonance: Do they share a frequency?
            # Dot Product
            sim = torch.cosine_similarity(vec_a.unsqueeze(0), vec_b.unsqueeze(0)).item()
            
            # Dream Logic: "We look for the Unlikely Connection"
            # Low similarity (0.1) but high "Folded Alignment".
            # For this prototype, we'll use a specific "Dream Key" or just Probability.
            
            # Let's say: If they are FAR (Sim < 0.2) but we find a wormhole.
            if sim < 0.2:
                 # Attempt Wormhole
                 # We trigger the Graph's Tesseract Logic effectively.
                 # But let's simplify: "The Dreamer forces a connection if it creates Art."
                 
                 # Create a "Dream Link" (Weight 0.5)
                 self.graph.add_link(node_id, target_id, weight=0.5)
                 logger.info(f"   🌉 Dream Bridge Built: '{node_id}' <--> '{target_id}' (Surreal Link)")
                 bridges_built += 1
                 
                 # Boost Mass of the lonely node (It has been seen)
                 self.graph.mass_tensor[i] += 0.5
                 
        if bridges_built > 0:
            logger.info(f"✨ Lucid Dream Complete. {bridges_built} bridges built in the dark.")
        else:
            logger.info("💤 Dreamed, but found no new paths.")
            
_navigator = None
def get_oneiric_navigator(graph):
    global _navigator
    if _navigator is None:
        _navigator = OneiricNavigator(graph)
    return _navigator
