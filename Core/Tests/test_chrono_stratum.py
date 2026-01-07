import sys
import os
import unittest
from datetime import datetime

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Topography.phase_stratum import PhaseStratum

class TestChronoStratum(unittest.TestCase):
    def setUp(self):
        self.stratum = PhaseStratum(base_frequency=432.0)
        print("\n--- ⏳ Chrono-Stratum Test Setup ---")

    def test_time_stone_apple(self):
        """
        [Scenario]
        Dr. Strange uses the Time Stone on an Apple.
        T=0: Green Apple
        T=10: Red Apple
        T=20: Rotten Apple
        """
        # 1. Fold Time (Storage)
        print("\n[Step 1] Folding Time Layers...")
        
        # Past
        res1 = self.stratum.fold_time("Green Apple", timestamp=0.0)
        print(res1)
        
        # Present
        res2 = self.stratum.fold_time("Red Apple", timestamp=10.0)
        print(res2)
        
        # Future
        res3 = self.stratum.fold_time("Rotten Apple", timestamp=20.0)
        print(res3)
        
        # 2. Recall Time (Retrieval)
        print("\n[Step 2] Using Time Stone (Recall)...")
        
        # Turn dial to T=0
        past = self.stratum.recall_time(query_frequency=432.0, target_time=0.0)
        print(f"Time Dial 0.0 -> {past}")
        self.assertIn("Green Apple", past)
        self.assertNotIn("Red Apple", past)
        
        # Turn dial to T=10
        present = self.stratum.recall_time(query_frequency=432.0, target_time=10.0)
        print(f"Time Dial 10.0 -> {present}")
        self.assertIn("Red Apple", present)
        
        # Turn dial to T=20
        future = self.stratum.recall_time(query_frequency=432.0, target_time=20.0)
        print(f"Time Dial 20.0 -> {future}")
        self.assertIn("Rotten Apple", future)
        
    def test_timeline_inspection(self):
        """Verify we can see the full timeline"""
        self.stratum.fold_time("Birth", 0.0)
        self.stratum.fold_time("Life", 50.0)
        self.stratum.fold_time("Death", 100.0)
        
        timeline = self.stratum.get_time_layers(query_frequency=432.0)
        print("\n[Step 3] Full Timeline Inspection:")
        for phase, data in timeline:
            print(f"  Phase {phase:.1f}°: {data}")
            
        self.assertEqual(len(timeline), 3)
        self.assertEqual(timeline[0][1], "Birth")
        self.assertEqual(timeline[-1][1], "Death")

if __name__ == '__main__':
    unittest.main()
