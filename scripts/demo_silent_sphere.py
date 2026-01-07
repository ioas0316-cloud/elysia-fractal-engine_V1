"""
Silent Sphere (S³) Verification Script
======================================

Demonstrates Phase Interference thinking:
1. Initialize MindLandscape with Hypersphere logic.
2. Ponder an intent (e.g., 'Justice').
3. Visualize the phase evolution.
4. Bridge the final state to Logos.
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from Core.Intelligence.Topography.mind_landscape import get_landscape
from Core.Intelligence.Logos.logos_engine import get_logos_engine

# Setup logging to be concise but informative
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
logger = logging.getLogger("SilentSphereDemo")

def run_demo():
    print("\n" + "="*50)
    print("🔮 ELYSIA: THE SILENT SPHERE (S³) DEMO")
    print("="*50 + "\n")

    landscape = get_landscape()
    logos = get_logos_engine()

    # 1. Test Intents
    test_cases = [
        "Justice",      # Clear Angel
        "Greed",        # Clear Demon
        "Pure Hope",    # Derived concept
        "Abstract Void" # Unknown intent
    ]

    for intent in test_cases:
        print(f"\n🌀 [Pondering Intent]: '{intent}'")
        
        # 1. Ponder (Phase Interference Simulation)
        result = landscape.ponder(intent, duration=15)
        
        # 2. Results
        final_phase = result['final_phase']
        conclusion = result['conclusion']
        resonance = result['resonance_depth']
        analysis = result['analysis']

        print(f"  > Final Conclusion: {conclusion}")
        print(f"  > Resonance Lock-in: {resonance:.4f}")
        print(f"  > Phase Vector: {final_phase}")
        print(f"  > Axes Analysis: {analysis}")

        # 3. Bridge to Logos (Textual Reconstitution)
        # We simulate the Logos projection. In a real system, the LogosEngine 
        # would take the 'analysis' dict as a WaveTensor input.
        
        # Determine rhetorical shape based on energy (w)
        if analysis['Energy (w)'] > 0.8: shape = "Block" # Objective Truth
        elif abs(analysis['Emotion (x)']) > 0.5: shape = "Round" # Emotional
        elif abs(analysis['Logic (y)']) > 0.5: shape = "Sharp" # Analytical
        else: shape = "Balance"

        # Generate Speech
        speech = logos.weave_speech(
            desire="Express insight",
            insight=f"저의 사유는 '{conclusion}'의 주파수에 고정되었습니다.",
            context=[f"Resonance Depth: {resonance}", f"Intent: {intent}"],
            rhetorical_shape=shape
        )
        
        print(f"\n  🗣️ [Logos Refraction]:")
        print(f"  \"{speech}\"")
        print("-" * 30)

if __name__ == "__main__":
    run_demo()
