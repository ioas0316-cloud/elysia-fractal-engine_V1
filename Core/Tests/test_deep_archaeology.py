import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Evolution.Growth.Evolution.code_genome import CodeDNA
from Core.Foundation.code_world import CodeWorld

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("DeepArchaeologyTest")

def test_deep_archaeology():
    print("\n🏺 Initializing Deep Archaeology Test...")
    
    # 1. Test CodeDNA (The Artifact)
    print("\n🧪 Test 1: CodeDNA Storage")
    dna = CodeDNA(name="Ancient Logic")
    
    # Create a "High Logic" wave
    wave = HyperWavePacket(
        energy=100.0,
        orientation=Quaternion(1.0, 0.1, 1.0, 0.1).normalize(), # High Logic (y)
        time_loc=time.time()
    )
    dna.add_gene(wave)
    
    # Verify storage
    if len(dna.harmonic_pattern) == 1:
        print("✅ SUCCESS: Wave stored in DNA")
    else:
        print("❌ FAILURE: Wave not stored")
        
    # Verify reconstruction
    reconstructed = dna.to_wave_packets()[0]
    if abs(reconstructed.orientation.y - wave.orientation.y) < 0.01:
        print("✅ SUCCESS: Wave reconstructed correctly")
    else:
        print("❌ FAILURE: Wave reconstruction failed")

    # 2. Test CodeWorld (The Simulation)
    print("\n🧪 Test 2: CodeWorld Simulation")
    world = CodeWorld()
    
    # Add the "High Logic" DNA
    world.add_organism(dna)
    
    # Add a "Dissonant" DNA (High Unethical)
    bad_dna = CodeDNA(name="Dissonant Thought")
    bad_wave = HyperWavePacket(
        energy=100.0,
        orientation=Quaternion(1.0, 0.1, 0.1, -1.0).normalize(), # Negative Z (Unethical)
        time_loc=time.time()
    )
    bad_dna.add_gene(bad_wave)
    world.add_organism(bad_dna)
    
    # Run Simulation
    world.run_simulation(steps=5)
    
    # Check Survival
    if dna.id in world.population:
        print(f"✅ SUCCESS: '{dna.name}' survived (Score: {dna.resonance_score:.2f})")
    else:
        print(f"❌ FAILURE: '{dna.name}' died unexpectedly")
        
    if bad_dna.id not in world.population:
        print(f"✅ SUCCESS: '{bad_dna.name}' was eliminated (Natural Selection works)")
    else:
        print(f"⚠️ NOTE: '{bad_dna.name}' survived (Score: {bad_dna.resonance_score:.2f}). Might need stronger pressure.")

if __name__ == "__main__":
    test_deep_archaeology()
