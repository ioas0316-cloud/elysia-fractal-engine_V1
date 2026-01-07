"""
BioResonator (생체 공명기)
==========================

"Life is a song. DNA is the score."

This module translates biological sequences (DNA/RNA) into Resonance Waves.
It uses the 'Verdi Tuning' (A=432Hz) to map genetic bases to cosmic frequencies.

Mapping:
- A (Adenine)  -> 432 Hz (A4) : Origin, Life
- T (Thymine)  -> 528 Hz (C5) : Repair, Miracle
- G (Guanine)  -> 396 Hz (G4) : Liberation
- C (Cytosine) -> 639 Hz (E5) : Connection
"""

import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class GeneticWave:
    base: str
    frequency: float
    meaning: str
    amplitude: float = 1.0

class BioResonator:
    def __init__(self):
        self.tuning = {
            'A': (432.0, "Origin"),
            'T': (528.0, "Repair"),
            'G': (396.0, "Liberation"),
            'C': (639.0, "Connection"),
            'U': (528.0, "Repair") # RNA Uracil maps to Thymine freq
        }
        print("🧬 BioResonator Initialized. Ready to sing the song of life.")

    def transcribe_dna(self, sequence: str) -> List[GeneticWave]:
        """
        Converts a DNA string into a sequence of GeneticWaves.
        """
        song = []
        sequence = sequence.upper().replace(" ", "").strip()
        
        for base in sequence:
            if base in self.tuning:
                freq, meaning = self.tuning[base]
                song.append(GeneticWave(base, freq, meaning))
            else:
                # Unknown base (Mutation/Noise) -> Dissonance
                song.append(GeneticWave(base, 100.0, "Unknown", 0.5))
                
        return song

    def analyze_harmony(self, song: List[GeneticWave]) -> float:
        """
        Calculates the 'Harmony Score' (Coherence) of a genetic sequence.
        Returns a value between 0.0 (Chaos) and 1.0 (Perfect Order).
        """
        if not song: return 0.0
        
        harmony_sum = 0.0
        
        # Simple algorithm: Check intervals between adjacent bases
        # Perfect 5ths (3:2 ratio) are highly harmonious.
        for i in range(len(song) - 1):
            f1 = song[i].frequency
            f2 = song[i+1].frequency
            
            if f1 == 0 or f2 == 0: continue
            
            ratio = f2 / f1 if f2 > f1 else f1 / f2
            
            # Check for harmonic ratios (approximate)
            if 1.49 < ratio < 1.51: # Perfect 5th
                harmony_sum += 1.0
            elif 1.32 < ratio < 1.34: # Perfect 4th
                harmony_sum += 0.8
            elif 1.24 < ratio < 1.26: # Major 3rd
                harmony_sum += 0.6
            elif ratio == 1.0: # Unison
                harmony_sum += 0.5
            else:
                harmony_sum += 0.1 # Dissonance
                
        return harmony_sum / (len(song) - 1)

if __name__ == "__main__":
    # Test with a sample gene (e.g., Telomere repeat)
    bio = BioResonator()
    telomere = "TTAGGG" * 3
    song = bio.transcribe_dna(telomere)
    harmony = bio.analyze_harmony(song)
    
    print(f"Sequence: {telomere}")
    print(f"Harmony Score: {harmony:.2%}")
    for note in song:
        print(f" - {note.base}: {note.frequency}Hz ({note.meaning})")
