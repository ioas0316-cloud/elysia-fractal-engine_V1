"""
Regional Ethos Demo: The Mage and the Northern Gale ❄️🛡️✨

"Environment is the invisible law. To be abnormal is to feel the weight of the world."

This script demonstrates 'Regional Induction':
1. A Mage attempting to exist in a Warrior-centric region (High Friction/Stigma).
2. A Mage thriving in an intellectual region (Low Friction/Normalcy).
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.memetic_legacy import SpiritualDNA, RegionalField

def run_regional_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*85)
    print("      [ ELYSIA: REGIONAL ETHOS - THE MAGE'S BURDEN ]")
    print("="*85)
    
    # 1. Define Regions
    # The Frozen North: Values strength, physical mastery, and cold honor.
    north_ethos = SpiritualDNA(technique=0.9, reason=0.2, meaning=0.1, moral_valence=0.1)
    frozen_north = RegionalField("Frozen_North", dominant_archetype="Warrior/Blacksmith", ethos_dna=north_ethos)
    
    # The Magic Tower: Values reason, synthesis, and intellectual warmth.
    tower_ethos = SpiritualDNA(technique=0.3, reason=0.9, meaning=0.7, moral_valence=0.8)
    magic_tower = RegionalField("Magic_Tower", dominant_archetype="Mage/Merchant/Ruler", ethos_dna=tower_ethos)
    
    print(f"[System] Defined {frozen_north.name} (Warrior Ethos) and {magic_tower.name} (Mage Ethos).")
    
    # 2. The Characters
    print("\n" + "-"*85)
    print("[Chapter 1: The 'Abnormal' and the 'Natural']")
    
    # Kael: A Mage born in the North (High Friction)
    kael = SubjectiveEgo("Kael_The_Awkward", depth=4, region=frozen_north)
    kael.state.archetype_path = "Mage/Merchant/Ruler" # Manually override for the demo
    kael.state.satisfaction = 0.5
    
    # Lira: A Mage born in the Tower (Low Friction)
    lira = SubjectiveEgo("Lira_The_Scholar", depth=4, region=magic_tower)
    lira.state.archetype_path = "Mage/Merchant/Ruler"
    lira.state.satisfaction = 0.8
    
    # 3. Simulation
    print("\n[Chapter 2: The Weight of Atmosphere]")
    for cycle in range(3):
        print(f"\n--- Cycle {cycle+1} ---")
        kael.update(1.0)
        lira.update(1.0)
        
        kael.perform_action()
        lira.perform_action()
        time.sleep(0.1)
        
    # 4. Final Comparison
    print("\n" + "-"*85)
    print("[Chapter 3: The Result of Inductive Pressure]")
    print("-"*85)
    print(kael.get_subjective_report())
    if kael.state.regional_friction > 0.4:
         print(f" ⚠️ LOG: Kael is considered 'Mol-Sang-Sik' (Absurd) in his village.")
         
    print("\n" + "-"*15)
    print(lira.get_subjective_report())
    if lira.state.regional_friction < 0.2:
         print(f" ✨ LOG: Lira is a respected scholar of the ivory halls.")

    print("\n[Admin] Worldview Induction complete. Regional 'Common Sense' is an invisible field.")
    print("="*85)

if __name__ == "__main__":
    run_regional_demo()
