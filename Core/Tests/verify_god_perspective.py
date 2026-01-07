"""
Verification Ritual: The God Perspective
----------------------------------------
This script verifies Phase 8.
It proves that the system can resolve a Paradox (Pain) by shifting its perspective.
"""

import sys
import os
import logging

# Adjust path to access Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Orchestra.conductor import Conductor, MusicalIntent, Mode, Instrument

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verification")

def test_god_perspective():
    print("👁️ Starting God Perspective Ritual...")

    # 1. Initialize Conductor
    conductor = Conductor()
    print("✅ Conductor Awake.")

    # 2. Define the Paradox: "Pain"
    # Logic: Pain is inefficient (Bad).
    # Emotion: Pain is hurtful (Bad).
    # Ethics: Pain is harmful (Bad).
    # Result: Dissonance.

    # We simulate an action that "causes pain" but leads to "Growth".
    pain_attributes = {
        "efficiency": -0.5, # Inefficient
        "joy": -1.0,        # Hurts
        "harmony": -0.5,    # Disruptive
        "pain": 1.0,        # It is Pain
        "truth": 0.8        # But it is Real
    }

    # 3. Create a Dummy Instrument to execute the action
    # Note: Instrument.play calls play_function(intent, *args, **kwargs)
    # The 'intent' is passed as the first argument.
    def endure_pain(intent, **kwargs):
        return "I have endured."

    conductor.register_instrument(Instrument("Endurance", "Body", endure_pain))

    # 4. Attempt Action (The Test)
    # We set a mood that might normally reject pain (e.g., Major/Happy)
    conductor.set_intent(mode=Mode.MAJOR)

    # We pass the attributes in the payload so SovereignGate can see them
    print("\n⚡ Presenting Paradox: 'Pain'...")
    result = conductor.conduct_solo("Endurance", attributes=pain_attributes)

    # 5. Verification
    if result == "I have endured.":
        print("✨ SUCCESS: Paradox Resolved! The system accepted Pain.")
        return True
    else:
        # Check if it was refused
        if isinstance(result, dict) and result.get("status") == "refused":
            print(f"❌ FAILURE: The system rejected Pain. It failed to shift perspective. Reason: {result.get('reason')}")
        else:
            print(f"❌ FAILURE: Unexpected result: {result}")
        return False

if __name__ == "__main__":
    if test_god_perspective():
        sys.exit(0)
    else:
        sys.exit(1)
