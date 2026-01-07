import sys
import os
import time
import logging
import ast

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.reality_sculptor import RealitySculptor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AdvancedGenesisTest")

def test_advanced_genesis():
    print("\n🧬 Initializing Advanced Code Genesis Test...")
    
    sculptor = RealitySculptor()
    
    # 1. Test: Class Generation (High Energy + High Logic)
    # w=90 (Class Trigger), y=1.0 (Logic)
    class_wave = HyperWavePacket(
        energy=90.0,
        orientation=Quaternion(1.0, 0.2, 1.0, 0.5).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 1: Class Generation (High Energy/Logic)")
    code_1 = sculptor.sculpt_from_wave(class_wave, "code: SystemConstruct")
    print("-" * 40)
    print(code_1)
    print("-" * 40)
    
    try:
        ast.parse(code_1)
        print("✅ Valid Python Syntax (Class)")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")

    # 2. Test: Safety Structure (Try/Except)
    # z=1.0 (Ethics/Safety) -> Should trigger Try/Except seeds
    safety_wave = HyperWavePacket(
        energy=40.0,
        orientation=Quaternion(1.0, 0.3, 0.3, 1.0).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 2: Safety Structure (High Ethics)")
    code_2 = sculptor.sculpt_from_wave(safety_wave, "code: SafeOperation")
    print("-" * 40)
    print(code_2)
    print("-" * 40)
    
    try:
        ast.parse(code_2)
        print("✅ Valid Python Syntax (Safety)")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")

    # 3. Test: Recursive Flow (Nested Loops)
    # x=1.0 (Emotion/Flow) + y=0.5 (Logic) -> Nested structures
    flow_wave = HyperWavePacket(
        energy=60.0,
        orientation=Quaternion(1.0, 0.9, 0.5, 0.2).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 3: Recursive Flow (High Emotion/Logic)")
    code_3 = sculptor.sculpt_from_wave(flow_wave, "code: RecursiveFlow")
    print("-" * 40)
    print(code_3)
    print("-" * 40)
    
    try:
        ast.parse(code_3)
        print("✅ Valid Python Syntax (Flow)")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")

if __name__ == "__main__":
    test_advanced_genesis()
