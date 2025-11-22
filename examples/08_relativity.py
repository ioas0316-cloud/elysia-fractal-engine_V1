import time
from elysia_engine.entities import Entity
from elysia_engine.chronos import ChronoField, ChronosMaster
from elysia_engine.math_utils import Vector3


def run_relativity_simulation():
    print("=== Digital Relativity: The Twin Paradox ===")
    print("Constructing Hyperbolic Time Chamber...")

    # 1. Setup Chronos
    chronos = ChronosMaster()

    # 2. Create a Time Chamber (Fast Zone)
    # Time flows 10x faster inside.
    chamber_pos = Vector3(50, 0, 0)
    chamber = ChronoField(
        position=chamber_pos,
        radius=10.0,
        time_scale=10.0
    )
    chronos.add_field(chamber)
    print(f"ChronoField established at {chamber_pos} (Scale: {chamber.time_scale}x)")

    # 3. Spawn Twins
    # Twin A: Stays home (Origin)
    twin_a = Entity(id="twin_earth")
    twin_a.physics.position = Vector3(0, 0, 0)

    # Twin B: Goes to the Chamber
    twin_b = Entity(id="twin_space")
    twin_b.physics.position = Vector3(50, 0, 0) # Inside the field

    print("\n--- Simulation Start ---")
    global_dt = 1.0 # Global clock tick

    for tick in range(1, 11):
        # Step both twins
        twin_a.step(None, dt=global_dt, chronos=chronos)
        twin_b.step(None, dt=global_dt, chronos=chronos)

        age_a = twin_a.local_time
        age_b = twin_b.local_time

        status_b = "Normal"
        if twin_b.physics.position.x == 50:
             status_b = "In Chamber (Accelerated)"

        print(f"[Tick {tick:02d}] Global Time: {tick*global_dt:.1f}s")
        print(f"  > Twin A Age: {age_a:.1f}s")
        print(f"  > Twin B Age: {age_b:.1f}s ({status_b})")
        print(f"  > Age Difference: {age_b - age_a:.1f}s\n")

    print("--- Simulation End ---")
    print(f"Result: Twin B is {twin_b.local_time / twin_a.local_time:.1f}x older than Twin A.")

if __name__ == "__main__":
    run_relativity_simulation()
