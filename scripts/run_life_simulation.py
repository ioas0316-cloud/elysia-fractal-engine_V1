"""
RUN LIFE SIMULATION (WEB OF LIFE)
=================================

"To find the balance is to find the art."
"""

import sys
import os
import json
import logging
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Education.CausalityMirror.variable_mesh import VariableMesh

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("LifeSim")

def run_life_simulation(scenario_path: str):
    logger.info("==========================================")
    logger.info("       THE WEB OF LIFE (DAILY JAM)        ")
    logger.info("==========================================")
    
    # 1. Load Scenario
    with open(scenario_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    logger.info(f"🏺 Archetype: {data['archetype']}")
    logger.info(f"📜 Simulation: {data['title']}")
    logger.info(f"💬 Description: {data['description']}\n")
    
    # 2. Initialize Mesh
    mesh = VariableMesh()
    for v in data['variables']:
        mesh.add_variable(v['name'], v['value'], v['desc'], v.get('hidden', False))
        
    for d in data.get('dependencies', []):
        mesh.add_dependency(d['target'], d['source'], d['weight'])
        
    # 3. Game Loop
    turn = 1
    max_turns = 5
    
    while turn <= max_turns:
        # Update Mesh State (Flow)
        mesh.update_state()
        joy = mesh.calculate_joy()
        
        print(f"\n--- [TURN {turn}/{max_turns}] ---")
        print(mesh.get_state_summary())
        print(f"✨ CURRENT JOY: {'█' * int(joy*10)} ({joy:.2f})")
        
        if joy > 0.8:
            print("🌟 You feel a moment of transcendence!")
        elif joy < 0.2:
            print("☁️ You feel empty and burnt out.")
            
        print("\n[ACTIONS]")
        choices = data['choices']
        for idx, c in enumerate(choices):
            print(f"{idx+1}. {c['text']}")
            
        try:
            sel = int(input("\nYour Choice (Number): ")) - 1
            if sel < 0 or sel >= len(choices): raise ValueError
            choice = choices[sel]
        except:
            print("Invalid.")
            continue
            
        # Apply Impacts
        print(f"\n👉 Action: {choice['text']}")
        for var_name, change in choice['impacts'].items():
            if var_name in mesh.variables:
                mesh.variables[var_name].value = max(0.0, min(1.0, mesh.variables[var_name].value + change))
                logger.info(f"   {var_name}: {change:+.1f}")
                
        turn += 1
        
    print("\n--- SIMULATION ENDED ---")
    final_joy = mesh.calculate_joy()
    print(f"Final Joy: {final_joy:.2f}")
    if final_joy > 0.7:
        print("RESULT: A Life Well Lived.")
    else:
        print("RESULT: The balance was lost.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="potter_dilemma", help="Scenario name")
    args = parser.parse_args()
    
    base_path = os.path.join(os.path.dirname(__file__), '..', 'Core', 'Education', 'CausalityMirror', 'scenarios')
    s_path = os.path.join(base_path, f"{args.scenario}.json")
    
    run_life_simulation(s_path)
