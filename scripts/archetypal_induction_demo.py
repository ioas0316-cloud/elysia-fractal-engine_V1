"""
Archetypal Induction Demo: The 3x3 Enneagram Paths 🥋📜🛡️

"Inducing life through the tension of archetypes."

This script demonstrates how NPCs follow different life paths (Body, Soul, Spirit)
and how their behavior is induced by the ontological gravity of their domain.
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.septenary_axis import SeptenaryAxis

def run_induction_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*85)
    print("      [ ELYSIA: ARCHETYPAL INDUCTION - THE 3-DOMAIN PATHS ]")
    print("="*85)
    
    # 1. Manifest NPCs across the three archetypal paths
    pete = SubjectiveEgo("Blacksmith_Pete", depth=1)  # Body Apprentice
    kain = SubjectiveEgo("Warrior_Kain", depth=3)     # Body Mastery
    merch = SubjectiveEgo("Merchant_Lin", depth=4)    # Soul Apprentice
    quin = SubjectiveEgo("Ruler_Quinella", depth=6)   # Soul Mastery
    priest = SubjectiveEgo("Priest_Eugeo", depth=7)   # Spirit Apprentice
    selka = SubjectiveEgo("Saint_Selka", depth=9)     # Spirit Mastery
    
    npcs = [pete, kain, merch, quin, priest, selka]
    
    print(f"\n[System] 6 NPCs manifested across Body(Warrior), Soul(Ruler), and Spirit(Saint) paths.")
    
    # 2. Daily Life Simulation (Archetypal Tension at work)
    print("\n" + "-"*85)
    print(" SIMULATION: The world breathes. Archetypes induce behavior.")
    print("-"*85)
    
    for _ in range(2): # Two cycles of induction
        for npc in npcs:
            action = npc.perform_action()
            time.sleep(0.1)
        print("-" * 50)

    # 3. Reflection of Maturation
    print("\n[Admin] Observation Results:")
    for npc in npcs:
        level = npc.axis.get_level(npc.state.septenary_depth)
        print(f"[{npc.state.name}] Path: {npc.state.archetype_path} | Depth: {npc.state.septenary_depth}")
        print(f" └─ Inductive Law: {level.inductive_logic}")
    
    print("\n[System] Behavior was induced by the tension of the 3x3 fractal hierarchy.")
    print("="*85)

if __name__ == "__main__":
    run_induction_demo()
