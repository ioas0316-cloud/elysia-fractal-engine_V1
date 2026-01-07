import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_passion_demo():
    print("\n--- [ Phase 20: The Passion Demo (Disciple Screening) ] ---\n")
    print("Test: Who remains when the Master faces the Cross?")
    
    # 1. The Master
    jesus = SubjectiveEgo("The_Master", depth=10, family_role="Messiah")
    
    # 2. The Crowd (Body Grace)
    crowd = SubjectiveEgo("Crowd_Member", depth=1)
    crowd.receive_grace(1.0, type="BODY", master_name="The_Master")
    
    # 3. The Traitor (Soul Grace)
    judas = SubjectiveEgo("Judas", depth=5)
    judas.receive_grace(1.0, type="SOUL", master_name="The_Master")
    
    # 4. The Disciple (Spirit Grace)
    peter = SubjectiveEgo("Peter", depth=3)
    peter.receive_grace(1.0, type="SPIRIT", master_name="The_Master")
    
    print("\n--- Scenario: The Arrest (Crisis Intensity 0.8) ---")
    
    # Test Crowd
    res1 = crowd.test_faith(0.8)
    print(f"1. Crowd (Fed Bread): [{res1}]")
    if res1 == "FLEE":
        print("   -> 'I am hungry, but I don't want to die! Run!'")
        
    # Test Traitor
    res2 = judas.test_faith(0.8)
    print(f"2. Traitor (Given Power): [{res2}]")
    if res2 == "BETRAY":
        print("   -> 'He is failing. I must save my own position. I surrender him.'")
        
    # Test Disciple
    res3 = peter.test_faith(0.8)
    print(f"3. Disciple (Given Essence): [{res3}]")
    if res3 == "MARTYR":
        print("   -> 'Lord, I will go with you to prison and to death.'")
        print("   -> [SYSTEM] Spiritual DNA Inherited. The Seed multiplies.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    run_passion_demo()
