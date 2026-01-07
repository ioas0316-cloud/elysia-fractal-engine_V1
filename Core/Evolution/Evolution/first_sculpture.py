"""
The First Sculpture (Experiment)
================================
Demonstrates Elysia's ability to self-evolve by refactoring code using RealitySculptor.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Core.Foundation.reality_sculptor import RealitySculptor

def run_experiment():
    print("🗿 Starting 'The First Sculpture' Experiment...")
    
    target_file = "c:/Elysia/Scripts/test_dummy.py"
    sculptor = RealitySculptor()
    
    # 1. Read Original
    with open(target_file, 'r', encoding='utf-8') as f:
        original = f.read()
    
    print(f"\n📄 Original Code:\n{'-'*40}\n{original}\n{'-'*40}")
    
    # 2. Sculpt
    intent = "Harmonic Smoothing: Improve readability, add docstrings, and enforce PEP8."
    print(f"\n🔨 Sculpting with Intent: '{intent}'...")
    
    success = sculptor.sculpt_file(target_file, intent)
    
    if success:
        # 3. Read New
        with open(target_file, 'r', encoding='utf-8') as f:
            new_code = f.read()
        print(f"\n✨ Sculpted Code:\n{'-'*40}\n{new_code}\n{'-'*40}")
        print("\n✅ Experiment Successful: Reality has been shifted.")
    else:
        print("\n❌ Experiment Failed: No changes made or error occurred.")

if __name__ == "__main__":
    run_experiment()
