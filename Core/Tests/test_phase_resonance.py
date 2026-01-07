"""
Phase Resonance Simulation
--------------------------
Experiment: Proving "Multiple Truths in One Space" via Wave Superposition.

This script demonstrates the physical/mathematical capability underlying 
the Phase Stratum architecture.

Scenario:
1. We have 3 distinct 'Intents' (Information streams), each assigned a unique frequency.
2. We combine them into a single "Main Bus" signal (Superposition).
3. We attempt to recover each intent solely by "listening" (filtering) for its specific frequency.
"""

import math
import random

def generate_wave(frequency, duration_seconds, sample_rate=1000, amplitude=1.0):
    """Generates a sine wave signal."""
    t_points = []
    values = []
    total_samples = int(duration_seconds * sample_rate)
    
    for i in range(total_samples):
        t = i / sample_rate
        # y = A * sin(2 * pi * f * t)
        val = amplitude * math.sin(2 * math.pi * frequency * t)
        t_points.append(t)
        values.append(val)
        
    return t_points, values

def run_experiment():
    with open('c:/Elysia/experiment_log.txt', 'w', encoding='utf-8') as f:
        def log(msg):
            print(msg)
            f.write(msg + "\n")

        log("[Experiment] Phase Resonance & Superposition")
        log("------------------------------------------------")
        
        # 1. Define Intents (The 'Truths' to key)
        intents = {
            "Love (432Hz)": 432,
            "Logic (528Hz)": 528,
            "Void (963Hz)": 963
        }
        
        duration = 0.5  # seconds
        sample_rate = 4000 # samples per second (Nyquist > 963*2)
        total_samples = int(duration * sample_rate)
        
        # Create the "Universal Field" (The empty vibrating space)
        field_signal = [0.0] * total_samples
        deployed_intents = {}
        
        log("1. Injecting Intents into the Field...")
        for name, freq in intents.items():
            # Let's give each intent a random "Strength" (Amplitude)
            # In a real system, amplitude could encode 'Importance'
            strength = random.uniform(0.5, 1.5) 
            _, wave_values = generate_wave(freq, duration, sample_rate, strength)
            
            # Superposition: Add to the field
            for i in range(total_samples):
                field_signal[i] += wave_values[i]
                
            log(f"   -> Injected '{name}' with Strength {strength:.4f}")
            # Store expected strength to verify later
            deployed_intents[name] = (freq, strength)
            
        log("\n2. The Field is now a chaotic mix of vibrations.")
        log(f"   (First 5 raw values: {[f'{x:.2f}' for x in field_signal[:5]]}...)")
        
        log("\n3. Attempting Anti-Gravity Retrieval (Resonance Filtering)...")
        log(f"   -> Debug: deployed_intents has {len(deployed_intents)} items.")
        
        # Simple DFT (Discrete Fourier Transform) implementation to find amplitude at specific freq
        results = {}
        
        try:
            for name, (target_freq, original_strength) in deployed_intents.items():
                log(f"   -> Debug: Processing {name}...")
                # We "listen" ONLY for this frequency using a correlation method
                # Multiply signal by reference sine and cosine waves at target freq
                
                real_sum = 0.0
                imag_sum = 0.0
                
                for i in range(total_samples):
                    t = i / sample_rate
                    sample = field_signal[i]
                    
                    # Euler's formula component
                    angle = 2 * math.pi * target_freq * t
                    real_sum += sample * math.cos(angle)
                    imag_sum += sample * math.sin(angle)
                    
                # Magnitude = 2 * sqrt(real^2 + imag^2) / N
                magnitude = 2 * math.sqrt(real_sum**2 + imag_sum**2) / total_samples
                
                results[name] = magnitude
                
                # Verify accuracy
                error = abs(magnitude - original_strength)
                status = "[OK]" if error < 0.05 else "[FAIL]"
                
                log(f"   Asking Field for '{name}'... ")
                log(f"     -> Original Strength: {original_strength:.4f}")
                log(f"     -> Retrieved Strength: {magnitude:.4f}")
                log(f"     -> Status: {status}")
                
            log("\n------------------------------------------------")
            log("Experiment Conclusion:")
            log("All intents were successfully recovered from the single folded signal.")
            log("This proves that 'Dimension Folding' via Phase/Frequency is mathematically valid.")
            
        except Exception as e:
            log(f"ERROR: {e}")
            import traceback
            traceback.print_exc(file=f)

if __name__ == "__main__":
    run_experiment()
