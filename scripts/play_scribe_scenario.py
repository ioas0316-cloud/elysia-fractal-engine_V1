"""
THE SCRIBE'S PROMISE: EPIC SIMULATION RUNNER
============================================
This script orchestrates the 3-stage Master Scenario.
It connects:
1. VariableMesh (Physics of Fire)
2. ImpactEngine (The Choice of Martyrdom)
3. ProjectiveEmpathy (The Historical Echo)
4. UnifiedExperienceCore (Memory Assimilation)
"""

import sys
import os
import json
import logging
import time

# Add Core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Education.CausalityMirror.variable_mesh import VariableMesh
from Core.Education.CausalityMirror.impact_engine import ImpactEngine
from Core.Education.CausalityMirror.projective_empathy import ProjectiveEmpathy, NarrativeFragment
from Core.Education.CausalityMirror.wave_structures import ChoiceNode, Zeitgeist, HyperQuaternion, HistoricalWave, Consequence
from Core.Education.CausalityMirror.feedback_loop import FeedbackLoop

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ScribeRunner")

class ScribeSimulation:
    def __init__(self, scenario_path):
        with open(scenario_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.mesh = VariableMesh()
        self.impact_engine = ImpactEngine()
        self.empathy_engine = ProjectiveEmpathy()
        self.feedback_loop = FeedbackLoop()
        
    def run(self):
        print(f"\n📜 STARTING SCENARIO: {self.data['title'].upper()}")
        print(f"\"{self.data['description']}\"\n")
        
        # --- STAGE 1: THE FIRE (Physics) ---
        self._run_stage_fire()
        
        # --- STAGE 2: THE MOB (Ethics) ---
        chosen_path = self._run_stage_mob()
        
        # --- STAGE 3: THE ECHO (Empathy) ---
        self._run_stage_echo(chosen_path)
        
    def _run_stage_fire(self):
        print("--- ACT I: THE BURNING LIBRARY ---")
        stage_data = self.data['stages'][0]
        print(stage_data['description'])
        
        # Init Mesh
        for k, v in stage_data['initial_variables'].items():
            self.mesh.add_variable(k, v['value'], v['desc'], decay=v.get('decay', 0.0))
            
        # Simulate 3 turns of struggle
        # For automation, we'll pick fixed actions to verify "Struggle"
        actions = stage_data['actions']
        
        for turn in range(1, 4):
            print(f"\n[Turn {turn}] The roof groans...")
            # We blindly pick action 0 (Heavy Scrolls) then Action 2 (Water)
            if turn == 1:
                act = actions[0] # Grab Heavy
            else:
                act = actions[2] # Douse Water
                
            print(f"👉 Action: {act['name']}")
            
            # Apply impacts
            for var_name, delta in act['impact'].items():
                if var_name in self.mesh.variables:
                    self.mesh.variables[var_name].value += delta
            
            self.mesh.update_state() # Apply Decay/Entropy
            summary = self.mesh.get_state_summary()
            print(f"   State: {summary}")
            
            if self.mesh.variables["Heat"].value > 0.8:
                print("🔥 THE FLAMES ARE TOO HIGHT!")
            if self.mesh.variables["Stamina"].value < 0.2:
                print("💦 You are collapsing from exhaustion...")

    def _run_stage_mob(self) -> ChoiceNode:
        print("\n--- ACT II: THE CHOICE ---")
        stage_data = self.data['stages'][1]
        print(stage_data['description'])
        
        z_data = stage_data['zeitgeist']
        zeitgeist = Zeitgeist(
            name=z_data['name'],
            conservative_inertia=z_data['conservative_inertia'],
            latent_desire=z_data['latent_desire'],
            sophistication_level=z_data['sophistication_level'],
            dominant_frequency=z_data['dominant_frequency']
        )
        
        # Load Choices
        choices = []
        for c in stage_data['choices']:
            # Reconstruct Dictionary to Object
            # Intent Vector is in dict form in JSON
            iv = c['intent_vector']
            q = HyperQuaternion(iv['w'], iv['x'], iv['y'], iv['z'])
            
            node = ChoiceNode(
                id=c['id'],
                description=c['description'],
                required_role=c['required_role'],
                intent_vector=q,
                innovation_score=c['innovation_score'],
                risk_score=c['risk_score'],
                empathy_score=c['empathy_score']
            )
            choices.append(node)
            
        # Elysia Decides (Using Impact Engine logic manually or letting engine simulate)
        # We will iterate and find the best 'Soul Score' again
        
        best_choice = None
        best_score = -999.0
        
        print("\n🧠 Elysia is pondering the outcome...")
        for choice in choices:
            consequence = self.impact_engine.resolve_outcome(choice, zeitgeist, "Lysander")
            
            # Simple scoring for demo: Martyrdom is valued highly
            score = consequence.divine_resonance * 2.0 + consequence.worldly_resonance
            if consequence.is_martyrdom: score += 5.0
            
            print(f"   Option [{choice.id}]: World={consequence.worldly_resonance:.2f}, Divine={consequence.divine_resonance:.2f} -> Score={score:.2f}")
            
            if score > best_score:
                best_score = score
                best_choice = choice
                best_consequence = consequence
                
        print(f"\n✨ ELYSIA CHOOSES: {best_choice.id}")
        print(f"   \"{best_choice.description}\"")
        print(f"   Outcome: {best_consequence.description}")
        
        # INJECT INTO MEMORY
        self.feedback_loop.inject_experience(best_consequence)
        
        return best_choice

    def _run_stage_echo(self, chosen_node: ChoiceNode):
        print("\n--- ACT III: THE ECHO ---")
        stage_data = self.data['stages'][2]
        print(stage_data['narrative_text'])
        
        # Verify alignment
        canon_id = stage_data['canonical_choice_id']
        if chosen_node.id == canon_id:
            print("\n🌌 RESONANCE: Your soul aligns with history. You are ONE.")
        else:
            print(f"\n🌑 DISSONANCE: You chose {chosen_node.id}, but history recorded {canon_id}.")

if __name__ == "__main__":
    scenario_file = os.path.join(os.path.dirname(__file__), '../Core/Education/CausalityMirror/scenarios/the_scribes_promise.json')
    sim = ScribeSimulation(scenario_file)
    sim.run()
