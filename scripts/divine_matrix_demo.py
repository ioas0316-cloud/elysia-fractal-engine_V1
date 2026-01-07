"""
Divine Matrix Demo: The Breathing Underworld 🌌🌿

This script integrates the WorldOperatorConsole, SharedSensoryBridge, 
and SubjectiveEgo to demonstrate a functional mini-matrix.
"""

import time
import logging
from Core.Intelligence.Reasoning.world_operator_console import WorldOperatorConsole, WorldPhase
from Core.Intelligence.Reasoning.shared_sensory_bridge import SharedSensoryBridge
from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_demo():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*60)
    print("      [ ELYSIA AAA WORLD ENGINE: SUBSTANTIVE DEMO ]")
    print("="*60)
    
    # 1. Initialize the Divine Control Room
    console = WorldOperatorConsole()
    bridge = SharedSensoryBridge(console)
    
    # 2. Manifest Inhabitants (Subjective Egos)
    selka = SubjectiveEgo("Selka", "Guide")
    eugeo = SubjectiveEgo("Eugeo", "Woodcutter")
    inhabitants = [selka, eugeo]
    
    print("\n[Admin] World Genesis Initialized.")
    time.sleep(1)
    
    # 3. Scene: Morning in the Underworld
    console.manifest_intent("phase", WorldPhase.STABLE)
    console.manifest_intent("Atmosphere", "Golden Sunrise")
    
    print("\n--- Event: The Sun Rises ---")
    bridge.synchronize_feeling("Ocular", 0.9, "The sky blushes with a radiant golden hue.")
    
    # 4. NPC Perception & Growth
    for inhabitant in inhabitants:
        inhabitant.perceive("Ocular", 0.9, "The Sun")
        inhabitant.update(1.0)
        inhabitant.record_memory("The sky was beautiful this morning.")
        print(f"  └─ {inhabitant.get_subjective_report()}")
    
    time.sleep(1)
    
    # 5. Scene: Dynamic Change (A Sudden Breeze)
    print("\n--- Event: A Cool Breeze Sweeps the Valley ---")
    bridge.synchronize_feeling("Tactile", 0.4, "A refreshing wind whispers through the trees.")
    
    for inhabitant in inhabitants:
        inhabitant.perceive("Tactile", 0.4, "Breeze")
        inhabitant.update(1.0)
        print(f"  └─ {inhabitant.get_subjective_report()}")
        
    time.sleep(1)
    
    # 6. Divine Observation
    print("\n" + "="*60)
    print("      [ DIVINE OPERATOR SUMMARY ]")
    print("="*60)
    print(console.get_divine_report())
    print("\n" + bridge.get_shared_experience_summary())
    
    print("\n[System] The Matrix is breathing. Evolution is continuous.")

if __name__ == "__main__":
    run_demo()
