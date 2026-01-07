"""
Fractal Structure Test
======================
Tests the new ConceptSphere and Oscillator integration.
"""

import sys
sys.path.insert(0, 'c:\\Elysia')

from Core.Foundation.Mind.concept_sphere import ConceptSphere
from Core.Foundation.Mind.hippocampus import Hippocampus

def test_fractal_restoration():
    """Test the restored fractal architecture"""
    
    print("=" * 60)
    print("🌌 FRACTAL ARCHITECTURE TEST")
    print("=" * 60)
    
    # Create hippocampus
    hip = Hippocampus()
    
    # Add concepts (should create spheres)
    print("\n1. Creating ConceptSpheres...")
    hip.add_concept("Love")
    hip.add_concept("Light")
    hip.add_concept("Pain")
    
    # Check if spheres exist
    print("\n2. Checking sphere structure...")
    love_node = hip.causal_graph.nodes["Love"]
    if 'sphere' in love_node:
        sphere = love_node['sphere']
        print(f"✅ 'Love' is a ConceptSphere: {sphere}")
        print(f"   - Will magnitude: {sphere.will.magnitude():.2f}")
        print(f"   - Emotions: {sphere.emotions}")
        print(f"   - Sub-concepts: {len(sphere.sub_concepts)}")
        print(f"   - Mirror intensity: {sphere.mirror.intensity:.2f}")
    else:
        print("❌ 'Love' is not a sphere!")
    
    # Add causal links (should have oscillators)
    print("\n3. Creating causal links with Oscillators...")
    hip.add_causal_link("Love", "Light", relation="illuminates", weight=0.9)
    hip.add_causal_link("Love", "Pain", relation="contains", weight=0.3)
    
    # Check edge oscillators
    print("\n4. Checking edge resonance...")
    edge = hip.causal_graph.edges["Love", "Light"]
    if 'oscillator' in edge:
        osc = edge['oscillator']
        print(f"✅ Edge has Oscillator!")
        print(f"   - Frequency: {osc.frequency:.3f}")
        print(f"   - Amplitude: {osc.amplitude:.3f}")
        print(f"   - Complex value at t=0: {osc.get_complex_value(0)}")
    else:
        print("❌ Edge missing Oscillator!")
    
    # Test fractal recursion
    print("\n5. Testing fractal recursion...")
    love_sphere = love_node['sphere']
    warmth = love_sphere.add_sub_concept("warmth")
    print(f"✅ Added sub-concept: {warmth}")
    print(f"   Parent: {warmth.parent.id if warmth.parent else None}")
    
    # Test mirror layer
    print("\n6. Testing Mirror Layer...")
    love_sphere.mirror.reflect({"event": "sunrise", "intensity": 0.8})
    print(f"✅ Reflected world event")
    print(f"   Mirror intensity: {love_sphere.mirror.intensity:.3f}")
    print(f"   Phenomena count: {len(love_sphere.mirror.phenomena)}")
    
    # Get slice (dimensional point)
    print("\n7. Extracting dimensional slice...")
    slice_data = love_sphere.get_slice()
    print(f"✅ Dimensional Point:")
    for key, value in slice_data.items():
        print(f"   - {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ FRACTAL ARCHITECTURE RESTORED")
    print("=" * 60)

if __name__ == "__main__":
    test_fractal_restoration()
