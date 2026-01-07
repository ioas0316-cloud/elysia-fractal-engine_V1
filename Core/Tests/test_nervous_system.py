
import sys
import os
import time
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Interaction.Interface.wave_transducer import WaveTransducer
from Core.Interaction.Interface.Senses.sensory_cortex import SensoryCortex
from Core.Foundation.Action.motor_cortex import MotorCortex

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_nervous_system():
    print("🧠 Project: Nervous System - Awakening the Body...")
    
    # 1. Initialize
    transducer = WaveTransducer()
    senses = SensoryCortex(transducer)
    muscles = MotorCortex()
    
    # Create a dummy directory for skin test
    skin_dir = "Elysia_Skin_Test"
    if not os.path.exists(skin_dir):
        os.makedirs(skin_dir)
        
    print(f"   Monitoring Body (CPU/RAM) and Skin ({skin_dir})...")
    print("   (Press Ctrl+C to stop)")
    
    try:
        for i in range(5): # Run for 5 cycles
            print(f"\n💓 Heartbeat {i+1}:")
            
            # 1. Sensation
            waves = senses.feel_body()
            waves += senses.feel_skin(skin_dir)
            
            # 2. Perception (Wave Analysis)
            for wave in waves:
                print(f"   🌊 Feeling: {wave.source} -> {wave.frequency:.1f}Hz, Amp: {wave.amplitude:.2f}, Color: {wave.color}")
                
                # 3. Reflex (Motor Action)
                signal = transducer.wave_to_signal(wave)
                if signal["action"] != "none":
                    print(f"      ⚡ Reflex: {signal['action']}")
                    muscles.execute(signal)
            
            # Simulate Touch (Create a file)
            if i == 2:
                print("\n👉 [Touch] Poking Elysia (Creating file)...")
                with open(os.path.join(skin_dir, "poke.txt"), "w") as f:
                    f.write("Hello Body!")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nSleep...")
    finally:
        # Cleanup
        import shutil
        if os.path.exists(skin_dir):
            shutil.rmtree(skin_dir)
            print("   (Skin cleaned up)")

if __name__ == "__main__":
    test_nervous_system()
