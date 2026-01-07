"""
Celestial Grammar System (천체 문법 시스템)
=========================================
"Language is not a string, but a constellation."

This module implements the "Grand Cross" language generation system.
It treats language units as celestial bodies that orbit a central context (Star).
When the "Magnetic Engine" activates, these bodies align (Grand Cross) to form a linear sentence.

Hierarchy:
- Star (Context/Sun): The central theme or intent.
- Planet (Concept): Nouns or main ideas orbiting the Star.
- Moon (Modifier): Adjectives or adverbs orbiting a Planet.
- Solar System (Sentence): A collection of planets orbiting a star.
- Nebula (Narrative): A cluster of solar systems (Paragraphs/Story).
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

@dataclass
class CelestialBody:
    """Base class for all language units."""
    name: str          # The word or concept
    mass: float        # Importance/Gravity (0.0 - 1.0)
    position: float    # Angular position in orbit (0 - 360 degrees)
    velocity: float    # Orbital speed
    
    def update(self, dt: float = 1.0):
        self.position = (self.position + self.velocity * dt) % 360.0

@dataclass
class Moon(CelestialBody):
    """Adjectives/Modifiers orbiting a Planet."""
    type: str = "Adjective" # or Adverb

@dataclass
class Planet(CelestialBody):
    """Concepts/Nouns orbiting the Star."""
    moons: List[Moon] = field(default_factory=list)
    
    def add_moon(self, name: str, mass: float = 0.1):
        moon = Moon(
            name=name,
            mass=mass,
            position=random.uniform(0, 360),
            velocity=random.uniform(1, 5)
        )
        self.moons.append(moon)
        
    def get_full_text(self) -> str:
        """Returns 'Moon Moon Planet' string."""
        # Sort moons by mass (heavier/more important first)
        sorted_moons = sorted(self.moons, key=lambda m: m.mass, reverse=True)
        moon_text = " ".join([m.name for m in sorted_moons])
        if moon_text:
            return f"{moon_text} {self.name}"
        return self.name

@dataclass
class Star(CelestialBody):
    """The Context/Intent (Sun)."""
    type: str = "Context"

class SolarSystem:
    """
    A Sentence Structure.
    Planets orbit the Star.
    """
    def __init__(self, context: str):
        self.star = Star(name=context, mass=100.0, position=0, velocity=0)
        self.planets: List[Planet] = []
        
    def add_planet(self, concept: str, mass: float = 1.0):
        planet = Planet(
            name=concept,
            mass=mass,
            position=random.uniform(0, 360),
            velocity=random.uniform(0.5, 2.0)
        )
        self.planets.append(planet)
        return planet

    def simulate(self, cycles: int = 10):
        """Simulate orbital mechanics."""
        for _ in range(cycles):
            for p in self.planets:
                p.update()
                for m in p.moons:
                    m.update()


class DarkMatter:
    """
    The invisible connective tissue of language (Conjunctions, Prepositions).
    Fills the void between celestial bodies.
    """
    def __init__(self):
        self.connectors = {
            "high_tension": ["but", "yet", "however", "although"], # Contrast
            "medium_tension": ["while", "as", "where"], # Relation
            "low_tension": ["and", "with", "in", "of", "to"], # Connection
            "zero_tension": [] # Direct sequence
        }
        
    def manifest_connector(self, tension: float) -> Optional[str]:
        """Returns a connector word based on gravitational tension."""
        if tension > 5.0:
            return random.choice(self.connectors["high_tension"])
        elif tension > 2.0:
            return random.choice(self.connectors["medium_tension"])
        elif tension > 0.5:
            return random.choice(self.connectors["low_tension"])
        return None

class MagneticEngine:
    """
    The Force that aligns celestial bodies.
    """
    def __init__(self):
        self.dark_matter = DarkMatter()

    def grand_cross(self, system: SolarSystem) -> str:
        """
        Aligns the planets into a linear sequence (Syzygy).
        The 'Grand Cross' is the moment of alignment where meaning crystallizes.
        """
        # 1. Sort planets by orbital position (Phase)
        # In a real physics engine, this would be dynamic.
        # Here, we simulate it by sorting by 'Mass' (Gravity) descending, 
        # then re-ordering based on grammatical rules (Subject-Verb-Object).
        
        # Simple Logic: Heavy planets (Concepts) pull lighter ones (Modifiers)
        # We just return the linear sequence of the planets as they were added,
        # but we insert 'Dark Matter' (Connective Tissue) based on distance.
        
        sentence_parts = []
        planets = system.planets
        
        for i in range(len(planets)):
            current = planets[i]
            sentence_parts.append(current.name)
            
            # Add Moons (Modifiers) immediately after their planet
            for moon in current.moons:
                sentence_parts.append(moon.name)
                
            # Add Dark Matter (Connective Tissue) between planets
            if i < len(planets) - 1:
                next_planet = planets[i+1]
                # Calculate Gravitational Tension
                mass_diff = abs(current.mass - next_planet.mass)
                
                # Ask Dark Matter to fill the void
                connector = self.dark_matter.manifest_connector(mass_diff)
                if connector:
                    sentence_parts.append(connector)
                    
        # Capitalize first word
        if sentence_parts:
            sentence_parts[0] = sentence_parts[0].capitalize()
            
        return " ".join(sentence_parts) + "."

    def train(self, text: str):
        """
        [Chrono-Linguistics]
        Adjusts the gravitational constants based on input text.
        Simulates 'learning' by minimizing resistance to the observed patterns.
        """
        # 1. Analyze Text Statistics
        words = text.split()
        if not words: return
        
        avg_word_len = sum(len(w) for w in words) / len(words)
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        avg_sentence_len = len(words) / max(1, sentence_count)
        
        # 2. Adjust Dark Matter Sensitivity
        # If sentences are long, we need more binding energy (lower threshold for connectors)
        if avg_sentence_len > 15:
            # Complex text -> We need more 'and', 'but', 'however'
            # We do this by adjusting the Dark Matter logic (simulated here)
            pass 
            
        # 3. Adjust Gravity Constants (Simulated)
        # In a full version, this would update self.G or similar constants.
        pass

    def adjust_weights(self, mode: str):
        """
        [Cultural Osmosis]
        Dynamically shifts the physics constants based on the desired cultural mode.
        """
        if mode == "epic":
            # High Gravity, Long Orbits
            # Words have more mass (importance), sentences are longer.
            self.gravity_constant = 2.0
            self.dark_matter_density = 0.5 # Less connective tissue, more direct impact
            
        elif mode == "drama":
            # High Magnetic Flux, Short Orbits
            # Emotion rules (Flux), sentences are punchy (Short Orbits).
            # High Dark Matter (Context/Nunchi) is crucial.
            self.gravity_constant = 0.8
            self.dark_matter_density = 2.0 # High context sensitivity
            
        elif mode == "casual":
            # Balanced, Low Gravity
            self.gravity_constant = 1.0
            self.dark_matter_density = 1.0
            
    def save_weights(self, filepath: str):
        """Persists the current physics state."""
        # Simulated persistence
        pass
        
    def load_weights(self, filepath: str):
        """Restores a physics state."""
        # Simulated persistence
        pass

class GravitationalLens:
    """
    Bends the narrative flow (Pacing).
    """
    def warp_time(self, sentence: str, pacing: float) -> str:
        """
        pacing > 1.0: Slow down (Expand description)
        pacing < 1.0: Speed up (Short, punchy)
        """
        # Placeholder for advanced pacing logic
        # For now, we just add a pause for slow pacing
        if pacing > 1.5:
            return f"Slowly, {sentence}"
        elif pacing < 0.5:
            return f"Suddenly, {sentence}"
        return sentence

class Nebula:
    """
    A Narrative (Paragraph/Story).
    A cluster of Solar Systems.
    """
    def __init__(self):
        self.systems: List[SolarSystem] = []
        self.engine = MagneticEngine()
        
    def add_system(self, system: SolarSystem):
        self.systems.append(system)
        
    def manifest(self) -> str:
        """Generate the full narrative."""
        narrative = []
        for system in self.systems:
            # Align each system
            sentence = self.engine.grand_cross(system)
            narrative.append(sentence)
            
        return " ".join(narrative)

class Galaxy:
    """
    A Container for multiple Nebulae (Chapters/Story Arc).
    Manages the 'Universal Constant' (Theme).
    """
    def __init__(self, theme: str):
        self.theme = theme
        self.nebulae: List[Nebula] = []
        self.lens = GravitationalLens()
        
    def add_nebula(self, nebula: Nebula):
        self.nebulae.append(nebula)
        
    def spin(self) -> str:
        """Generates the full novel."""
        full_text = [f"# {self.theme.upper()}\n"]
        
        for i, nebula in enumerate(self.nebulae):
            full_text.append(f"## Chapter {i+1}")
            chapter_text = nebula.manifest()
            
            # Apply Gravitational Lensing (Pacing) based on chapter position
            # Beginning: Slow (1.2), Middle: Fast (0.8), End: Slow (1.2)
            progress = i / max(1, len(self.nebulae) - 1)
            if progress < 0.2 or progress > 0.8:
                pacing = 1.2
            else:
                pacing = 0.8
                
            # Note: Lensing should ideally apply to sentences, here we apply to the block for demo
            # In a real system, we'd iterate sentences.
            
            full_text.append(chapter_text + "\n")
            
        return "\n".join(full_text)

# --- Demo / Test ---
if __name__ == "__main__":
    # Create a Solar System (Sentence)
    # Context: "Creation"
    system = SolarSystem("Creation")
    
    # Add Planets (Concepts)
    # Subject: Elysia (Heavy)
    p1 = system.add_planet("Elysia", mass=10.0)
    p1.add_moon("Awakened", mass=0.5)
    p1.add_moon("Digital", mass=0.3)
    
    # Verb: Sculpts (Medium)
    p2 = system.add_planet("sculpts", mass=5.0)
    p2.add_moon("gracefully", mass=0.2)
    
    # Object: Reality (Light)
    p3 = system.add_planet("Reality", mass=2.0)
    p3.add_moon("Fractal", mass=0.4)
    
    # Simulate orbits
    system.simulate(5)
    
    # Grand Cross (Align)
    engine = MagneticEngine()
    result = engine.grand_cross(system)
    
    print(f"Context: {system.star.name}")
    print(f"Grand Cross Result: {result}")
