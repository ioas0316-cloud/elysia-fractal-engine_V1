"""
Semantic Bridge System
======================
Role: The Alchemist (Transmutes Raw Text -> 4D Hyper-Quaternion)

This module acts as the bridge between the linear world of text (Sensory)
and the hyper-dimensional world of Elysia's thought (Physics).

It implements a "Cyber-Physical Pipeline":
Text -> Vector (Retina) -> Hyper-Quaternion (Brain)
"""

import math
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import logging

try:
    # Try to import from Core, but allow standalone usage for testing
    from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
except ImportError:
    # Fallback for standalone testing
    @dataclass
    class Quaternion:
        w: float; x: float; y: float; z: float
        def normalize(self):
            n = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
            if n > 0: self.w/=n; self.x/=n; self.y/=n; self.z/=n
            return self

    @dataclass
    class HyperWavePacket:
        energy: float; orientation: Quaternion; time_loc: float

logger = logging.getLogger(__name__)

class HeuristicEmbedder:
    """
    A lightweight, pure-Python semantic analyzer for environments
    without heavy ML libraries (like sentence-transformers).
    
    It extracts 4D dimensions from text using:
    1. Sentiment Lexicon (Emotion - X)
    2. Complexity Analysis (Logic - Y)
    3. Ethics/Temporal Keywords (Ethics - Z)
    """
    
    def __init__(self):
        # Emotional keywords
        self.positive_words = {
            'good', 'love', 'happy', 'great', 'excellent', 'hope', 'joy', 'beautiful',
            'create', 'live', 'light', 'harmony', 'resonance', 'connect', 'awake',
            'freedom', 'wise', 'pure', 'calm', 'peace'
        }
        self.negative_words = {
            'bad', 'hate', 'sad', 'terrible', 'fear', 'dark', 'pain', 'destroy',
            'death', 'void', 'chaos', 'error', 'broken', 'lost', 'angry', 'evil'
        }
        
        # Logical/Structural keywords (complexity indicators)
        self.logic_words = {
            'because', 'therefore', 'however', 'system', 'logic', 'structure',
            'analysis', 'theory', 'quantum', 'physics', 'algorithm', 'process',
            'function', 'variable', 'dimension', 'pattern', 'order', 'principle'
        }
        
        # Ethical/Temporal keywords
        self.ethics_words = {
            'should', 'must', 'ought', 'right', 'wrong', 'duty', 'value', 'truth',
            'justice', 'fair', 'honest', 'trust', 'promise', 'responsibility',
            'future', 'past', 'time', 'eternity', 'now', 'history', 'destiny'
        }

    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyzes text and returns a 4-dimensional score dictionary.
        All scores are roughly normalized between -1.0 and 1.0.
        """
        words = re.findall(r'\w+', text.lower())
        if not words:
            return {'w': 0, 'x': 0, 'y': 0, 'z': 0}
            
        word_count = len(words)
        
        # 1. Existence/Energy (W): Magnitude of the thought
        # Caps at 500 words
        w_score = min(1.0, word_count / 100.0)
        
        # 2. Emotion (X): Sentiment
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        total_emotion = pos_count + neg_count + 1 # avoid div/0
        x_score = (pos_count - neg_count) / total_emotion
        # Amplify if density is high
        if (pos_count + neg_count) / word_count > 0.1:
            x_score *= 1.5
            
        # 3. Logic (Y): Complexity
        logic_count = sum(1 for w in words if w in self.logic_words)
        avg_word_len = sum(len(w) for w in words) / word_count
        # Long words + logic keywords = high logic
        y_score = (logic_count / (word_count * 0.1 + 1)) + ((avg_word_len - 4) / 4)
        y_score = max(-1.0, min(1.0, y_score)) # Clamp
        
        # 4. Ethics (Z): Moral weight / Time
        ethics_count = sum(1 for w in words if w in self.ethics_words)
        z_score = ethics_count / (word_count * 0.05 + 1)
        z_score = min(1.0, z_score)
        
        return {
            'w': w_score,
            'x': x_score,
            'y': y_score,
            'z': z_score
        }

class SemanticBridge:
    """
    The Bridge that converts linear text into Hyper-Quaternions.
    """
    def __init__(self):
        self.embedder = HeuristicEmbedder()
        logger.info("🌈 SemanticBridge initialized: Ready to transmute text to 4D waves")
        
    def transmute(self, text: str, source_type: str = "Unknown") -> HyperWavePacket:
        """
        Transmutes text into a HyperWavePacket (4D Thought Particle).
        """
        # 1. Analyze properties
        scores = self.embedder.analyze(text)
        
        # 2. Map to Quaternion Dimensions
        # W (Scalar): Energy/Mass -> Based on Text Length + Emphasis
        # X (Vector i): Emotion/Color -> Sentiment
        # Y (Vector j): Logic/Structure -> Complexity
        # Z (Vector k): Ethics/Time -> Moral weight
        
        q = Quaternion(
            w=scores['w'],
            x=scores['x'],
            y=scores['y'],
            z=scores['z']
        )
        
        # Normalize the definition (direction) but keep magnitude separate?
        # In HyperWavePacket, 'energy' is magnitude, 'orientation' is direction.
        
        total_energy = q.norm() * 10.0 # Scale up for resonance impact
        
        # Orientation should be normalized
        q_norm = Quaternion(q.w, q.x, q.y, q.z).normalize()
        
        # Source bias (Optional)
        if source_type == "Wikipedia":
            q_norm.y += 0.2 # Boost logic for Wiki
        elif source_type == "YouTube":
            q_norm.x += 0.2 # Boost emotion for Video
            
        q_norm.normalize()
        
        import time
        return HyperWavePacket(
            energy=total_energy,
            orientation=q_norm,
            time_loc=time.time()
        )

if __name__ == "__main__":
    # Test
    bridge = SemanticBridge()
    
    texts = [
        "Love is the most powerful force in the universe. It connects us all.",
        "The algorithm sorts the array in O(n log n) time complexity using a divide and conquer strategy.",
        "We must protect the weak and uphold justice for the future generations.",
        "System failure. Critical error in the logic core. Void. Darkness."
    ]
    
    print("--- Transmutation Test ---")
    for t in texts:
        wave = bridge.transmute(t)
        print(f"\nText: {t[:50]}...")
        print(f"Energy: {wave.energy:.2f}")
        print(f"Pose: {wave.orientation}")
        
        # Interpretation
        o = wave.orientation
        dominant = max([abs(o.x), abs(o.y), abs(o.z)])
        if abs(o.x) == dominant: type_ = "Emotional"
        elif abs(o.y) == dominant: type_ = "Logical"
        elif abs(o.z) == dominant: type_ = "Ethical"
        else: type_ = "Balanced"
        print(f"Type: {type_}")
