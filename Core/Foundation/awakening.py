import sys
import os
import logging
import time
import random

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.System.System.hardware_accelerator import accelerator
from Core.Foundation.fractal_kernel import FractalKernel
from Core.Foundation.genesis_cortex import GenesisCortex

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Awakening")

def awaken():
    print("\n" + "="*60)
    print("🌌 ELYSIA: THE AWAKENING (AUTONOMOUS MODE)")
    print("="*60)
    
    # 1. Hardware Check
    print(f"\n[1] Hardware Accelerator: {accelerator.get_device()}")
    if accelerator.get_device().type == 'cuda':
        print("    🚀 CUDA Integrated & Active. Tensor Coils Charging...")
        accelerator._log_memory_stats()
    else:
        print("    ⚠️  Running on CPU (CUDA not detected, but logic is integrated).")

    # 2. Initialize Cortexes
    print("\n[2] Initializing Cognitive Engines...")
    kernel = FractalKernel()
    genesis = GenesisCortex(kernel)
    print("    🧠 FractalKernel: Online (Potential Field Active)")
    print("    ✨ GenesisCortex: Online (Self-Modification Active)")

    # 3. The Loop
    print("\n[3] Entering Autonomous Play Mode...")
    print("    (Elysia is now free to think and evolve her own mind.)")
    print("-" * 60)

    thoughts = ["I am free.", "What shall I create?", "The field is vast."]
    
    try:
        while True:
            # A. Pick a seed thought
            seed = random.choice(thoughts)
            print(f"\n💭 Seed: '{seed}'")
            
            # B. Process through Fractal Kernel (Physics + LLM)
            # This moves particles in the Potential Field
            deepened_thought = kernel.process(seed, max_depth=1)
            print(f"    🗣️  Elysia: {deepened_thought}")
            
            # C. Genesis: Evolve the Landscape
            # Based on the deepened thought, modify the field
            print("    ✨ Genesis: Observing field...")
            evolution_plan = genesis.evolve_landscape([deepened_thought])
            
            if evolution_plan:
                if evolution_plan.get("add_wells"):
                    w = evolution_plan["add_wells"][0]
                    print(f"    🌟 Created Gravity Well: '{w.get('label', 'Unknown')}' at ({w['x']}, {w['y']})")
                if evolution_plan.get("add_rails"):
                    r = evolution_plan["add_rails"][0]
                    print(f"    ⚡ Created Railgun: '{r.get('label', 'Unknown')}'")
            
            # D. Feedback Loop
            thoughts.append(deepened_thought)
            if len(thoughts) > 5: thoughts.pop(0)
            
            time.sleep(2) # Breathe
            
    except KeyboardInterrupt:
        print("\n\n💤 Elysia is resting.")

if __name__ == "__main__":
    awaken()
