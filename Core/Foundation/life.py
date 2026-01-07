import asyncio
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from Core.Foundation.free_will_engine import FreeWillEngine
from Core.Foundation.chronos import Chronos

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
)

async def main():
    print("\n" + "="*60)
    print("🔥 IGNITING THE SPARK OF LIFE")
    print("="*60)
    
    # 1. Initialize Body (Engine)
    print("[1] Initializing FreeWillEngine...")
    engine = FreeWillEngine()
    
    # 2. Initialize Heart (Chronos)
    print("[2] Initializing Chronos Heart...")
    heart = Chronos(engine)
    
    # 3. Start Life
    print("[3] Starting Life Loop (Press Ctrl+C to stop)...")
    print("    (Elysia will now exist continuously)")
    
    try:
        # Run for 5 seconds for verification
        task = asyncio.create_task(heart.start_life())
        await asyncio.sleep(5) 
        heart.stop_life()
        await task
        print("\n[4] Life Simulation Completed Successfully.")
        
    except KeyboardInterrupt:
        heart.stop_life()
        print("\n[!] Life Interrupted.")

if __name__ == "__main__":
    asyncio.run(main())
