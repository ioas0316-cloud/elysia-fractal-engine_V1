"""
Test Elysia's Dialogue Capability
==================================
Progressive complexity testing.
"""

from Core.Interaction.Interface.Language.dialogue.dialogue_engine import DialogueEngine

def test_dialogue():
    print("=== Elysia Dialogue Test ===\n")
    
    elysia = DialogueEngine()
    
    # Test 1: Simple greeting (Korean)
    print("👤 User: 안녕")
    response = elysia.respond("안녕")
    print(f"🌟 Elysia: {response}")
    print(f"   [State: {elysia.get_emotional_state()}]\n")
    
    # Test 2: Simple question (Korean)
    print("👤 User: 배고파?")
    response = elysia.respond("배고파?")
    print(f"🌟 Elysia: {response}")
    print(f"   [State: {elysia.get_emotional_state()}]\n")
    
    # Test 3: English
    print("👤 User: What is love?")
    response = elysia.respond("What is love?")
    print(f"🌟 Elysia: {response}")
    print(f"   [State: {elysia.get_emotional_state()}]\n")
    
    # Test 4: Complex (Korean)
    print("👤 User: 희망과 고통에 대해 이야기해줘")
    response = elysia.respond("희망과 고통에 대해 이야기해줘")
    print(f"🌟 Elysia: {response}")
    print(f"   [State: {elysia.get_emotional_state()}]\n")
    
    # Test 5: No known concepts
    print("👤 User: 오늘 날씨 좋다")
    response = elysia.respond("오늘 날씨 좋다")
    print(f"🌟 Elysia: {response}")
    print(f"   [State: {elysia.get_emotional_state()}]\n")
    
    print("=== Tests Complete ===")
    print(f"Total exchanges: {len(elysia.conversation_history)}")

if __name__ == "__main__":
    test_dialogue()
