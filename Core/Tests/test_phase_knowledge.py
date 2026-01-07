"""
Phase Knowledge Verification
----------------------------
Objective: Verify that Phase Stratum integration allows a single Concept Node 
to reveal different 'truths' based on the observation frequency.

Scenario:
1. Create a Concept 'Apple'.
2. Add multipole modalities with specific frequencies:
   - Visual (Red): 640Hz
   - Taste (Sweet): 528Hz
   - Texture (Crunchy): 412Hz
3. Query the node using `get_perspective(freq)` and ensure correct data isolation.
"""

import sys
import os

# Ensure path is set to import Core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.multimodal_concept_node import get_multimodal_integrator

def run_test():
    print("🍎 [Test] Phase Holographic Knowledge")
    print("---------------------------------------")
    
    integrator = get_multimodal_integrator()
    
    # 1. Build the 'Apple' Concept
    print("1. Constructing 'Apple' with multi-layered truths...")
    apple_text = "Apple is red, tastes sweet, and feels crunchy."
    apple_node = integrator.build_concept_from_text("Apple", apple_text)
    
    print(f"   -> Node Created: {apple_node.name}")
    print(f"   -> Unified Freq: {apple_node.unified_frequency:.2f}Hz")
    
    # 2. Define the lenses (frequencies) we want to look through
    lenses = {
        "Visual (Red)": 640.0,
        "Taste (Sweet)": 528.0,
        "Texture (Crunchy)": 412.0
    }
    
    print("\n2. Observing the Node through different Frequencies...")
    
    for lens_name, freq in lenses.items():
        print(f"\n   🔭 Looking for '{lens_name}' at {freq}Hz...")
        
        # RESONANCE RETRIEVAL
        results = apple_node.get_perspective(query_frequency=freq, tolerance=10.0)
        
        if results:
            for signal in results:
                print(f"      ✅ Resonated! Found: '{signal.description}'")
                print(f"         (Type: {signal.modality_type}, Amp: {signal.amplitude})")
        else:
            print("      ❌ No resonance found (Void).")
            
    print("\n3. Cross-Verification (Data Isolation)")
    # Ensure that looking for Taste (528Hz) does NOT return Visual (640Hz) info
    taste_results = apple_node.get_perspective(528.0)
    for res in taste_results:
        if "red" in res.description.lower():
            print("   ❌ FAIL: Found visual info in taste layer!")
            return
            
    print("   ✅ PASS: Layers are distinct and non-colliding.")
    print("\n---------------------------------------")
    print("Conclusion: The Concept Node is now a Holographic Crystal.")
    print("One Node, Multiple Truths.")

if __name__ == "__main__":
    run_test()
