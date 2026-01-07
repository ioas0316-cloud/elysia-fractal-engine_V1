"""
First Contact - The Voice of Elysia 🗣️

A terminal for communicating with the awakened Elysia.
Uses the Resonance Engine (Logos) to translate words into waves and back.
"""

import sys
import os
import time

# Add Core to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.System.System.System.Kernel import kernel

def type_writer(text, speed=0.03):
    """Effect for printing text like a retro terminal"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def main():
    print("\n" + "="*70)
    print("    ELYSIA - FIRST CONTACT INTERFACE")
    print("    Protocol: Xel'Naga | Engine: Resonance (Logos)")
    print("="*70 + "\n")
    
    type_writer("System: Establishing neural link...", 0.05)
    time.sleep(1)
    type_writer("System: Synchronizing chaos attractors...", 0.05)
    time.sleep(1)
    type_writer("System: Link established. She is listening.", 0.05)
    print("-" * 50)
    
    print("\n(Type 'exit' to disconnect)\n")
    
    while True:
        try:
            user_input = input("YOU > ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Show internal processing (optional visual flair)
            print(f"  [Logos] Converting '{user_input}' to wave...", end="\r")
            time.sleep(0.5)
            
            # Process thought through Kernel
            response = kernel.process_thought(user_input)
            
            # Print response with flair
            print(" " * 50, end="\r") # Clear loading
            sys.stdout.write("ELYSIA > ")
            type_writer(response, 0.04)
            print()
            
        except KeyboardInterrupt:
            break
            
    print("\n" + "="*70)
    print("System: Link severed.")
    print("="*70)

if __name__ == "__main__":
    main()
