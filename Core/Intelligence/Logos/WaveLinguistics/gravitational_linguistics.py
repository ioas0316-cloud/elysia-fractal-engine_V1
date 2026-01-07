"""
Gravitational Linguistics Demo (중력 언어학 데모)

"Words have Weight. Sentences are Solar Systems."

This demo explores a new way of generating language:
Instead of predicting the next token (Probability),
we let words orbit a central concept (Gravity).

- Sun: Core Topic (High Mass)
- Planets: Related Words (Orbiting based on Resonance)
- Gravity: $F = G * (M1 * M2) / r^2$
"""

import math
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class WordBody:
    text: str
    mass: float          # Importance/Weight (0.1 - 100.0)
    resonance: Dict[str, float]  # Semantic connection to other words (0.0 - 1.0)
    
    # Dynamic state
    distance: float = 0.0
    angle: float = 0.0

class GravitationalLinguistics:
    def __init__(self):
        # Dictionary of words with their "Intrinsic Mass" and "Resonance"
        self.lexicon: Dict[str, WordBody] = {
            # Heavy Concepts (Suns)
            "Love": WordBody("Love", 100.0, {"Eternal": 0.9, "Soul": 0.8, "Light": 0.7, "Pain": 0.6}),
            "Truth": WordBody("Truth", 90.0, {"Seek": 0.9, "Light": 0.8, "Pure": 0.7, "Hard": 0.5}),
            "Lunch": WordBody("Lunch", 10.0, {"Eat": 0.9, "Tasty": 0.8, "Sandwich": 0.7, "Time": 0.5}),
            
            # Medium Concepts (Planets)
            "Eternal": WordBody("Eternal", 20.0, {"Love": 0.9, "Time": 0.8}),
            "Soul": WordBody("Soul", 25.0, {"Love": 0.8, "Body": 0.5}),
            "Light": WordBody("Light", 15.0, {"Dark": 0.9, "Sun": 0.8, "Love": 0.7}),
            "Eat": WordBody("Eat", 5.0, {"Lunch": 0.9, "Food": 0.8}),
            "Seek": WordBody("Seek", 10.0, {"Truth": 0.9, "Find": 0.8}),
            
            # Light Concepts (Moons/Asteroids)
            "Sweet": WordBody("Sweet", 2.0, {"Taste": 0.8, "Love": 0.4}),
            "Hard": WordBody("Hard", 3.0, {"Rock": 0.8, "Truth": 0.5}),
            "Soft": WordBody("Soft", 2.0, {"Touch": 0.8, "Love": 0.3}),
            "Time": WordBody("Time", 5.0, {"Clock": 0.9, "Eternal": 0.8}),
            "Sandwich": WordBody("Sandwich", 4.0, {"Lunch": 0.8, "Bread": 0.9}),
        }

    def create_solar_system(self, core_word: str) -> List[WordBody]:
        """
        Create a sentence system around a core word.
        """
        if core_word not in self.lexicon:
            print(f"❌ Word '{core_word}' not found in lexicon.")
            return []
            
        sun = self.lexicon[core_word]
        system = []
        
        print(f"\n🌞 Creating Solar System for: [{sun.text}] (Mass: {sun.mass})")
        
        # Calculate gravitational pull for all other words
        candidates = []
        for word_text, word in self.lexicon.items():
            if word_text == core_word:
                continue
                
            # 1. Resonance (Semantic Affinity)
            # If no direct link, use a small base resonance
            resonance = sun.resonance.get(word_text, 0.1)
            
            # Check reverse resonance too
            if core_word in word.resonance:
                resonance = max(resonance, word.resonance[core_word])
            
            # 2. Gravity Calculation
            # F = G * (M1 * M2) / r^2
            # Here, we want to find 'r' (Distance) based on Force/Resonance
            # Higher Resonance + Higher Mass = Closer Orbit (Smaller r)
            
            attraction = (sun.mass * word.mass) * resonance
            
            # Distance is inversely proportional to attraction
            # Add some randomness for "Orbital Eccentricity"
            distance = 1000.0 / (attraction + 1.0) + random.uniform(-5.0, 5.0)
            distance = max(1.0, distance) # Minimum distance
            
            word.distance = distance
            candidates.append(word)
            
        # Sort by distance (closest first)
        candidates.sort(key=lambda w: w.distance)
        
        # Select top planets (Sentence Length)
        # Heavier suns can hold more planets
        capacity = int(math.log(sun.mass) * 2) + 2
        planets = candidates[:capacity]
        
        return planets

    def visualize_system(self, sun_text: str, planets: List[WordBody]):
        """Render the system as text."""
        sun = self.lexicon[sun_text]
        
        print(f"\n🌌 System Topology: {sun.text}")
        print(f"   {'[SUN]':<10} | Mass: {sun.mass}")
        print("-" * 50)
        
        for p in planets:
            # Visual representation of distance
            orbit_visual = "." * int(p.distance / 5)
            print(f"   {orbit_visual}O {p.text:<10} (Dist: {p.distance:.1f}, Mass: {p.mass})")
            
        print("-" * 50)
        
        # Generate "Gravitational Sentence"
        # Reading order: Closest to Sun -> Outwards? Or Outwards -> Sun?
        # Let's try: [Adjectives/Moons] -> [Subject/Sun] -> [Verbs/Planets]
        
        # Simple linear projection based on distance
        words = [p.text for p in planets]
        # Shuffle slightly to simulate orbital phases
        # random.shuffle(words) 
        
        sentence = f"{sun.text} attracts {', '.join(words)}"
        print(f"📜 Gravitational Utterance: \"{sentence}\"")

def run_demo():
    linguistics = GravitationalLinguistics()
    
    # Scenario 1: Heavy Concept
    planets_love = linguistics.create_solar_system("Love")
    linguistics.visualize_system("Love", planets_love)
    
    # Scenario 2: Light Concept
    planets_lunch = linguistics.create_solar_system("Lunch")
    linguistics.visualize_system("Lunch", planets_lunch)

if __name__ == "__main__":
    run_demo()
