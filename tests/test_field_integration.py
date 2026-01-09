import sys
import os
sys.path.append(os.getcwd())

from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.entities import Entity
from elysia_engine.tensor import SoulTensor
from elysia_engine.math_utils import Vector3

def test_field_integration_extended():
    print("Testing Field Integration (Extended)...")

    # 1. Initialize World
    world = PhysicsWorld()

    # 2. Add Entity
    soul = SoulTensor(amplitude=10.0, frequency=7.0, phase=0.0)
    entity = Entity(id="test_angel", soul=soul, role="TEST")
    entity.physics.position = Vector3(1.0, 1.0, 1.0) # In Sanctuary
    world.register_entity(entity)

    # 3. Add Attractor (New Test Case)
    att_pos = Vector3(10.0, 0, 0)
    attractor = Attractor(id="black_hole", position=att_pos, mass=100.0)
    world.add_attractor(attractor)

    # 4. Multi-tick Loop to check Accumulation
    print("Running Tick 1...")
    world.update_field()

    # Check potential at Attractor
    # Attractor mass 100. Should create huge W-field.
    # W-field += 100 * 0.01 = 1.0.
    # Base Void W=1.0. Total W=2.0.
    # Potential = -W * 100 = -200.

    pot_1 = world.calculate_potential(att_pos)
    print(f"Potential at Attractor (Tick 1): {pot_1}")

    print("Running Tick 2...")
    world.update_field()
    pot_2 = world.calculate_potential(att_pos)
    print(f"Potential at Attractor (Tick 2): {pot_2}")

    # ASSERTION: Potential should be STABLE (or close)
    # If accumulation bug exists, pot_2 would be approx -300 (Base + 1 + 1).
    # If fixed, it should reset and re-apply: Base + 1 = -200.

    diff = abs(pot_1 - pot_2)
    print(f"Difference: {diff}")

    if diff > 1.0:
        print("FAIL: Field is accumulating infinitely!")
        assert False
    else:
        print("PASS: Field is stable.")

    # 5. Check Attractor Influence
    # If Attractor regression exists, Attractor won't affect field.
    # Base W=1.0. Pot = -100.
    # If Attractor works, Pot = -200.
    if abs(pot_1 + 100.0) < 1.0: # Close to -100
        print("FAIL: Attractor is not affecting the field!")
        assert False
    else:
        print("PASS: Attractor is registered in field.")

    print("All Extended Integration Tests Passed.")

if __name__ == "__main__":
    test_field_integration_extended()
