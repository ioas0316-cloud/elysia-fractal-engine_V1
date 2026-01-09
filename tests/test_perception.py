import sys
import os
import math
sys.path.append(os.getcwd())

from elysia_engine.physics import PhysicsWorld
from elysia_engine.entities import Entity, PhysicsState
from elysia_engine.tensor import SoulTensor
from elysia_engine.math_utils import Vector3, Quaternion

def run_perception_test():
    print("\n" + "="*50)
    print("👁️ [Elysia] Testing Perception-Field Mapping")
    print("="*50 + "\n")

    world = PhysicsWorld()

    # 1. Setup Entity (Observer)
    # Frequency 100.0
    observer = Entity(
        id="observer",
        physics=PhysicsState(position=Vector3(0,0,0)),
        soul=SoulTensor(
            amplitude=10.0,
            frequency=100.0,
            phase=0.0,
            orientation=Quaternion.identity() # Facing +Z
        )
    )
    world.register_entity(observer)

    # 2. Setup Field Targets (using manual Node Injection for test control)
    # Target A (Front): Perfect Resonance (Freq 100) at (0,0,5)
    # Target B (Back):  Dissonance (Freq 0) at (0,0,-5)

    # We use 'Attractors' to paint the field naturally
    from elysia_engine.physics import Attractor

    # "The Mirror" (Resonant Object)
    mirror = Attractor(
        id="mirror",
        position=Vector3(0,0,5),
        mass=50.0,
        soul=SoulTensor(amplitude=50.0, frequency=100.0, phase=0.0)
    )

    # "The Void" (Dissonant Object)
    void_obj = Attractor(
        id="void_obj",
        position=Vector3(0,0,-5),
        mass=50.0,
        soul=SoulTensor(amplitude=50.0, frequency=0.0, phase=0.0)
    )

    world.add_attractor(mirror)
    world.add_attractor(void_obj)

    # Update field to propagate values
    world.update_field()

    print("🧪 Scenario 1: Looking at the Mirror (Resonance)")
    # Observer faces +Z (Default)
    # Mirror is at +Z
    experience_1 = world.perceive(observer, range_dist=5.0)

    print(f"   - Gaze Direction: {experience_1['gaze_direction']}")
    print(f"   - Field Frequency: {experience_1['field_frequency']:.2f}")
    print(f"   - Resonance: {experience_1['resonance']:.4f}")
    print(f"   - Narrative: {experience_1['narrative']}")

    if experience_1['resonance'] > 0.9:
        print("   ✅ SUCCESS: High resonance detected.")
    else:
        print("   ❌ FAILURE: Resonance too low.")

    print("\n🧪 Scenario 2: Looking at the Void (Dissonance)")
    # Rotate Observer to face -Z
    # Axis (0,1,0) Angle PI
    rot_back = Quaternion.from_axis_angle(Vector3(0,1,0), math.pi)
    observer.soul.orientation = rot_back

    experience_2 = world.perceive(observer, range_dist=5.0)

    print(f"   - Gaze Direction: {experience_2['gaze_direction']}")
    print(f"   - Field Frequency: {experience_2['field_frequency']:.2f}")
    print(f"   - Resonance: {experience_2['resonance']:.4f}")
    print(f"   - Narrative: {experience_2['narrative']}")

    if experience_2['resonance'] < 0.1:
        print("   ✅ SUCCESS: Low resonance (Alien Noise) detected.")
    else:
        print("   ❌ FAILURE: Resonance too high for void.")

    print("\n" + "="*50)

if __name__ == "__main__":
    run_perception_test()
