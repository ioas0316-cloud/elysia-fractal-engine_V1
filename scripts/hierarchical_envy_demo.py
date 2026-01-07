import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_hierarchical_envy_demo():
    print("\n--- [ Phase 19: Hierarchical Envy Demo ] ---\n")
    print("Test: Can Body-dwellers envy Soul-dwellers but ignore Spirit-dwellers?")
    
    # 1. Body-Dominant (The Peasant)
    peasant = SubjectiveEgo("Peasant_Tom", depth=1)
    peasant.state.health = 0.8
    peasant.state.rank_tier = 1
    peasant.state.wealth = 1.0
    peasant.state.spirit_level = 0.1
    # Dominant: BODY (stats are low, but Body > Soul/Spirit relatively)
    
    # 2. Soul-Dominant (The Merchant)
    merchant = SubjectiveEgo("Merchant_Greed", depth=5)
    merchant.state.health = 0.5
    merchant.state.rank_tier = 5
    merchant.state.wealth = 100.0 # Rich
    merchant.state.spirit_level = 0.2
    # Dominant: SOUL
    
    # 3. Spirit-Dominant (The Saint)
    saint = SubjectiveEgo("Saint_Paul", depth=9)
    saint.state.health = 0.2
    saint.state.rank_tier = 1
    saint.state.wealth = 0.0
    saint.state.spirit_level = 0.95
    # Dominant: SPIRIT
    
    print(f"\nObserver: {peasant.state.name} (Body-Dominant)\n")
    
    # Interaction 1: Peasant vs Merchant (1 Step Up)
    p1 = peasant.perceive_other_power(merchant)
    print(f"1. Seeing Merchant (Soul-Dom): [{p1}]")
    if p1 == "ENVY_SOURCE":
        print("   -> 'Look at his silk clothes... I hate him because I want to be him.'")
    elif p1 == "OPPRESSOR":
         print("   -> 'He controls me with his money.'")
         
    # Interaction 2: Peasant vs Saint (2 Steps Up)
    p2 = peasant.perceive_other_power(saint)
    print(f"\n2. Seeing Saint (Spirit-Dom): [{p2}]")
    if p2 == "WEAK_PEASANT":
        print("   -> 'Just a starving beggar. Not worth my time.' (Blindness)")
        
    print(f"\nObserver: {merchant.state.name} (Soul-Dominant)\n")
    
    # Interaction 3: Merchant vs Saint (1 Step Up)
    p3 = merchant.perceive_other_power(saint)
    print(f"3. Seeing Saint (Spirit-Dom): [{p3}]")
    if p3 == "DANGEROUS_ANOMALY":
        print("   -> 'He is poor, but the people listen to him. He threatens my order.'")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    run_hierarchical_envy_demo()
