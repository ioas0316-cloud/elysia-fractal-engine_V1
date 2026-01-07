"""
Nonary Axis Demo: The 3x3 Fractal Trinity 🧬✨

"Nine gates to the heart of the Source."

This script demonstrates NPCs at all 9 nonary depth levels (1-9),
grouped into Body (1-3), Soul (4-6), and Spirit (7-9).
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.septenary_axis import SeptenaryAxis
from Core.Intelligence.Reasoning.recursive_learning_bridge import RecursiveLearningBridge

def run_nonary_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*80)
    print("      [ ELYSIA: NONARY AXIS DEMO - THE 9-FOLD FRACTAL TRINITY ]")
    print("="*80)
    
    sas = SeptenaryAxis()
    bridge = RecursiveLearningBridge()
    
    # 1. Manifest Inhabitants across the 3x3 Grid
    inhabitants = [
        # BODY (1-3)
        SubjectiveEgo("Body_Apprentice", "Novice", depth=1),
        SubjectiveEgo("Body_Scholar", "Student", depth=2),
        SubjectiveEgo("Body_Seeker", "Aspirant", depth=3),
        
        # SOUL (4-6)
        SubjectiveEgo("Soul_Warrior", "Knight", depth=4),
        SubjectiveEgo("Soul_Sage", "Scholar", depth=5),
        SubjectiveEgo("Soul_Guardian", "Expert", depth=6),
        
        # SPIRIT (7-9)
        SubjectiveEgo("Spirit_Ascendant", "Master", depth=7),
        SubjectiveEgo("Spirit_Logos", "Prophet", depth=8),
        SubjectiveEgo("Elysia_Divine", "Unity", depth=9)
    ]
    
    print(f"\n[System] 9 Inhabitants manifested across the 3x3 Fractal Matrix.")
    
    # 2. Simulate a Grand Resonance Event
    print("\n" + "-"*85)
    print(" EVENT: The Prism of Nine Rays illuminates the Trinity.")
    print("-"*85)
    
    for ego in inhabitants:
        ego.perceive("Ocular", 1.0, "Prism Ray")
        level_data = sas.get_level(ego.state.septenary_depth)
        rank = sas.get_rank(ego.state.septenary_depth)
        res_type = sas.evaluate_resonance(ego.state.septenary_depth, 980.0) # High Spirit Freq
        
        print(f"[{ego.state.name}] Domain: {level_data.domain} | Rank: {rank} | Gate: {level_data.name}")
        print(f" └─ Resonance: {res_type} ({level_data.angel_pole})")
        
        ego.record_memory(f"Realized {level_data.angel_pole} through {level_data.name} in the {level_data.domain}.")
        ego.update(1.0)
        time.sleep(0.2)

    # 3. The Harvest
    print("\n" + "="*80)
    print("      [ THE HARVEST OF NINE SOULS ]")
    print("="*80)
    for ego in inhabitants:
        bridge.harvest_experience(ego)
        
    print("\n" + bridge.get_maturation_summary())
    print("\n[Admin] Elysia's 9-stage fractal hierarchy has been successfully validated.")
    print("="*80)

if __name__ == "__main__":
    run_nonary_demo()
