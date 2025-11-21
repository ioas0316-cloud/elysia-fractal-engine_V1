import time
from elysia_engine.entities import Entity
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.tensor_coil import CoilStructure
from elysia_engine.math_utils import Vector3


def run_hyperdrive_simulation():
    print("=== Digital Physics: Hyperdrive Simulation ===")
    print("Initializing Quantum Vacuum...")

    # 1. Setup the Universe
    p_world = PhysicsWorld()

    # 2. Create the 'Answer' (Attractor)
    # Placed perfectly in the path of the coil's projection
    # Coil Axis is Z. Spiral radius is 10.
    # So if we shoot up Z, we should put the answer on the Z axis or nearby.
    answer_pos = Vector3(0.0, 0.0, 150.0)
    truth = Attractor(id="truth_001", position=answer_pos, mass=20000.0, radius=5.0)
    p_world.add_attractor(truth)
    print(f"TRUTH established at {truth.position} with Mass {truth.mass}")

    # 3. Create the Coil (Topology)
    # It's a giant spiral aiming somewhat towards the truth
    coil = CoilStructure(
        center=Vector3(0, 0, 0),
        radius=10.0,
        frequency=2.0, # Axial push
        strength=50.0  # High acceleration
    )
    print("Tensor Coil Field generated.")

    # 4. Create the Query (Entity)
    query = Entity(id="query_agent")
    # Start ON THE WIRE (Radius 10) to surf the current
    query.physics.position = Vector3(10.0, 0.0, 0.0)
    print(f"Query Agent spawned at {query.physics.position}")

    # 5. Run Simulation
    dt = 0.1
    for i in range(1, 101): # 100 ticks
        # Update Physics
        query.apply_physics(coil, p_world, dt)

        pos = query.physics.position
        vel = query.physics.velocity
        dist = (truth.position - pos).magnitude

        print(f"[Tick {i:03d}] Pos: {pos} | Vel: {vel.magnitude:.1f} | Dist to Truth: {dist:.1f}")

        # Check if we arrived
        if dist < truth.radius * 2:
            print(f"\n>>> ⚡ HYPERDRIVE SINGULARITY REACHED ⚡ <<<")
            print(f"Tick {i}: The apple has fallen. The circuit is closed.")
            print(f"Final Position: {pos}")
            break

        # time.sleep(0.01)

if __name__ == "__main__":
    run_hyperdrive_simulation()
