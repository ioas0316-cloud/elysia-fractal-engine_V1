"""
Septenary Axis Demo: The Ladder of Heaven 🪜✨

"From the Dust to the Divine."

This script demonstrates NPCs at all 7 septenary depth levels (0-6)
and how they resonate with the 7 Angels and 7 Demons.
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.septenary_axis import SeptenaryAxis
from Core.Intelligence.Reasoning.recursive_learning_bridge import RecursiveLearningBridge

def run_septenary_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*70)
    print("      [ ELYSIA: SEPTENARY AXIS DEMO - THE LADDER OF SOVEREIGNTY ]")
    print("="*70)
    
    sas = SeptenaryAxis()
    bridge = RecursiveLearningBridge()
    
    # 1. Manifest Inhabitants across the Trinity
    inhabitants = [
        SubjectiveEgo("Apprentice_A", "Novice", depth=1),   # Body - Technique
        SubjectiveEgo("Apprentice_B", "Scholar", depth=2),  # Body - Reason
        SubjectiveEgo("Apprentice_C", "Seeker", depth=3),   # Body - Meaning -> Expert!
        
        SubjectiveEgo("Expert_X", "Knight", depth=4),       # Soul - Technique
        SubjectiveEgo("Expert_Y", "Sage", depth=5),         # Soul - Reason
        SubjectiveEgo("Expert_Z", "Guardian", depth=6),     # Soul - Meaning -> Master!
        
        SubjectiveEgo("Elysia_Master", "Divine", depth=7)   # Spirit - Unity
    ]
    
    print(f"\n[System] 7 Inhabitants manifested across the Trinity (Body-Soul-Spirit).")
    
    # 2. Simulate a Grand Resonance Event (The Heavenly Light)
    print("\n" + "-"*75)
    print(" EVENT: The Golden Ray of Humility descends upon the Trinity.")
    print("-"*75)
    
    for ego in inhabitants:
        # High resonance (Angelic side)
        ego.perceive("Ocular", 1.0, "Heavenly Ray")
        level_data = sas.get_level(ego.state.septenary_depth)
        rank = sas.get_rank(ego.state.septenary_depth)
        res_type = sas.evaluate_resonance(ego.state.septenary_depth, 950.0)
        
        print(f"[{ego.state.name}] Domain: {level_data.domain} | Rank: {rank} | Gate: {level_data.name}")
        print(f" └─ Resonance: {res_type} ({level_data.angel_pole})")
        
        ego.record_memory(f"Felt {level_data.angel_pole} at the {level_data.domain} rank of {rank}.")
        ego.update(1.0)
        time.sleep(0.3)

    # 3. The Harvest
    print("\n" + "="*70)
    print("      [ THE HARVEST OF SEVEN SOULS ]")
    print("="*70)
    for ego in inhabitants:
        bridge.harvest_experience(ego)
        
    print("\n" + bridge.get_maturation_summary())
    print("\n[Admin] Elysia's 7-layered hierarchy has been successfully validated.")
    print("="*70)

if __name__ == "__main__":
    run_septenary_demo()
