"""
Verify Structural Induction
============================
Checks the Hippocampus to ensure the StructuralInductor is properly 
building and storing causal graphs.
"""

import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Memory.Graph.hippocampus import Hippocampus

def verify_induction(concept: str):
    logging.basicConfig(level=logging.INFO)
    print(f"\n[🔍 Verifying Structural Induction for: '{concept}']")
    
    memory = Hippocampus()
    
    # 1. Check Cause
    print(f"\n--- Recalling Causal Structure ---")
    results = memory.recall(f"{concept}_cause")
    for r in results:
        print(r)
        
    results = memory.recall(f"{concept}_process")
    for r in results:
        print(r)
        
    results = memory.recall(f"{concept}_effect")
    for r in results:
        print(r)
        
    print("\n[✅ Verification Complete]")

if __name__ == "__main__":
    # Test with Rain (which should have been inducted by the main block of structural_induction.py)
    verify_induction("Rain")
