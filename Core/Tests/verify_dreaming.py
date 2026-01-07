"""
Verification Ritual: The Dreaming
---------------------------------
This script verifies Phase 5: The Dreaming.
It simulates a Day/Night cycle where memories are formed, and then the system sleeps to consolidate/prune them.
"""

import sys
import os
import math
import shutil

# Adjust path to access Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Foundation.Memory.Orb.orb_manager import OrbManager
from Core.Foundation.Memory.dream_cortex import DreamCortex
from Core.Foundation.Protocols.pulse_protocol import WavePacket, PulseType

TEST_DB_PATH = "data/memory/test_dreams/"

def clean_slate():
    """Wipes the test memory db."""
    if os.path.exists(TEST_DB_PATH):
        shutil.rmtree(TEST_DB_PATH)
    os.makedirs(TEST_DB_PATH, exist_ok=True)

def test_dreaming_cycle():
    print("💤 Starting Sleep Ritual...")
    clean_slate()

    # 1. Initialize Body (Hippocampus & DreamCortex)
    manager = OrbManager(persistence_path=TEST_DB_PATH)
    dreamer = DreamCortex(manager)
    print("✅ System Awake.")

    # 2. The Day (Accumulating Memories)
    print("\n☀️  Daytime: Experiencing life...")

    # Strong Memory 1 (Joy)
    # High amplitude data/emotion -> High Mass
    joy_wave = [1.0] * 64
    manager.save_memory("First_Flight", joy_wave, joy_wave)

    # Strong Memory 2 (Pain)
    pain_wave = [-1.0] * 64
    manager.save_memory("Broken_Wing", pain_wave, pain_wave)

    # Weak Memory 1 (Noise)
    # Very low amplitude -> Low Mass
    noise_wave = [0.01] * 64
    manager.save_memory("Passing_Cloud", noise_wave, noise_wave)

    # Weak Memory 2 (Trivial)
    trivial_wave = [0.02] * 64
    manager.save_memory("Lunch_Menu", trivial_wave, trivial_wave)

    print(f"   - Created 4 memories. Current Count: {len(manager.orbs)}")

    # Verify Mass (Sanity Check)
    # OrbFactory calculates mass as sum of abs(hologram).
    # Since Hologram = FFT(A) * FFT(B), and A,B are small, result is small.
    # Note: OrbFactory logic maps mass. Let's check.
    cloud = manager.get_orb("Passing_Cloud")
    flight = manager.get_orb("First_Flight")
    print(f"   - 'First_Flight' Mass: {flight.mass:.2f}")
    print(f"   - 'Passing_Cloud' Mass: {cloud.mass:.2f}")

    # Ensure our pruning threshold (0.2) is appropriate
    # If Passing_Cloud is > 0.2, we might need to lower its input or raise threshold.
    if cloud.mass > 0.2:
        print(f"⚠️ Warning: Noise mass ({cloud.mass}) is higher than default pruning threshold (0.2).")
        print("   - Adjusting DreamCortex threshold for this test might be needed.")

    # 3. The Night (Dreaming)
    print("\n🌙 Nighttime: Entering the Dream...")

    start_pulse = WavePacket(
        sender="TestConductor",
        type=PulseType.DREAM_CYCLE,
        payload={"action": "START"}
    )
    dreamer.resonate(start_pulse)

    # At this point, DreamCortex should have:
    # 1. Replayed memories (logged)
    # 2. Pruned weak ones

    # 4. The Morning (Wake Up)
    print("\n☀️  Morning: Waking up...")
    stop_pulse = WavePacket(
        sender="TestConductor",
        type=PulseType.DREAM_CYCLE,
        payload={"action": "STOP"}
    )
    dreamer.resonate(stop_pulse)

    # 5. Verification
    remaining_count = len(manager.orbs)
    print(f"\n✨ Result: {remaining_count} memories remain.")

    # We expect Strong ones to remain, Weak ones to be gone.
    has_flight = manager.get_orb("First_Flight") is not None
    has_cloud = manager.get_orb("Passing_Cloud") is not None

    if has_flight and not has_cloud:
        print("✅ SUCCESS: Important memories kept, noise forgotten.")
        return True
    elif has_cloud:
        print("❌ FAILURE: Noise was NOT pruned. Dreaming failed to clean up.")
        return False
    elif not has_flight:
        print("❌ FAILURE: Important memory was LOST. Dreaming was too aggressive.")
        return False

    return False

if __name__ == "__main__":
    success = test_dreaming_cycle()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
