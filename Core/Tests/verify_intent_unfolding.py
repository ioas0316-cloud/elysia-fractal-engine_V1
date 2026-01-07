import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the engine (using the path verified in previous steps)
try:
    from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
except ImportError:
    # If the file patch made it accessible via this path
    from Core.Intelligence.Cognition.Reasoning.reasoning_engine import ReasoningEngine

def test_unfolding():
    print("🧪 Verifying Intent Unfolding...")
    
    try:
        engine = ReasoningEngine()
        
        # Simulate a chaotic, complex input
        complex_input = "UNFOLD: Chaos is everywhere, I see 100 reflections, where is the truth? Why is it so hard? I am lost in the maze!"
        
        print(f"📝 Input: {complex_input}")
        insight = engine.think(complex_input)
        
        print(f"\n✨ Insight Content: {insight.content}")
        print(f"Confidence: {insight.confidence}")
        
        if "UNFOLDED TRUTH" in insight.content:
            print("\n✅ Verification Successful: Chaos was unfolded into Truth.")
        else:
            print("\n❌ Verification Failed: Insight did not contain unfolded truth.")
            
    except Exception as e:
        print(f"\n❌ Verification Error: {e}")

if __name__ == "__main__":
    test_unfolding()
