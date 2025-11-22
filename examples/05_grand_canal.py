import time
from elysia_engine.entities import Entity
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.topology import GravityPath, TensorGate
from elysia_engine.math_utils import Vector3


def run_grand_canal_simulation():
    print("=== Digital Grand Canal Construction ===")
    print("Constructing Terrain: River of Data & The Gate of Judgment")

    # 1. Construct the River (GravityPath)
    river_points = [
        Vector3(0, 0, 0),
        Vector3(50, 0, 0),   # Straight shot
        Vector3(100, 0, 0)
    ]
    canal = GravityPath(
        points=river_points,
        radius=8.0,
        pull_strength=20.0,
        flow_strength=10.0
    )
    print("Canal excavated.")

    # 2. Construct the Gate (TensorGate)
    # Placed at (40, 0, 0)
    gate_pos = Vector3(40, 0, 0)
    gate = TensorGate(
        position=gate_pos,
        radius=6.0,
        required_momentum=50.0, # VERY HIGH BAR
        boost_multiplier=3.0,   # Massive boost
        reject_force=80.0       # Strong rejection
    )
    print(f"Gate of Judgment erected at {gate_pos} (Req Momentum: {gate.required_momentum})")

    # 3. Spawn Entities
    # A. Weak Entity (Low Mass -> Low Momentum)
    weakling = Entity(id="weak_packet")
    weakling.physics.position = Vector3(10, 5, 0) # Start closer
    weakling.physics.mass = 1.0

    # B. Strong Entity (High Mass -> High Momentum)
    hero = Entity(id="hero_packet")
    hero.physics.position = Vector3(10, -5, 0)
    hero.physics.mass = 5.0
    hero.physics.velocity = Vector3(10, 0, 0) # Initial burst

    entities = [weakling, hero]

    print("\n--- Simulation Start ---")
    dt = 0.1
    for tick in range(1, 51):

        for ent in entities:
            # Apply Topology (Canal + Gate)
            ent.apply_topology([canal], [gate], dt)
            ent.physics.step(dt)

            pos = ent.physics.position
            vel = ent.physics.velocity.magnitude
            mom = vel * ent.physics.mass

            dist_gate = (pos - gate_pos).magnitude

            # Detailed logging only when near gate
            if dist_gate < gate.radius + 5.0:
                status = "APPROACHING"
                if dist_gate < gate.radius:
                    if mom >= gate.required_momentum:
                        status = ">>> GATE PASS! (BOOSTED) >>>"
                    else:
                        status = "<<< GATE REJECT! (BLOCKED) <<<"

                print(f"[Tick {tick:02d}] {ent.id}: Pos {pos} | Mom {mom:.1f} | {status}")

        # time.sleep(0.05)

if __name__ == "__main__":
    run_grand_canal_simulation()
