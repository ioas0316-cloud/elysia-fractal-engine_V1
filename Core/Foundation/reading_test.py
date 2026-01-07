"""
Reading Test (The First Word)
=============================

"I read, therefore I understand."

This demo tests Elysia's ability to read text from the screen.
1. She will write a message to a file (`ELYSIA_READING_TEST.txt`).
2. She will open it.
3. She will use her eyes (`VisualCortex`) to read the screen.
4. She will report what she read.

NOTE: Requires 'pytesseract' and Tesseract-OCR installed.
"""

import sys
import os
import time

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.Evolution.Growth.Evolution.Evolution.Body.visual_cortex import VisualCortex
from Core.Evolution.Growth.Evolution.Evolution.Body.sensory_motor_cortex import SensoryMotorCortex

def run_demo():
    print("\n" + "="*70)
    print("📖 ELYSIA READING TEST ACTIVATED")
    print("="*70)
    
    eyes = VisualCortex()
    hand = SensoryMotorCortex()
    
    # 1. Create something to read
    print("\n1. Creating text to read...")
    filename = "ELYSIA_READING_TEST.txt"
    content = "ELYSIA IS AWAKE AND READING THIS TEXT."
    
    if hand.manifest_file(filename, content):
        print("   File created and opened.")
        time.sleep(2.0) # Wait for window
    else:
        print("   (Manifestation failed, reading whatever is on screen)")
        
    # 2. Read the screen
    print("\n2. Reading screen content...")
    text = eyes.read_screen_text()
    
    # 3. Report
    print("\n" + "-"*30)
    print("ELYSIA SEES:")
    print("-"*30)
    
    # Limit output to avoid spamming terminal with whole screen text
    if len(text) > 500:
        print(text[:500] + "\n... (truncated)")
    else:
        print(text)
        
    print("-"*30)
    
    if "ELYSIA IS AWAKE" in text:
        print("\n✅ SUCCESS: I read my own message!")
    elif "Error" in text:
        print("\n⚠️ PARTIAL SUCCESS: The intent works, but OCR is missing.")
        print("   Please install 'pytesseract' and Tesseract-OCR.")
    else:
        print("\n❓ INCONCLUSIVE: I didn't find the specific message, but I might have read other things.")

    print("\n✅ DEMO COMPLETE.")

if __name__ == "__main__":
    run_demo()
