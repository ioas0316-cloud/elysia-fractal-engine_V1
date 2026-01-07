import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_misunderstood_saint_demo():
    print("\n--- [ Phase 19: The Misunderstood Saint Demo ] ---\n")
    print("Test: Perception changes based on Experiential Grace.")
    
    # 1. The Saint (Spirit Dominant)
    saint = SubjectiveEgo("Saint_Paul", depth=9)
    saint.state.spirit_level = 0.95
    saint.state.health = 0.3
    
    # 2. Peasant A: The Skeptic (No Grace)
    skeptic = SubjectiveEgo("Skeptic_Thomas", depth=1)
    skeptic.state.spirit_level = 0.1
    skeptic.state.health = 0.8
    skeptic.state.grace_received = 0.0 # Never helped
    
    # 3. Peasant B: The Healed (Grace Received)
    healed = SubjectiveEgo("Healed_Mary", depth=1)
    healed.state.spirit_level = 0.15
    healed.state.health = 0.8
    healed.state.grace_received = 1.0 # Received miracle
    
    print(f"\nTarget: {saint.state.name} (Spirit-Dom)\n")
    
    # Interaction 1: Skeptic vs Saint
    p1 = skeptic.perceive_other_power(saint)
    print(f"1. Skeptic (No Grace) sees Saint as: [{p1}]")
    if p1 == "WEAK_HYPOCRITE":
        print("   -> 'Look at that beggar acting holy. He's just lazy.'")
    elif p1 == "WEAK_PEASANT":
        print("   -> 'Just another weakling.'")
        
    # Interaction 2: Healed vs Saint
    p2 = healed.perceive_other_power(saint)
    print(f"\n2. Healed (Has Grace) sees Saint as: [{p2}]")
    if p2 == "SAVIOR":
        print("   -> 'My eyes were open when he healed me. I see his true power.'")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    run_misunderstood_saint_demo()
