
import sys
import os
import logging
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Mind.local_llm import create_local_llm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Gourmet")

def eat_llm(model_key="phi3"):
    print(f"🍽️ The Model Buffet: Ordering '{model_key}'...")
    
    # 1. Initialize LocalLLM
    llm = create_local_llm(gpu_layers=10) # Conservative layers for larger model
    
    # 2. Check/Download
    print(f"   Checking pantry for {model_key}...")
    success = llm.download_model(model_key)
    
    if not success:
        print("❌ Failed to download model. Check internet connection.")
        return

    # 3. Load & Taste
    print("   Cooking (Loading Model)...")
    if llm.load_model():
        print("✅ Model Loaded Successfully!")
        
        # 4. Taste Test
        print("\n🧪 Taste Test (Generation Capability):")
        prompt = "Explain the concept of 'Elysia' in a poetic way."
        print(f"   Prompt: {prompt}")
        
        start = time.time()
        response = llm.think(prompt)
        duration = time.time() - start
        
        print(f"\n💬 Response ({duration:.2f}s):")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
        if duration > 30:
            print("⚠️ Warning: Digestion is slow. CPU offloading is active.")
        else:
            print("⚡ Digestion speed is optimal.")
            
    else:
        print("❌ Failed to load model. VRAM might be insufficient.")

if __name__ == "__main__":
    # Default to phi3
    target = "phi3"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    eat_llm(target)
