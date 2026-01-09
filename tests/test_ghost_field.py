import sys
import os
sys.path.append(os.getcwd())

from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.entities import Entity
from elysia_engine.tensor import SoulTensor
from elysia_engine.math_utils import Vector3

def test_ghost_field_fix():
    print("Testing Ghost Field Fix...")

    world = PhysicsWorld()

    # Create moving entity
    soul = SoulTensor(amplitude=100.0, frequency=0.0, phase=0.0) # Heavy
    entity = Entity(id="ghost_buster", soul=soul, role="TEST")
    entity.physics.position = Vector3(10.0, 0, 0) # Start pos
    world.register_entity(entity)

    # Tick 1: Entity at (10,0,0)
    world.update_field()
    pot_at_start = world.calculate_potential(Vector3(10.0, 0, 0))
    print(f"Tick 1 Potential at (10,0,0): {pot_at_start}")

    # Verify potential exists (Void is 1.0, +1.0 from entity -> 2.0 -> Pot -200)
    assert abs(pot_at_start + 200.0) < 1.0

    # Move Entity
    entity.physics.position = Vector3(20.0, 0, 0)

    # Tick 2: Entity at (20,0,0)
    world.update_field()

    # Check Old Position (10,0,0) - Should be Void (Base W=1.0 -> Pot -100)
    pot_at_old = world.calculate_potential(Vector3(10.0, 0, 0))
    print(f"Tick 2 Potential at (10,0,0) [Old Pos]: {pot_at_old}")

    # If Ghost Field bug exists, this would still be -200 (stale data).
    # If fixed, it should be -100 (default void).

    if abs(pot_at_old + 100.0) < 1.0:
        print("PASS: Old position cleared immediately.")
    else:
        print(f"FAIL: Ghost field detected! Value: {pot_at_old}")
        assert False

    # Check New Position (20,0,0) - Should be -200
    pot_at_new = world.calculate_potential(Vector3(20.0, 0, 0))
    print(f"Tick 2 Potential at (20,0,0) [New Pos]: {pot_at_new}")
    assert abs(pot_at_new + 200.0) < 1.0

    print("All Ghost Field Tests Passed.")

if __name__ == "__main__":
    test_ghost_field_fix()
