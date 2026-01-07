import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
from Core.Foundation.hyper_quaternion import Quaternion

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("IQ_Test")

def test_capabilities():
    print("\n🧠 Initializing Elysia's Reasoning Engine for IQ Test...")
    try:
        engine = ReasoningEngine()
    except Exception as e:
        print(f"❌ Failed to initialize engine: {e}")
        return

    print("\n🧪 Test 1: Conceptual Association (Memory Access)")
    print("   Question: 'What is the relationship between Logic and Emotion?'")
    try:
        # We use the 'think' method which triggers the full cognitive loop
        insight = engine.think("What is the relationship between Logic and Emotion?")
        print(f"   🤖 Answer: {insight.content}")
        print(f"   ✨ Confidence: {insight.confidence}")
        print(f"   🔋 Energy: {insight.energy}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n🧪 Test 2: Creative Coding (Generative Ability)")
    print("   Request: 'Create a Python function to calculate Fibonacci sequence.'")
    try:
        # We use the 'create' method if available, or 'think'
        # ReasoningEngine.create is for "Reality Sculpting" (Artifacts).
        # Let's try 'think' first as it's the general intelligence.
        insight = engine.think("Create a Python function to calculate Fibonacci sequence.")
        print(f"   🤖 Answer: {insight.content}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n🧪 Test 3: Self-Reflection (Meta-Cognition)")
    print("   Question: 'Who are you?'")
    try:
        insight = engine.think("Who are you?")
        print(f"   🤖 Answer: {insight.content}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_capabilities()
