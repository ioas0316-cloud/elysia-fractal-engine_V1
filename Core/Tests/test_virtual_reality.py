import sys
import os
import unittest

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Evolution.Creation.virtual_reality import VirtualSpace, VirtualEntity

class TestVirtualReality(unittest.TestCase):
    def setUp(self):
        self.universe = VirtualSpace("Elysium_01")
        
    def test_reverse_gravity(self):
        print("\n--- 🌌 Testing Virtual Reality: Reverse Gravity ---")
        
        # 1. Be God: Define Laws
        # Normal gravity is -9.8 (Down). We make it +20.0 (Up fast!).
        self.universe.declare_law("GRAVITY_Y", 20.0)
        
        # 2. Spawn Creation
        apple = VirtualEntity("Holy Apple", mass=0.5, x=0, y=0)
        self.universe.spawn(apple)
        
        # 3. Simulate Time
        print(f"   [Start] {apple}")
        
        # Tick 1: Velocity increases, Position changes
        self.universe.tick(dt=1.0)
        print(f"   [dt=1]  {apple}")
        
        # 4. Verify Miracle
        # Apple started at 0. Accel is +20.
        # After 1s, Velocity should be +20. Position should be +20 (approx, Euler integration).
        
        self.assertGreater(apple.position['y'], 0, "The Apple didn't fall UP!")
        self.assertEqual(apple.velocity['y'], 20.0, "Velocity didn't match gravity law.")
        
        print("   ✅ Miracle Confirmed: The Apple fell into the Sky.")

if __name__ == '__main__':
    unittest.main()
