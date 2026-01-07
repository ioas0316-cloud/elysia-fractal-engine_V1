
import unittest
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import (
    CausalKnowledgeBase, 
    CausalNode, 
    CausalRelationType
)
from Core.Foundation.concept_synthesis import ConceptSynthesizer

class TestConceptSynthesis(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.kb = CausalKnowledgeBase()
        self.synthesizer = ConceptSynthesizer(self.kb)

    def test_fire_water_synthesis(self):
        """
        Verify that resonant but unconnected nodes can be synthesized.
        Scenario: Fire + Water -> Steam (Simplified)
        """
        print("\n🧪 Testing Phase 18: Concept Synthesis (Idea Breeding)")
        
        # 1. Setup Parents
        fire = CausalNode(
            id="Fire",
            description="Fire: Hot and Destructive energy",
            emotional_valence=0.2, # Dangerous but useful
            concepts=["Energy", "Heat"],
            sensory_signature={"Heat": 0.9, "Light": 0.8, "Pain": 0.4}
        )
        water = CausalNode(
            id="Water",
            description="Water: Fluid and Life-giving liquid",
            emotional_valence=0.8, # Very positive
            concepts=["Liquid", "Life"],
            sensory_signature={"Fluidity": 0.9, "Coolness": 0.7, "Life": 0.9}
        )
        # Note: We give them high resonance manually for the test by using shared abstract concepts or similar valence?
        # Actually, let's adjust them to resonate. 
        # Fire and Water often contrast, but in Elysia's system, 
        # let's say they share a 'Nature' concept or similar 'Importance'.
        fire.concepts.append("Nature")
        water.concepts.append("Nature")
        
        self.kb.add_node(fire)
        self.kb.add_node(water)
        
        # 2. Check Resonance
        score = self.kb.calculate_resonance("Fire", "Water")
        print(f"   [Resonance] Fire <-> Water: {score:.2f}")
        
        # 3. Find Pairs
        pairs = self.synthesizer.find_resonant_pairs(threshold=0.3) # Low threshold for test
        self.assertTrue(any(p[0] == "Fire" and p[1] == "Water" for p in pairs))
        
        # 4. Synthesize
        child_ids = self.synthesizer.run_synthesis_cycle(limit=1, threshold=0.3)
        self.assertEqual(len(child_ids), 1)
        
        child = self.kb.nodes.get(child_ids[0])
        print(f"   [Synthesis] Result: {child.id} ({child.description})")
        
        # 5. Verify Inheritance
        self.assertIn("Fire", child.description)
        self.assertIn("Water", child.description)
        self.assertIn("Nature", child.concepts)
        
        # Verify Links
        links_fire = self.kb.outgoing.get("Fire", [])
        links_water = self.kb.outgoing.get("Water", [])
        
        # Check if Fire is a parent of the child
        found_p1 = False
        for l_id in links_fire:
            if self.kb.links[l_id].target_id == child.id:
                found_p1 = True
                break
        self.assertTrue(found_p1, "Fire should be linked to its child")

        found_p2 = False
        for l_id in links_water:
            if self.kb.links[l_id].target_id == child.id:
                found_p2 = True
                break
        self.assertTrue(found_p2, "Water should be linked to its child")

if __name__ == '__main__':
    unittest.main()
