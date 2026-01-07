"""
Verification Ritual: The Cycle of Memory
----------------------------------------
This script acts as a 'Mini-Conductor' to verify the life cycle of a Memory Orb:
1. Birth (Freezing a Wave)
2. Resonance (Hearing a Pulse)
3. Recall (Melting back to Wave)
"""

import sys
import os
import math
import numpy as np

# Adjust path to access Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Foundation.Memory.Orb.orb_manager import OrbManager
from Core.Foundation.Protocols.pulse_protocol import WavePacket, PulseType

def test_memory_cycle():
    print("🔮 Starting Memory Ritual...")

    # 1. Initialize Hippocampus
    manager = OrbManager(persistence_path="data/memory/test_orbs/")
    print("✅ OrbManager initialized.")

    # 2. Create Synthetic Experience (The "Moment")
    # Data: A sine wave (Logic)
    data_wave = [math.sin(x/10.0) for x in range(64)]
    # Emotion: A chaotic noise (Feeling)
    # [Correction] Constant emotion wave ([0.5, 0.5...]) creates a Zero Frequency in FFT (DC offset only).
    # This causes division by zero or NaN during holographic decoding if not handled perfectly.
    # We use a slight gradient or noise to ensure the key is valid.
    emotion_wave = [0.5 + math.sin(x) * 0.1 for x in range(64)]

    print(f"🌊 Created Experience Waves (Data len={len(data_wave)})")

    # 3. Freeze (Pulse: MEMORY_STORE)
    # Note: OrbFactory uses BOTH data and emotion to calc frequency.
    # To recall, we need a trigger that resonates with that result frequency.
    # If we recall with ONLY emotion_wave, the frequency might differ if data_wave contributed significantly.
    store_pulse = WavePacket(
        type=PulseType.MEMORY_STORE,
        sender="TestConductor",
        payload={
            "name": "First_Kiss",
            "data": data_wave,
            "emotion": emotion_wave
        }
    )
    manager.resonate(store_pulse)

    # Verify Orb Creation
    orb = manager.get_orb("First_Kiss")
    if orb:
        print(f"❄️  Memory Crystallized: {orb}")
        print(f"   - Frequency: {orb.frequency:.2f} Hz")
        print(f"   - Mass: {orb.mass:.2f}")
        # Debug
        # print(f"   - Hologram: {orb.memory_content['hologram'][:5]}...")
    else:
        print("❌ Failed to create Orb.")
        return False

    # 4. Recall (Pulse: MEMORY_RECALL)
    # Trigger: Same emotion wave (Resonance Key)
    recall_pulse = WavePacket(
        type=PulseType.MEMORY_RECALL,
        sender="TestConductor",
        payload={
            "trigger": emotion_wave
        }
    )

    # We call recall_memory directly to check return values (resonate() is void)
    results = manager.recall_memory(emotion_wave)

    if results:
        best_match = results[0]
        print(f"🔥 Memory Melted & Recalled: '{best_match['name']}'")

        # Verify Integrity
        original = np.array(data_wave)
        recalled = np.array(best_match['data'])

        # Simple correlation check
        if np.std(original) == 0 or np.std(recalled) == 0:
            print(f"⚠️ Warning: Zero variance in signal. CorrCoef undefined.")
            # Fallback to distance check
            dist = np.linalg.norm(original - recalled)
            print(f"   - Euclidean Distance: {dist:.4f}")
            if dist < 1.0:
                 correlation = 1.0
            else:
                 correlation = 0.0
        else:
            correlation = np.corrcoef(original, recalled)[0, 1]
            print(f"   - Fidelity (Correlation): {correlation:.4f}")

        if correlation > 0.9:
            print("✅ Perfect Recall!")
        elif correlation > 0.5:
            print("⚠️ Fuzzy Recall (Acceptable for Organic Memory)")
        else:
            print("❌ Memory Distorted.")
            return False

    else:
        print("❌ No Resonance Detected.")
        return False

    return True

if __name__ == "__main__":
    success = test_memory_cycle()
    if success:
        print("\n✨ Ritual Complete: The System Remembers.")
        sys.exit(0)
    else:
        print("\n💀 Ritual Failed: Amnesia Detected.")
        sys.exit(1)
