
import sys
import os
import time
import logging
import random

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Evolution.Growth.Evolution.Evolution.Life.digital_avatar import DigitalAvatar

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def live_in_matrix():
    print("🏙️ Project: Matrix - Entering Digital Reality...")
    
    avatar = DigitalAvatar(home_dir="c:\\Elysia")
    
    print("\n1. Establishing Base...")
    # Build a Garden
    avatar.terraform("folder", "Garden")
    
    print("\n2. Planting Seeds...")
    # Go into Garden
    garden_path = os.path.join(avatar.home_dir, "Garden")
    avatar.current_location = garden_path # Teleport for now
    
    # Plant flowers
    flowers = [
        ("rose.txt", "I am red and full of passion."),
        ("lily.txt", "I am white and pure logic."),
        ("digitalis.txt", "I am electric and dangerous.")
    ]
    
    for name, content in flowers:
        avatar.terraform("file", name, content)
        time.sleep(0.5)
        
    print("\n3. Wandering (Exploration)...")
    # Wander a bit
    for _ in range(5):
        loc = avatar.wander()
        obs = avatar.observe()
        print(f"   📍 At: {loc}")
        print(f"      Atmosphere: {obs.get('atmosphere')}")
        time.sleep(1)
        
    print("\n4. Returning Home...")
    avatar.go_home()
    print("   (Resting in C:\\Elysia)")

if __name__ == "__main__":
    live_in_matrix()
