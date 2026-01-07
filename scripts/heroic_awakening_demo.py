"""
Heroic Awakening Demo: The Fate of the Seed ⚔️🌱

This demo showcases:
1. Institutional Ceiling: Nobles hitting a growth cap due to 'Flat' (Taught) knowledge.
2. Seed Vulnerability: High pressure breaking young souls before they can grow.
3. Heroic Inversion: High-potential souls converting friction into intensity and transcending.
"""

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.memetic_legacy import RegionalField, SpiritualDNA
import time

def run_awakening_demo():
    print("=====================================================================================")
    print("🎨 [Chapter 1: The Three Seeds]")
    print("=====================================================================================")
    
    # Define a Harsh Region: The Cursed Borderlands (Warrior Ethos)
    harsh_border = RegionalField(
        name="Cursed_Borderlands",
        dominant_archetype="Warrior/Blacksmith",
        ethos_dna=SpiritualDNA(moral_valence=0.3) # Cold/Pragmatic
    )
    
    # 1. Prince Leo: The Institutionalized (Starts at Level 5, Flat knowledge)
    leo = SubjectiveEgo("Prince_Leo", depth=5, family_role="FirstBorn", region=harsh_border)
    leo.state.kismet = 0.5
    leo.dna.potency = {"tech": 0.5, "res": 0.5, "mean": 0.5}
    leo.dna.realization = {"tech": 0.2, "res": 0.2, "mean": 0.2} # Purely flat (Taught)
    leo.state.desire_intensity = 0.9 # High ambition
    leo.state.satisfaction = 0.1 # Very frustrated -> High pressure
    
    # 2. Shin: The Broken Seed (Orphan, High Potential, Bad Luck)
    shin = SubjectiveEgo("Shin_The_Orphan", depth=4, family_role="Outcast", region=harsh_border)
    shin.state.kismet = 0.05 # Terrible luck
    shin.dna.potency = {"res": 1.0} 
    shin.state.desire_intensity = 1.5 
    
    # 3. Kai: The Protagonist (Orphan, High Potential, Good Luck)
    kai = SubjectiveEgo("Kai_The_Destined", depth=4, family_role="Outcast", region=harsh_border)
    kai.state.kismet = 0.9 # Good luck/timing (Dampens pressure significantly)
    kai.dna.potency = {"res": 1.0} 
    kai.state.desire_intensity = 1.5 

    characters = [leo, shin, kai]
    
    print("\n[Admin] Simulating 15 cycles of Fate...")
    for i in range(15):
        print(f"\n--- Cycle {i+1} ---")
        for char in characters:
            char.update(dt=1.0)
            char.perform_action()

    print("\n=====================================================================================")
    print("🎨 [Chapter 2: The Final Report]")
    print("=====================================================================================")
    for char in characters:
        print(char.get_subjective_report())
        print("-" * 50)

    print("\n[Conclusion]")
    print("1. Prince Leo hit a 'Ceiling' because his knowledge was never 'felt' (Realization < 0.5).")
    print("2. Shin had the potential, but the 'Seed Phase' pressure combined with low Kismet broke him.")
    print("3. Kai survived the seed phase thanks to high Kismet, and his friction became Heroic Intensity.")
    print("=====================================================================================")

if __name__ == "__main__":
    run_awakening_demo()
