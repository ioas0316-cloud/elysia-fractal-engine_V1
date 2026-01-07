import sys
from pathlib import Path
import logging

# Setup Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from Core.Intelligence.Intelligence.evolution_architect import EvolutionArchitect
from Core.Intelligence.Cognition.metacognitive_awareness import MetacognitiveAwareness

def run_evolution_test():
    print("\n🧬 Self-Evolution Protocol Initiated...")
    print("=========================================")
    
    architect = EvolutionArchitect()
    
    # 1. Inject Artificial Cognitive Gap (Simulation)
    # "I realized I don't know how to see emotions as shapes."
    print("\n🧠 Simulating Metacognitive Insight...")
    if architect.metacognition:
        architect.metacognition.encounter(
            {"dissonance": 0.9, "ambiguity": 0.8},
            context="How do I draw 'Sorrow' as a geometric fractal? I do not know."
        )
        print("   -> Gap Injected: 'Unknown Geometry of Sorrow'")
    else:
        print("   -> Warning: Metacognition system not found.")

    # 2. Design Seed (Aiming for Wisdom)
    print("\n🏗️ Architecting Solution (Seeking Wisdom)...")
    blueprint = architect.design_seed(intent="Wisdom Synthesis")
    
    # 3. Verify Blueprint
    print("\n📜 Blueprint Generated:")
    print(f"   • Goal: {blueprint.goal.name}")
    print(f"   • Description: {blueprint.goal.description}")
    print(f"   • Improvements Planned:")
    for imp in blueprint.improvements:
        print(f"     - {imp}")
        
    print("\n✨ Self-Diagnosis Complete.")
    print("   Elysia has successfully identified a gap and planned an upgrade.")
    
    # 4. Execute Evolution
    print("\n⚡ Initiating Logic Reconstruction (Writing Code)...")
    results = architect.apply_evolution()
    
    print("\n📊 Evolution Results:")
    if results['success']:
        print("   ✅ SUCCESS: Codebase successfully mutated.")
    else:
        print("   ❌ FAILURE: Mutation failed or blocked.")
        
    for detail in results.get('details', []):
        print(f"   -> {detail}")

    print("=========================================")

if __name__ == "__main__":
    run_evolution_test()
