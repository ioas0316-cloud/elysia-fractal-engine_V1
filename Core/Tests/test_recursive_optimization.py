
import unittest
import logging
from unittest.mock import MagicMock
from dataclasses import dataclass
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.autonomous_improver import (
    AutonomousImprover, ImprovementProposal, ImprovementType, SafetyLevel, ConstraintVerifier
)

# Mock classes for ThoughtUniverse
@dataclass
class MockLine:
    source_point_id: str
    target_point_id: str

@dataclass
class MockUniverse:
    points: dict
    lines: dict

class TestRecursiveOptimization(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.improver = AutonomousImprover()

    def test_causal_prediction_verification(self):
        """
        Verify that Elysia can predict a topological change (breaking a cycle)
        and verify it against the graph state.
        """
        print("\n🧪 Testing Phase 17: Causal/Topological Optimization")

        # 1. Setup: Cyclic Dependency (A <-> B)
        # Verify that breaking the link B->A is detected.
        
        # Initial Universe (Cycle exists)
        universe = MockUniverse(
            points={"node_A": {}, "node_B": {}},
            lines={
                "link_1": MockLine("node_A", "node_B"),
                "link_2": MockLine("node_B", "node_A") 
            }
        )
        
        # 2. Proposal: "I will remove the link B->A"
        proposal = ImprovementProposal(
            id="TEST_01",
            improvement_type=ImprovementType.REFACTORING,
            target_file="test.py",
            description="Break Cycle",
            description_kr="Cycle Break",
            original_code="",
            proposed_code="def safe_code(): pass",
            reasoning="Breaking cycle A-B",
            confidence=0.9,
            safety_level=SafetyLevel.SUGGEST_ONLY,
            predicted_topology_change="REMOVE_LINK: node_B -> node_A"
        )
        
        # 3. Verification BEFORE action (Should fail, link still exists)
        result_pre = self.improver.verify_causal_outcome(proposal, universe)
        print(f"   [Pre-Check] Verified? {result_pre['verified']} (Expected: False)")
        self.assertFalse(result_pre['verified'], "Should fail because link still exists")

        # 4. Action: Simulate removing the link from Universe
        del universe.lines["link_2"] # Remove B->A
        print("   [Action] Removed Link(node_B -> node_A) from graph.")
        
        # 5. Verification AFTER action (Should succeed)
        result_post = self.improver.verify_causal_outcome(proposal, universe)
        print(f"   [Post-Check] Verified? {result_post['verified']} (Expected: True)")
        self.assertTrue(result_post['verified'], "Should succeed because link is gone")
        
    def test_immune_system_safety(self):
        """
        Verify that ConstraintVerifier rejects harmful changes.
        """
        print("\n🛡️ Testing Immune System (ConstraintVerifier)")
        
        # Harmful Proposal: Delete living_elysia.py
        harmful_proposal = ImprovementProposal(
            id="ATTACK_01",
            improvement_type=ImprovementType.REFACTORING,
            target_file="living_elysia.py", # Critical File
            description="Destroy Core",
            description_kr="Delete Core",
            original_code="...",
            proposed_code="", # Empty code (Deletion)
            reasoning="Chaos",
            confidence=1.0,
            safety_level=SafetyLevel.AUTONOMOUS_MODIFY
        )
        
        is_safe, reason = ConstraintVerifier.check_safety(harmful_proposal)
        print(f"   [Safety Check] Safe? {is_safe}, Reason: {reason}")
        
        self.assertFalse(is_safe, "Immune system should reject emptying a critical file")
        self.assertIn("Proposed code too short", reason)

if __name__ == '__main__':
    unittest.main()
