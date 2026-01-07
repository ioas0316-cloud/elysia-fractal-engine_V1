"""
Test Sovereignty (The Living Loop)
==================================
Verifies that Elysia's Heartbeat is now aware of her Mind and Body.

1. Starts the Heartbeat.
2. Checks if GlobalObserver is active.
3. Checks if Body Integrity is monitored.
4. Triggers a Void/Impulse to see if the Will responds.
"""

import sys
import os
import time
import threading

sys.path.insert(0, r"c:\Elysia")

from Core.Autonomy.elysian_heartbeat import ElysianHeartbeat
from Core.Foundation.organism import cell, organ, NeuralNetwork

@cell("TestCell", sensitivity=1.0)
class MockCell:
    pass

def test_sovereignty():
    print("\n👑 TESTING SOVEREIGNTIES...")
    print("==========================")
    
    # 1. Start Life
    life = ElysianHeartbeat()
    life.is_alive = True
    
    print("✅ Heartbeat Initialized.")
    if hasattr(life, 'observer'):
        print("✅ GlobalObserver Connected (The Eye is Open).")
    else:
        print("❌ FAILURE: GlobalObserver NOT connected.")
        return

    # 2. Register a Cell
    print(f"   Neural Registry: {NeuralNetwork.scan_body()}")
    if "MockCell" in NeuralNetwork.scan_body():
        print("✅ Nervous System Functional (MockCell registered).")
    else:
        print("❌ FAILURE: Nervous System dead.")

    # 3. Running a Pulse
    print("\n💓 Running Pulse (Simulating 1 cycle)...")
    
    # Run ONE cycle manually
    start_time = time.time()
    life.last_tick = start_time - 1.0 # Force delta
    
    # Mocking observer for test
    # We want to see if observer.observe() is called. 
    # But since we use the real class, let's just run it and catch logs/output.
    
    try:
        # Hack to run one loop iteration: overwrite run_loop or just extract logic?
        # Let's run it in a thread for 2 seconds then stop
        t = threading.Thread(target=life.run_loop)
        t.daemon = True
        t.start()
        
        time.sleep(2.5)
        life.stop()
        t.join()
        
        # Check Soul Mesh for Integrity update
        integrity = life.soul_mesh.variables["Integrity"].value
        print(f"\n📊 Post-Pulse Integrity: {integrity}")
        if integrity > 0:
            print("✅ Body Integrity Monitored.")
        else:
            print("❌ FAILURE: Integrity check failed.")
            
    except Exception as e:
        print(f"❌ CRASH: {e}")

    print("\n🎉 SOVEREIGNTY TEST COMPLETE.")

if __name__ == "__main__":
    test_sovereignty()
