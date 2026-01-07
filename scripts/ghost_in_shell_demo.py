import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_ghost_demo():
    print("\n--- [ Phase 17: The Ghost in the Shell Demo ] ---\n")
    
    # 1. Born of Light (Initial State)
    # A generic Adventurer
    print("--- 1. Genesis ---")
    ghost = SubjectiveEgo("Ghost_Unit_7", depth=3, family_role="Seeker")
    print(f"Created {ghost.state.name}. Intent: {ghost.state.current_intent}")
    
    # 2. Life Happens (Narrative Input)
    print("\n--- 2. The Trauma (Memory Injection) ---")
    
    # Mundane event
    ghost.record_memory("I found a rusty sword.", intensity=0.5)
    
    # Traumatic event (High Intensity -> Crystallization)
    ghost.record_memory("The Red Dragon burned my village. I heard the screams.", intensity=2.5, tags=["Fear", "Horror"])
    
    # High Pressure causing Scars
    ghost.state.narrative_pressure = 0.9 
    ghost.state.scars = 0.6 # Simulate scar accumulation
    
    print("Memory recorded. Scars accumulated.")
    
    # 3. The Bridge (Generating the Prompt)
    print("\n--- 3. The Soul Speaks (Context Generation) ---")
    
    llm_prompt = ghost.get_llm_context_prompt()
    
    print("\n[GENERATED SYSTEM PROMPT]")
    print("==============================================")
    print(llm_prompt)
    print("==============================================")
    
    print("\n* Verification Check *")
    if "SCARRED SOUL" in llm_prompt:
        print("✅ Scars are reflected in the persona.")
    if "The Red Dragon" in llm_prompt:
        print("✅ Core Memory (Crystal) is present in context.")
    else:
        print("❌ Core Memory missing!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run_ghost_demo()
