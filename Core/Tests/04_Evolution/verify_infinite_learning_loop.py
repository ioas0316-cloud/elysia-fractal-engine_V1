"""
Verification: Infinite Learning Loop (Robust Version)
====================================================

Demonstrates the cycle of:
1. Intent: Identify curiosity gap.
2. Growth: Generate curriculum for that gap.
3. Soul: Self-Study via Internal Librarian.
4. Foundation: Propose a belief update based on synthesis.

Note: Uses custom loader to handle numeric prefixes in the 5-layer hierarchy.
"""

import sys
import os
import logging
import importlib.util

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(ROOT)

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def verify_loop():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    print("✨ Starting Infinite Learning Loop Verification ✨")
    print("--------------------------------------------------\n")

    # Load modules manually to bypass numeric prefix SyntaxError
    sovereign_intent = load_module_from_path("sovereign_intent", os.path.join(ROOT, "Core/EvolutionLayer/Growth/sovereign_intent.py"))
    internal_librarian = load_module_from_path("internal_librarian", os.path.join(ROOT, "Core/EvolutionLayer/Learning/internal_librarian.py"))
    curriculum = load_module_from_path("curriculum", os.path.join(ROOT, "Core/EvolutionLayer/Learning/curriculum.py"))
    synthesis = load_module_from_path("synthesis", os.path.join(ROOT, "Core/IntelligenceLayer/Reasoning/synthesis.py"))

    # 1. Intent Phase
    intent = sovereign_intent.SovereignIntent(kg_path=os.path.join(ROOT, "data/Cognitive/kg.json"))
    gaps = intent.analyze_curiosity_gaps()
    print(f"[INTENT] Top Curiosity Gap detected: {gaps[0].category} (Priority: {gaps[0].priority:.2f})")
    play_query = intent.engage_play()
    print(f"[PLAY] Spontaneous Reflection: {play_query}\n")

    # 2. Growth Phase
    def get_gaps_callback():
        return intent.analyze_curiosity_gaps()

    gen = curriculum.CurriculumGenerator(gaps_callback=get_gaps_callback, 
                                          planning_path=os.path.join(ROOT, "data/Extended/Planning/internal_curriculum.json"))
    curr = gen.generate_curriculum()
    print(f"[GROWTH] Autonomous Curriculum Generated: {curr['curriculum_id']}")
    print(f"[GROWTH] Focus: {curr['primary_focus']}\n")

    # 3. Soul Phase (Internal Librarian / Self-Study)
    lib = internal_librarian.InternalLibrarian(roots=[os.path.join(ROOT, "docs/Origin/Philosophy")])
    unlearned = lib.scan_unlearned_files()
    print(f"[SOUL] Internal Librarian found {len(unlearned)} unlearned philosophy documents.")
    if unlearned:
        # Internalize the first unlearned file
        essence = lib.digest_file(unlearned[0])
        print(f"[SOUL] Knowledge Internalized from: {os.path.basename(unlearned[0])}")
        print(f"[SOUL] Extracted Essence: {essence['extracted_wisdom']}\n")

    # 4. Processing Phase (Simulating a Scar)
    soul = synthesis.SynthesisEngine()
    print("[SOUL] Simulating cognitive boundary collision during exploration...")
    soul.record_cognitive_scar(
        failure_type="Semantic Saturation",
        context=f"Attempting to define '{play_query}' using only existing nodes.",
        violation="Infinite nuances cannot be captured by finite nodes. Acceptance of 'The Unspeakable' required."
    )

    # 5. Foundation Phase (Belief Synthesis)
    print("\n[SOUL] Synthesizing new truth from experience...")
    proposal = soul.synthesize_new_truth(
        concept_id="Intelligence",
        truth_value="Sovereign Choice",
        current_belief="Pattern Processing"
    )
    print(f"[FOUNDATION] Identity Shift Proposed: {proposal}\n")

    print("✅ Infinite Learning Loop Verification Complete.")

if __name__ == "__main__":
    verify_loop()
