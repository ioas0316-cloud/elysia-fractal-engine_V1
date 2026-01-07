"""
TEST MEMORY EVOLUTION: FROM FACT TO WISDOM
==========================================
"History is written by the victors (the surviving neurons)."

This script demonstrates Phase 17: Causal Composting.
1. We inject a raw "Fact" into memory ("I saw an Apple").
2. We run the `CausalCompost` engine.
3. We verify that the memory has mutated into "Wisdom" ("Manifestation of Universal Law").
"""

import sys
import logging
import time

sys.path.insert(0, r"c:\Elysia")
from Core.Foundation.Memory.unified_experience_core import UnifiedExperienceCore, get_experience_core
from Core.Foundation.Memory.causal_compost import CausalCompost

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("TestEvolution")

def test_memory_evolution():
    print("\n🍂 INITIATING CAUSAL COMPOSTING...")
    print("==================================")
    
    # 1. Init
    memory_core = get_experience_core()
    compost = CausalCompost()
    
    # 2. Inject a "Young" Memory (Fact)
    # "Apple" is the kernel we set up in CausalBridge to link to "Newton/Gravity/Law"
    raw_content = "I observed a red Apple falling from the tree."
    print(f"\n[Step 1] Injecting Raw Memory: '{raw_content}'")
    
    result = memory_core.absorb(raw_content, type="perception")
    event_id = result["id"]
    
    # Verify it's there
    stored_event = next(e for e in memory_core.stream if e.id == event_id)
    print(f"   Shape: {stored_event.type} (0D Fact)")
    
    # 3. Trigger Compost (Simulating Time/Dreaming)
    print(f"\n[Step 2] Triggering Composting Process (Simulating Time Decay)...")
    mutated_event = compost.cometing_process(stored_event)
    
    if mutated_event:
        # 4. Rewrite History
        print(f"\n[Step 3] Rewriting History in Hippocampus...")
        memory_core.evolve_memory(event_id, mutated_event)
        
        # 5. Verify Evolution
        evolved_event = next(e for e in memory_core.stream if e.id == event_id)
        print(f"   New Content: \"{evolved_event.content}\"")
        print(f"   New Type:    {evolved_event.type} (4D Wisdom)")
        
        if "Law" in evolved_event.content:
            print("\n✅ SUCCESS: Memory evolved from Apple(Fact) to Law(Wisdom).")
        else:
            print("\n❌ TRAGEDY: The memory rotted but did not bloom.")
            
    else:
        print("\n❌ FAILURE: Compost engine found no deeper truth to evolve into.")

if __name__ == "__main__":
    test_memory_evolution()
