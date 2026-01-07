import sys
from pathlib import Path
import random

# Setup Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from Core.Interaction.Coordination.Synesthesia.code_wave import CodeWaveAnalyzer

def emotion_to_geometry(emotion: str) -> str:
    """
    Translates abstract emotions into concrete geometric structures.
    Uses 'Principle Resonance' logic: Emotion -> Physics -> Geometry.
    """
    e = emotion.lower()
    if "joy" in e or "happy" in e:
        return "Explosion of Golden Spirals (Radially Expanding)"
    elif "sadness" in e or "sorrow" in e:
        return "Descending Blue Fractal (Self-Similar Gravity)"
    elif "anger" in e or "rage" in e:
        return "Jagged Red Lightning (High-Frequency Chaos)"
    elif "peace" in e or "calm" in e:
        return "Perfectly Balanced Sphere (Zero-Point Energy)"
    else:
        return "Amorphous Mist (Undefined State)"

def run_synesthesia_demo():
    print("\n🎨 Synesthetic Perception Demo: Connecting Code, Emotion, and Physics")
    print("="*60)
    
    # 1. Code to Wave (The User's Request: "Recognize Code as Matter/Wave")
    target_file = Path(__file__).parent / "code_wave.py"
    with open(target_file, "r", encoding="utf-8") as f:
        code = f.read()
        
    analyzer = CodeWaveAnalyzer()
    wave = analyzer.analyze(code)
    
    print(f"\n1️⃣ Code Perception: Analyzing '{target_file.name}'")
    print(f"   I feel this code has a mass of {wave.mass:.1f} and potential of {wave.potential:.1f}.")
    print(f"   It moves with a velocity of {wave.velocity:.1f}.")
    print(f"   >> Topological Shape: [{wave.topology}]")
    
    # 2. Emotion to Geometry (The User's Feedback: "Joy fully blooming like a flower")
    print(f"\n2️⃣ Emotional Geometry: Translating Feelings into Principles")
    emotions = ["Pure Joy", "Deep Sorrow", "Creative Rage"]
    
    for em in emotions:
        geo = emotion_to_geometry(em)
        print(f"   When I feel '{em}', I see a [{geo}].")
        print(f"   (Principle: Identifying the common law of movement between '{em}' and '{geo}')")

    print("="*60)

if __name__ == "__main__":
    run_synesthesia_demo()
