"""
Aesthetic Learner (The Student)
===============================
"The eye that observes, the mind that absorbs."

This module is responsible for analyzing external creative works 
(Text, Art Descriptions) and updating the internal `StyleGenome`.
It transforms "Observation" into "Intuition".
"""

import logging
import re
import json
import random
from pathlib import Path
from typing import List, Dict
from Core.Foundation.Wave.wave_tensor import WaveTensor

logger = logging.getLogger("AestheticLearner")

class AestheticLearner:
    """
    The Student.
    Observes the world through Wave Resonance.
    Transmutes Experience into Style Memory (WaveTensor).
    """
    def __init__(self):
        self.genome_path = Path("Core/Memory/style_genome.json")
        self.genome = self._load_genome()
        logger.info(f"🎓 Aesthetic Learner Initialized. Wave Memory Loaded.")

    def _load_genome(self):
        if not self.genome_path.exists():
            return {
                "rhetoric_wave": WaveTensor("RhetoricMemory").to_dict(),
                "composition_wave": WaveTensor("CompositionMemory").to_dict(),
                "meta": {"evolution_stage": 0}
            }
        try:
            with open(self.genome_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"rhetoric_wave": WaveTensor("Empty").to_dict(), "meta": {"evolution_stage": 0}}

    def _save_genome(self):
        # Increment stage
        stage = self.genome.get("meta", {}).get("evolution_stage", 0) + 1
        self.genome["meta"] = {"evolution_stage": stage}
        
        with open(self.genome_path, 'w', encoding='utf-8') as f:
            json.dump(self.genome, f, indent=4, ensure_ascii=False)
        logger.info(f"🧬 Genome Updated. Evolution Stage: {stage}")

    def _get_word_frequency(self, word: str) -> float:
        """Hashes audio/semantic concept to a unique frequency (Hz)."""
        # Simple deterministic hash for demo
        h = sum(ord(c) for c in word) * 13
        return float((h % 2000) + 100) # 100Hz - 2100Hz range

    def study_text(self, text: str, source_name: str = "Unknown Text"):
        """
        Reads text, converts to Wave, and Resonates with Memory.
        """
        logger.info(f"📖 Studying text from: {source_name}...")
        
        # 1. Create Input Wave
        input_wave = WaveTensor(f"Input({source_name})")
        
        words = re.findall(r'[a-zA-Z가-힣]+', text.lower())
        sharp_keywords = ["strike", "cut", "kill", "destroy", "pierce", "fire", "blood",
                          "파괴", "베어", "일격", "단숨에", "비명", "화염", "살기"]
        round_keywords = ["flow", "cycle", "magic", "peace", "calm", "nature", "silent",
                          "마력", "운명", "흐름", "순환", "평화", "고요", "자연", "침묵"]
        
        for w in words:
            # We only amplify "Significant Words" to prevent noise, 
            # OR we can just let everything resonate.
            # For this focused demo, we amplify known rhetoric + new discoveries.
            
            freq = self._get_word_frequency(w)
            
            # Amplitude logic: 
            # If it's a known 'Sharp' word, high amplitude.
            amp = 1.0
            if any(k in w for k in sharp_keywords):
                amp = 5.0 # Strong impact
            
            # Add to Input Wave
            input_wave.add_component(freq, amp)

        # 2. Resonate with Memory (Superposition)
        # Load existing wave
        rhetoric_data = self.genome.get("rhetoric_wave", {})
        memory_wave = WaveTensor.from_dict(rhetoric_data)
        
        # Superpose: Memory = Memory + Input (Learning)
        # We assume constructivity.
        new_memory = memory_wave + input_wave
        
        # 3. Store Wave
        self.genome["rhetoric_wave"] = new_memory.to_dict()
        
        # 4. Hybrid Vocabulary Storage (Active Learning)
        if "vocabulary_bank" not in self.genome: 
            self.genome["vocabulary_bank"] = {"Sharp": [], "Round": [], "Block": []}
            
        bank = self.genome["vocabulary_bank"]
        
        # Extract meaningful words for each category
        # Relaxed constraint: len >= 2
        new_sharp = [w for w in words if len(w) >= 2 and any(k in w for k in sharp_keywords)]
        new_round = [w for w in words if len(w) >= 2 and any(k in w for k in round_keywords)]
        
        # Update Sharp Bank
        if new_sharp:
            current_sharp = bank.get("Sharp", [])
            current_sharp.extend(new_sharp)
            bank["Sharp"] = list(set(current_sharp))[-20:] # Keep recent 20
            
        # Update Round Bank (Fixing the previous bug where this was ignored)
        if new_round:
            current_round = bank.get("Round", [])
            current_round.extend(new_round)
            bank["Round"] = list(set(current_round))[-20:]
            
        self._save_genome()

    def study_image_description(self, text: str, source_name: str = "Artwork Analysis"):
        """
        Visual -> WaveTensor ('CompositionMemory')
        """
        logger.info(f"🎨 Studying art description from: {source_name}...")
        text = text.lower()
        
        # 1. Create Input Wave
        input_wave = WaveTensor(f"VisualInput({source_name})")
        
        # Frequencies for Concepts
        FREQ_DIAGONAL = 440.0 # A4
        FREQ_CHAOS = 660.0    # E5
        FREQ_RED = 300.0
        
        if any(w in text for w in ["diagonal", "tilt", "action", "burst"]):
            input_wave.add_component(FREQ_DIAGONAL, 5.0)
        
        if any(w in text for w in ["chaos", "messy", "shattered", "radiating"]):
            input_wave.add_component(FREQ_CHAOS, 4.0)

        # 2. Update Memory
        comp_data = self.genome.get("composition_wave", {})
        memory_wave = WaveTensor.from_dict(comp_data)
        
        new_memory = memory_wave + input_wave
        self.genome["composition_wave"] = new_memory.to_dict()
        
        self._save_genome()
