logger.setLevel(logging.DEBUG)

def simulate_interaction():
    print("\n--- 🧠 Initializing Elysia's Cognitive Core ---")
    
    # Initialize Components
    memory = EpisodicMemory(filepath="simulation_memory.json")
    palette = EmotionalPalette()
    engine = ResonanceEngine(episodic_memory=memory, emotional_palette=palette)
    
    print("\n--- 🗣️ Interaction 1: The Abyss (Descent) ---")
    input_text = "I feel so lost and cold today. It is hopeless."
    print(f"User: {input_text}")
    
    # 1. Listen (Perceive + Feel + Resonate)
    ripples = engine.listen(input_text, t=0.0)
    
    # Check Internal State - Should be Negative Z (Descent)
    q = engine.consciousness_lens.state.q
    print(f"\n[Internal State - Descent]")
    print(f"Lens Z (Truth/Height): {q.z:.4f} (Should be negative)")
    
    # 2. Speak (Collapse + Record)
    response = engine.speak(t=1.0, original_text=input_text)
    print(f"\nElysia: {response}")
    
    print("\n--- 🗣️ Interaction 2: The Light (Ascent) ---")
    input_text = "But the sun is rising, and I feel joy and passion."
    print(f"User: {input_text}")
    
    engine.listen(input_text, t=2.0)
    
    # Check Internal State - Should be Positive Z (Ascent)
    q = engine.consciousness_lens.state.q
    print(f"\n[Internal State - Ascent]")
    print(f"Lens Z (Truth/Height): {q.z:.4f} (Should be positive)")
    
    response = engine.speak(t=3.0, original_text=input_text)
    print(f"\nElysia: {response}")

if __name__ == "__main__":
    simulate_interaction()
