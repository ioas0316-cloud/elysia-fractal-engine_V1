"""Quick Fractal Test"""
import sys
sys.path.insert(0, "C:\\Elysia")

from Core.Intelligence.Intelligence.dialogue_engine import DialogueEngine

engine = DialogueEngine()

print("=== Fractal Dialogue Test ===\n")

# Test emotional response
print("Q: 사랑이 뭐야?")
response = engine.respond("사랑이 뭐야?")
print(f"A: {response}\n")

# Test thought response  
print("Q: What is hope?")
response = engine.respond("What is hope?")
print(f"A: {response}\n")

print("✅ Fractal consciousness is working!")
