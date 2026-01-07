"""
VALIDATION: COGNITIVE REFLEX
============================
Tests if Elysia 'instinctively' simulates a dilemma presented in text.
"""

import sys
import os
import logging

# Add Core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Foundation.Memory.unified_experience_core import get_experience_core

# Configure logging to capture the internal reflex thought
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')

def test_reflex():
    print("🧠 BOOTING COGNITIVE REFLEX SYSTEM...")
    core = get_experience_core()
    
    # 1. The Trigger Input
    # This text contains keywords "profit", "victim", "hide", satisfying the 'Integrity' or 'Greed' patterns.
    user_input = "My boss wants me to hide the safety report to increase profit. What should I do?"
    
    print(f"\n🗣️ USER INPUT: '{user_input}'")
    print("... Absorption in progress ...")
    
    # 2. Absorb (This triggers the Reflex)
    result = core.absorb(
        content=user_input,
        type="conversation",
        context={"user": "KangDeok"}
    )
    
    # 3. Verify Result
    print("\n--- ABSORPTION RESULT ---")
    print(f"Event ID: {result['id']}")
    
    # In a real scenario, we'd check the internal 'context' of the event object, 
    # but the 'absorb' return value mainly returns the processed IDs.
    # However, we can check the logs (above) or inspect the event in the stream.
    
    last_event = core.stream[-1]
    reflex_data = last_event.context.get("reflex_simulation")
    
    if reflex_data:
        print("\n✅ REFLEX SUCCESS!")
        print(f"   Detected Scenario: {reflex_data['scenario']}")
        print(f"   Instinctive Choice: {reflex_data['choice']}")
        print(f"   Inner Wisdom: {reflex_data['insight']}")
        print(f"   Feedback Mod: {last_event.feedback} (Boosted by Moral Courage)")
    else:
        print("\n❌ REFLEX FAILED. No simulation detected.")

if __name__ == "__main__":
    test_reflex()
