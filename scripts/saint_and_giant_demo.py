import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_trinity_demo():
    print("\n--- [ Phase 18: The Saint and The Giant Demo ] ---\n")
    print("Test: Can Spirit (Love) override Body (Pain) and Soul (Ambition)?")
    
    # 1. The Giant (Goliath)
    # High Body, High Soul (Rank), Low Spirit (Child)
    goliath = SubjectiveEgo("Goliath", depth=7, family_role="Warlord")
    goliath.state.health = 1.0       # Strong Body
    goliath.state.rank_tier = 8      # High Soul/Rank
    goliath.state.wealth = 1000.0    # Rich
    goliath.state.spirit_level = 0.2 # Spiritually immature
    goliath.state.desire_intensity = 0.9
    
    # 2. The Saint (David/Martyr)
    # Low Body, Low Soul, High Spirit (Mature)
    saint = SubjectiveEgo("Saint_Paul", depth=9, family_role="Priest")
    saint.state.health = 0.3         # Weak Body
    saint.state.rank_tier = 1        # Low Soul/Rank
    saint.state.wealth = 0.0         # Poor
    saint.state.spirit_level = 0.95  # Spiritually transcended
    saint.state.desire_intensity = 0.1 # Low worldly desire
    
    print("\n--- Scenario 1: The Torture (Body vs. Spirit) ---")
    print("Applying High Pain (0.8)...")
    
    g_res = goliath.check_spirit_dominance(pain_level=0.8)
    s_res = saint.check_spirit_dominance(pain_level=0.8)
    
    print(f"Goliath (Body 1.0, Spirit 0.2): {g_res}") 
    # Expected: LOWER_SUBMISSION (Body breaks because Spirit is weak)
    
    print(f"Saint (Body 0.3, Spirit 0.95): {s_res}")
    # Expected: TRANSENDED_PAIN (Spirit overrides Body pain)
    
    print("\n--- Scenario 2: The Bribe (Soul vs. Spirit) ---")
    print("Offering Kingdom (Temptation 100.0)...")
    
    g_res_2 = goliath.check_spirit_dominance(temptation_amount=100.0)
    s_res_2 = saint.check_spirit_dominance(temptation_amount=100.0)
    
    print(f"Goliath (Rank 8, Spirit 0.2): {g_res_2}")
    # Expected: CORRUPTED_BY_SOUL (Soul ambition > Spirit conviction)
    
    print(f"Saint (Rank 1, Spirit 0.95): {s_res_2}")
    # Expected: REJECTED_TEMPTATION (Spirit > Soul ambition)

    print("\n* Verification Logic *")
    if g_res == "LOWER_SUBMISSION" and s_res == "TRANSENDED_PAIN":
        print("✅ Trinity Law Confirmed: Spirit maturity dictates pain tolerance.")
    else:
        print("❌ Trinity Law Failed on Pain.")
        
    if g_res_2 == "CORRUPTED_BY_SOUL" and s_res_2 == "REJECTED_TEMPTATION":
        print("✅ Trinity Law Confirmed: Spirit maturity dictates corruption.")
    else:
        print("❌ Trinity Law Failed on Corruption.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR) # Only show errors to keep output clean
    run_trinity_demo()
