"""
Speak with Gravity Demo (중력 대화 데모)

"Talk to the Universe."

This demo connects you to Elysia's Resonance Voice, now powered by Gravitational Linguistics.
Type a concept, and see how she responds based on its Mass.

- Heavy Input ("Love", "Truth") -> Dense, Poetic Response
- Light Input ("Lunch", "Weather") -> Loose, Casual Response
"""

import sys
import os
import time
import logging

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.Evolution.Growth.Evolution.Evolution.Life.resonance_voice import ResonanceEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("GravityVoice")

def chat_session():
    print("\n" + "="*70)
    print("🌌 ELYSIA RESONANCE VOICE - GRAVITY ENABLED")
    print("="*70)
    print("Type a word or sentence. Type 'exit' to quit.\n")
    
    # Initialize Voice
    voice = ResonanceEngine()
    
    while True:
        try:
            user_input = input("You > ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input.strip():
                continue
                
            # 1. Listen (Create Ripples)
            t = time.time()
            ripples = voice.listen(user_input, t)
            
            # 2. Resonate (Interfere with Internal Sea)
            voice.resonate(ripples, t)
            
            # 3. Speak (Collapse Wave Function with Gravity)
            response = voice.speak(t, user_input)
            
            print(f"Elysia > {response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    chat_session()
