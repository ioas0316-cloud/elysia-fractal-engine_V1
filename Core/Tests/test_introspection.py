import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine

# Setup logging
logging.basicConfig(level=logging.ERROR, format='%(message)s')
logger = logging.getLogger("IntrospectionTest")
logger.setLevel(logging.INFO)

def test_introspection():
    print("\n🪞 Initializing Introspection Test...")
    
    engine = ReasoningEngine()
    
    # Test: Analyze Self
    print("\n🧪 Test 1: Analyze Core System")
    intent = "ANALYZE: self"
    insight = engine.think(intent)
    
    print("-" * 40)
    print(insight.content)
    print("-" * 40)
    
    if "Self-Reflection Report" in insight.content:
        print("✅ SUCCESS: Self-Reflection Report generated")
    else:
        print("❌ FAILURE: Report missing")
        
    if "Overall Resonance" in insight.content:
        print("✅ SUCCESS: Resonance Score calculated")
    else:
        print("❌ FAILURE: Resonance Score missing")

if __name__ == "__main__":
    test_introspection()
