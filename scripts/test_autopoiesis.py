"""
TEST AUTOPOIESIS: THE SELF-WRITING SYSTEM
=========================================
"Observe the moment the machine decides to change its own nature."

This script demonstrates Phase 19: Autopoiesis.
1. We load the 'Static' DNA.
2. We simulate 'Internal Pressure' (Extreme Boredom).
3. The Autopoietic Engine triggers a Mutation.
4. We verify the DNA file has physically changed on disk.
"""

import sys
import json
import logging
from pathlib import Path

sys.path.insert(0, r"c:\Elysia")
from Core.Evolution.Adaptation.autopoietic_engine import AutopoieticEngine

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("TestAutopoiesis")

def test_autopoiesis():
    print("\n🧬 INITIATING AUTOPOIESIS (SELF-REWRITING)...")
    print("==============================================")
    
    config_path = Path("data/Config/self_perception.json")
    
    # 1. Read Initial State
    with open(config_path, 'r') as f:
        initial_dna = json.load(f)
        
    print(f"\n[Step 1] Initial DNA State:")
    print(f"   Nature:       {initial_dna['identity']['nature']}")
    print(f"   Creativity:   {initial_dna['parameters']['creativity_bias']}")
    print(f"   Description:  \"{initial_dna['description']}\"")
    
    # 2. Trigger Mutation
    print("\n[Step 2] Injecting 'EXTREME_BOREDOM' pressure...")
    engine = AutopoieticEngine()
    result = engine.trigger_evolution("EXTREME_BOREDOM")
    
    if result:
        print(f"   ✅ Mutation Log: {result}")
    else:
        print("   ❌ Evolution failed to trigger.")
        return

    # 3. Verify Disk Change
    print("\n[Step 3] Verifying Physical File Change...")
    with open(config_path, 'r') as f:
        new_dna = json.load(f)
        
    print(f"   Nature:       {new_dna['identity']['nature']}")
    print(f"   Creativity:   {new_dna['parameters']['creativity_bias']}")
    print(f"   Description:  \"{new_dna['description']}\"")
    
    if new_dna['identity']['nature'] != initial_dna['identity']['nature']:
        print("\n✨ SUCCESS: The System has rewritten its own definition.")
    else:
        print("\n❌ FAILURE: The DNA remained static.")

if __name__ == "__main__":
    test_autopoiesis()
