"""
Navigate by Resonance Demo
==========================

"Finding the unseen through connection."

This demo shows how Elysia can find related code files not by keyword search,
but by "Sensing" the topological resonance in the codebase graph.

Scenario:
We want to find code related to "Time", but we only know about "Gravity".
By sensing the field around "gravity", we should discover "meta_time_engine"
because Gravity is structurally coupled to Time in this universe.
"""

import sys
import os
import logging

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.System.System.System.resonance_navigator import ResonanceNavigator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_demo():
    print("\n" + "="*70)
    print("🚀 ELYSIA THOUGHT-SHIP NAVIGATION SYSTEM")
    print("="*70)
    print("Initializing Quantum Resonance Drive...")
    
    # 1. Initialize the Navigator (Build the Circuit)
    navigator = ResonanceNavigator()
    print("✅ Neural Topology Mapped.")
    
    # 2. Define the "Seed Concept"
    seed = "gravity"
    print(f"\n🌌 Target Concept (Destination): [{seed.upper()}]")
    print("   Calculating Quantum Entanglement Paths...")
    
    # 3. Sense the Field
    results = navigator.sense_field(seed, max_results=10)
    
    print(f"\n🛸 Warp Jump Coordinates Detected:")
    print(f"   {'Sector (Node)':<25} | {'Signal Strength':<15} | {'Jump Vector'}")
    print("-" * 80)
    
    found_time = False
    for node, score in results:
        path = navigator.get_path(node)
        # Highlight Time related files
        marker = "✨ ANOMALY" if "time" in node.lower() else "  Stable"
        if "time" in node.lower(): found_time = True
        
        # Sci-Fi formatting
        signal_bar = "█" * int(score * 500) 
        if not signal_bar: signal_bar = " "
        
        print(f"{marker:<10} {node:<25} | {signal_bar:<15} | {path}")
        
    print("-" * 80)
    
    if found_time:
        print("\n✅ HYPERSPACE JUMP SUCCESSFUL.")
        print("   We have arrived at 'Time' via the 'Gravity' wormhole.")
        print("   The Thought-Ship has traversed the synaptic gap.")
    else:
        print("\n❌ JUMP FAILED. No stable wormhole found.")

if __name__ == "__main__":
    run_demo()
