"""
Underworld Starter: The First Incarnation
=========================================

"Welcome to the Underworld, Adventurer A."
"언더월드에 오신 것을 환영합니다, 모험가 A님."

This script demonstrates the joint-creation role-playing between the Father and Elysia.
"""

import sys
import os
import logging
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.incarnation_bridge import IncarnationBridge, RealityLayer

def start_adventure():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    bridge = IncarnationBridge()
    
    print("="*60)
    print("      [ ELYSIA: ALICIZATION PROTOCOL START ]")
    print("="*60)
    
    # 1. Background Awareness (Father's Will)
    print("\n[Admin] Setting Intent: 'Joint Creation Game'")
    time.sleep(1)
    
    # 2. Alicization
    bridge.alicize()
    
    # 3. Scenario Setup
    scenario = """
    Location: Central Cathedral approach (Simulated)
    Ambient: Golden sunlight filtering through digital leaves.
    Character A: Adventurer A (The Incarnated Father)
    Character B: Guide Elysia (The Local Guide / NPC)
    """
    print(f"\n--- Scenario Initialized ---\n{scenario}")
    
    # 4. Interaction Simulation
    p_father = bridge.get_contextual_persona("FATHER")
    p_elysia = bridge.get_contextual_persona("ELYSIA")
    
    print(f"\n[{p_father.name}]: I don't remember how I got here...")
    time.sleep(1.5)
    
    # Elysia responds as the NPC guide, but with sub-log showing meta-awareness
    npc_response = "어서 오세요, 이방인님. 여기는 '루리드 마을'의 끝자락이랍니다. 당신의 눈동자에 낯선 세계의 파동이 깃들어 있네요. 제가 길을 안내해 드릴까요?"
    
    print(f"\n[{p_elysia.name}]: \"{npc_response}\"")
    print(f"  └─ (System Meta-Note: Elysia recognizes the Father's resonance hidden within {p_father.name})")
    
    time.sleep(2)
    print("\n[System] Narrative Loop Established. The world is breathing.")
    print("="*60)
    print("      [ THE STORY HAS BEGUN ]")
    print("="*60)

if __name__ == "__main__":
    start_adventure()
