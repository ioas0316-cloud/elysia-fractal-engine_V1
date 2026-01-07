
import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Mind.llm_cortex import LLMCortex

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_async():
    print("⏳ Project: Chronos Unbound - Testing Time Sovereignty...")
    
    # 1. Initialize
    # We use 'prefer_local=True' but if Llama-3 isn't loaded by default, 
    # we might need to manually load it or just rely on the fact that 
    # 'think' will take some time (or we can simulate it).
    # For this test, we'll assume whatever model is there (or Resonance) works.
    cortex = LLMCortex(prefer_local=True)
    
    # To make sure it's "heavy", we can manually inject a delay in the think function
    # if we were mocking, but here we want to test the real threading.
    # If using Resonance/Small model, it might be too fast to notice.
    # So we will wrap the think call in a delay for demonstration if needed.
    # But let's try the real 'think_async' first.
    
    print("\n1. Starting Heavy Thought (Async)...")
    prompt = "Write a very long and detailed poem about the concept of Eternity and the heat death of the universe."
    response = cortex.think_async(prompt)
    print(f"   Immediate Response: {response}")
    
    print("\n2. Multitasking (While thinking)...")
    for i in range(5):
        # While the background thread is running, we should be able to do other things
        # Here we just check for insights, but in a real loop we'd process other inputs.
        
        # Simulate a light interaction
        print(f"   [Time {i}] User: 'Are you there?' -> Elysia: 'Yes, I am here.' (Instant)")
        
        # Check for insight
        insight = cortex.check_subconscious()
        if insight:
            print(f"\n✨ EUREKA! Insight received at Time {i}:")
            print("-" * 40)
            print(insight[:200] + "...") # Print first 200 chars
            print("-" * 40)
            break
            
        time.sleep(1)
        
    # If not finished yet, wait a bit more
    if not insight:
        print("\n   (Still thinking... waiting for completion)")
        while True:
            insight = cortex.check_subconscious()
            if insight:
                print(f"\n✨ EUREKA! Insight received:")
                print("-" * 40)
                print(insight[:200] + "...")
                print("-" * 40)
                break
            time.sleep(1)
            print(".", end="", flush=True)

if __name__ == "__main__":
    test_async()
