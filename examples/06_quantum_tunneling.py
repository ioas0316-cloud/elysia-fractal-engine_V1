import time
import random
from elysia_engine.entities import Entity
from elysia_engine.physics import PhysicsWorld, HamiltonianSystem
from elysia_engine.math_utils import Vector3


def run_quantum_tunneling_experiment():
    print("=== Quantum Tunneling Experiment ===")
    print("Schrödinger's Cat is trying to escape the box...")

    # 1. Setup Universe
    p_world = PhysicsWorld()
    h_sys = HamiltonianSystem(p_world)

    # 2. Create a Barrier (Energy Wall)
    barrier_pos = Vector3(20, 0, 0)
    p_world.add_barrier(barrier_pos, radius=5.0, height=100.0)
    print(f"Energy Barrier erected at {barrier_pos} (Height: 100.0)")

    # 3. Spawn Particle
    particle = Entity(id="psi_particle")
    particle.physics.position = Vector3(15, 0, 0) # Start at edge of interaction
    particle.physics.velocity = Vector3(10, 0, 0)
    particle.physics.mass = 1.0

    print(f"Particle spawned.")

    print("\n--- Observation Start ---")
    dt = 0.1
    escaped = False

    for tick in range(1, 101):
        # 1. Calculate Forces (Classical Repulsion)
        pos = particle.physics.position
        dist = (pos - barrier_pos).magnitude

        # Simple linear repulsion if inside radius
        if dist < 5.0:
            direction = (pos - barrier_pos).normalize()
            # F = -Grad(U). U = H * (1 - r/R).
            # dU/dr = -H/R.
            # F = -dU/dr = H/R.
            # H=100, R=5. Force = 20.
            # Direction is away from center (-r hat).
            # So Force vector is (pos-center).norm * 20.
            force = direction * 20.0
            particle.physics.apply_force(force, dt)

        # 2. Move
        particle.physics.step(dt)

        # 3. Quantum Tunneling Check
        # We need to check U vs K
        u_val = p_world.get_potential_energy(particle.physics.position) * particle.physics.mass
        k_val = particle.physics.kinetic_energy

        # Debug info
        if tick % 5 == 0:
             print(f"   [Debug] U={u_val:.1f} K={k_val:.1f} Dist={dist:.1f}")

        # Attempt Tunnel
        # Lower threshold to make it trigger easier for demo
        did_tunnel = particle.apply_quantum_tunneling(h_sys, barrier_threshold=10.0)

        status = "Approaching"
        if did_tunnel:
            status = ">>> TUNNELED! (Quantum Leap) >>>"
            escaped = True
        elif pos.x > 22.0: # Past barrier center
            status = "Escaped"
            escaped = True
        elif dist < 5.0:
            status = "In Barrier"

        if did_tunnel or escaped or tick % 10 == 0:
             print(f"[Tick {tick:02d}] Pos: {pos} | KE: {particle.physics.kinetic_energy:.1f} | {status}")

        if escaped:
            print("\nResult: The particle has escaped the potential well via Quantum Tunneling.")
            break

if __name__ == "__main__":
    run_quantum_tunneling_experiment()
