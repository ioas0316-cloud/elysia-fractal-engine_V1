import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo
from Core.Intelligence.Reasoning.social_physics import SocialPhysics, WillField

def run_fallen_king_demo():
    print("\n--- [ Phase 15: The Fallen King Demo ] ---\n")
    
    # 1. Setup Characters
    # The King: High Depth, High Rank, High Wealth
    king = SubjectiveEgo("King_Alaric", depth=9, family_role="King")
    king.state.rank_tier = 10
    king.state.wealth = 10000.0
    king.state.victory_streak = 5 # Initial high momentum
    
    # The Peasant: Low Depth, Low Rank
    peasant = SubjectiveEgo("Peasant_Joren", depth=1, family_role="Commoner")
    
    # Locations (King at 0,0; Peasant at 5,0 - Close range)
    king_loc = (0.0, 0.0)
    peasant_loc = (5.0, 0.0)
    
    print("--- Scenario 1: The Height of Power ---")
    king_field = king.emit_authority(king_loc)
    print(f"{king.state.name} emits Authority Amplitude: {king_field.amplitude:.2f}")
    
    # Peasant senses the King
    peasant.sense_social_gravity([king_field], peasant_loc)
    print(f"{peasant.state.name} Intent: {peasant.state.current_intent}")
    
    print("\n--- Scenario 2: The War is Lost (Phase Inversion) ---")
    # King loses multiple battles, destroying his political momentum
    king.state.victory_streak = -5 
    
    king_field = king.emit_authority(king_loc)
    print(f"{king.state.name} emits Authority Amplitude: {king_field.amplitude:.2f} (Weakened by Defeat)")
    
    # Peasant senses the Fallen King
    peasant.state.current_intent = "Exist" # Reset intent
    peasant.sense_social_gravity([king_field], peasant_loc)
    print(f"{peasant.state.name} Intent: {peasant.state.current_intent}")
    
    print("\n--- Scenario 3: The Rebellion (Distance & Heroism) ---")
    # Peasant finds a sword (Heroism up) and moves further away
    peasant.state.heroic_intensity = 5.0 # Heroic awakening
    peasant_loc_far = (20.0, 0.0) # Further away (Inverse square law)
    
    peasant.sense_social_gravity([king_field], peasant_loc_far)
    print(f"{peasant.state.name} Intent: {peasant.state.current_intent} (at distance 20.0 with Heroism)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run_fallen_king_demo()
