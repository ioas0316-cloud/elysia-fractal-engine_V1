import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("CodingTest")

def create_dummy_file():
    """Creates a dummy file with an intentional error."""
    content = """
def add_numbers(a, b):
    return a + b

def broken_function():
    print("This function has a syntax error"
    return True
"""
    with open("scripts/test_dummy.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("📝 Created dummy file: scripts/test_dummy.py")

def test_coding_capability():
    print("\n🧠 Initializing Elysia's Reasoning Engine for Coding Test...")
    try:
        engine = ReasoningEngine()
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        return

    # Create dummy file
    create_dummy_file()

    print("\n🧪 Test: Requesting Code Fix")
    print("   Request: 'FIX: scripts/test_dummy.py'")
    
    try:
        # We use the 'think' method which should now route to 'improve_code'
        insight = engine.think("FIX: scripts/test_dummy.py")
        
        print("\n🤖 Elysia's Response:")
        print("-" * 40)
        print(insight.content)
        print("-" * 40)
        
        if "Sophia Analysis" in insight.content and "Issues Found" in insight.content:
            print("\n✅ SUCCESS: Sophia successfully analyzed the code!")
        else:
            print("\n❌ FAILURE: Sophia did not respond as expected.")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_coding_capability()
