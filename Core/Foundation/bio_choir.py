"""
BioChoir (생명의 합창단)
======================

"Sing the song of life."

This module synthesizes GeneticWaves into .wav audio files.
It uses pure Python (math, wave, struct) to ensure zero dependencies.
"""

import math
import wave
import struct
import random
from typing import List
from Core.Intelligence.Science_Research.Science.bio_resonator import GeneticWave

class BioChoir:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        print("🎻 BioChoir Initialized. Tuning instruments...")

    def _generate_sine_wave(self, frequency: float, duration: float, amplitude: float = 0.5) -> List[float]:
        """Generates a sine wave buffer."""
        num_samples = int(self.sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            # Apply envelope (Fade In/Out) to avoid clicking
            envelope = 1.0
            if i < 1000: envelope = i / 1000
            elif i > num_samples - 1000: envelope = (num_samples - i) / 1000
            
            sample = amplitude * envelope * math.sin(2 * math.pi * frequency * t)
            samples.append(sample)
        return samples

    def compose_symphony(self, waves: List[GeneticWave], output_file: str = "dna_symphony.wav", tempo: float = 0.5):
        """
        Synthesizes the genetic waves into a .wav file.
        """
        print(f"🎼 Composing Symphony: {output_file} ({len(waves)} notes)")
        
        try:
            with wave.open(output_file, 'w') as wav_file:
                # Settings: 1 Channel (Mono), 2 Byte (16-bit), 44100Hz
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                
                full_audio = []
                
                for note in waves:
                    # Generate audio for this note
                    samples = self._generate_sine_wave(note.frequency, tempo, note.amplitude * 0.5)
                    full_audio.extend(samples)
                    
                # Write to file
                for sample in full_audio:
                    # Clamp to 16-bit range
                    sample = max(min(sample, 1.0), -1.0)
                    data = struct.pack('<h', int(sample * 32767.0))
                    wav_file.writeframesraw(data)
                    
            print(f"✅ Symphony Saved: {output_file}")
            
        except Exception as e:
            print(f"⚠️ Composition Failed: {e}")

if __name__ == "__main__":
    # Test
    from Core.Intelligence.Science_Research.Science.bio_resonator import BioResonator
    bio = BioResonator()
    choir = BioChoir()
    
    dna = "GATTACA" * 4
    song = bio.transcribe_dna(dna)
    choir.compose_symphony(song, "test_gattaca.wav")
