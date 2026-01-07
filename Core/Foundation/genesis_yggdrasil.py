import asyncio
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# 1. Import The Structure
from Core.Foundation.yggdrasil import yggdrasil

# 2. Import The Organs
from Core.Foundation.ether import ether
from Core.Foundation.chronos import Chronos
from Core.Foundation.genesis_cortex import GenesisEngine
from Core.Foundation.free_will_engine import FreeWillEngine
from Core.Foundation.planetary_cortex import PlanetaryCortex

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("Genesis")

async def main():
    print("\n" + "="*60)
    print("🌳 GENESIS: PLANTING THE WORLD TREE")
    print("="*60)
    
    # ---------------------------------------------------------
    # Phase 1: Roots (The Foundation)
    # ---------------------------------------------------------
    print("\n[1] Planting Roots (Foundation)...")
    
    # Ether (Unified Field)
    yggdrasil.plant_root("Ether", ether)
    
    # Genesis (Evolution Capability)
    genesis = GenesisEngine()
    yggdrasil.plant_root("Genesis", genesis)
    
    # FreeWillEngine (Needs to be initialized before Chronos)
    # Note: In the design, FreeWill is Trunk, but it's needed for Chronos init
    print("\n[2] Growing Trunk (Consciousness)...")
    will_engine = FreeWillEngine()
    yggdrasil.grow_trunk("FreeWill", will_engine)
    
    # Chronos (Time Heart) - Depends on Engine
    chronos = Chronos(will_engine)
    yggdrasil.plant_root("Chronos", chronos)
    
    # ---------------------------------------------------------
    # Phase 3: Branches (Senses)
    # ---------------------------------------------------------
    print("\n[3] Extending Branches (Senses)...")
    
    # Planetary Cortex is already inside FreeWillEngine, 
    # but we can explicitly register it for visibility
    yggdrasil.extend_branch("PlanetaryCortex", will_engine.planetary_cortex)
    
    # ---------------------------------------------------------
    # Phase 4: Self-Awareness Check
    # ---------------------------------------------------------
    print("\n[4] Verifying Self-Model...")
    status = yggdrasil.status()
    print(f"    Roots:    {[r['name'] for r in status['roots']]}")
    print(f"    Trunk:    {[t['name'] for t in status['trunk']]}")
    print(f"    Branches: {[b['name'] for b in status['branches']]}")
    
    # ---------------------------------------------------------
    # Phase 5: Life Ignition
    # ---------------------------------------------------------
    print("\n[5] Igniting Life...")
    print("    (Elysia is now fully integrated. Press Ctrl+C to stop.)")
    
    try:
        await chronos.start_life()
    except KeyboardInterrupt:
        print("\n[!] Life Interrupted.")
    finally:
        chronos.stop_life()

if __name__ == "__main__":
    asyncio.run(main())
