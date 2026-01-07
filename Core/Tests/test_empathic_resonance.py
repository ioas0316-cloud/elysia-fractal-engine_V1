import sys
import os
import unittest

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Sensory.Auditory.tone_analyzer import ToneAnalyzer

class TestEmpathicResonance(unittest.TestCase):
    def setUp(self):
        self.ear = ToneAnalyzer()
        print("\n--- 🎻 Empathic Resonance Test Setup ---")

    def test_emotional_hearing(self):
        """
        Verify that the Ear can hear the 'Tone' behind the words.
        """
        scenarios = [
            ("Logic Mode", "Can you explain the logic behind this?", 432.0),
            ("Love Mode", "I love this result so much.", 528.0),
            ("Awakening Mode", "Wow, this is a miracle!", 963.0),
            ("Fear Mode", "I am scared, please help me.", 396.0),
            ("Neutral Mode", "Just a random sentence.", 432.0) # Should default to 432
        ]
        
        print("\n[Step 1] Listening to User Voice...")
        for name, text, expected_freq in scenarios:
            freq = self.ear.analyze_tone(text)
            desc = self.ear.get_tone_description(freq)
            print(f"🎤 Input: '{text}'")
            print(f"   → Detected: {freq}Hz [{desc}]")
            
            # Allow some tolerance if algorithms change, but here direct mapping
            self.assertEqual(freq, expected_freq, f"Failed on {name}")
            print("   ✅ Resonance Confirmed\n")

if __name__ == '__main__':
    unittest.main()
