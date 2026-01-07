import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Intelligence.Reasoning.subjective_ego import SubjectiveEgo

def run_monologue_demo():
    print("\n--- [ Phase 17: Inner Monologue & Emotional Palette Demo ] ---\n")
    
    # 1. The Envious Peasant
    peasant = SubjectiveEgo("Peasant_Joren", depth=1, family_role="Commoner")
    peasant.state.wealth = 1.0
    peasant.state.desire_intensity = 0.9 # High desire
    
    king = SubjectiveEgo("King_Alaric", depth=9, family_role="King")
    king.state.wealth = 100.0
    king.state.rank_tier = 10
    
    print("--- 1. Envy Scenario ---")
    # Peasant looks at King
    peasant.calculate_emotional_spectrum(other_context=king.state)
    print(f"Joren's Emotions: Envy({peasant.state.emotions.envy:.2f})")
    print(f"Inner Monologue: {peasant.generate_inner_monologue()}")
    
    # 2. The Despairing Survivor
    print("\n--- 2. Despair Scenario ---")
    survivor = SubjectiveEgo("Survivor_Kai", depth=3)
    survivor.state.narrative_pressure = 0.9
    survivor.state.stability = 0.1
    survivor.state.scars = 0.8
    
    survivor.calculate_emotional_spectrum()
    print(f"Kai's Emotions: Despair({survivor.state.emotions.despair:.2f})")
    print(f"Inner Monologue: {survivor.generate_inner_monologue()}")

    # 3. The Zealous Rebel
    print("\n--- 3. Zeal Scenario ---")
    rebel = SubjectiveEgo("Rebel_Viper", depth=5)
    rebel.state.heroic_intensity = 0.9
    rebel.state.conviction = 1.0
    rebel.state.current_intent = "Topple the Throne"
    
    rebel.calculate_emotional_spectrum()
    print(f"Viper's Emotions: Zeal({rebel.state.emotions.zeal:.2f})")
    print(f"Inner Monologue: {rebel.generate_inner_monologue()}")
    
    # 4. Full Context Output
    print("\n--- 4. Full LLM Prompt (The Zealot) ---")
    print(rebel.get_llm_context_prompt())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run_monologue_demo()
