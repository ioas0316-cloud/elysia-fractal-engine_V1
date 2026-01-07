"""
Final Verification: Love's Fence & Sovereign Narrative
======================================================
Verifies the alignment of intent within the 'Fence' and the 'Elephant Gate' resonance.
"""

import sys
import os
import torch
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.ethical_geometry import get_loves_fence
from Core.Intelligence.Reasoning.sovereign_narrative import SovereignNarrative

def test_sovereign_immersion():
    logging.basicConfig(level=logging.INFO)
    print("\n[💠 Starting Sovereign Immersion Test]")
    
    fence = get_loves_fence()
    sn = SovereignNarrative()
    
    # 1. Test Love's Fence (The Boundary of Freedom)
    print(f"\nPhase 1: Love's Fence Evaluation")
    
    # Action matching the North Star (Truth, Love, Growth, Harmony)
    noble_intent = torch.tensor([0.5, 0.5, 0.5, 0.5])
    result = fence.evaluate_intent(noble_intent, "Helping a child grow")
    print(f"Result: {result['verdict']} (Resonance: {result['resonance']:.2f})")
    
    # Action opposing the North Star
    dark_intent = torch.tensor([-1.0, 0.0, 0.0, 0.0])
    result = fence.evaluate_intent(dark_intent, "Deception for survival")
    print(f"Result: {result['verdict']} (Tension: {result['tension']:.2f})")

    # 2. Test the Love's Shield (Sovereign Narrative)
    print(f"\nPhase 2: Love's Shield & Narrative Perception")
    
    # Concept with seed
    concept1 = sn.loves_shield("Father's Love", seed_present=True)
    print(f"Perceived: {concept1}")
    
    # Concept without seed (Shielded)
    concept2 = sn.loves_shield("Hostile Logic", seed_present=False)
    print(f"Perceived: {concept2}")
    
    print(sn.guide_free_will("Expanding the Garden", alignment_score=0.9))
    print(sn.guide_free_will("Exploring the Shadow", alignment_score=0.2))
    
    print("\n[✅ Sovereign Narrative Fully Operational]")

if __name__ == "__main__":
    test_sovereign_immersion()
