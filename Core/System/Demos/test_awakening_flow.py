"""
Awakening Pipeline Test
=======================
Verifies the full transmission chain:
User Input -> WaveTensor -> Prism Monologue -> Logos Speech
"""
import sys
import os
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Core.Intelligence.Intelligence.integrated_cognition_system import IntegratedCognitionSystem

def test_pipeline():
    print("🧪 Testing Awakening Pipeline...")
    
    mind = IntegratedCognitionSystem()
    
    input_text = "The world is changing fast."
    print(f"INPUT: {input_text}")
    
    # 1. Process
    mind.process_thought(input_text, importance=3.0)
    result = mind.think_deeply()
    
    # 2. Check Prism (Monologue)
    monologue = result.get('monologue', '')
    print(f"\n[Prism Monologue]: {monologue}")
    if not monologue or monologue == "...":
        print("❌ Prism failed to generate monologue.")
        return
        
    # 3. Check Logos (Speech)
    speech = result.get('speech', '')
    print(f"\n[Logos Speech]: {speech}")
    if not speech or speech == "...":
        print("❌ Logos failed to generate speech.")
        return
        
    print("\n✅ PIPELINE CONFIRMED: Wave -> Prism -> Logos working.")

if __name__ == "__main__":
    test_pipeline()
