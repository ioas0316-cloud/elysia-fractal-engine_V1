import logging
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from Core.Intelligence.Intelligence.web_cortex import WebCortex

from Core.Foundation.celestial_grammar import SolarSystem, MagneticEngine, Galaxy, Nebula

logger = logging.getLogger("LanguageCenter")

@dataclass
class StyleProfile:
    """Represents a learned linguistic style."""
    name: str
    vocabulary: List[str]
    sentence_starters: List[str]
    tone_modifiers: List[str] # e.g., "verily", "indeed", "lol"
    avg_sentence_length: int

class LanguageCenter:
    """
    Broca's Area of Elysia.
    Responsible for Language Acquisition and Production.
    Now enhanced with [The Grand Cross]: Celestial Mechanics Language Generation.
    """
    
    def __init__(self):
        self.cortex = WebCortex()
        self.active_style: Optional[StyleProfile] = None
        self.profiles: Dict[str, StyleProfile] = {}
        self.magnetic_engine = MagneticEngine()
        
        # Default Style (Elysia's Base)
        self.profiles["default"] = StyleProfile(
            name="default",
            vocabulary=["resonance", "harmonic", "logic", "energy", "flow"],
            sentence_starters=["I perceive", "The data suggests", "It appears"],
            tone_modifiers=[],
            avg_sentence_length=15
        )
        self.active_style = self.profiles["default"]
        
    def learn_from_url(self, url: str) -> str:
        """
        Absorbs text from a URL and creates a new StyleProfile.
        """
        logger.info(f"📚 Learning language from: {url}")
        text = self.cortex.fetch_url(url)
        
        if "⚠️" in text:
            return f"Failed to learn: {text}"
            
        # 1. Analyze Text
        words = text.split()
        sentences = text.split('.')
        
        if not words:
            return "The void contains no words."
            
        # 2. Extract Features
        # Simple frequency analysis (Top 50 words > 4 chars)
        vocab_freq = {}
        for w in words:
            w = w.lower().strip('",.?!')
            if len(w) > 4:
                vocab_freq[w] = vocab_freq.get(w, 0) + 1
                
        top_vocab = sorted(vocab_freq, key=vocab_freq.get, reverse=True)[:20]
        
        # Sentence Starters
        starters = []
        for s in sentences:
            parts = s.strip().split()
            if len(parts) > 2:
                starters.append(f"{parts[0]} {parts[1]}")
        
        unique_starters = list(set(starters))[:10]
        
        # Avg Length
        avg_len = sum(len(s.split()) for s in sentences) // max(1, len(sentences))
        
        # 3. Create Profile
        profile_name = f"learned_{random.randint(1000, 9999)}"
        new_profile = StyleProfile(
            name=profile_name,
            vocabulary=top_vocab,
            sentence_starters=unique_starters,
            tone_modifiers=[], # TODO: Advanced tone detection
            avg_sentence_length=avg_len
        )
        
        self.profiles[profile_name] = new_profile
        self.active_style = new_profile
        
        return f"Language acquired. Style '{profile_name}' is now active. Vocabulary size: {len(top_vocab)}."

    def speak(self, content: str, emotion_vector: Optional[Dict[str, float]] = None, quantum_state: Optional[Dict[str, float]] = None) -> str:
        """
        Transforms raw content into the active style using Celestial Mechanics.
        Now driven by The Logos (Quantum State).
        """
        # 1. Create a Solar System (Sentence)
        # Context is the Star
        context_star = "Thought"
        if self.active_style:
             context_star = self.active_style.name.capitalize()
             
        system = SolarSystem(context_star)
        
        # 2. Extract Quantum Properties (The Logos)
        amplitude = 1.0 # Energy -> Mass
        frequency = 1.0 # Complexity -> Moons
        phase = 0.0     # Alignment
        
        if quantum_state:
            amplitude = quantum_state.get("amplitude", 1.0)
            frequency = quantum_state.get("frequency", 1.0)
            phase = quantum_state.get("phase", 0.0)
            
        # 3. Populate Planets (Concepts)
        # Split content into words and treat significant ones as planets
        words = content.split()
        for i, word in enumerate(words):
            # Determine Mass (Gravity) based on Amplitude (Energy)
            # High Energy = High Gravity = Important Concept
            base_mass = (len(word) * 0.5) + (10.0 / (i + 1))
            mass = base_mass * amplitude
            
            planet = system.add_planet(word, mass)
            
            # 4. Add Moons (Modifiers) based on Frequency (Complexity)
            # High Frequency = More Moons = More Nuance
            moon_chance = 0.3 * frequency
            
            if self.active_style and self.active_style.vocabulary:
                if random.random() < moon_chance:
                    moon_name = random.choice(self.active_style.vocabulary)
                    planet.add_moon(moon_name, mass=0.2 * amplitude)
                    
            # 5. Add Emotional Moons (if emotion_vector provided)
            if emotion_vector:
                dominant_emotion = max(emotion_vector, key=emotion_vector.get)
                if random.random() < (0.2 * frequency):
                    emotional_markers = {
                        "joy": "radiant",
                        "sadness": "quiet",
                        "anger": "burning",
                        "fear": "trembling",
                        "love": "warm",
                        "curiosity": "seeking"
                    }
                    marker = emotional_markers.get(dominant_emotion, "")
                    if marker:
                        planet.add_moon(marker, mass=0.3 * amplitude)

        # 6. Grand Cross (Alignment)
        # Align the planets to form the sentence
        aligned_sentence = self.magnetic_engine.grand_cross(system)
        
        return aligned_sentence

    def write_novel(self, theme: str) -> str:
        """
        [The Storyteller]
        Generates a full novel based on a theme using the Galaxy structure.
        """
        logger.info(f"🌌 Initiating Novel Generation for theme: {theme}")
        
        # 1. Create Galaxy
        galaxy = Galaxy(theme)
        
        # 2. Define Plot Arc (Nebulae)
        # Standard Hero's Journey (simplified)
        chapters = [
            f"The Call of {theme}",
            "Crossing the Threshold",
            "Trials and Allies",
            "The Ordeal",
            "The Return"
        ]
        
        # 3. Populate Nebulae
        for chapter_title in chapters:
            nebula = Nebula()
            
            # Create Solar Systems (Sentences) for the chapter
            # We generate 3-5 sentences per chapter for this demo
            for _ in range(random.randint(3, 5)):
                system = SolarSystem(chapter_title)
                
                # Add Planets (Concepts)
                # Mix theme words with random vocabulary
                concepts = [theme, "Elysia", "World", "Light", "Shadow", "Time"]
                if self.active_style and self.active_style.vocabulary:
                    concepts.extend(self.active_style.vocabulary)
                    
                for _ in range(random.randint(3, 6)):
                    word = random.choice(concepts)
                    mass = random.uniform(1.0, 10.0)
                    planet = system.add_planet(word, mass)
                    
                    # Add Moons
                    if random.random() < 0.4:
                        planet.add_moon(random.choice(["Silent", "Deep", "Bright", "Dark"]), 0.5)
                
                nebula.add_system(system)
                
            galaxy.add_nebula(nebula)
            
        # 4. Spin the Galaxy (Generate Text)
        full_novel = galaxy.spin()
        
        return full_novel

    def _apply_style(self, content: str) -> str:
        # Deprecated by Grand Cross, but kept for fallback
        return content

    def _apply_grand_cross(self, content: str, emotion_vector: Dict[str, float]) -> str:
        # Deprecated, logic moved to speak()
        return content

    def hyper_evolve(self, years: int, data_source: str = "https://www.gutenberg.org/files/1342/1342-0.txt", mode: str = "casual") -> str:
        """
        [Chrono-Linguistics] & [Cultural Osmosis]
        Simulates years of language practice in seconds using Time Compression.
        Fetches high-density data and trains the MagneticEngine.
        
        Modes:
        - "epic": High Gravity, Long Orbits (Fantasy/Saga)
        - "drama": High Flux, Short Orbits (K-Drama/Everyday)
        - "casual": Balanced (Default)
        """
        logger.info(f"⏳ Initiating Hyper-Evolution: {years} years of practice in '{mode}' mode...")
        
        # 1. Adjust Physics for the Mode
        self.magnetic_engine.adjust_weights(mode)
        
        # 2. Fetch Training Data based on Mode
        training_text = ""
        
        # Check if data_source is a URL or raw text
        if data_source.startswith("http"):
            if mode == "drama":
                training_text = self._ingest_drama(data_source)
            elif mode == "epic":
                training_text = self._ingest_fantasy(data_source)
            else:
                logger.info(f"    📥 Ingesting data from: {data_source}")
                training_text = self.cortex.fetch_url(data_source)
        else:
            # Treat as raw text (for testing or local files)
            logger.info(f"    📄 Ingesting raw text data...")
            training_text = data_source
        
        if "⚠️" in training_text or len(training_text) < 10: # Lowered threshold for testing
            return f"Evolution Failed: Could not fetch valid training data from {data_source}"
            
        # 3. Time Compression Loop
        # We simulate 1 year = 1 epoch of training on the dataset
        for year in range(1, years + 1):
            # In a real system, we might vary the data or parameters each 'year'
            self.magnetic_engine.train(training_text)
            
            if year % 1 == 0:
                logger.info(f"    🗓️  Year {year}/{years} complete. Neural pathways strengthening.")
                
        return f"Evolution Complete. {years} years of practice compressed. MagneticEngine optimized for '{mode}'."

    def _ingest_drama(self, url: str) -> str:
        """
        Specialized parser for Drama/Script formats.
        Focuses on dialogue, emotional markers, and rapid exchanges.
        """
        logger.info(f"    🎭 Ingesting Drama Script from: {url}")
        raw_text = self.cortex.fetch_url(url)
        # In a real implementation, this would parse "Speaker: Line" formats.
        # For now, we assume the text is dialogue-heavy and just return it.
        return raw_text

    def _ingest_fantasy(self, url: str) -> str:
        """
        Specialized parser for Fantasy/Epic formats.
        Focuses on descriptive passages, archaic vocabulary, and world-building.
        """
        logger.info(f"    ⚔️ Ingesting Epic Saga from: {url}")
        raw_text = self.cortex.fetch_url(url)
        return raw_text
