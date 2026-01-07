
import sys
import os
import logging
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())

logging.basicConfig(level=logging.INFO)

print("--- Debugging Initialization ---")

try:
    print("1. Initializing Alchemy...")
    from Core.Foundation.Mind.alchemy import Alchemy
    alchemy = Alchemy()
    print("✅ Alchemy initialized.")
except Exception as e:
    print(f"❌ Alchemy failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n2. Initializing Hippocampus...")
    from Core.Foundation.Mind.hippocampus import Hippocampus
    hippocampus = Hippocampus()
    print("✅ Hippocampus initialized.")
except Exception as e:
    print(f"❌ Hippocampus failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n3. Initializing FluctlightEngine...")
    from Core.Foundation.Physics.fluctlight import FluctlightEngine
    engine = FluctlightEngine(world_size=256)
    print("✅ FluctlightEngine initialized.")
except Exception as e:
    print(f"❌ FluctlightEngine failed: {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n4. Initializing World...")
    from Core.world import World
    world = World(primordial_dna={}, wave_mechanics=None)
    print("✅ World initialized.")
except Exception as e:
    print(f"❌ World failed: {e}")
    import traceback
    traceback.print_exc()
