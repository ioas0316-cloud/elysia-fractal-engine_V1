
import sys
import os
import logging
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Intelligence.Cognition.predictive_mind import PredictiveMind
from Core.Foundation.causal_narrative_engine import CausalNarrativeEngine, CausalChain, CausalLink, CausalRelationType

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AdvancedNarrativeTest")

def verify_advanced_narrative():
    print("="*60)
    print("📖 Advanced Causal Narrative Verification")
    print("   Complex Chains & Narrative Synthesis")
    print("="*60)
    
    # 1. Initialize
    mind = PredictiveMind()
    engine = mind.narrative_engine
    
    # 2. Simulate a Complex Chain (Seed -> Sprout -> Tree -> Fruit)
    print("\n1. Constructing Causal Chain: Seed -> Fruit")
    
    chain = CausalChain(id="chain_growth", node_sequence=["Seed", "Sprout", "Tree", "Fruit"])
    chain.links = [
        CausalLink("Seed", "Sprout", CausalRelationType.CAUSES),
        CausalLink("Sprout", "Tree", CausalRelationType.ENABLES),
        CausalLink("Tree", "Fruit", CausalRelationType.CAUSES)
    ]
    
    # 3. Synthesize Narrative
    print("\n2. Synthesizing Narrative...")
    narrative = engine.synthesize_narrative(chain)
    print(f"   📝 Generated Narrative:\n   \"{narrative}\"")
    
    # 4. Formulate Complex Hypothesis
    print("\n3. Formulating Complex Hypothesis...")
    hyp = mind.formulate_complex_hypothesis("Seed", "Fruit", ["Sprout", "Tree"])
    
    print(f"   💭 Hypothesis Premise: {hyp.premise}")
    print(f"   💭 Hypothesis Prediction: {hyp.prediction}")
    
    # 5. Verify Complex Hypothesis against Narrative
    # Ideally, we verify against the generated narrative itself
    print("\n4. Verifying Complex Hypothesis...")
    
    # We verify if the prediction's key steps exist in the 'reality' (narrative)
    evidence = narrative
    result = mind.verify_hypothesis(hyp, evidence)
    print(f"   ✅ Verification Result: {result}")
    
    if result == "VERIFIED":
        print("   🎉 SUCCESS: Complex Chain was predicted, synthesized, and verified.")
    else:
        print("   ❌ FAILURE: Failed to verify complex chain.")

    # 6. Goal-Directed Pathfinding
    from Core.Foundation.self_governance import SelfGovernance
    print("\n5. Testing Goal-Directed Pathfinding...")
    gov = SelfGovernance()
    goal = "I want to harvest Fruit"
    current = "I only have a Seed"
    
    path = gov.find_path_to_goal("Fruit", "Seed")
    print(f"   My Goal: {goal}")
    print(f"   Current: {current}")
    print(f"   Found Path: {path}")
    
    if "Grow Tree" in path:
        print("   ✅ SUCCESS: Pathfinding identified necessary intermediate steps.")
    else:
        print("   ❌ FAILURE: Pathfinding failed.")

if __name__ == "__main__":
    verify_advanced_narrative()
