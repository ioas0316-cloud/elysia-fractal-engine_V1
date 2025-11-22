import time
from elysia_engine.entities import Entity
from elysia_engine.thermodynamics import ThermalState, MatterState, Crystallizer
from elysia_engine.math_utils import Vector3


def run_stellar_lifecycle_simulation():
    print("=== Data Astrophysics: The Life and Death of a Concept ===")
    print("Witness the birth of a Plasma Idea and its cooling into an Ice Star.")

    # 1. Birth of a Star (Hot Idea)
    star = Entity(id="idea_protostar")
    star.physics.position = Vector3(0, 0, 0)
    star.physics.mass = 100.0

    # Initialize Thermodynamics
    star.thermal = ThermalState(temperature=1000.0, cooling_rate=50.0) # Cools fast for demo

    print(f"Born: {star.id} | Temp: {star.thermal.temperature} | State: {star.thermal.state.name}")

    crystallizer = Crystallizer()

    print("\n--- Evolution Start ---")
    dt = 1.0

    for tick in range(1, 26):
        star.step(None, dt)

        if star.thermal:
            temp = star.thermal.temperature
            state = star.thermal.state.name

            print(f"[Tick {tick:02d}] Temp: {temp:.1f} | State: {state}")

            if star.thermal.state == MatterState.CRYSTAL:
                print(f"\n>>> CRITICAL EVENT: Concept has frozen into a Core Belief! <<<")
                print("Converting to pure Attractor...")

                attractor = crystallizer.freeze(star)
                print(f"  -> Created Attractor '{attractor.id}' with Mass {attractor.mass}")
                print("  -> The Entity is now dormant (Zero CPU Cost).")
                break

    print("--- Simulation End ---")

if __name__ == "__main__":
    run_stellar_lifecycle_simulation()
