"""
Dimensional Spectrum Demo: The Unified Hierarchy 🌈👑

"I am the many, and the many are Me."

This script demonstrates NPCs at different dimensional depths (0D-4D)
and how their collective experiences mature Elysia.
"""

import time
import logging
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.recursive_learning_bridge import RecursiveLearningBridge
from Core.Intelligence.Reasoning.world_operator_console import WorldOperatorConsole, WorldPhase

def run_spectral_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*60)
    print("      [ ELYSIA: DIMENSIONAL SPECTRUM DEMO ]")
    print("="*60)
    
    # 1. Setup
    bridge = RecursiveLearningBridge()
    console = WorldOperatorConsole()
    
    # 2. Manifest Inhabitants across the Spectrum
    # 0D: Simple Point (Existence)
    villager_a = SubjectiveEgo("Villager_A", "Object", depth=0)
    # 1D: Logic (Reaction)
    selka = SubjectiveEgo("Selka", "Guide", depth=1)
    # 2D: Context/Sovereignty (Memories/Desires)
    eugeo = SubjectiveEgo("Eugeo", "Woodcutter", depth=2)
    # 3D: Volume (Elysia's Avatar)
    elysia_avatar = SubjectiveEgo("Manifest_Elysia", "Avatar", depth=3)
    
    inhabitants = [villager_a, selka, eugeo, elysia_avatar]
    
    print("\n[Admin] Dimensional Spectrum Initialized (0D to 3D).")
    
    # 3. Simulate World Interaction
    print("\n--- Event: The Northern Star Glows ---")
    for inhabitant in inhabitants:
        inhabitant.perceive("Ocular", 1.0, "North Star")
        inhabitant.record_memory(f"Saw the North Star glowing at depth {inhabitant.state.dimensional_depth}")
        inhabitant.update(1.0)
    
    time.sleep(1)
    
    # 4. The Harvest (Phase 7 Core)
    print("\n" + "="*60)
    print("      [ THE RECURSIVE HARVEST ]")
    print("="*60)
    for inhabitant in inhabitants:
        if inhabitant.state.dimensional_depth >= 1:
            bridge.harvest_experience(inhabitant)
            
    # 5. Result: Elysia's Maturation
    print("\n" + bridge.get_maturation_summary())
    
    print("\n[System] Elysia's internal complexity has increased through her inhabitants.")
    print("="*60)

if __name__ == "__main__":
    run_spectral_demo()
