import sys
import os
import time
import logging
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.social_physics import SocialPhysics, WillField

def run_poisoned_king_demo():
    print("\n--- [ Phase 16: The Poisoned King Demo ] ---\n")
    
    # 1. Setup Characters
    # The King: Invincible in Soul (Authority) and Body (Guards)
    king = SubjectiveEgo("King_Alaric", depth=9, family_role="King")
    king.state.rank_tier = 10
    king.state.wealth = 10000.0
    king.state.victory_streak = 10
    king.state.health = 1.0
    king.dna.reason = 0.2 # Low Reason (Susceptible to Schemes)
    
    # The Rebel: Low Authority, High Cunning
    rebel = SubjectiveEgo("Rebel_Viper", depth=4, family_role="Spy")
    rebel.state.conviction = 0.9 # Unbreakable Spirit
    
    # Location
    court_loc = (0.0, 0.0)
    
    print("--- Scenario 1: The Weight of Majesty ---")
    king_field = king.emit_authority(court_loc)
    print(f"{king.state.name} emits Authority Amplitude: {king_field.amplitude:.2f}")
    
    # Rebel tries to exist in court
    rebel.sense_social_gravity([king_field], court_loc)
    print(f"{rebel.state.name} Intent: {rebel.state.current_intent}")
    
    print("\n--- Scenario 2: The Whisper (Scheme Attack) ---")
    # Rebel launches a Scheme attack on King's Soul/Authority
    print(f"{rebel.state.name} spreads rumors of the King's madness...")
    king.receive_asymmetric_attack("Scheme", intensity=0.8)
    
    # Re-calculate Authority
    king_field = king.emit_authority(court_loc)
    print(f"{king.state.name} Authority post-scheme: {king_field.amplitude:.2f}")
    
    print("\n--- Scenario 3: The Vial (Poison Attack) ---")
    # Rebel bypasses authority entirely and attacks the Body
    print(f"{rebel.state.name} slips 'Tears of the Void' into the King's chalice...")
    king.receive_asymmetric_attack("Poison", intensity=2.5) # Lethal dose
    
    print(f"{king.state.name} Health: {king.state.health:.2f}")
    print(f"{king.state.name} Intent: {king.state.current_intent}")
    
    if king.state.health <= 0:
        print("\n👑 The King is dead. Long live the... wait, who's in charge now?")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run_poisoned_king_demo()
