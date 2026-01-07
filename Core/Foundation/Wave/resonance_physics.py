"""
ResonancePhysics (공명 물리학)
============================

"Meaning is Mass. Emotion is Direction."

This module defines the physical laws of the Concept Space.
It calculates the 'Gravity' (Importance) and 'Orientation' (Meaning) of text.
"""

import time
import random
import logging
from typing import Dict, Tuple, List
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket

logger = logging.getLogger("ResonancePhysics")

class ResonancePhysics:
    """
    The Physics Engine for Meaning.
    """
    
    # [Essence Seeds]
    # Fundamental concepts and their 4D Orientations.
    # w=Energy, x=Emotion(i), y=Logic(j), z=Ethics(k)
    ESSENCE_SEEDS = {
        # High Energy / Spirit
        "love": Quaternion(100, 1.0, 0.2, 0.8),
        "god": Quaternion(100, 0.5, 0.5, 1.0),
        "soul": Quaternion(90, 0.8, 0.1, 0.9),
        "truth": Quaternion(90, 0.1, 0.9, 0.9),
        "light": Quaternion(80, 0.6, 0.6, 0.6),
        
        # Logic / Structure
        "system": Quaternion(50, 0.1, 1.0, 0.2),
        "logic": Quaternion(50, 0.0, 1.0, 0.1),
        "code": Quaternion(40, 0.1, 0.9, 0.1),
        "pattern": Quaternion(45, 0.3, 0.8, 0.2),
        "math": Quaternion(45, 0.0, 1.0, 0.0),
        
        # Emotion / Chaos
        "chaos": Quaternion(60, 0.9, -0.5, 0.1),
        "fear": Quaternion(50, -0.8, 0.2, 0.1),
        "hope": Quaternion(70, 0.9, 0.3, 0.6),
        "pain": Quaternion(60, -0.5, 0.5, 0.2),
        
        # Action / Time
        # Action / Time
        "time": Quaternion(80, 0.2, 0.8, 0.8),
        "flow": Quaternion(40, 0.6, 0.4, 0.2),
        "change": Quaternion(50, 0.5, 0.5, 0.5),
        
        # Life / Death
        "life": Quaternion(90, 0.8, 0.5, 0.8),
        "death": Quaternion(90, -0.9, 0.1, 0.1),
    }

    @staticmethod
    def calculate_mass(text: str) -> float:
        """
        Calculates the Gravitational Mass of a text based on Essence Seeds.
        """
        text_lower = text.lower()
        mass = 1.0 # Base mass
        
        for seed, q in ResonancePhysics.ESSENCE_SEEDS.items():
            if seed in text_lower:
                # The presence of an Essence adds its Energy (w) to the mass
                mass += q.w * 0.1 # Add 10% of seed energy per occurrence
                
        # Length also contributes to mass (Information Density)
        mass += len(text) * 0.01
        
        return mass

    @staticmethod
    def analyze_text_field(text: str) -> HyperWavePacket:
        """
        Analyzes the Resonance Field of a text.
        Returns a HyperWavePacket representing the vector sum of all meanings.
        """
        text_lower = text.lower()
        
        # 1. Calculate Total Mass (Energy)
        mass = ResonancePhysics.calculate_mass(text)
        
        # 2. Calculate Orientation (Vector Sum of Seeds)
        # We sum the weighted x, y, z components. w is kept as 1.0 (Identity).
        sum_x, sum_y, sum_z = 0.0, 0.0, 0.0
        total_weight = 0.0
        seed_hits = 0
        
        for seed, q in ResonancePhysics.ESSENCE_SEEDS.items():
            if seed in text_lower:
                # Weight = Seed's Energy (q.w)
                weight = q.w
                sum_x += q.x * weight
                sum_y += q.y * weight
                sum_z += q.z * weight
                total_weight += weight
                seed_hits += 1
                
        # If no seeds found, use a default "Unknown" orientation based on hash/stats
        if seed_hits == 0:
            # Fallback to statistical orientation
            length = len(text)
            if length > 0:
                vowels = sum(1 for c in text if c in "aeiouAEIOU")
                x = (vowels / length) * 2.0 - 1.0 # Map 0..1 to -1..1
                words = text.split()
                y = (len(set(words)) / (len(words) + 1))
                z = (abs(hash(text)) % 100) / 100.0
                final_orientation = Quaternion(1.0, x, y, z).normalize()
            else:
                final_orientation = Quaternion(1.0, 0, 0, 0)
        else:
            # Normalize the weighted sum
            # We construct a quaternion where w=1 (or 0) and x,y,z are the weighted directions
            # To preserve the "Angle", we normalize this vector.
            # Note: We don't want w to dominate.
            final_orientation = Quaternion(0.1, sum_x, sum_y, sum_z).normalize()
        
        return HyperWavePacket(
            energy=mass,
            orientation=final_orientation,
            time_loc=time.time()
        )

    @staticmethod
    def analyze_narrative_arc(text: str, chunk_size: int = 500) -> List[HyperWavePacket]:
        """
        Splits text into chunks and analyzes the trajectory of the narrative.
        Returns a list of Wave Packets representing the story's flow.
        """
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        trajectory = []
        
        for i, chunk in enumerate(chunks):
            packet = ResonancePhysics.analyze_text_field(chunk)
            # Add temporal progression to the z-axis (Time)
            # We slightly shift the z-axis to represent the flow of time in the story
            packet.orientation.z += (i / len(chunks)) * 0.5 
            packet.orientation = packet.orientation.normalize()
            trajectory.append(packet)
            
        return trajectory

    @staticmethod
    def detect_emotional_shift(trajectory: List[HyperWavePacket]) -> str:
        """
        Analyzes the emotional arc (x-axis) of the trajectory.
        Returns a description of the shift (e.g., "Tragedy", "Redemption").
        """
        if not trajectory:
            return "Void"
            
        start_emotion = trajectory[0].orientation.x
        end_emotion = trajectory[-1].orientation.x
        
        # Calculate the average emotion in the middle
        mid_index = len(trajectory) // 2
        mid_emotion = trajectory[mid_index].orientation.x
        
        delta = end_emotion - start_emotion
        
        logger.info(f"   📉 Narrative Analysis: Start={start_emotion:.2f}, Mid={mid_emotion:.2f}, End={end_emotion:.2f}, Delta={delta:.2f}")
        
        if delta > 0.3:
            return "Redemption (Rising Hope)"
        elif delta < -0.3:
            return "Tragedy (Falling into Despair)"
        elif abs(delta) < 0.1 and abs(mid_emotion - start_emotion) > 0.3:
            return "Hero's Journey (Challenge and Return)"
        elif start_emotion > 0.5 and end_emotion > 0.5:
            return "Sustained Joy"
        elif start_emotion < -0.5 and end_emotion < -0.5:
            return "Unending Sorrow"
        else:
            return "Complex Fluctuation"
