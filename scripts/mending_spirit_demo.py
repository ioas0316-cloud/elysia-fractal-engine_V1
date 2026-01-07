import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.memetic_legacy import RegionalField

def run_mending_demo():
    print("\n--- [ Phase 13: Trauma, Grace & Relational Induction Demo ] ---\n")
    
    # 1. Setup Region: The Land of Trials (High Friction)
    from Core.Intelligence.Reasoning.memetic_legacy import SpiritualDNA
    ethos = SpiritualDNA(technique=0.8, reason=0.2, meaning=0.5)
    trials = RegionalField("Land of Trials", dominant_archetype="Warrior", ethos_dna=ethos)
    
    # 2. Setup NPCs
    # Shin: Broken from Phase 12
    shin = SubjectiveEgo("Shin_The_Broken", depth=1, region=trials)
    shin.state.is_broken = True
    shin.state.stability = 0.0
    shin.state.scars = 0.8
    
    # Kai: The Hero who will provide grace
    kai = SubjectiveEgo("Kai_The_Herald", depth=5, family_role="Adventurer", region=trials)
    kai.state.heroic_intensity = 2.5
    
    # Leo: The Noble bound by Institutional Inertia
    leo = SubjectiveEgo("Prince_Leo", depth=6, family_role="Noble", region=trials)
    leo.dna.realization = {"tech": 0.2, "res": 0.2, "mean": 0.2} # Purely flat (taught)
    leo.state.scars = 0.3 # Small trauma from expectations
    
    npcs = [shin, kai, leo]
    
    print("Initial State:")
    for npc in npcs:
        print(npc.get_subjective_report())
    
    # Simulation Cycle 1: The Encounter
    print("\n--- Cycle 1: The Herald's Grace ---")
    kai.interact_with(shin)
    kai.interact_with(leo)
    
    for npc in npcs:
        npc.update(1.0)
        print(npc.get_subjective_report())
        
    # Simulation Cycle 2: Heavy Pressure (Trying to transcend inertia)
    print("\n--- Cycle 2: Trying to Transcend ---")
    leo.state.desire_intensity = 1.0 # Intense desire to be an adventurer
    
    for _ in range(3):
        for npc in npcs:
            npc.update(1.0)
            
    print("\nFinal State after 5 ticks:")
    for npc in npcs:
        print(npc.get_subjective_report())
    
    if not shin.state.is_broken:
        print("\n✨ SHIN IS NO LONGER BROKEN! The Herald's grace mended his spirit.")
    else:
        print("\n🌑 Shin's spirit remains fractured. He needs more grace.")
        
    if leo.state.archetype_path != "Adventurer":
        print("🧱 LEO remains a Noble. His Structural Inertia is too high for his current depth.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run_mending_demo()
