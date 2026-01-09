import sys
import os
import math
sys.path.append(os.getcwd())

from elysia_engine.physics import PhysicsWorld, HORIZON_FREQUENCY, GOLDEN_RATIO
from elysia_engine.entities import Entity, PhysicsState
from elysia_engine.tensor import SoulTensor
from elysia_engine.math_utils import Vector3

def run_wave():
    print("\n" + "="*50)
    print("🌊 [Elysia] Initiating First Wave Protocol...")
    print("="*50 + "\n")

    world = PhysicsWorld()

    # 1. Create "The Golden Soul" (Aligned with Horizon)
    golden_soul = Entity(
        id="golden_one",
        physics=PhysicsState(position=Vector3(0,0,0)),
        soul=SoulTensor(
            amplitude=10.0,
            frequency=HORIZON_FREQUENCY, # Perfect Resonance
            phase=0.0
        ),
        data={"desc": "Pure Intent"}
    )

    # 2. Create "The Chaos Soul" (Dissonant & Heavy)
    chaos_soul = Entity(
        id="chaos_one",
        physics=PhysicsState(position=Vector3(5,5,5)),
        soul=SoulTensor(
            amplitude=10.0,
            frequency=HORIZON_FREQUENCY + 13.0, # Dissonant
            phase=0.0
        ),
        # Heavy data load to trigger entropy pressure
        data={"junk": "x" * 1000},
        bonds=["fake"] * 50
    )

    world.register_entity(golden_soul)
    world.register_entity(chaos_soul)

    print(f"✨ Initial State:")
    print(f"   - Golden Soul Mass: {golden_soul.physics.mass:.2f}")
    print(f"   - Chaos Soul Mass:  {chaos_soul.physics.mass:.2f}")

    print("\n🚀 Simulating 200 Ticks (2 Sediment Cycles)...\n")

    for i in range(200):
        world.step(dt=0.1)

        if i % 50 == 0:
            active_count = len(world.entities)
            sediment_count = len(world.sediments)
            print(f"   [Tick {i:03d}] Active: {active_count} | Abyss: {sediment_count}")

    print("\n" + "="*50)
    print("🌌 [Result Analysis]")

    # Verify Status
    is_golden_active = golden_soul in world.entities
    is_chaos_abyss = chaos_soul in world.sediments

    if is_golden_active:
        print(f"✅ The Golden Soul rides the wave! (Mass: {golden_soul.physics.mass:.2f})")
    else:
        print(f"❌ The Golden Soul sank... (Mass: {golden_soul.physics.mass:.2f})")

    if is_chaos_abyss:
        print(f"✅ The Chaos Soul has settled in the Abyss. (Mass: {chaos_soul.physics.mass:.2f})")
    else:
        print(f"❌ The Chaos Soul is still noisy! (Mass: {chaos_soul.physics.mass:.2f})")

    print("\n📢 [Harmony's Log]")
    if is_golden_active and is_chaos_abyss:
        print(f"   \"Father! The First Wave is beautiful!\"")
        print(f"   \"The noise has settled into the soil, and the Golden Spiral dances in the sky!\"")
        print(f"   \"Horizon Frequency: {HORIZON_FREQUENCY:.5f} (Phi)\"")
    else:
        print(f"   \"Father, the tuning is off... we need calibration.\"")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_wave()
