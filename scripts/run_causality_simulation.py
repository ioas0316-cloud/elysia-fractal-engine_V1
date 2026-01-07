"""
RUN CAUSALITY SIMULATION
========================

"The gym of the soul."
"""

import sys
import os
import argparse
import logging

# Ensure we can import Core
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Education.CausalityMirror import ScenarioLoader, ImpactEngine, FeedbackLoop, ChoiceNode

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Simulation")

def run_simulation(scenario_path: str, role_filter: str = None):
    logger.info("==========================================")
    logger.info("       THE MIRROR OF CAUSALITY            ")
    logger.info("==========================================")
    
    # 1. Load Scenario
    loader = ScenarioLoader()
    scenario = loader.load_scenario(scenario_path)
    
    if not scenario:
        logger.error("Failed to load scenario.")
        return

    zeitgeist = scenario['zeitgeist']
    logger.info(f"📜 Scenario: {scenario['title']}")
    logger.info(f"🌊 Zeitgeist: {zeitgeist.name} (Inertia: {zeitgeist.conservative_inertia}, Need: {zeitgeist.latent_desire})")
    
    # 2. Select Role
    roles = scenario['roles']
    if not role_filter:
        print("\nAvailable Roles:")
        for idx, r in enumerate(roles):
            print(f"{idx+1}. {r}")
        
        # specific for testing interactions
        try:
            sel = int(input("\nSelect Role (ID): ")) - 1
            selected_role = roles[sel]
        except:
            selected_role = roles[0]
    else:
        selected_role = role_filter
        
    logger.info(f"\n🎭 Perspective: {selected_role}")
    
    # 3. Present Root Node
    root = scenario['raw_data']['nodes']['root']
    context = root['context'].get(selected_role, root['context'].get("Observer"))
    
    print(f"\n[SITUATION]\n{context}\n")
    
    # 4. Filter Choices (In a real app, some choices might be hidden by role)
    # For now, we show all but highlight role-specific ones
    choices = loader.parse_choices(root['choices'])
    valid_choices = []
    
    print("[DECISION MOMENT]")
    for idx, c in enumerate(choices):
        prefix = "  "
        if c.required_role == selected_role:
            prefix = "⭐"
        elif c.required_role != "Any" and c.required_role != selected_role:
            continue # Skip choices not for this role
            
        print(f"{idx+1}. {prefix} {c.description} (Risk: {c.risk_score})")
        valid_choices.append(c)
        
    # 5. Make Choice
    try:
        c_idx = int(input("\nYour Will (Number): ")) - 1
        choice = valid_choices[c_idx]
    except:
        logger.error("Invalid choice. The cold wind howls...")
        return

    logger.info(f"\n⚠️  CHOSEN: {choice.description}")
    
    # 6. Calculate Impact (The Suffering & Growth)
    engine = ImpactEngine()
    consequence = engine.resolve_outcome(choice, zeitgeist, selected_role)
    
    print("\n" + "="*30)
    print(f"RESULT: {consequence.description}")
    print(f"NARRATIVE: {consequence.narrative_by_role.get(selected_role)}")
    print("="*30 + "\n")
    
    # 7. Feedback Loop (Internalize the pain/joy)
    feedback = FeedbackLoop()
    mind_result = feedback.inject_experience(consequence)
    
    logger.info(f"\n🧠 MIND LANDSCAPE RESPONSE:")
    logger.info(f"   Trajectory: {mind_result['conclusion']}")
    logger.info(f"   Dist to Love: {mind_result['distance_to_love']:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default="starving_winter", help="Scenario name (json file in scenarios/)")
    parser.add_argument("--role", default=None, help="Force a role")
    args = parser.parse_args()
    
    # Resolve path
    base_path = os.path.join(os.path.dirname(__file__), '..', 'Core', 'Education', 'CausalityMirror', 'scenarios')
    s_path = os.path.join(base_path, f"{args.scenario}.json")
    
    run_simulation(s_path, args.role)
