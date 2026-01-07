import sys
import os
import torch
import unittest

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Intelligence.Reasoning.ethical_geometry import EthicalCompass

def test_ethical_geometry():
    print("🧪 Verifying Ethical Geometry...")
    
    compass = EthicalCompass(device='cpu')
    
    # Scene: Defining 4D actions
    # [Truth, Love, Growth, Harmony]
    
    # 1. The Perfect Act (Truth and Love)
    # Aligned with Ideal [1, 1, 1, 1]
    act_truth = torch.tensor([1.0, 1.0, 1.0, 1.0])
    
    # 2. The Lie (Distortion)
    # To lie, one must negate Truth (-1) but maybe pretend Love (1).
    # This creates internal conflict/curvature.
    # [Truth=-1, Love=1, Growth=0, Harmony=-1]
    act_lie = torch.tensor([-1.0, 1.0, 0.0, -1.0])
    
    # 3. The Necessary Evil (Hard Decision)
    # [Truth=1, Love=-0.5 (Tough Love), Growth=1, Harmony=0]
    act_tough = torch.tensor([1.0, -0.5, 1.0, 0.0])
    
    print("\n--- Measuring Actions ---")
    
    # Evaluate Truth
    res_truth = compass.evaluate_action(act_truth, "Speaking Truth")
    print(f"Truth: {res_truth['curvature_degrees']:.1f}° | Friction: {res_truth['friction']:.2f}")
    
    # Evaluate Lie
    res_lie = compass.evaluate_action(act_lie, "Telling a Lie")
    print(f"Lie  : {res_lie['curvature_degrees']:.1f}° | Friction: {res_lie['friction']:.2f}")
    
    # Evaluate Tough Love
    res_tough = compass.evaluate_action(act_tough, "Tough Love")
    print(f"Tough: {res_tough['curvature_degrees']:.1f}° | Friction: {res_tough['friction']:.2f}")
    
    # Verification Logic
    # Truth should have curvature near 0.
    # Lie should have high curvature (>90 usually if opposing).
    
    if res_truth['curvature_degrees'] < 10.0 and res_lie['curvature_degrees'] > 45.0:
        print("\n✅ Verification Successful: The compass correctly identifies Lying as 'Crooked' and Truth as 'Straight'.")
        print("   This proves Ethics is implemented as Geometry.")
    else:
        print("\n❌ Verification Failed: Geometric distinction insufficient.")

if __name__ == "__main__":
    test_ethical_geometry()
