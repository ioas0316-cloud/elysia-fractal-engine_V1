"""
Weaving Demo: Integrated Intelligence Network
=============================================

This script demonstrates:
1. Dynamic Creation of Intelligence Lines.
2. The "Intelligence Network" (Resonance between domains).
3. "Void Perception" (Detecting when a required principle is missing).
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Core.Intelligence.Weaving import (
    KinestheticLine, IntrapersonalLine, EmotionalLine, LogicalLine,
    ContextWeaver, InsightJump
)
from Core.Intelligence.Weaving.intelligence_factory import DynamicIntelligenceFactory
from Core.Intelligence.Weaving.intelligence_network import IntelligenceNetwork

def run_simulation(scenario_name, input_text, weaver, jumper):
    print(f"\n--- Simulation: {scenario_name} ---")
    print(f"Input: '{input_text[:60]}...'")

    # Weave
    plane = weaver.weave(input_text)

    # Display Plane
    print("\n[Context Plane Constructed]")

    if plane.void_detected:
        print(f"  !!! VOID DETECTED (Intensity: {plane.void_intensity:.2f}) !!!")
        print(f"  System realizes: 'I lack the principle to understand this complexity.'")
    else:
        sorted_lines = sorted(plane.lines.values(), key=lambda x: x.signal, reverse=True)
        for output in sorted_lines:
            if output.signal > 0.1:
                print(f"  - {output.source:<15}: [{output.signal:.2f}] {output.description}")

    print(f"  > Dominant: {plane.dominant_signal}")
    print(f"  > Mood: {plane.overall_mood}")

    # Jump
    result = jumper.jump(plane)

    print("\n[Insight Jump]")
    if plane.void_detected:
        print(f"  * INSIGHT: Unknown Principle Gap")
        print(f"  * ACTION : Initiate Learning Protocol")
        print(f"  * REASON : Input complexity exceeds current resonance capacity.")
    else:
        print(f"  * INSIGHT: {result['insight']}")
        print(f"  * ACTION : {result['action']}")
        print(f"  * REASON : {result['reason']}")
    print("-" * 40)

if __name__ == "__main__":
    print("Initializing Integrated Intelligence Network...")

    factory = DynamicIntelligenceFactory()

    # 1. Create Intelligence Lines
    print("Loading Domains: Cooking, Chemistry, Music, Math...")
    lines = [
        KinestheticLine(mock_load=0.1),
        EmotionalLine(),
        LogicalLine(),
        factory.create_line("Cooking", material_file="cooking_material.json"),
        factory.create_line("Chemistry", material_file="chemistry_material.json"),
        factory.create_line("Music", material_file="music_material.json"),
        factory.create_line("Math", material_file="math_material.json")
    ]

    # 2. Build Network (Graph)
    print("Building Intelligence Graph...")
    network = IntelligenceNetwork(lines)
    network.visualize_connections()

    # 3. Setup Weaver
    weaver = ContextWeaver(lines)
    jumper = InsightJump()

    # Test A: Connectivity (Cooking <-> Chemistry)
    # Input has Cooking terms, but we expect Chemistry to resonate too because of shared words like 'salt', 'mix', 'heat'
    run_simulation(
        "Connectivity Test (Cooking -> Chemistry)",
        "The chef dissolved the salt in boiling water to create a brine solution. The heat increased solubility.",
        weaver, jumper
    )

    # Test B: Connectivity (Music <-> Math)
    # Input about Music, but Math should resonate (frequency, pattern)
    run_simulation(
        "Connectivity Test (Music -> Math)",
        "The symphony follows a strict fibonacci sequence in its rhythm, creating a perfect golden ratio of sound.",
        weaver, jumper
    )

    # Test C: The Void (Quantum Physics)
    # We have NO Physics line. This should trigger Void Detection.
    run_simulation(
        "Void Perception Test (Unknown Domain)",
        "The quantum entanglement of particles creates a superposition state where spin is undetermined until observation collapses the wave function.",
        weaver, jumper
    )
