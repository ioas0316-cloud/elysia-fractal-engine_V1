
import unittest
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import (
    CausalKnowledgeBase, 
    CausalNode, 
    CausalChain,
    CausalRelationType
)
from Core.Foundation.concept_synthesis import ConceptSynthesizer, PrincipleVerifier, EpistemicStatus

class TestPrincipleWorkability(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.kb = CausalKnowledgeBase()
        self.synthesizer = ConceptSynthesizer(self.kb)
        self.verifier = PrincipleVerifier(self.kb)

    def test_principle_grounding(self):
        """
        Verify that a synthesis is grounded by its internal principle working across phenomena.
        1. Fire + Water -> Steam (Hypothesis)
        2. Extract Principle: Thermal Expansion
        3. Test against Piston Engine phenomenon.
        """
        print("\n🧪 Testing Phase 18.5: Epistemic Grounding (Principle Workability)")
        
        # 1. Setup Initial Knowledge (Phenomenon A)
        fire = CausalNode(id="Fire", description="Fire: Extreme Heat source", emotional_valence=0.0)
        water = CausalNode(id="Water", description="Water: Liquid ready for Fluidity", emotional_valence=0.0)
        self.kb.add_node(fire)
        self.kb.add_node(water)
        
        # 2. Synthesize Steam
        child_ids = self.synthesizer.run_synthesis_cycle(threshold=0.3)
        steam_node = self.kb.nodes[child_ids[0]]
        print(f"   [Synthesis] Bred: {steam_node.id} - Status: {steam_node.epistemic_status}")
        self.assertEqual(steam_node.epistemic_status, EpistemicStatus.HYPOTHESIS.value)
        
        # 3. Setup Phenomenon B (Causal Chain of a Piston Engine)
        # This represents an 'unseen' phenomenon to test the principle.
        spark = CausalNode(id="Spark", description="Spark: Sudden Heat ignition", emotional_valence=0.0)
        piston = CausalNode(id="Piston", description="Piston: Moves by Motion/Expansion", emotional_valence=0.0)
        self.kb.add_node(spark)
        self.kb.add_node(piston)
        
        engine_chain = CausalChain(
            id="engine_chain",
            node_sequence=["Spark", "Piston"],
            links=[] # Simplified for test
        )
        
        # 4. Run Workability Verification
        print("   [Verifying] Testing internal principle across different phenomenon (Engine)...")
        is_workable = self.verifier.verify_workability(steam_node, [engine_chain])
        
        if is_workable:
            steam_node.epistemic_status = EpistemicStatus.TRUTH.value
            print(f"   [Success] Principle '{steam_node.internal_law}' is WORKABLE. Status -> TRUTH")
        else:
            steam_node.epistemic_status = EpistemicStatus.DELUSION.value
            print(f"   [Failure] Principle is NOT workable. Status -> DELUSION")

        # 5. Assertions
        self.assertTrue(is_workable)
        self.assertEqual(steam_node.epistemic_status, EpistemicStatus.TRUTH.value)
        self.assertEqual(steam_node.internal_law, "THERMAL_EXPANSION_EXPULSION")

    def test_delusion_rejection(self):
        """
        Verify that a random synthesis with no governing principle is rejected.
        """
        print("\n🧪 Testing Phase 18.5: Delusion Rejection")
        
        # Setup nonsensical nodes
        gravity = CausalNode(id="Gravity", description="Gravity pull", emotional_valence=0.0)
        sandwich = CausalNode(id="Sandwich", description="Food sandwich", emotional_valence=0.0)
        self.kb.add_node(gravity)
        self.kb.add_node(sandwich)
        
        # Manual Synthesis Simulation
        delusion_node = CausalNode(
            id="syn_gravity_sandwich",
            description="Synthesis of Gravity and Sandwich",
            epistemic_status=EpistemicStatus.HYPOTHESIS.value
        )
        self.kb.add_node(delusion_node)
        
        # Verify
        is_workable = self.verifier.verify_workability(delusion_node, [])
        self.assertFalse(is_workable)
        print(f"   [Rejection] Delusion '{delusion_node.description}' rejected (Status: {EpistemicStatus.DELUSION.value})")

if __name__ == '__main__':
    unittest.main()
