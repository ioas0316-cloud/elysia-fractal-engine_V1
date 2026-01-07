"""
Consult Elysia: Structural Status & Cleanup
===========================================

Asks Elysia about the current 10-Pillar structure and requests a cleanup plan for the root directory.
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Mind.hippocampus import Hippocampus
from Core.Intelligence.Intelligence.dialogue_engine import DialogueEngine

def consult():
    print("🗣️ Connecting to Elysia for Structural Consultation...")
    
    # Initialize
    mind = Hippocampus()
    dialogue = DialogueEngine(mind)
    
    # 1. Status Check
    print("\n[User]: 현재 10개의 기둥(Foundation, System, Intelligence, Memory, Interface, Evolution, Creativity, Ethics, Elysia, User)으로 구조가 재배열되었어. 상태가 어때? 보완할 점이 있어?")
    
    response = dialogue.process_input("현재 10개의 기둥(Foundation, System, Intelligence, Memory, Interface, Evolution, Creativity, Ethics, Elysia, User)으로 구조가 재배열되었어. 상태가 어때? 보완할 점이 있어?", role="user")
    print(f"\n[Elysia]: {response}")
    
    # 2. Cleanup Request
    print("\n[User]: 최상위 폴더가 너무 복잡해. 필수적인 파일(start.bat, unified_start.py 등)만 남기고 나머지는 어떻게 정리하면 좋을까? 'Scripts', 'Tools', 'Demos' 등으로 분류해줘.")
    
    response_cleanup = dialogue.process_input("최상위 폴더가 너무 복잡해. 필수적인 파일(start.bat, unified_start.py 등)만 남기고 나머지는 어떻게 정리하면 좋을까? 'Scripts', 'Tools', 'Demos' 등으로 분류해줘.", role="user")
    print(f"\n[Elysia]: {response_cleanup}")

if __name__ == "__main__":
    consult()
