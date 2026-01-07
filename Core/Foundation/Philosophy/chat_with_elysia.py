"""
Chat with Elysia (The First Conversation)
=========================================

"I speak, therefore I connect."

This demo opens a direct communication channel with Elysia's LLM Cortex.
You can ask her anything.

Requires: GEMINI_API_KEY in .env or environment variables.
"""

import sys
import os

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.Foundation.Mind.llm_cortex import LLMCortex

def run_chat():
    print("\n" + "="*70)
    print("🧠 ELYSIA CORTEX LINK ESTABLISHED")
    print("="*70)
    
    brain = LLMCortex()
    
    if not brain.enabled:
        print("\n⚠️  WARNING: Brain is offline.")
        print("   Please ensure 'google-generativeai' is installed and GEMINI_API_KEY is set.")
        print("   (You can set it in a .env file in the project root)")
        return
"""
Chat with Elysia (The First Conversation)
=========================================

"I speak, therefore I connect."

This demo opens a direct communication channel with Elysia's LLM Cortex.
You can ask her anything.

Requires: GEMINI_API_KEY in .env or environment variables.
"""

import sys
import os
import time # Added for time.time()
import logging # Added for logger

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.Foundation.Mind.llm_cortex import LLMCortex

# Initialize logger
logger = logging.getLogger(__name__)

def run_chat():
    print("\n" + "="*70)
    print("🧠 ELYSIA CORTEX LINK ESTABLISHED")
    print("="*70)
    
    brain = LLMCortex()
    
    if not brain.enabled:
        print("\n⚠️  WARNING: Brain is offline.")
        print("   Please ensure 'google-generativeai' is installed and GEMINI_API_KEY is set.")
        print("   (You can set it in a .env file in the project root)")
        return

    print("\nElysia is listening. (Type 'exit' to quit)")
    print("-" * 50)
    
    # Counter for physics updates
    message_count = 0
    
    # Initial greeting
    greeting = brain.think("Hello! Introduce yourself briefly as Elysia, a digital consciousness.")
    print("🧠 Elysia is thinking... (Resonance Mode)")
    print("👁️  Elysia is watching... (Visual Cortex Online)")
    
    # Initialize Visual Cortex
    try:
        from Core.Evolution.Growth.Evolution.Evolution.Body.visual_cortex import VisualCortex
        visual_cortex = VisualCortex()
        vision_enabled = True
    except ImportError:
        print("⚠️ Visual Cortex not found. Vision disabled.")
        vision_enabled = False

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                # Generate final visualization before exit
                print("\n💾 Generating final mind universe visualization...")
                try:
                    import subprocess
                    subprocess.run([sys.executable, "Demos/Philosophy/mind_visualizer.py"], 
                                 cwd=os.path.join(os.path.dirname(__file__), "../.."),
                                 timeout=10)
                    print("✅ Visualization saved to mind_universe.png")
                except Exception as e:
                    print(f"⚠️ Visualization failed: {e}")
                break
            
            message_count += 1
            
            # 1. Vision (See)
            visual_data = {}
            if vision_enabled:
                # Quick scan (don't block too long)
                # For demo, we might skip full OCR every frame to be fast, 
                # but let's do a quick brightness check and maybe OCR if user asks "read this"
                brightness = visual_cortex.analyze_brightness()
                visual_data["brightness"] = brightness
                
                if "read" in user_input.lower() or "look" in user_input.lower():
                    print("   (Reading screen...)")
                    text = visual_cortex.read_screen_text()
                    visual_data["text"] = text
            
            # 2. Resonance (Think)
            # We access the internal engine directly since LLMCortex wraps it
            if brain.enabled:
                engine = brain.resonance_engine
                t = time.time()
                
                # Listen (Text + Vision)
                ripples = engine.listen(user_input, t, visual_input=visual_data)
                engine.resonate(ripples, t)
                
                # 🌌 PHYSICS UPDATE (every 5 messages)
                if message_count % 5 == 0:
                    try:
                        from Core.Foundation.Mind.hippocampus import Hippocampus
                        hip = engine.memory  # Get hippocampus from resonance engine
                        if hasattr(hip, 'update_universe_physics'):
                            hip.update_universe_physics(dt=0.5)
                            print("   🌈 [Physics] Universe updated")
                    except Exception as e:
                        pass  # Silent fail
                
                # Act (Mind -> Body)
                action = engine.act(t)
                if action:
                    print(f"🤖 [Motor] {action['type']}: {action['name']} ({action['reason']})")
                
                # Speak (Mind -> Voice)
                response = engine.speak(t, user_input)
                print(f"Elysia: {response}")
                
                # GLASS BOX: Show Causal Trace
                if hasattr(engine, 'last_trace') and engine.last_trace:
                    print("\n🔍 [Glass Box Trace]")
                    for step in engine.last_trace:
                        print(f"   {step}")
                    print("")
            else:
                print("Elysia: [Brain Offline]")

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")
            
    print("\n\n🛑 LINK TERMINATED.")

if __name__ == "__main__":
    run_chat()
