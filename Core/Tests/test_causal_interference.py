import sys
import os
import unittest

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Creation.interference_engine import InterferenceEngine

class TestCausalInterference(unittest.TestCase):
    def setUp(self):
        self.engine = InterferenceEngine()
        print("\n--- 🌌 Creative Interference Test Setup ---")

    def test_reality_vs_fantasy(self):
        """
        [Scenario]
        Fire (700Hz) meets Water (400Hz).
        What happens? It depends on the DOMAIN.
        """
        freq_fire = 700.0
        freq_water = 400.0
        
        # 1. Physics Domain (Reality)
        print("\n[Case 1] Collision in REALITY (Physics Law)")
        outcomes_phys = self.engine.spark_creation(
            "Fire", freq_fire, "Water", freq_water, domain_filter="PHYSICS"
        )
        for res in outcomes_phys:
            print(f"👉 Result: {res['result']} ({res['frequency']}Hz)")
            print(f"   Principle: {res['principle_used']}")
            
        self.assertEqual(len(outcomes_phys), 1)
        self.assertEqual(outcomes_phys[0]['result'], "Steam")
        
        # 2. Fantasy Domain (Imagination)
        print("\n[Case 2] Collision in FANTASY (Magic Rule)")
        outcomes_magic = self.engine.spark_creation(
            "Fire", freq_fire, "Water", freq_water, domain_filter="FANTASY"
        )
        for res in outcomes_magic:
            print(f"👉 Result: {res['result']} ({res['frequency']}Hz)")
            print(f"   Principle: {res['principle_used']}")

        self.assertEqual(len(outcomes_magic), 1)
        self.assertEqual(outcomes_magic[0]['result'], "Oblivion Spell")
        self.assertEqual(outcomes_magic[0]['frequency'], 0.0) # Annihilation
        
    def test_chaos_collision(self):
        """
        [Scenario]
        Fire meets Stone. Assuming we haven't taught it 'Lava' principle yet.
        Should result in noise.
        """
        print("\n[Case 3] Collision without Principle")
        outcomes = self.engine.spark_creation("Fire", 700.0, "Stone", 800.0)
        
        print(f"👉 Result: {outcomes[0]['result']}")
        self.assertEqual(outcomes[0]['result'], "Chaos")

if __name__ == '__main__':
    unittest.main()
