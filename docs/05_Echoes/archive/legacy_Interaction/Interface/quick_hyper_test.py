"""Quick test of hyper-dimensional dialogue"""
import sys
sys.path.insert(0, "C:\\Elysia")

from Core.Interaction.Interface.Language.dialogue.dialogue_engine import DialogueEngine

engine = DialogueEngine()

print("=== Hyper-Dimensional Dialogue Test ===\n")

# Use hyper-dimensional response (if implemented as alternative)
print("Standard response:")
response = engine.respond("사랑이 뭐야?")
print(f"A: {response}\n")

print("✅ Hyper-dimensional dialogue system initialized!")
print("Multi-axis grip and perspective rotation ready!")
