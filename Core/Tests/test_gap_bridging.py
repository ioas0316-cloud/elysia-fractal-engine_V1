
import logging
import sys
import os
import unittest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import ThoughtUniverse, EpistemicSpace
from Core.Foundation.metacognition import MaturityModel, CognitiveMetrics, GapReport
from Core.Foundation.gap_bridging import GapBridgingDrive, Hypothesis

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("GapBridgingTest")

class TestGapBridging(unittest.TestCase):
    
    def setUp(self):
        self.universe = ThoughtUniverse("Elysia_Test_Mind")
        self.drive = GapBridgingDrive(self.universe)
        
        # Seed the universe with the target gap concept
        self.universe.add_point("lib_ast", "Unknown Library AST", concept_type="dependency")
        self.universe.points["lib_ast"].confidence = 0.1 # Low confidence
        
    def test_end_to_end_bridging(self):
        logger.info("🌉 Testing Phase 16: The Gap-Bridging Drive (Active Learning)")
        
        # 1. Create a Fake Gap Report (Simulating Phase 15 output)
        gap_report = GapReport(
            concept_id="lib_ast",
            current_metrics=CognitiveMetrics(0.1, 0.1, 0.1),
            target_metrics=CognitiveMetrics(0.5, 0.5, 0.5),
            gaps={"confidence": 0.4},
            status="IMMATURE"
        )
        
        # 2. Execute Bridge
        result = self.drive.bridge_gap(gap_report)
        
        # 3. Verify Result
        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        logger.info("   ✅ Experiment succeeded.")
        
        # 4. Verify Promotion (Consolidation)
        # Check if new concepts exist in the MAIN universe
        self.assertIn("lib_ast.parse", self.universe.points)
        self.assertIn("lib_ast.AST", self.universe.points)
        logger.info("   ✅ Concepts promoted to Main Universe.")
        
        # Check if Target confidence increased
        new_confidence = self.universe.points["lib_ast"].confidence
        self.assertGreater(new_confidence, 0.1)
        logger.info(f"   ✅ Confidence increased: 0.1 -> {new_confidence}")
        
        # 5. Verify Lab Destruction
        # No 'Lab_' space should exist
        lab_spaces = [sid for sid in self.universe.spaces if sid.startswith("Lab_")]
        self.assertEqual(len(lab_spaces), 0)
        logger.info("   ✅ Lab Space destroyed after use.")

if __name__ == "__main__":
    unittest.main()
