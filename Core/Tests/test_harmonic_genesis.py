import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.reality_sculptor import RealitySculptor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("HarmonicGenesisTest")

def test_harmonic_genesis():
    print("\n🌊 Initializing Harmonic Logic Genesis Test...")
    
    sculptor = RealitySculptor()
    
    # 1. Test: Logic Flow (Attractors)
    # y=1.0 (Logic) -> Should create Attractors
    logic_wave = HyperWavePacket(
        energy=80.0,
        orientation=Quaternion(1.0, 0.2, 1.0, 0.2).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 1: Logic Flow (Attractor Generation)")
    code_1 = sculptor.sculpt_from_wave(logic_wave, "code: DecisionProcess")
    print("-" * 40)
    print(code_1)
    print("-" * 40)
    
    if "field.add_attractor" in code_1:
        print("✅ SUCCESS: Generated Attractors for Logic")
    else:
        print("❌ FAILURE: Failed to generate Attractors")

    # 2. Test: Creative Flow (Velocity)
    # x=1.0 (Emotion) -> Should create Flows
    creative_wave = HyperWavePacket(
        energy=60.0,
        orientation=Quaternion(1.0, 1.0, 0.2, 0.2).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 2: Creative Flow (Velocity Generation)")
    code_2 = sculptor.sculpt_from_wave(creative_wave, "code: CreativeStream")
    print("-" * 40)
    print(code_2)
    print("-" * 40)
    
    if "field.inject_flow" in code_2:
        print("✅ SUCCESS: Generated Flow for Emotion")
    else:
        print("❌ FAILURE: Failed to generate Flow")

    # 3. Test: Safety Barrier (Repulsors)
    # z=1.0 (Ethics) -> Should create Repulsors
    safety_wave = HyperWavePacket(
        energy=50.0,
        orientation=Quaternion(1.0, 0.2, 0.2, 1.0).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 3: Safety Barrier (Repulsor Generation)")
    code_3 = sculptor.sculpt_from_wave(safety_wave, "code: SafetyGuard")
    print("-" * 40)
    print(code_3)
    print("-" * 40)
    
    if "field.add_repulsor" in code_3:
        print("✅ SUCCESS: Generated Repulsors for Ethics")
    else:
        print("❌ FAILURE: Failed to generate Repulsors")

if __name__ == "__main__":
    test_harmonic_genesis()
