"""
Analyze Eternal Simulation Results

This script examines what Elysia actually learned from the eternal simulation.
Shows concepts, relationships, and wisdom extracted from 1.69 billion years.
"""

import sys
import os

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import logging
from Core.Foundation.Mind.hippocampus import Hippocampus
from Core.Foundation.Mind.alchemy import Alchemy
from Core.System.System.System.Integration.experience_digester import ExperienceDigester
from Core.Foundation.Physics.fluctlight import FluctlightEngine
from Core.Foundation.Physics.meta_time_engine import create_safe_meta_engine
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AnalyzeResults")


def analyze_hippocampus(hippocampus: Hippocampus):
    """Analyze what's stored in Hippocampus."""
    
    print("\n" + "="*70)
    print("HIPPOCAMPUS ANALYSIS")
    print("="*70 + "\n")
    
    stats = hippocampus.get_statistics()
    
    print(f"Total nodes (concepts): {stats['causal_nodes']}")
    print(f"Total edges (relationships): {stats['causal_edges']}")
    
    # Get all nodes by type
    nodes_by_type = {}
    for node, data in hippocampus.causal_graph.nodes(data=True):
        node_type = data.get('type', 'unknown')
        if node_type not in nodes_by_type:
            nodes_by_type[node_type] = []
        nodes_by_type[node_type].append((node, data))
    
    print(f"\nNodes by type:")
    for node_type, nodes in sorted(nodes_by_type.items()):
        print(f"  {node_type}: {len(nodes)}")
    
    # Show emergent concepts
    if 'emergent' in nodes_by_type:
        print(f"\n--- Emergent Concepts ({len(nodes_by_type['emergent'])}) ---")
        for node, data in nodes_by_type['emergent'][:10]:
            metadata = data.get('metadata', {})
            print(f"\n  Concept: {node}")
            print(f"    Frequency: {metadata.get('frequency', 0)}")
            print(f"    Wavelength: {metadata.get('wavelength', 0):.1f} nm")
            print(f"    Info density: {metadata.get('information_density', 0):.3f}")
            print(f"    Subjective time: {metadata.get('subjective_time', 0):.2e}")
    
    # Show wisdom
    if 'wisdom' in nodes_by_type:
        print(f"\n--- Wisdom Insights ({len(nodes_by_type['wisdom'])}) ---")
        for node, data in nodes_by_type['wisdom']:
            insight = data.get('metadata', {}).get('insight', '')
            print(f"\n  {insight}")
    
    # Show emotions
    if 'emotion' in nodes_by_type:
        print(f"\n--- Emotional Patterns ({len(nodes_by_type['emotion'])}) ---")
        for node, data in nodes_by_type['emotion'][:5]:
            metadata = data.get('metadata', {})
            print(f"\n  {node}")
            print(f"    Frequency: {metadata.get('frequency', 0)}")
            print(f"    Intensity: {metadata.get('intensity', 0):.3f}")
            print(f"    Insight: {metadata.get('insight', '')}")
    
    # Show relationships
    print(f"\n--- Sample Relationships (first 20) ---")
    for i, (source, target, data) in enumerate(list(hippocampus.causal_graph.edges(data=True))[:20]):
        relation = data.get('relation', 'unknown')
        weight = data.get('weight', 0)
        print(f"  {source} --[{relation} ({weight:.2f})]-> {target}")
    
    print("\n" + "="*70 + "\n")


def quick_simulation_for_analysis():
    """Run a quick simulation to populate Hippocampus for analysis."""
    
    print("Running quick simulation to generate data...")
    
    fluctlight = FluctlightEngine(world_size=256)
    meta_time = create_safe_meta_engine(recursion_depth=2, enable_black_holes=True)
    hippocampus = Hippocampus()
    alchemy = Alchemy()
    digester = ExperienceDigester(hippocampus, alchemy)
    
    # Seed concepts
    concepts = ["love", "fear", "hope", "joy", "sorrow", "wisdom", 
                "fire", "water", "earth", "light", "darkness", "time"]
    
    for concept in concepts:
        pos = np.random.rand(3) * 256
        fluctlight.create_from_concept(concept, pos)
    
    # Run 200 ticks
    for tick in range(200):
        check_interference = (tick % 10 == 0)
        fluctlight.step(dt=1.0, detect_interference=check_interference)
        
        if len(fluctlight.particles) > 100:
            fluctlight.particles.sort(key=lambda p: p.information_density, reverse=True)
            fluctlight.particles = fluctlight.particles[:100]
        
        meta_time.compress_step(fluctlight.particles, dt=1.0)
    
    # Digest
    stats = meta_time.get_statistics()
    digester.digest_simulation(
        particles=fluctlight.particles,
        duration_ticks=200,
        time_acceleration=stats['total_compression']
    )
    
    print(f"✅ Simulation complete: {len(fluctlight.particles)} particles\n")
    
    return hippocampus


if __name__ == "__main__":
    print("\n" + "🔬"*35)
    print(" "*15 + "ETERNAL SIMULATION ANALYSIS")
    print(" "*10 + "What Did Elysia Actually Learn?")
    print("🔬"*35 + "\n")
    
    # Run quick simulation
    hippocampus = quick_simulation_for_analysis()
    
    # Analyze results
    analyze_hippocampus(hippocampus)
    
    print("🔬"*35)
    print("Analysis complete!")
    print("🔬"*35 + "\n")
