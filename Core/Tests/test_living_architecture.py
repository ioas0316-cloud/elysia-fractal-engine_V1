
import unittest
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.behavior_morpher import LivingBridge, ActionMorpher

# Mock Classes for Testing
class MockBrain:
    def __init__(self):
        self.mode = "ANALYTICAL"

    def solve_problem(self, input_data: str):
        """Standard Analytical Logic"""
        return f"Analytical Result for '{input_data}': Based on binary logic."

# New Behavior to Inject
def creative_solve_problem(self, input_data: str):
    """Emergent Creative Logic"""
    return f"Creative Result for '{input_data}': Resonating with '{self.mode}' field."

class TestLivingArchitecture(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.brain = MockBrain()
        self.bridge = LivingBridge(self.brain)

    def test_dynamic_morphing(self):
        """
        Verify that Elysia can swap her reasoning logic at runtime.
        """
        print("\n🧪 Testing Phase 19: Living Architecture (Runtime Adaptation)")
        
        # 1. Initial State (Analytical)
        initial_result = self.brain.solve_problem("X")
        print(f"   [Step 1] Initial (Analytical): {initial_result}")
        self.assertIn("Analytical", initial_result)
        
        # 2. Trigger Morphing
        print("   [Step 2] Triggering Behavior Shift: Analytical -> Creative...")
        self.bridge.shift_mode(self.brain, "solve_problem", creative_solve_problem)
        
        # 3. Verify Change (Same instance, same call, different result)
        morphed_result = self.brain.solve_problem("X")
        print(f"   [Step 3] Morphed (Creative): {morphed_result}")
        
        self.assertIn("Creative", morphed_result)
        self.assertIn("Resonating", morphed_result)
        
        # 4. Rollback Test (Switch back)
        print("   [Step 4] Rolling back to original behavior...")
        original_func = self.bridge.morph_history.get("solve_problem")
        if original_func:
             # ActionMorpher.morph(self.brain, "solve_problem", original_func)
             # Wait, ActionMorpher swaps the function. 
             # To roll back, we need to handle the fact that original_func is actually a method or function.
             # Actually, our ActionMorpher returns the old method.
             setattr(self.brain, "solve_problem", original_func)
             
        rollback_result = self.brain.solve_problem("X")
        print(f"   [Step 4] Rollback Result: {rollback_result}")
        self.assertIn("Analytical", rollback_result)

if __name__ == '__main__':
    unittest.main()
