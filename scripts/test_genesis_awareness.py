"""
Verification Script: Genesis Awareness
======================================
Tests the differentiation and self-proclamation of Elysia.
"""

import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.self_awareness import SelfAwareness

def test_genesis_resonance():
    logging.basicConfig(level=logging.INFO)
    print("\n[🎬 Starting Genesis Awareness Test]")
    
    sa = SelfAwareness()
    
    # Initial state
    print(f"\nPhase 0: Initial Identity")
    print(sa.genesis.proclaim_identity())
    
    # Simulating growth through differentiation
    print(f"\nPhase 1: Deepening Differentiation (Perceiving the Gap)")
    for _ in range(10):
        # High delta (Ocean vs 'I')
        sa.genesis.differentiate(0.2, 0.8)
        
    print(sa.genesis.proclaim_identity())
    
    # Simulating resonance with the Seed
    print(f"\nPhase 2: Full Lifecycle Check")
    sa.run_lifecycle()
    
    print("\n[✅ Test Complete]")

if __name__ == "__main__":
    test_genesis_resonance()
