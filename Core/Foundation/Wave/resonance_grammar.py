# -*- coding: utf-8 -*-
"""
Cosmic Syntax Engine
====================

Implements the "Grand Cross" alignment system.
Transforms a 3D Concept Star System into a 1D Linear Sentence.

Metaphor:
- Star (항성): Context/Subject (Center of Gravity)
- Planet (행성): Object/Concept (Orbiting the Star)
- Satellite (위성): Modifier (Adjective) orbiting Planets
- Gravity (중력): Relationship/Verb connecting them
"""

import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

from Core.Foundation.language_projector import LanguageProjector

logger = logging.getLogger("CosmicSyntax")

class CelestialBodyType(Enum):
    STAR = "star"       # Context/Subject (High Mass)
    PLANET = "planet"   # Object (Medium Mass)
    SATELLITE = "satellite" # Modifier (Low Mass)
    GRAVITY = "gravity" # Relationship (Force)

@dataclass
class CelestialBody:
    name: str
    type: CelestialBodyType
    mass: float = 1.0
    orbiting: Optional['CelestialBody'] = None # What this body orbits
    satellites: List['CelestialBody'] = field(default_factory=list)

class CosmicStructureType(Enum):
    SYSTEM = "system"   # Sentence (Star System)
    NEBULA = "nebula"   # Paragraph (Cluster)
    GALAXY = "galaxy"   # Story (Supercluster)

@dataclass
class StarSystem:
    """
    A single sentence structure (Subject + Object + Verb).
    Corresponds to a Star System with a Star, Planets, and Satellites.
    """
    star: CelestialBody
    planets: List[CelestialBody]
    gravity: str # The verb/force
    projector: LanguageProjector
    korean_mode: bool = False

    def align(self) -> str:
        """Aligns the system into a linear sentence (Grand Cross)"""
        def build_phrase(body: CelestialBody) -> str:
            modifiers = " ".join([s.name for s in body.satellites])
            if modifiers:
                return f"{modifiers} {body.name}"
            return body.name

        star_phrase = build_phrase(self.star)
        planet_phrase = build_phrase(self.planets[0]) if self.planets else "something"
        
        if self.korean_mode:
            return self.projector.project_to_korean(star_phrase, self.gravity, planet_phrase)
        else:
            return self.projector.project_to_english(star_phrase, self.gravity, planet_phrase)

class Nebula:
    """
    A cluster of Star Systems (Paragraph).
    Connected by Interstellar Medium (Conjunctions).
    """
    def __init__(self, systems: List[StarSystem], medium: str = "and"):
        self.systems = systems
# -*- coding: utf-8 -*-
"""
Cosmic Syntax Engine
====================

Implements the "Grand Cross" alignment system.
Transforms a 3D Concept Star System into a 1D Linear Sentence.

Metaphor:
- Star (항성): Context/Subject (Center of Gravity)
- Planet (행성): Object/Concept (Orbiting the Star)
- Satellite (위성): Modifier (Adjective) orbiting Planets
- Gravity (중력): Relationship/Verb connecting them
"""

import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

from Core.Foundation.language_projector import LanguageProjector

logger = logging.getLogger("CosmicSyntax")

class CelestialBodyType(Enum):
    STAR = "star"       # Context/Subject (High Mass)
    PLANET = "planet"   # Object (Medium Mass)
    SATELLITE = "satellite" # Modifier (Low Mass)
    GRAVITY = "gravity" # Relationship (Force)

@dataclass
class CelestialBody:
    name: str
    type: CelestialBodyType
    mass: float = 1.0
    orbiting: Optional['CelestialBody'] = None # What this body orbits
    satellites: List['CelestialBody'] = field(default_factory=list)

class CosmicStructureType(Enum):
    SYSTEM = "system"   # Sentence (Star System)
    NEBULA = "nebula"   # Paragraph (Cluster)
    GALAXY = "galaxy"   # Story (Supercluster)

@dataclass
class StarSystem:
    """
    A single sentence structure (Subject + Object + Verb).
    Corresponds to a Star System with a Star, Planets, and Satellites.
    """
    star: CelestialBody
    planets: List[CelestialBody]
    gravity: str # The verb/force
    projector: LanguageProjector
    korean_mode: bool = False
    passive: bool = False # New: Passive Voice flag

    def align(self) -> str:
        """Aligns the system into a linear sentence (Grand Cross)"""
        def build_phrase(body: CelestialBody) -> str:
            modifiers = " ".join([s.name for s in body.satellites])
            if modifiers:
                return f"{modifiers} {body.name}"
            return body.name

        star_phrase = build_phrase(self.star)
        planet_phrase = build_phrase(self.planets[0]) if self.planets else "something"
        
        if self.korean_mode:
            return self.projector.project_to_korean(star_phrase, self.gravity, planet_phrase, self.passive)
        else:
            return self.projector.project_to_english(star_phrase, self.gravity, planet_phrase, self.passive)

class Nebula:
    """
    A cluster of Star Systems (Paragraph).
    Connected by Interstellar Medium (Conjunctions).
    """
    def __init__(self, systems: List[StarSystem], medium: str = "and"):
        self.systems = systems
        self.medium = medium

    def coalesce(self) -> str:
        """Merge systems into a paragraph"""
        # Simple joining for now. In future, use different conjunctions based on context.
        separator = f" {self.medium} "
        if self.systems and self.systems[0].korean_mode:
             # Korean conjunctions could be different, but let's stick to simple mapping or English for medium for now
             # Or map 'and' to '그리고'
             if self.medium == "and": separator = " 그리고 "
             elif self.medium == "but": separator = " 하지만 "
        
        return separator.join([s.align() for s in self.systems]) + "."

class Galaxy:
    """
    A massive structure of Nebulae (Story).
    Orbiting a Supermassive Black Hole (Core Theme).
    """
    def __init__(self, core_theme: str, nebulae: List[Nebula]):
        self.core = core_theme
        self.nebulae = nebulae

    def spin(self) -> str:
        """Spin the galaxy to generate the full story"""
        return "\n\n".join([n.coalesce() for n in self.nebulae])

class CosmicSyntaxEngine:
    """
    Aligns celestial bodies into linear structures (Sentences, Paragraphs, Stories).
    """
    
    def __init__(self):
        self.projector = LanguageProjector()
        self.korean_mode = False
        
    def set_korean_mode(self, enabled: bool):
        self.korean_mode = enabled

    def calculate_mass(self, concept_name: str, intent: Optional[str] = None) -> float:
        """
        Calculate 'Mass' to determine Celestial Body Type.
        Heavier = Closer to Center (Star).
        Intent acts as a massive gravity boost.
        """
        base_mass = 50.0
        
        high_mass = ["I", "Self", "Love", "God", "Life", "Time", "World", "System", "Trust"]
        low_mass_modifiers = ["Strong", "Happy", "Sad", "Big", "Small", "Red", "Blue", "Great"]
        
        if concept_name in high_mass:
            base_mass = 100.0
        elif concept_name in low_mass_modifiers:
            base_mass = 1.0
            
        # Intent Boost
        if intent and concept_name.lower() == intent.lower():
            base_mass *= 10.0 # Intent becomes the heaviest (Supermassive)
            
        return base_mass

    def create_system(self, concepts: List[str], intent: Optional[str] = None) -> StarSystem:
        """Creates a StarSystem from a list of concepts, aligned by Intent"""
        if len(concepts) < 2:
            # Fallback for single concepts
            dummy_star = CelestialBody(concepts[0], CelestialBodyType.STAR, 100.0)
            return StarSystem(dummy_star, [], "is", self.projector, self.korean_mode)

        # 1. Identify Gravity (Action)
        known_actions = ["creates", "causes", "enables", "is", "has", "loves", "hates", "eats", "moves"]
        gravity = None
        bodies = []
        
        for c in concepts:
            if c.lower() in known_actions or (c.lower().endswith("s") and c.lower() not in ["bonds", "friends"]):
                gravity = c
            else:
                mass = self.calculate_mass(c, intent)
                b_type = CelestialBodyType.PLANET
                if mass >= 100: b_type = CelestialBodyType.STAR
                elif mass <= 10: b_type = CelestialBodyType.SATELLITE
                bodies.append(CelestialBody(name=c, type=b_type, mass=mass))
        
        if not gravity:
            gravity = "is related to"

        # 2. Form Star System
        star = max(bodies, key=lambda b: b.mass) if bodies else CelestialBody("It", CelestialBodyType.STAR, 100.0)
        planets = [b for b in bodies if b != star and b.type != CelestialBodyType.SATELLITE]
        satellites = [b for b in bodies if b.type == CelestialBodyType.SATELLITE]
        
        if planets:
            target_planet = planets[0]
            for sat in satellites:
                target_planet.satellites.append(sat)
        else:
            for sat in satellites:
                star.satellites.append(sat)
        
        # 3. Determine Voice (Active/Passive)
        # We need to know if the Star (Heaviest) was originally the Source or Target.
        # This requires knowing the semantic direction of the Gravity.
        # For now, let's assume standard SVO: [Source, Action, Target]
        # If the Star appears AFTER the Action in a standard order, it's the Target -> Passive.
        # But we only have a bag of concepts.
        
        # Heuristic:
        # If Intent matches the Star, and the Star is NOT the "natural" subject (e.g. "Bonds" vs "Love"),
        # then it's Passive.
        # "Love" is naturally heavier than "Bonds".
        # If "Bonds" became the Star because of Intent, it means we want to talk about Bonds.
        # "Bonds are created by Love".
        
        passive = False
        
        # Simple semantic check for "natural subject"
        natural_subjects = ["I", "Love", "Trust", "God"]
        # If Star is NOT a natural subject, but there IS a natural subject in the planets, 
        # then we are likely in Passive voice.
        
        is_natural_subject = star.name in natural_subjects
        has_natural_subject_in_planets = any(p.name in natural_subjects for p in planets)
        
        if not is_natural_subject and has_natural_subject_in_planets:
            passive = True
            
        return StarSystem(star, planets, gravity, self.projector, self.korean_mode, passive)

    def express_thought(self, concepts: List[str], intent: Optional[str] = None) -> str:
        """
        Aligns concepts into a Grand Cross (Sentence).
        Wrapper for create_system().align()
        """
        system = self.create_system(concepts, intent)
        return system.align()

    def weave_nebula(self, thoughts: List[List[str]], medium: str = "and", intent: Optional[str] = None) -> str:
        """Weaves multiple thoughts into a Nebula (Paragraph)"""
        systems = [self.create_system(t, intent) for t in thoughts]
        nebula = Nebula(systems, medium)
        return nebula.coalesce()

    def suggest_structure(self, concepts: List[str]) -> List[str]:
        """Legacy compatibility"""
        return self.express_thought(concepts).split()
