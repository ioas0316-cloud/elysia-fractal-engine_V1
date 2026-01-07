import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("BabelTest")

def test_babel():
    print("\n🗼 Initializing Babel Test...")
    
    engine = ReasoningEngine()
    
    # 1. Create a dummy text file to learn from
    dummy_text = """
    Verily, the code is a magnificent beast. It flows like a river of stars.
    Indeed, we must contemplate the nature of the loop.
    Forsooth, the variable is but a vessel for the soul.
    """
    dummy_path = os.path.abspath("babel_test.txt")
    with open(dummy_path, "w") as f:
        f.write(dummy_text)
        
    dummy_url = f"file:///{dummy_path}" # WebCortex uses urllib, so file:// works
    
    # 2. Learn Language
    print(f"\n📚 Learning from: {dummy_url}")
    intent = f"LEARN_LANGUAGE: {dummy_url}"
    insight = engine.think(intent)
    print(f"Result: {insight.content}")
    
    # 3. Speak (Simulate a thought)
    # We manually trigger _collapse_wave to test speaking since think() usually does search/create/analyze
    # But wait, think() calls _collapse_wave at the end if no special intent.
    # So let's just ask a normal question.
    
    print("\n🗣️ Testing Speech...")
    # We need to ensure think() reaches _collapse_wave.
    # If we ask "What is code?", it might search.
    # Let's just call speak directly on the language center for unit testing, 
    # or rely on the engine's state if we can.
    
    # Since think() is complex, let's test the component directly first to be sure.
    if hasattr(engine, 'language_center'):
        speech = engine.language_center.speak("Hello World")
        print(f"Spoken: {speech}")
        
        if "learned_" in speech or "Verily" in speech or "Indeed" in speech or "Forsooth" in speech:
             print("✅ SUCCESS: Style applied")
        else:
             print("❌ FAILURE: Style not applied")
    else:
        print("❌ FAILURE: LanguageCenter not initialized")

    # 4. Test Grand Cross (Celestial Mechanics)
    print("\n⚔️ Testing Grand Cross (Celestial Mechanics)...")
    if hasattr(engine, 'language_center'):
        # Simulate an emotion vector
        emotion_vector = {"joy": 0.8, "love": 0.5}
        
        # Input sentence
        input_text = "Elysia creates fractal reality"
        
        speech = engine.language_center.speak(input_text, emotion_vector)
        print(f"Grand Cross Speech: {speech}")
        
        # Check if output is a valid sentence (ends with punctuation)
        if speech.endswith((".", "!", "?")):
             print("✅ SUCCESS: Grand Cross Aligned (Sentence formed)")
        else:
             print("❌ FAILURE: Grand Cross Alignment Failed")
             
        # Check for moons (modifiers)
        if "radiant" in speech or "warm" in speech:
             print("✅ SUCCESS: Moons (Adjectives) Orbiting")
    
    # Cleanup
    if os.path.exists(dummy_path):
        os.remove(dummy_path)

if __name__ == "__main__":
    test_babel()
