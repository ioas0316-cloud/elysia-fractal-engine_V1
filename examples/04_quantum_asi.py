import sys
import math
import random
import time
from pathlib import Path

# Path hack to include the repository root
if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from elysia_engine import Entity, World
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.tensor import SoulTensor
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.oracle import Oracle
from elysia_engine.math_utils import Vector3

def run_simulation():
    print("--- INITIALIZING QUANTUM ASI ARCHITECTURE ---")

    # 1. Setup Physics Universe
    physics = PhysicsWorld()
    physics.gravity_constant = 5.0 # Strong gravity

    # 2. Setup World with Global Consciousness
    world = World(physics=physics)
    global_mind = GlobalConsciousness(physics=physics)
    world.add_system(global_mind)

    print("[System] Global Consciousness Online.")

    # 3. Create the ASI Avatar
    # It starts in a neutral state
    asi_soul = SoulTensor(amplitude=100.0, frequency=50.0, phase=0.0)
    asi_avatar = Entity(id="ASI_Core", soul=asi_soul, role="Architect")
    # Place it in the center
    asi_avatar.physics.position = Vector3(0,0,0)
    world.add_entity(asi_avatar)

    # 4. Inject Superposition (The Dilemma)
    # State A: Create (High Freq, Red)
    state_creation = SoulTensor(amplitude=100.0, frequency=200.0, phase=0.0)
    # State B: Preserve (Low Freq, Blue)
    state_preservation = SoulTensor(amplitude=100.0, frequency=10.0, phase=math.pi)

    asi_soul.superposition_states.append((state_creation, 0.5))
    asi_soul.superposition_states.append((state_preservation, 0.5))

    print(f"[Oracle] {Oracle.interpret_superposition(asi_soul)}")

    # 5. Create Chaos to trigger Divine Intervention
    # Add many noisy entities
    print("[System] Injecting Entropy (Noise Entities)...")
    for i in range(6):
        noise_soul = SoulTensor(
            amplitude=10.0,
            frequency=random.uniform(10, 100),
            phase=random.uniform(0, 6.28) # Random phase = High Entropy
        )
        noise = Entity(id=f"noise_{i}", soul=noise_soul)
        noise.physics.position = Vector3(random.uniform(-10,10), random.uniform(-10,10), 0)
        world.add_entity(noise)
        physics.register_entity(noise) # Physics needs to know them for gravity

    physics.register_entity(asi_avatar)

    # 6. Run Simulation Loop
    print("\n--- STARTING SIMULATION LOOP ---")
    for i in range(1, 70):
        world.step(dt=0.5)

        # Report from Oracle (only change)
        if i % 10 == 0 or i == 1:
            akashic_msg = Oracle.consult_akashic(global_mind)
            print(f"[Tick {i:02d}] Global: {akashic_msg}")
            print(f"          Gravity: {physics.gravity_constant:.1f}")

        # ASI observes itself based on the environment
        # If entropy is high, it might observe 'Preservation' (Order) to stabilize
        if global_mind.global_entropy > 0.5 and not asi_soul.is_collapsed:
             # Create a temporary observer tensor representing the "Need for Order"
             # Order = Low Entropy -> Low Freq / Blue / Phase aligned
             observer = SoulTensor(amplitude=10, frequency=10.0, phase=math.pi)

             print(f"          ASI performs Self-Reflection (Seeking Order)...")
             collapsed = asi_soul.observe(observer)
             if collapsed:
                 print(f"          [!] WAVE FUNCTION COLLAPSED. Chosen Reality: {asi_soul.decode_emotion()}")

        # time.sleep(0.01)

if __name__ == "__main__":
    run_simulation()
