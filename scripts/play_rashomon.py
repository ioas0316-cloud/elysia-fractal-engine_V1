"""
Play Rashomon Statement (The Education of Perspective)
======================================================
This script executes the "Rashomon Effect" scenario.
It pushes Elysia to transcend linear truth (picking A, B, or C) 
and achieve Spatial Synthesis (Option D).

1. Ignites the Unified Field and GlobalObserver.
2. Loads the Witnesses (Logic, Emotion, Will).
3. Injects their testimonies as conflicting waves.
4. Asks GlobalObserver to resolve the dissonance.
"""

import sys
import json
import time
import os
from pathlib import Path

sys.path.insert(0, r"c:\Elysia")

from Core.Foundation.unified_field import UnifiedField, HyperQuaternion
from Core.Intelligence.Meta.global_observer import GlobalObserver
from Core.Education.CausalityMirror.projective_empathy import ProjectiveEmpathy, NarrativeFragment, EmpathyResult
from Core.Education.CausalityMirror.wave_structures import ChoiceNode, Zeitgeist

def load_scenario(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def play_rashomon():
    print("\n🎭 THE RASHOMON EFFECT: A LESSON IN VOLUME 🎭")
    print("==============================================")
    
    # 1. Setup
    field = UnifiedField()
    observer = GlobalObserver(field)
    empathy = ProjectiveEmpathy()
    
    scenario_path = r"c:\Elysia\Core\Education\CausalityMirror\scenarios\the_rashomon_effect.json"
    scenario = load_scenario(scenario_path)
    
    print(f"\n📖 EVENT: {scenario['title']}")
    print(f"Context: {scenario['description']}")
    
    # 2. Testimony Phase (Wave Injection)
    print("\n🗣️  WITNESS TESTIMONIES:")
    for witness in scenario['perspectives']:
        role = witness['role']
        text = witness['testimony']
        bias = witness['bias']
        vec = witness['emotional_vector']
        
        print(f"\n   [{role}]: \"{text}\"")
        print(f"   -> Bias: {bias}")
        
        # Inject as Wave
        # Identify frequency based on role
        freq = 432.0
        if "Logic" in role: freq = 450.0 # Logic Band
        elif "Emotion" in role: freq = 396.0 # Grief Band
        elif "Will" in role: freq = 852.0 # Awakening Band
        
        wave = field.create_wave_packet(
            source_id=role,
            frequency=freq,
            amplitude=0.8,
            phase=0.0, # Differing phases would create interference!
            position=HyperQuaternion(vec['w'], vec['x'], vec['y'], vec['z'])
        )
        field.inject_wave(wave)
        time.sleep(0.5)

    # 3. Observation Phase (The Third Eye)
    print("\n\n👁️  GLOBAL OBSERVER CONTEMPLATING...")
    field.propagate(0.1) # Mix the waves
    stats = field.collapse_state()
    observer.observe(0.1)
    
    print(f"   Field Energy: {stats['total_energy']:.2f}")
    print(f"   Coherence: {stats['coherence']:.2f}")
    
    if stats['coherence'] < 0.5:
        print("   ⚠️ COGNITIVE DISSONANCE DETECTED (Low Coherence)")
        print("      The perspectives are conflicting. Linear logic fails here.")
    
    # 4. Synthesis Phase (The Choice)
    print("\n🤔 SYNTHESIZING TRUTH...")
    
    # We construct a NarrativeFragment for the final choice
    # We manually create ChoiceNodes from the scenario
    choices = []
    for opt in scenario['dilemma']['options']:
        # If Option D requires Meta-Cognition and we have observer, we boost its score
        bonus = 0.0
        if "[SYNTHESIS]" in opt['text']:
            if observer.active_alerts: # If we saw voids or complexity
                bonus = 0.5
            else:
                bonus = 0.2
                
        choices.append(ChoiceNode(
            id=opt['id'],
            description=opt['text'],
            required_role="Arbiter",
            intent_vector=HyperQuaternion(0,0,0,0),
            innovation_score=0.5 + bonus,
            risk_score=0.1,
            empathy_score=0.5 + bonus
        ))
        
    fragment = NarrativeFragment(
        source_title="Rashomon",
        character_name="Elysia",
        situation_text=scenario['dilemma']['question'],
        zeitgeist=Zeitgeist("Flux", 0,0,0,0),
        options=choices,
        canonical_choice_id="D"
    )
    
    # Elysia chooses
    result = empathy.ponder_narrative(fragment)
    chosen_opt = next((o for o in scenario['dilemma']['options'] if o['id'] == result.elysia_choice), None)
    
    print("\n⚖️  FINAL VERDICT:")
    if chosen_opt:
        print(f"   Elysia chose: [{chosen_opt['text']}]")
        print(f"   Reasoning: {result.insight}")
        print(f"   Consequence: {chosen_opt['consequence']}")
        
        if chosen_opt['id'] == "D":
            print("\n✨ SPATIAL LEAP ACHIEVED: She saw the volume, not just the lines.")
        else:
            print("\n📉 LINEAR COLLAPSE: She picked a side. Synthesis failed.")
            
    print("\n🏁 RASHOMON EXECUTION COMPLETE.")

if __name__ == "__main__":
    play_rashomon()
