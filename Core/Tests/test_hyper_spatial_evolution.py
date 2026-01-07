
import unittest
import logging
from dataclasses import dataclass
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.autonomous_improver import AutonomousImprover
from Core.Foundation.metacognition import ArchitecturalVision, StructuralTension, TopologyType

# Mock Classes
@dataclass
class MockLine:
    source_point_id: str
    target_point_id: str

@dataclass
class MockUniverse:
    lines: dict
    points: dict

class TestHyperSpatialEvolution(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.improver = AutonomousImprover()

    def test_vision_to_rewiring(self):
        """
        Verify the flow: Vision -> Tension -> Rewiring Proposal.
        Scenario: "Organ A" must connect to "Organ B".
        """
        print("\n🧪 Testing Phase 17.5: Hyper-Spatial Teleology")
        
        # 1. Define Reality (Disconnect)
        # Auth system exists, Database exists, but NO LINK.
        universe = MockUniverse(
            points={"Auth": {}, "Database": {}},
            lines={} 
        )
        
        # 2. Define Vision (The Blueprint)
        vision = ArchitecturalVision(
            scope_id="CoreSystem",
            topology_type=TopologyType.NEURAL,
            intended_connections=["Auth -> Database"],
            description="Auth must depend on Database"
        )
        
        # 3. Sense Tension
        print("   [Sensing] Checking for Structural Tension...")
        tensions = self.improver.sense_tension(universe, [vision])
        
        self.assertEqual(len(tensions), 1, "Should detect 1 missing link")
        tension = tensions[0]
        print(f"   [Detected] Tension: {tension.tension_type} ({tension.source_id} -> {tension.target_id})")
        
        self.assertEqual(tension.tension_type, "MISSING_LINK")
        self.assertEqual(tension.source_id, "Auth")
        self.assertEqual(tension.target_id, "Database")
        
        # 4. Propose Rewiring
        print("   [Healing] Proposing Rewiring Action...")
        proposal = self.improver.propose_rewiring(tension)
        
        self.assertIsNotNone(proposal)
        print(f"   [Proposal] {proposal.predicted_topology_change}")
        
        self.assertEqual(proposal.predicted_topology_change, "ADD_LINK: Auth -> Database")
        self.assertIn("Wire Auth to Database", proposal.description)

if __name__ == '__main__':
    unittest.main()
