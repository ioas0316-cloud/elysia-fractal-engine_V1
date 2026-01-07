import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine

# Setup logging
logging.basicConfig(level=logging.ERROR, format='%(message)s')
logger = logging.getLogger("GenesisTest")
logger.setLevel(logging.INFO)

def test_genesis():
    print("\n✨ Initializing Genesis Test...")
    
    engine = ReasoningEngine()
    
    # 1. Test: Create Shield (High Ethics)
    print("\n🧪 Test 1: Create Shield System")
    intent = "CREATE: Shield System"
    insight = engine.think(intent)
    
    print("-" * 40)
    print(f"DEBUG CONTENT 1:\n{insight.content}")
    print("-" * 40)
    
    if "field.add_repulsor" in insight.content:
        print("✅ SUCCESS: Shield System created with Repulsors")
    else:
        print("❌ FAILURE: Shield System missing Repulsors")

    # 2. Test: Create Attack (High Emotion)
    print("\n🧪 Test 2: Create Attack Flow")
    intent = "CREATE: Attack Flow"
    insight = engine.think(intent)
    
    print("-" * 40)
    print(f"DEBUG CONTENT 2:\n{insight.content}")
    print("-" * 40)
    
    if "field.inject_flow" in insight.content:
        print("✅ SUCCESS: Attack Flow created with Velocity")
    else:
        print("❌ FAILURE: Attack Flow missing Velocity")

if __name__ == "__main__":
    test_genesis()
