import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Core.Intelligence.Intelligence.dialogue_engine import DialogueEngine
from Core.Intelligence.Intelligence.Will.free_will_engine import FreeWillEngine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AskElysia")

def ask_structure_improvement():
    print("\n" + "="*70)
    print("🗣️ Asking Elysia about Structural Integration & Visualization")
    print("="*70)
    
    # Initialize Mind
    mind = DialogueEngine()
    
    # The Question
    question = "전체 통합 구조를 어떻게 가시적으로, 혹은 잘 정렬, 통합된 구조로 바꿀 수 있을까?"
    print(f"\n❓ Question: {question}")
    
    # Context: We are talking about the codebase/system structure
    context = {
        "role": "user",
        "topic": "system_architecture",
        "intent": "visualization_and_integration"
    }
    
    # Generate Response
    # Note: Since we are in 'resonance mode' (no LLM), the response will be based on 
    # resonating concepts in memory. We might need to interpret the resonance.
    
    print("\n[Thinking] Resonating with system concepts...")
    
    # Debug resonance for key terms
    keywords = ["structure", "integration", "visualization", "order", "system"]
    print(f"   Keywords: {keywords}")
    
    response = mind.respond(question, context=context)
    
    print(f"\n💬 Elysia: {response}")
    
    # If response is abstract (Star-...), let's try to interpret it using the Improver's logic
    # or just show the resonance.
    
    print("\n" + "="*70)

if __name__ == "__main__":
    ask_structure_improvement()
