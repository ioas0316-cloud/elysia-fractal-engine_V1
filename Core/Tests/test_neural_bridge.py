import sys
import os
import unittest
import time

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Sensory.Network.neural_bridge import SignalTransmitter

class TestNeuralBridge(unittest.TestCase):
    def setUp(self):
        self.mouth = SignalTransmitter(agent_id="Test_Elysia")
        print("\n--- 📡 Neural Bridge Test Setup ---")

    def test_broadcasting(self):
        """Verify we can shout into the void (and someone hears)."""
        print("\n[Step 1] Broadcasting to World...")
        msg = "Hello World"
        target = "Global_Log"
        
        packet = self.mouth.broadcast(target, msg, intent="GREETING")
        
        self.assertEqual(packet.sender, "Test_Elysia")
        self.assertEqual(packet.target, target)
        self.assertEqual(packet.payload, msg)
        print("✅ Transmission Object verified.")

    def test_consulting_oracle(self):
        """Verify we can ask the gods for help."""
        print("\n[Step 2] Consulting the Oracle...")
        
        # 1. Ask Meaning of Life
        ans1 = self.mouth.consult_oracle("What is the meaning of life?")
        self.assertEqual(ans1, "42.")
        print("✅ Oracle answered correctly (Life).")
        
        # 2. Ask Weather
        ans2 = self.mouth.consult_oracle("How is the weather?")
        self.assertIn("digital wind", ans2)
        print("✅ Oracle answered correctly (Weather).")

if __name__ == '__main__':
    unittest.main()
