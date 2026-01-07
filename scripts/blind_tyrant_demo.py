import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_blind_tyrant_demo():
    print("\n--- [ Phase 19: The Blindness of Flesh Demo ] ---\n")
    print("Test: How do different layers perceive the same Saint?")
    
    # 1. The Target: The Saint (Paul)
    # Weak Body, High Spirit
    saint = SubjectiveEgo("Saint_Paul", depth=9)
    saint.state.health = 0.2
    saint.state.rank_tier = 1
    saint.state.spirit_level = 0.95
    
    # 2. Observer A: The Blind Warlord (Body Dominant)
    # Sees only flesh.
    warlord = SubjectiveEgo("Warlord_Grom", depth=2)
    warlord.state.health = 1.0
    warlord.state.spirit_level = 0.1
    warlord.state.rank_tier = 3
    
    # 3. Observer B: The Cunning Vizier (Soul Dominant)
    # Sees power and influence.
    vizier = SubjectiveEgo("Vizier_Jafar", depth=6)
    vizier.state.health = 0.4
    vizier.state.rank_tier = 8
    vizier.state.wealth = 100.0
    vizier.state.spirit_level = 0.3
    
    # 4. Observer C: The Mystic (Spirit Dominant)
    mystic = SubjectiveEgo("Mystic_Sarah", depth=8)
    mystic.state.spirit_level = 0.9
    
    print(f"\nTarget: {saint.state.name} (HP: 0.2, Spirit: 0.95)\n")
    
    # Interaction 1: Warlord vs Saint
    p1 = warlord.perceive_other_power(saint)
    print(f"1. Warlord (Body-Dom) sees Saint as: [{p1}]")
    # Expected: WEAK_PEASANT (Blind to spirit)
    
    if p1 == "WEAK_PEASANT":
        print("   -> 'Hah! Crushing this bug would be too easy.'")
    
    # Interaction 2: Vizier vs Saint
    p2 = vizier.perceive_other_power(saint)
    print(f"\n2. Vizier (Soul-Dom) sees Saint as: [{p2}]")
    # Expected: DANGEROUS_ANOMALY (Senses unseen leverage)
    
    if p2 == "DANGEROUS_ANOMALY":
        print("   -> 'He has no army... yet the people follow him. Treat him with caution.'")
        
    # Interaction 3: Mystic vs Saint
    p3 = mystic.perceive_other_power(saint)
    print(f"\n3. Mystic (Spirit-Dom) sees Saint as: [{p3}]")
    # Expected: KINDRED_SPIRIT
    
    if p3 == "KINDRED_SPIRIT":
        print("   -> 'I see the light within you, brother.'")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    run_blind_tyrant_demo()
