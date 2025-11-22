import time
import random
import math
from elysia_engine.world import World
from elysia_engine.entities import Entity
from elysia_engine.tensor_coil import CoilStructure
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.quantum import QuantumDNA
from elysia_engine.math_utils import Vector3

def main():
    print("🌌 Initializing Project Genesis... [Quantum DNA Protocol]")

    # 1. Create World & Physics
    world = World()
    physics_world = PhysicsWorld()

    # Add a central "Star" (Attractor) to pull memes together
    star = Attractor(id="CentralStar", position=Vector3(0,0,0), mass=500.0, radius=2.0)
    physics_world.add_attractor(star)

    # Create the Coil (The Womb) - Accelerates them around the star
    coil = CoilStructure(
        center=Vector3(0, 0, 0),
        axis=Vector3(0, 0, 1),
        radius=5.0,  # Tighter radius
        frequency=0.5,
        strength=20.0
    )

    # 2. Spawn Adam & Eve (Digital Photons)
    # Adam: Low Frequency (Ice/Stability)
    adam = Entity(id="Adam")
    adam.dna = QuantumDNA(frequency=20.0, phase=0.0, amplitude=100.0, spin=1.0)
    adam.physics.position = Vector3(5, 0, 0)
    adam.physics.velocity = Vector3(0, 5, 0) # Orbital velocity
    world.add_entity(adam)

    # Eve: High Frequency (Fire/Passion)
    eve = Entity(id="Eve")
    eve.dna = QuantumDNA(frequency=80.0, phase=math.pi/2, amplitude=100.0, spin=-1.0)
    eve.physics.position = Vector3(-5, 0, 0)
    eve.physics.velocity = Vector3(0, -5, 0) # Counter-orbit? Or same direction?
    # Let's make them crash: distinct orbits
    world.add_entity(eve)

    print(f"✨ Created Progenitors:")
    print(f" - Adam: {adam.dna.decode_meaning()} ({adam.dna.frequency}Hz)")
    print(f" - Eve:  {eve.dna.decode_meaning()} ({eve.dna.frequency}Hz)")
    print("-" * 50)

    # 3. Simulation Loop
    max_ticks = 200
    population_limit = 20

    for i in range(max_ticks):
        dt = 0.1
        current_entities = list(world.entities.values())

        # A. Physics Step
        for ent in current_entities:
            # Apply all physics (Gravity + Coil + Movement)
            ent.apply_physics(coil, physics_world, dt)

            # Simple bounds check
            if ent.physics.position.magnitude > 50:
                 ent.physics.velocity = ent.physics.velocity * -0.5 # Bounce back
                 ent.physics.position = ent.physics.position * 0.9

        # B. Quantum Incubation (Breeding)
        new_children = coil.incubate(current_entities, world.time)

        if new_children:
            for child in new_children:
                if len(world.entities) < population_limit:
                    world.add_entity(child)
                    meaning = child.dna.decode_meaning()
                    print(f"👶 [Tick {i}] NEW LIFE BORN: {child.id}")
                    print(f"   🧬 DNA: {meaning} ({child.dna.frequency:.1f}Hz)")
                    print(f"   ⚡ Amp: {child.dna.amplitude:.1f}")
                else:
                    # System overload protection
                    pass

        # C. Population Control (Energy Decay)
        keys_to_remove = []
        for eid, ent in world.entities.items():
            if ent.dna:
                # Natural entropy
                ent.dna.amplitude *= 0.99
                if ent.dna.amplitude < 5.0:
                    keys_to_remove.append(eid)

        for k in keys_to_remove:
            del world.entities[k]
            # print(f"💀 {k} faded away.") # Reduce spam

        world.step(dt)

        if not world.entities:
            print("🌑 The void has reclaimed all.")
            break

    print("-" * 50)
    print(f"🏁 Simulation Ended. Final Population: {len(world.entities)}")
    for ent in world.entities.values():
         print(f" > {ent.id}: {ent.dna.decode_meaning()} (Freq: {ent.dna.frequency:.1f}, Amp: {ent.dna.amplitude:.1f})")

if __name__ == "__main__":
    main()
