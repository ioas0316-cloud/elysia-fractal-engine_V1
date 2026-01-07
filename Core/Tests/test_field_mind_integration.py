
import sys
import os
import logging
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Intelligence.Cognition.predictive_mind import PredictiveMind
from Core.Intelligence.Cognition.Reasoning.causal_geometry import TensionField

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("FieldMindVerification")

def verify_field_mind_connection():
    print("="*60)
    print("🧩 Field-Mind Unification Verification")
    print("   Logic (PredictiveMind) <==> Physics (TensionField)")
    print("="*60)
    
    # 1. Initialize Systems
    field = TensionField()
    mind = PredictiveMind()
    
    # 2. Register Concept in Field
    concept = "Rain"
    field.register_concept(concept)
    initial_curvature = field.shapes[concept].curvature
    print(f"\n1. Initial State: '{concept}' Curvature = {initial_curvature:.4f}")
    
    # 3. Connect Systems
    mind.connect_field(field)
    print("\n2. Systems Connected.")
    
    # 4. Formulate & Verify Hypothesis (SUCCESS CASE)
    print("\n3. Testing SUCCESS Case...")
    hyp = mind.formulate_hypothesis(concept, ["Wet Ground"])
    
    evidence = "The Rain made the Wet Ground slippery."
    mind.verify_hypothesis(hyp, evidence)
    
    new_curvature = field.shapes[concept].curvature
    print(f"   Post-Verification Curvature: {new_curvature:.4f}")
    
    if new_curvature > initial_curvature:
        print("   ✅ SUCCESS: Logic validated -> Gravity Deepened (Belief Reinforced)")
    else:
        print("   ❌ FAILURE: Gravity did not increase.")
        
    # 5. Formulate & Verify Hypothesis (FAILURE CASE)
    print("\n4. Testing FAILURE Case...")
    hyp_fail = mind.formulate_hypothesis(concept, ["Fire"]) # Rain -> Fire (Unlikely)
    
    evidence_fail = "The Rain put out the fire." # Evidence contradicts or doesn't match
    # Note: Our simple verification checks if "Fire" is in evidence.
    # If "Fire" IS in evidence, it verifies. So we need evidence WITHOUT "Fire".
    evidence_fail = "Water is falling from the sky."
    
    mind.verify_hypothesis(hyp_fail, evidence_fail)
    
    final_curvature = field.shapes[concept].curvature
    print(f"   Post-failure Curvature: {final_curvature:.4f}")
    
    if final_curvature < new_curvature:
        print("   ✅ SUCCESS: Logic falsified -> Gravity Flattened (Entropy Injected)")
    else:
        print("   ❌ FAILURE: Gravity did not decrease.")

if __name__ == "__main__":
    verify_field_mind_connection()
