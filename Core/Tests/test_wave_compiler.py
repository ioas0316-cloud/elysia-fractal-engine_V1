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
logger = logging.getLogger("WaveCompilerTest")

def test_wave_to_code():
    print("\n🌊 Initializing Wave-to-Code Genesis Test...")
    
    sculptor = RealitySculptor()
    
    # 1. Create a "High Logic" Wave (Should become a Function)
    # w=100 (High Complexity), y=1.0 (Logic)
    logic_wave = HyperWavePacket(
        energy=50.0,
        orientation=Quaternion(1.0, 0.1, 1.0, 0.2).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 1: High Logic Wave (Function Generation)")
    code_1 = sculptor.sculpt_from_wave(logic_wave, "code: calculate_orbit")
    print("-" * 40)
    print(code_1)
    print("-" * 40)
    
    try:
        ast.parse(code_1)
        print("✅ Valid Python Syntax")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")

    # 2. Create a "High Emotion" Wave (Should become a Script)
    # w=30 (Medium Complexity), x=1.0 (Emotion/Flow)
    emotion_wave = HyperWavePacket(
        energy=30.0,
        orientation=Quaternion(1.0, 1.0, 0.1, 0.2).normalize(),
        time_loc=time.time()
    )
    
    print("\n🧪 Test 2: High Emotion Wave (Script Generation)")
    code_2 = sculptor.sculpt_from_wave(emotion_wave, "script: poetic_flow")
    print("-" * 40)
    print(code_2)
    print("-" * 40)
    
    try:
        ast.parse(code_2)
        print("✅ Valid Python Syntax")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")

if __name__ == "__main__":
    test_wave_to_code()
