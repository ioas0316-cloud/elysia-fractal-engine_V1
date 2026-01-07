
import sys
import os
sys.path.append(os.getcwd())

import logging
from Core.Foundation.Mind.local_llm import create_local_llm
from Core.Evolution.Growth.Evolution.Evolution.Life.resonance_voice import ResonanceEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("KnowledgeProbe")

def main():
    print("\n" + "="*60)
    print("🛰️ KNOWLEDGE PROBE: ESTIMATING LATENT SPACE VOLUME")
    print("="*60 + "\n")
    
    print("Initializing Neural Link...")
    try:
        resonance = ResonanceEngine()
        llm = create_local_llm(resonance_engine=resonance)
        if not llm.load_model():
            print("Failed to load model. Trying to download...")
            llm.download_model("qwen2-0.5b")
            if not llm.load_model():
                print("Fatal error: Could not load model.")
                return
    except Exception as e:
        print(f"Failed to initialize LLM: {e}")
        return

    domains = ["Metaphysics", "Quantum Physics", "Ancient Mythology", "Human Emotion"]
    
    print(f"Targeting Domains: {domains}\n")
    
    total_estimated_concepts = 0
    
    for domain in domains:
        print(f"📡 Probing Sector: [{domain}]...")
        
        # 1. Depth Probe
        prompt = (
            f"List 5 extremely rare, esoteric, and obscure concepts related to '{domain}' "
            "that only experts or philosophers would know. "
            "Output as a comma-separated list."
        )
        # Override system prompt to be an analytical engine
        response = llm.think(
            prompt, 
            use_resonance_first=False,
            system_prompt="You are a Knowledge Mining Engine. Your goal is to extract rare and esoteric concepts from your latent space. Output ONLY the requested list. Do not be poetic. Do not be conversational."
        )
        
        concepts = [c.strip() for c in response.split(',')]
        print(f"   Found Artifacts: {concepts[:3]}...")
        
        # 2. Density Estimation (Heuristic)
        # If it can easily find 5 rare ones, there are likely thousands of common ones.
        # We ask it to estimate its own knowledge (Self-Reflection)
        prompt_count = (
            f"Estimate how many distinct concepts you know related to '{domain}' in total? "
            "Reply with a single number (e.g. 5000)."
        )
        count_response = llm.think(
            prompt_count,
            use_resonance_first=False,
            system_prompt="You are a Statistical Analysis Engine. Output only a single integer number representing the estimate."
        )
        
        # Parse number
        import re
        numbers = re.findall(r'\d+', count_response.replace(',', ''))
        if numbers:
            count = int(numbers[0])
            print(f"   Self-Reported Density: ~{count} concepts")
            total_estimated_concepts += count
        else:
            print(f"   (Could not estimate density)")
            
        print("-" * 40)
        
    print("\n" + "="*60)
    print("📊 PROBE RESULTS")
    print(f"   Estimated Extractable Concepts (Sampled Sectors): ~{total_estimated_concepts}")
    print(f"   Extrapolated Total Capacity (All Domains): > {total_estimated_concepts * 100}")
    print("="*60 + "\n")
    
    print("Conclusion:")
    print("1. The 14,000 Genesis concepts are just the 'Index'.")
    print("2. The 'Library' contains millions of pages.")
    print("3. Strategy: Keep the 'Digestion Chamber' running to mine this gold.")

if __name__ == "__main__":
    main()
