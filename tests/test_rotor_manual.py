import math
import sys
import os

# Add repo root to path
sys.path.append(os.getcwd())

from elysia_engine.math_utils import Rotor, Vector4

def test_rotor():
    print("Testing Rotor Implementation...")

    # 1. Identity
    v = Vector4(1, 2, 3, 4)
    r_id = Rotor.identity()
    v_id = r_id.rotate(v)
    print(f"Identity: {v} -> {v_id}")
    assert abs(v_id.w - 1) < 1e-6
    assert abs(v_id.x - 2) < 1e-6

    # 2. Simple Rotation WX Plane (90 degrees)
    # W -> X
    angle = math.pi / 2
    r_wx = Rotor.from_plane_angle('wx', angle)

    v_w = Vector4(1, 0, 0, 0)
    v_res = r_wx.rotate(v_w)
    print(f"WX 90deg (1,0,0,0) -> {v_res}")

    # cos(90) = 0, sin(90) = 1.
    # W should become X. (or -X depending on handedness definition)
    # R = cos(45) - e_wx sin(45)
    # v' = R v R~
    # If e_wx v = e_w e_x e_w = -e_w e_w e_x = -(-1) e_x = e_x.
    # It should rotate W towards X?

    # Let's check the result
    # Expected: w=0, x=1, y=0, z=0 (approx)
    assert abs(v_res.w) < 1e-6
    assert abs(v_res.x - 1.0) < 1e-6

    # Check X -> -W
    v_x = Vector4(0, 1, 0, 0)
    v_res_x = r_wx.rotate(v_x)
    print(f"WX 90deg (0,1,0,0) -> {v_res_x}")
    assert abs(v_res_x.w + 1.0) < 1e-6
    assert abs(v_res_x.x) < 1e-6

    # 3. Double Rotation (WX then YZ)
    r_yz = Rotor.from_plane_angle('yz', angle)
    # How to compose? We don't have multiply yet, but we can rotate sequentially
    v_mix = Vector4(1, 0, 1, 0) # W=1, Y=1
    v_step1 = r_wx.rotate(v_mix) # W->X, Y->Y => X=1, Y=1
    v_final = r_yz.rotate(v_step1) # X->X, Y->Z => X=1, Z=1

    print(f"WX then YZ (1,0,1,0) -> {v_final}")
    assert abs(v_final.x - 1.0) < 1e-6
    assert abs(v_final.z - 1.0) < 1e-6

    print("All Rotor tests passed!")

if __name__ == "__main__":
    test_rotor()
