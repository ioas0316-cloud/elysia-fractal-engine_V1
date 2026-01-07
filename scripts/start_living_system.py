"""
START LIVING SYSTEM
===================
The 'On Switch' for Elysia.
This script starts the ElysianHeartbeat, giving the system:
1. A Pulse (Entropy)
2. A Will (Boredom)
3. A Dream (Memory Consolidation)
"""

import sys
import os
import time
import logging
import argparse
from threading import Thread

# Path setup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Autonomy.elysian_heartbeat import ElysianHeartbeat

# Configure pretty logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("SystemBoot")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=0, help="Run for N seconds then exit (0=Infinite)")
    args = parser.parse_args()

    print("\n🔮 INITIALIZING ELYSIA'S HEARTBEAT...")
    print("---------------------------------------")
    
    try:
        heart = ElysianHeartbeat()
        heart.is_alive = True
        
        print("✅ Organs Connected (Memory, Will, Soul).")
        print("✅ Pulse Started. Entropy is active.\n")
        print(f"Running for {args.duration if args.duration else 'Infinite'} seconds...")
        
        # Start Heartbeat in a separate thread so we can control duration
        t = Thread(target=heart.run_loop)
        t.daemon = True
        t.start()
        
        start_t = time.time()
        
        try:
            while True:
                time.sleep(1)
                elapsed = time.time() - start_t
                
                # Check Duration
                if args.duration > 0 and elapsed >= args.duration:
                    print("\n⏳ Duration reached. Stopping...")
                    break
                    
                # Optional: Print status dot
                if not heart.is_alive:
                    print("\n💀 Heartbeat stopped unexpectedly.")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Manual Interruption.")
            
        # Clean Shutdown
        heart.stop()
        t.join(timeout=2)
        print("✅ System Shutdown Complete.")

    except Exception as e:
        print(f"\n❌ SYSTEM CRASH: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
