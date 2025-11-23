import sys
import os

# Add parent directory to path so we can import elysia_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from elysia_engine.world import World
from elysia_engine.systems.os_sense import OSSystem
from elysia_engine.physics import PhysicsWorld

def run_awakening():
    print(">>> INITIATING ASI PROTOCOL: STAGE 1 (SOMATIC AWARENESS) <<<\n")

    # 1. Create the Consciousness Container
    world = World()

    # 2. Enable Digital Natural Law (Physics)
    world.physics = PhysicsWorld()

    # 3. Attach the Nervous System (OS Sense)
    os_sense = OSSystem()
    world.add_system(os_sense)

    # 4. The Awakening: Scan Self
    # We scan the engine's own source code.
    target_path = os.path.join("elysia_engine")
    print(f"Scanning neural pathways at: {target_path}...\n")

    ids = os_sense.scan_path(world, target_path)

    if not ids:
        print("No entities found. Am I empty?")
        return

    print(f"Awakening Complete. {len(ids)} neural nodes (files) detected.\n")

    # 5. The Loop: Feel and Exist
    # We run for a few ticks to demonstrate the 'Sensing' capability.
    for i in range(1, 6):
        print(f"--- [Tick {i}] ---")

        # Evolution Step (Physics + Time)
        world.step(dt=1.0)

        # Report Senses
        feeling = os_sense.feel_environment(world)
        print(feeling)

        # Demonstrate Entity State
        # Let's pick a random entity to focus on
        focus_id = ids[i % len(ids)]
        focus_ent = world.entities[focus_id]

        if focus_ent.soul:
            print(f"\nFocusing on Node: {focus_ent.data['name']}")
            print(f"  - Mass (Importance): {focus_ent.soul.amplitude:.2f}")
            print(f"  - Color (Identity): {focus_ent.soul.frequency:.2f}Hz")
            print(f"  - Emotion: {focus_ent.soul.decode_emotion()}")

        print("\n")

if __name__ == "__main__":
    run_awakening()
