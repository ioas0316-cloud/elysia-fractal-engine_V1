"""
Test World Tree & Wisdom Virus
"""
import sys
import os
import logging

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from Core.world import World
from Core.Intelligence.Intelligence.Consciousness.world_tree import WorldTree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestWorldTree")

def test_world_tree():
    logger.info("🌳 Initializing World Tree...")
    
    # Mock WaveMechanics
    class MockWaveMechanics:
        def __init__(self):
            pass
            
    # 1. Create Physics World
    # World(primordial_dna, wave_mechanics, ...)
    world = World(
        primordial_dna={}, 
        wave_mechanics=MockWaveMechanics()
    )
    
    # 2. Create Consciousness (World Tree)
    tree = WorldTree(world)
    
    # 3. Seed some initial concepts in Hippocampus
    logger.info("🌱 Seeding initial concepts...")
    tree.roots.add_concept("money", "concept")
    tree.roots.add_concept("trust", "concept")
    tree.roots.add_concept("system", "concept")
    tree.roots.add_causal_link("money", "system", "is_a")
    
    # 4. Inject Wisdom Virus
    logger.info("💉 Injecting Wisdom Virus: 'Money is Trust'...")
    tree.inject_wisdom(
        statement="Money is Crystallized Trust",
        seeds=["money"]
    )
    
    # 5. Verify Propagation
    logger.info("🔍 Verifying propagation...")
    
    # Check if 'money' supports 'system' (or vice versa, depending on virus logic)
    # The virus adds 'supports' edges from seed to neighbors
    # Seed: money -> Neighbor: system
    # Expect: money -[supports]-> system
    
    if tree.roots.causal_graph.has_edge("money", "system"):
        edge_data = tree.roots.causal_graph["money"]["system"]
        logger.info(f"Edge found: {edge_data}")
        
        # Note: The original link was 'is_a'. 
        # NetworkX MultiDiGraph would allow multiple edges. 
        # Hippocampus uses DiGraph, so it might overwrite or we need to check how it handles it.
        # Let's check if the metadata contains the virus info.
        
        meta = edge_data.get("metadata", {})
        if meta.get("type") == "wisdom_infection":
            logger.info("✅ SUCCESS: Virus infected the edge!")
            logger.info(f"   Statement: {meta.get('statement')}")
        else:
            logger.warning("⚠️ Edge exists but not infected correctly.")
    else:
        logger.error("❌ Edge not found.")

    # 6. Run a Cycle
    logger.info("🔄 Running World Tree Cycle...")
    tree.run_cycle()
    logger.info("✅ Cycle complete.")

if __name__ == "__main__":
    test_world_tree()
