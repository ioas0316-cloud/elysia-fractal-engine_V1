"""
Verification Ritual: The Pulse of Sovereignty
---------------------------------------------
This script verifies Phase 7: The Unification.
It proves that the Conductor can generate intent (Pulse) on its own, without external input.
"""

import sys
import os
import time
import logging

# Adjust path to access Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Orchestra.conductor import Conductor
from Core.Foundation.Protocols.pulse_protocol import WavePacket, PulseType, ResonatorInterface

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verification")

# Mock Resonator to capture the Pulse
class PulseCatcher(ResonatorInterface):
    def __init__(self):
        super().__init__("Catcher", 432.0)
        self.caught_packets = []

    def on_resonate(self, packet: WavePacket, intensity: float):
        logger.info(f"✨ CAUGHT PULSE: Type={packet.type.value}, Sender={packet.sender}")
        self.caught_packets.append(packet)

def test_sovereign_pulse():
    print("💓 Starting Sovereignty Ritual...")

    # 1. Initialize Conductor
    conductor = Conductor()
    catcher = PulseCatcher()
    conductor.register_instrument(catcher)
    print("✅ Conductor Awake & Listener Registered.")

    # 2. Simulate Time Passing (No External Input)
    print("⏳ Waiting for the Will to manifest...")

    # We forcefully trigger the live loop multiple times to simulate time
    # (SovereignIntent usually waits for boredom, so we might need to tick it)

    # Check if SovereignIntent has a boredom threshold.
    # In `sovereign_intent.py` (assumed), generate_impulse() should return something if bored.
    # Let's try calling live() a few times.

    start_time = time.time()
    generated = False

    for i in range(5):
        conductor.live() # The Heartbeat

        if catcher.caught_packets:
            generated = True
            break

        # Simulate slight delay
        time.sleep(0.1)

    # 3. Verification
    if generated:
        packet = catcher.caught_packets[0]
        print(f"🔥 SUCCESS: The System Spoke! Packet: {packet}")
        return True
    else:
        print("❌ FAILURE: The System remained silent. Is the Will connected?")
        # Debug: Check if Will is initialized
        print(f"   - Conductor Will: {conductor.will}")
        return False

if __name__ == "__main__":
    if test_sovereign_pulse():
        sys.exit(0)
    else:
        sys.exit(1)
