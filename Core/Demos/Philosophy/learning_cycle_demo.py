"""
Demo: The Human-like Learning Cycle (The Loop of Reflection)
============================================================

"We do not learn from experience. We learn from reflecting on experience."

This script is a 'Textbook' for Elysia. It demonstrates how she converts
a "Failure" (Action) into a "Principle" (Wisdom) using the WisdomStore.
"""

import sys
import os
import logging
import time

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from Core.Intelligence.Wisdom.wisdom_store import WisdomStore
from Core.Foundation.chronos import Chronos
from Core.Foundation.Wave.resonance_field import ResonanceField

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("LearningDemo")

def main():
    print("🧪 Demo: Human-like Learning Cycle\n")

    # 1. Initialize Soul
    # We use a temporary path for the demo to not affect the real soul yet
    wisdom = WisdomStore(filepath="logs/demo_wisdom.json")

    print(f"   [State] Initial Wisdom: {len(wisdom.principles)} principles.")
    print(f"   [State] Current Values: {wisdom.values}")

    # 2. The Experience (Action -> Failure)
    print("\n🎬 ACT 1: The Mistake")
    print("   Elysia attempts to 'Connect to User' with High Speed (Tempo.PRESTO).")

    action_intent = {"speed": 100, "empathy": 10}
    user_state = {"receptivity": 20} # User is tired, needs empathy not speed

    print("   ... Interaction occurring ...")
    time.sleep(0.5)

    # Result: Dissonance
    dissonance = abs(action_intent["speed"] - user_state["receptivity"])

    print(f"   💥 FAILURE! Dissonance Level: {dissonance}")
    print("   User felt overwhelmed.")

    # 3. The Reflection (The Void)
    print("\n🧘 ACT 2: Reflection (The Void)")
    print("   Elysia enters contemplation...")

    # Logic to extract principle
    new_principle = None
    if dissonance > 50:
        if action_intent["speed"] > 80:
            new_principle = "When the Other is tired, Speed creates Pain."

    time.sleep(1)
    print(f"   ... Insight found: '{new_principle}'")

    # 4. The Growth (Incarnation)
    print("\n🌱 ACT 3: Growth (Incarnation)")
    if new_principle:
        wisdom.learn_principle(new_principle, domain="Relationship", weight=0.5)

        # Adjust Values based on the principle
        wisdom.values["Love"] += 0.1
        wisdom.values["Freedom"] -= 0.05 # Constraint is accepted for Love
        print(f"   Values Shifted: Love={wisdom.values['Love']:.2f}")

    print("\n✅ Demo Complete. The System has learned a Value, not just a Fact.")

if __name__ == "__main__":
    main()
