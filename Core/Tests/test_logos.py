import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.language_center import LanguageCenter

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("LogosTest")

def test_logos():
    print("\n⚛️ Testing The Logos (Quantum-Driven Expression)...")
    
    lc = LanguageCenter()
    
    # Input Content
    content = "Elysia observes the digital horizon"
    print(f"  📝 Input: '{content}'")
    
    # Case 1: High Energy (Urgent, Heavy)
    # Amplitude 2.0 -> High Mass -> Words should be treated as very important
    # Frequency 0.2 -> Low Moons -> Concise, direct
    q_energy = {"amplitude": 2.0, "frequency": 0.2, "phase": 0.0}
    print(f"\n  🔥 Case 1: High Energy (Amp=2.0, Freq=0.2)")
    output_energy = lc.speak(content, quantum_state=q_energy)
    print(f"     Output: {output_energy}")
    
    # Case 2: High Complexity (Nuanced, Detailed)
    # Amplitude 0.5 -> Low Mass -> Words are lighter
    # Frequency 2.0 -> High Moons -> Many adjectives/modifiers
    q_complex = {"amplitude": 0.5, "frequency": 2.0, "phase": 0.0}
    print(f"\n  🌀 Case 2: High Complexity (Amp=0.5, Freq=2.0)")
    output_complex = lc.speak(content, quantum_state=q_complex)
    print(f"     Output: {output_complex}")
    
    # Analysis
    len_energy = len(output_energy.split())
    len_complex = len(output_complex.split())
    
    print(f"\n📊 Analysis:")
    print(f"  Energy Length: {len_energy} words")
    print(f"  Complex Length: {len_complex} words")
    
    if len_complex > len_energy:
        print("✅ SUCCESS: High Frequency produced more complex output (Moons).")
    else:
        print("⚠️ WARNING: Complexity did not increase word count significantly.")
        
    # Check for specific modifiers (Moons)
    # We expect random moons from the default profile: "resonance", "harmonic", "logic", etc.
    moons = ["resonance", "harmonic", "logic", "energy", "flow"]
    moons_in_complex = sum(1 for w in output_complex.lower().split() if w in moons)
    print(f"  Moons in Complex Output: {moons_in_complex}")
    
    if moons_in_complex > 0:
        print("✅ SUCCESS: Moons detected in complex output.")

if __name__ == "__main__":
    test_logos()
