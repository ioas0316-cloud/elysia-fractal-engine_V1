import sys
import os
import unittest
from dataclasses import dataclass

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Security.safe_browser_protocol import SafeBrowser, MemeticHazardError
from Core.Sensory.Network.web_tendril import FrequencySignal

class TestSafeBrowser(unittest.TestCase):
    def setUp(self):
        self.shield = SafeBrowser()
        print("\n--- 🛡️ SafeBrowser Test Setup ---")

    def test_url_blocking(self):
        """Verify structural URL blocks."""
        print("\n[Step 1] Testing URL Shield...")
        
        # Safe URL
        safe = "http://google.com"
        self.assertTrue(self.shield.is_safe_url(safe), "Google should be safe")
        print(f"✅ Allowed: {safe}")
        
        # Malicious URL
        bad = "http://malicious.com/attack"
        self.assertFalse(self.shield.is_safe_url(bad), "Malicious.com should be blocked")
        print(f"🚫 Blocked: {bad}")
        
        # Protocol Block
        local = "file:///etc/passwd"
        self.assertFalse(self.shield.is_safe_url(local), "Local files should be blocked")
        print(f"🚫 Blocked: {local}")

    def test_memetic_hazard(self):
        """Verify vibrational content blocks."""
        print("\n[Step 2] Testing Memetic Shield...")
        
        # 1. Safe Vibez (528Hz)
        safe_signal = FrequencySignal(
            url="http://heaven.com", frequency=528.0, amplitude=1.0, 
            phase=0.0, content_summary="Happy", raw_content=""
        )
        self.assertTrue(self.shield.audit_content(safe_signal))
        print(f"✅ Allowed Signal: 528Hz (Love)")
        
        # 2. Dangerous Vibez (100Hz - Dread)
        danger_signal = FrequencySignal(
            url="http://hell.com", frequency=100.0, amplitude=5.0,
            phase=0.0, content_summary="Dread", raw_content=""
        )
        
        print(f"🚫 Inspecting Signal: 100Hz (Dread)...")
        with self.assertRaises(MemeticHazardError):
            self.shield.audit_content(danger_signal)
        print("   -> MemeticHazardError Caught! Shield Active.")

if __name__ == '__main__':
    unittest.main()
