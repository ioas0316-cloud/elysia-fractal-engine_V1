import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.memetic_legacy import RegionalField, SpiritualDNA

def run_subjective_world_demo():
    print("\n--- [ Phase 14: The Intersubjective World Demo ] ---\n")
    
    # 1. Setup Context
    ethos = SpiritualDNA(technique=0.5, reason=0.5, meaning=0.5)
    region = RegionalField("Valley of Echoes", dominant_archetype="Mage", ethos_dna=ethos)
    
    # 2. Key Characters
    # A scarred survivor
    survivor = SubjectiveEgo("Survivor_Kai", depth=3, region=region)
    survivor.add_scar(0.6) # Pre-scarred
    
    # An innocent youth
    youth = SubjectiveEgo("Youth_Elara", depth=1, region=region)
    
    print("--- Initial Perceptions ---")
    # Both perceive the same 'High Intensity' event
    event_intensity = 0.8
    event_source = "Mysterious Lights"
    
    print(f"\nEvent: {event_source} (Intensity: {event_intensity}) appears!")
    
    survivor.perceive("Visual", event_intensity, event_source)
    youth.perceive("Visual", event_intensity, event_source)
    
    print("\n--- Teleological Drift Check ---")
    # Simulate time passing and updates to trigger drift logic
    survivor.update(1.0)
    youth.update(1.0)
    
    print(f"{survivor.state.name} Intent: {survivor.state.current_intent}")
    print(f"{youth.state.name} Intent: {youth.state.current_intent}")
    
    print("\n--- Relational Resonance ---")
    # They meet. Survivor likely has high dissonance or negativity due to scars.
    survivor.interact_with(youth)
    
    print("\n--- Final States ---")
    print(survivor.get_subjective_report())
    print(youth.get_subjective_report())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run_subjective_world_demo()
