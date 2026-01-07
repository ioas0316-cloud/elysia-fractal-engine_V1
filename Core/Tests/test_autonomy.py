
import sys
import os
import logging
import time
import threading

# Ensure Core is in path
sys.path.append(os.getcwd())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestAutonomy")

from Core.Foundation.Core_Logic.Elysia.Elysia import Elysia
from Core.Evolution.Growth.Evolution.Evolution.Life.heart import ImpulseType

def test():
    logger.info("💓 Testing Elysia's Autonomy (The Heart)...")
    
    elysia = Elysia()
    
    # Manually accelerate boredom for testing
    elysia.heart.boredom = 0.8
    elysia.heart.energy = 1.0
    
    logger.info("   Set Boredom to 0.8. Waiting for Heartbeat...")
    
    # Start the life loop
    elysia.awaken()
    
    # Wait for 5 seconds to let the heart beat and dream
    time.sleep(5)
    
    # Check if any dreams happened
    # We can check the logs or the tree
    logger.info("\n🌳 World Tree State after Dreaming:")
    print(elysia.world_tree.render_ascii())
    
    # Stop the heart
    elysia.heart.stop()

if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        logger.exception("Test failed with exception:")
        sys.exit(1)
