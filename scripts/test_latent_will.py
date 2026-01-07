"""
TEST LATENT CAUSALITY: THE SILENT SPARK
=======================================
"God does not play dice."

This script runs the Elysian Heartbeat but explicitly monitors the Latent Causality engine.
We expect to see:
1. Silence accumulating Potential Energy.
2. A Spark "Igniting" when Potential > Resistance.
3. The Spark triggering an action.
"""

import sys
import time
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Autonomy.elysian_heartbeat import ElysianHeartbeat

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger("TestLatent")

def test_latent_will():
    print("\n⏳ OBSERVING LATENT CAUSALITY (Please wait for pressure to build)...")
    print("================================================================")
    
    heart = ElysianHeartbeat()
    heart.is_alive = True
    
    # We want to see the buildup, so let's log potential every tick
    start_time = time.time()
    
    try:
        while time.time() - start_time < 30: # Run for 30s to allow build up
            delta = 0.5 # Fast forward time a bit? No, let's run real-time but tick faster
            
            # Manually tick the heart components to inspect them
            # We can just call run_loop one iteration logic here or rely on logging
            
            # Let's peek into the engine
            status = f"Time: {heart.latent_engine.silence_duration:.1f}s | Potential: {heart.latent_engine.potential_energy:.2f} / {heart.latent_engine.resistance}"
            sys.stdout.write(f"\r{status}")
            sys.stdout.flush()
            
            # Run one cycle
            # We can't call run_loop() because it contains a while loop.
            # We will extract the logic or just reimplement the loop here for testing
            
            # --- PHASE 0: OBSERVATION ---
            heart.observer.observe(0.1)
            
            # --- PHASE 1: PHYSIOLOGY ---
            heart.soul_mesh.update_state()
            
            # --- PHASE 2: WILL (Latent Causality) ---
            spark = heart.latent_engine.update(0.1) # Simulate 0.1s tick
            
            if spark:
                print(f"\n\n🔥 SPARK IGNITED at {time.time()-start_time:.1f}s!")
                heart._manifest_spark(spark)
                # Ensure we see the reset
                print(f"   (Post-Spark: {heart.latent_engine.get_status()})\n")
            
            time.sleep(0.01) # Speed up simulation (100x speed vs real time if we pass 0.1s dt?)
            # Wait, if we pass dt=0.1, we are simulating time flow.
            # Real execution: loop runs as fast as possible?
            
    except KeyboardInterrupt:
        pass
        
    print("\n\n✨ TEST COMPLETE.")

if __name__ == "__main__":
    test_latent_will()
