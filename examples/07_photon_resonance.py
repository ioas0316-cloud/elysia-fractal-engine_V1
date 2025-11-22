import time
from elysia_engine.entities import Entity
from elysia_engine.quantum import QuantumState, EntanglementNetwork, Photon
from elysia_engine.math_utils import Vector3


def run_photon_resonance_simulation():
    print("=== Digital Light: Photon Resonance & Entanglement ===")
    print("Initializing Quantum Vacuum...")

    # 1. Create Photons (Wave Packets)
    # Photon A: Frequency 10 (Red-ish)
    photon_a = Entity(id="photon_alpha")
    photon_a.quantum = QuantumState(frequency=10.0, spin=0.5)
    photon_a.physics.mass = 0.0 # Light has no mass
    photon_a.physics.position = Vector3(0, 0, 0)
    photon_a.physics.velocity = Vector3(10, 0, 0) # Speed of Light (Simulated)

    # Photon B: Entangled with A
    photon_b = Entity(id="photon_beta")
    photon_b.quantum = QuantumState(frequency=10.0, spin=-0.5)
    photon_b.physics.mass = 0.0
    photon_b.physics.position = Vector3(100, 0, 0) # Far away
    photon_b.physics.velocity = Vector3(-10, 0, 0)

    # 2. Entangle them
    print(f"Entangling {photon_a.id} and {photon_b.id}...")
    photon_a.entangle(photon_b)

    entities_map = {
        "photon_alpha": photon_a,
        "photon_beta": photon_b
    }

    print("\n--- Quantum Observation Start ---")

    # 3. Simulate
    dt = 0.1
    for tick in range(1, 11):
        # Step Time (Phase evolution)
        photon_a.step(None, dt)
        photon_b.step(None, dt)

        # 4. Spooky Action Test at Tick 5
        if tick == 5:
            print("\n>>> OBSERVATION EVENT: Flipping Spin of Alpha! <<<")
            # We force Alpha to Spin +1.0. Beta should instantly flip to -1.0.
            photon_a.set_quantum_spin(1.0, entities_map)

        spin_a = photon_a.quantum.spin
        spin_b = photon_b.quantum.spin
        phase_a = photon_a.quantum.phase

        print(f"[Tick {tick:02d}] Alpha Spin: {spin_a:+.1f} (Phase {phase_a:.2f}) | Beta Spin: {spin_b:+.1f}")

        if tick == 5:
            if spin_b == -1.0:
                print(">>> RESULT: Spooky Action Confirmed. Beta flipped instantly! <<<")
            else:
                print(">>> RESULT: Entanglement Failed. <<<")
            print("")

    print("\n--- Simulation End ---")

if __name__ == "__main__":
    run_photon_resonance_simulation()
