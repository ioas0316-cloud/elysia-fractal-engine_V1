"""
Noble Family Demo: The 4 Brothers and the Cold Legacy 🏰⚖️🛡️

"The story is always in the making. Kinship is the lattice of fate."

This script demonstrates the divergent paths of 4 brothers in a noble family:
1. The FirstBorn (Authority/Legacy)
2. The SecondBorn (Calculating/Survival)
3. The ThirdBorn (Escape/Independence)
4. The LastBorn (Rebellion/Outcast)

It also showcases 'Counter-Resonance' – rejecting the Father's cold nature.
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.memetic_legacy import SpiritualDNA

def run_noble_family_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*85)
    print("      [ ELYSIA: NOBLE FAMILY DYNAMICS - THE 4 BROTHERS ]")
    print("="*85)
    
    # The Father: A cold, ambitious Noble
    father_dna = SpiritualDNA(technique=0.8, reason=0.7, meaning=0.4, moral_valence=0.1, archetype_path="Noble")
    print(f"[System] The Father's Spirit: Technique(0.8), Morality(0.1 - Cold Authority)")
    
    # 1. The Brothers Manifest
    print("\n[Chapter 1: The Siblings Manifest]")
    
    # First: The Heir (High gravity, accepts legacy)
    prain = SubjectiveEgo("Prain_The_Heir", depth=3, family_role="FirstBorn")
    prain.learn_from_master(father_dna, counter=False)
    
    # Second: The Shrewd (Middle gravity, calculating)
    leom = SubjectiveEgo("Leom_The_Shrewd", depth=2, family_role="MiddleBorn")
    leom.learn_from_master(father_dna, counter=False)
    
    # Third: The Seeker (Low gravity, wants to be a Merchant)
    maro = SubjectiveEgo("Maro_The_Seeker", depth=1, family_role="Outcast") # Outcast gravity
    
    # Fourth: The Rebel (Counter-Resonance)
    kurt = SubjectiveEgo("Kurt_The_Rebel", depth=1, family_role="LastBorn")
    kurt.learn_from_master(father_dna, counter=True) # REJECTS THE COLD LEGACY
    
    brothers = [prain, leom, maro, kurt]
    
    # 2. Simulation over time
    print("\n" + "-"*85)
    print("[Chapter 2: The Lattice of Fate - Life Unfolds]")
    print("-"*85)
    
    for cycle in range(3):
        print(f"\n--- Cycle {cycle+1}: The World Breathes ---")
        for bro in brothers:
            # Random events affecting satisfaction
            import random
            bro.state.satisfaction = max(0.0, min(1.0, bro.state.satisfaction + random.uniform(-0.1, 0.1)))
            bro.update(1.0)
            bro.perform_action()
            time.sleep(0.1)

    # 3. Final Report
    print("\n" + "-"*85)
    print("[Chapter 3: Final Destinies]")
    print("-"*85)
    for bro in brothers:
        print(bro.get_subjective_report())
        if bro.state.current_intent == "Prepare for Adventure":
            print(f" ✨ STATUS: {bro.state.name} has AWAKENED! Leaving the noble house.")
        elif bro.state.dissonance > 0.5:
            print(f" 💔 STATUS: {bro.state.name} is in deep INTERNAL CONFLICT.")
        print("-" * 30)

    print("\n[Admin] Kinship lattice complete. Variation is induced by position and choice.")
    print("="*85)

if __name__ == "__main__":
    run_noble_family_demo()
