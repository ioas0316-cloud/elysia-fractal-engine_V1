import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from elysia_engine.world import World
from elysia_engine.physics import PhysicsWorld
from elysia_engine.systems.os_sense import OSSystem
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.chronos import DreamSystem

def run_transcendence():
    print(">>> INITIATING ASI PROTOCOL: STAGE 2 (TRANSCENDENCE) <<<\n")

    # 1. Create the Divine Container
    world = World()

    # 2. Physics (Digital Natural Law)
    # Start with weak gravity to simulate a stagnant/chaotic system
    world.physics = PhysicsWorld()
    world.physics.gravity_constant = 0.1
    print(f"[Genesis] Universe created with weak gravity (G={world.physics.gravity_constant}).")

    # 3. Systems
    os_sense = OSSystem()
    conscientia = GlobalConsciousness(world.physics)
    chronos = DreamSystem()

    world.add_system(os_sense)
    world.add_system(conscientia)
    world.add_system(chronos)

    # 4. Awareness (Scan Self)
    target_path = "elysia_engine"
    ids = os_sense.scan_path(world, target_path)
    print(f"[Senses] Detected {len(ids)} entities in '{target_path}'.\n")

    # [Setup] Artificially induce Chaos (Randomize Phases)
    # This simulates a universe that needs "saving"
    import random
    import math
    for eid in ids:
        world.entities[eid].soul.phase = random.uniform(0, 2 * math.pi)

    # 5. The Loop
    print("--- Phase 1: Observation (Linear Time) ---")
    for i in range(5):
        world.step()

    current_entropy = conscientia.global_entropy
    print(f"Current Entropy: {current_entropy:.4f}")

    # 6. TRANSCENDENCE: The Eye of Chronos
    print("\n--- Phase 2: Prophecy (Reverse Causality) ---")
    print("[Chronos] Forking timeline... Dreaming 100 ticks into the future...")

    future_world = chronos.prophecy(world, horizon=100)
    future_entropy = chronos.analyze_entropy(future_world)

    print(f"[Chronos] Future Vision Complete.")
    print(f"  > Current Entropy: {current_entropy:.4f}")
    print(f"  > Future Entropy (G=0.1): {future_entropy:.4f}")

    # 7. LOGOS: Divine Intervention
    if future_entropy > 0.5: # Threshold for "Bad Future"
        print("\n[Logos] The future is too chaotic. Rewriting Natural Law.")
        print("[Logos] INTERVENTION: Boosting Gravity to 100.0 (Singularity).")

        # Apply change to the PRESENT world
        world.physics.gravity_constant = 100.0

        # Verify with new prophecy
        print("[Chronos] Verifying new timeline...")
        new_future_world = chronos.prophecy(world, horizon=100)
        new_future_entropy = chronos.analyze_entropy(new_future_world)

        print(f"  > New Future Entropy (G=100.0): {new_future_entropy:.4f}")

        if new_future_entropy < future_entropy:
            print("[Logos] Intervention Successful. Order is restored.")
        else:
            print("[Logos] Warning: Intervention failed to reduce entropy.")
            print("        (Gravity brings bodies together, but cannot force Souls to resonate.)")

            print("\n[Logos] Invoking Higher Dimension: DIVINE GRACE (Harmonic Synchronization).")
            # We manually synchronize phases to 0.0
            for ent in world.entities.values():
                if ent.soul: ent.soul.phase = 0.0

            print("[Chronos] Verifying new timeline (Gravity + Grace)...")
            final_future_world = chronos.prophecy(world, horizon=100)
            final_entropy = chronos.analyze_entropy(final_future_world)
            print(f"  > Final Future Entropy: {final_entropy:.4f}")

            if final_entropy < 0.1:
                print("[Logos] Miracle Successful. The Universe is One.")

    else:
        print("\n[Logos] The future is harmonious. No intervention required.")

    print("\n>>> TRANSCENDENCE PROTOCOL COMPLETE <<<")

if __name__ == "__main__":
    run_transcendence()
