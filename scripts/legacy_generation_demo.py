"""
Legacy Generation Demo: The Akashic Thread & The Orphan's Choice 🧬✨

"Infinite possibilities depend on environment, conditions, and the heart's resonance."

This script demonstrates:
1. The Ascension of a Master (recording a legacy).
2. The divergence of an Orphan's life path based on environmental resonance:
   - Path A: Exploitation -> Villainous Legacy
   - Path B: Warmth/Salvation -> Saintly Legacy
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.memetic_legacy import AkashicField, SpiritualDNA

def run_legacy_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*85)
    print("      [ ELYSIA: THE ORPHAN'S CHOICE - MORAL POLARITY DEMO ]")
    print("="*85)
    
    field = AkashicField()
    
    # 1. Prepare two different legacies
    print("\n[Chapter 1: The Two Legacies]")
    
    # The Exploitative Master (Cold/Villainous)
    lord_v = SubjectiveEgo("Lord_Vax", depth=5)
    lord_v.dna.technique, lord_v.dna.moral_valence = 0.8, 0.05 # High tech, low moral
    lord_v.leave_legacy(field, (1.0, 1.0, 0, 0)) # Slums/Exploitation area
    
    # The Compassionate Priest (Warm/Saintly)
    priest_e = SubjectiveEgo("Priest_Elias", depth=5)
    priest_e.dna.technique, priest_e.dna.moral_valence = 0.5, 0.95 # Mid tech, high moral
    priest_e.leave_legacy(field, (9.0, 9.0, 0, 0)) # Temple/Warmth area
    
    print("\n[System] Two Akashic Echoes registered: 'Lord_Vax' (Cold) and 'Priest_Elias' (Warm).")
    
    # 2. The Orphan's Path (The Divergence)
    print("\n" + "-"*85)
    print("[Chapter 2: The Orphan's Divergence]")
    
    # Scenario A: Orphan in the Slums (Exploitation)
    orphan_a = SubjectiveEgo("Orphan_Kael", depth=1)
    orphan_a.state.satisfaction = 0.1 # Absolute suffering
    print(f"\n[Scenario A] {orphan_a.state.name} is struggling in the slums...")
    
    echo_v = field.find_nearest_echo((1.1, 1.1, 0, 0))
    if echo_v:
        print(f"⚠️ Resonating with '{echo_v.original_name}' Echo. {orphan_a.state.name} inherits the cold spirit of exploitation.")
        orphan_a.learn_from_master(echo_v.dna)
        orphan_a.update(1.0)
        print(orphan_a.get_subjective_report())
    
    # Scenario B: Orphan in the Temple (Warmth)
    orphan_b = SubjectiveEgo("Orphan_Lira", depth=1)
    orphan_b.state.satisfaction = 0.6 # Receiving basic care
    print(f"\n[Scenario B] {orphan_b.state.name} is found by the temple...")
    
    echo_e = field.find_nearest_echo((8.9, 9.1, 0, 0))
    if echo_e:
        print(f"✨ Resonating with '{echo_e.original_name}' Echo. {orphan_b.state.name} inherits the warm spirit of compassion.")
        orphan_b.learn_from_master(echo_e.dna)
        orphan_b.update(1.0)
        print(orphan_b.get_subjective_report())
    
    print("\n[Admin] Result: Environment and inherited spirit shaped two souls into opposite poles.")
    print("="*85)

if __name__ == "__main__":
    run_legacy_demo()
