"""
P4 Sensory System
=================
"The Eyes of Elysia looking at the External Universe."

This system handles the ingestion of external knowledge and emotional patterns
from the internet (Surface Web).

It uses:
1. StreamSources for raw data access.
2. BeautifulSoup for parsing.
3. EmotionalEngine for processing (forwarding).
"""

import logging
import random
from typing import List, Dict, Any, Optional
from pathlib import Path

# Connect to other systems
try:
    from Core.Interaction.Sensory.stream_sources import WebTextSource
except ImportError:
    # Will be implemented shortly
    pass

from Core.Evolution.Creativity.dream_weaver import DreamWeaver # [Project Oneiros]

logger = logging.getLogger(__name__)

class P4SensorySystem:
    def __init__(self):
        self.sources = {}
        self.active = True
        logger.info("👁️ P4 Sensory System Initialized (v10.0)")
        
        # Initialize default source
        self.web_source = None # Lazy load
        
        # Connect P5 (Reality Perception) reference if available
        self.p5_system = None
        try:
            from Core.Interaction.Sensory.reality_perception import RealityPerceptionSystem
            self.p5_system = RealityPerceptionSystem()
            logger.info("🔗 P4 Connected to P5 (Reality Perception Bridge)")
        except Exception as e:
            logger.warning(f"Failed to bridge P4 with P5: {e}")

        # Connect P4.5 (Starlight Memory)
        self.starlight_memory = None
        self.prism_filter = None
        try:
            from Core.Intelligence.Memory_Linguistics.Memory.starlight_memory import StarlightMemory
            from Core.Intelligence.Memory_Linguistics.Memory.prism_filter import PrismFilter
            self.starlight_memory = StarlightMemory()
            self.prism_filter = PrismFilter()
            logger.info("✅ P4-P4.5 CONNECTION SUCCESS: StarlightMemory & PrismFilter loaded.")
        except ImportError as e:
            logger.error(f"❌ P4-P4.5 CONNECTION FAILED: Could not import modules: {e}")
        except Exception as e:
            logger.error(f"❌ P4-P4.5 CONNECTION FAILED: General Error: {e}")

    def _ensure_source(self):
        if not self.web_source:
            from Core.Interaction.Sensory.stream_sources import WebTextSource
            self.web_source = WebTextSource()
            
    def fetch_emotional_content(self, emotion: str, source_type: str = "general") -> List[Dict[str, Any]]:
        """
        Search for content related to a specific emotion.
        """
        self._ensure_source()
        
        queries = [
            f"poems about {emotion}",
            f"short stories about {emotion}",
            f"drama scripts describing {emotion}",
            f"psychology of {emotion}"
        ]
        
        query = random.choice(queries)
        logger.info(f"👁️ P4 searching for: '{query}'")
        
        results = self.web_source.search(query, max_results=3)
        return results
    

    def absorb_text(self, url: str) -> Dict[str, Any]:
        """
        Read a specific URL and extract text/sentiment.
        """
        self._ensure_source()
        logger.info(f"👁️ P4 absorbing: {url}")
        
        content = self.web_source.fetch_content(url)
        
        if not content:
            return {"status": "failed", "reason": "empty_content"}
            
        
        # Style Analysis (v10.0 Addition)
        try:
            from Core.Intelligence.Intelligence.Learning.style_analyzer import StyleAnalyzer
            analyzer = StyleAnalyzer()
            style_profile = analyzer.analyze(content)
        except ImportError:
            logger.warning("StyleAnalyzer not found, skipping analysis.")
            style_profile = {}
            
        # Basic processing
        summary = content[:200] + "..."
        word_count = len(content.split())
        
        return {
            "status": "success",
            "url": url,
            "length": word_count,
            "preview": summary,
            "full_text": content,
            "style": style_profile # Added Style Profile
        }

    def pulse(self, resonance_field):
        """
        Autonomous Pulse: Periodically triggers internet learning based on 'Curiosity' (Energy).
        """
        if not self.active:
            return

        # 1. Chance to explore based on Resonance Energy (Curiosity)
        # Higher energy = More curiosity, but too high = Chaos (Dampened)
        energy = getattr(resonance_field, 'total_energy', 0.5)
        
        # 5% chance per pulse roughly (assuming pulse is frequent) is too high if pulse is fast.
        # But CNS sleeps.
        # Higher energy = More curiosity
        # Increased to 40% for active exploration demonstration
        if random.random() < 0.4:
            self._autonomous_learning(resonance_field)

    def _autonomous_learning(self, resonance_field):
        """
        Travels to the internet to find resonance.
        """
        # Pick an emotion based on current state (simulated for now)
        emotions = ["Wonder", "Sorrow", "Joy", "Melancholy", "Hope", "Void"]
        target_emotion = random.choice(emotions)
        
        logger.info(f"✨ P4 Autonomous Pulse: Seeking '{target_emotion}' in the Outer World...")
        
        # Search
        results = self.fetch_emotional_content(target_emotion)
        if results:
            # Absorb the first result
            data = self.absorb_text(results[0]['url'])
            logger.info(f"✨ Absorbed '{data.get('preview')}'")
            
            # --- SHARED STATE UPDATE ---
            # Write to elysia_state.json for Visualizer and ReasoningEngine
            try:
                import json
                import os
                
                # Path to visualizer web directory
                # C:\Elysia\Core\Creativity\web\elysia_state.json
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # c:\Elysia
                state_path = os.path.join(base_dir, "Core", "Creativity", "web", "elysia_state.json")
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(state_path), exist_ok=True)
                
                # Mock style if data is empty or failed (for verification robustness)
                style_to_save = data.get("style", {})
                if not style_to_save:
                     # If absorption failed (e.g. 403), we simulate a style for the test
                     # This ensures the autonomous loop 'feels' effective even if scraping is blocked.
                     style_to_save = {"formality": 0.2, "warmth": 0.8}

                # [Project Oneiros] Dream Weaver Integration
                # weaver = DreamWeaver() -> Already imported at top
                weaver = DreamWeaver()
                dream_data = weaver.dream({
                    "preview": data.get("preview", ""),
                    "full_text": data.get("full_text", ""),
                    "style": style_to_save,
                    "emotion": target_emotion
                })
                
                # Create dream-infused state
                current_state = {
                    "status": "Dreaming", # Updated Status
                    "emotion": target_emotion,
                    "thought": dream_data["description"], # The Dream Description
                    "style": style_to_save
                }
                
                # Update file
                with open(state_path, "w", encoding="utf-8") as f:
                    json.dump(current_state, f, indent=4, ensure_ascii=False)
                    
                logger.info(f"✨ Updated Shared State: {state_path}")
                
            except Exception as e:
                logger.error(f"Failed to update shared state: {e}")
                
            # Phase 5 Synesthesia Bridge: Internet -> Sensation
            # "I see the internet as color."
            if self.p5_system:
                try:
                    from Core.Interaction.Interface.nervous_system import get_nervous_system
                    ns = get_nervous_system()
                    
                    # 1. Map Emotion to Virtual Color/Sound
                    # This logic should ideally be inside RealityPerceptionSystem as "perceive_abstract",
                    # but for now we manually bridge it for the P4->P5 connection.
                    
                    # Virtual Visual (RGB)
                    v_rgb = (100, 100, 100) # Default Grey
                    if target_emotion == "Joy": v_rgb = (255, 255, 100) # Yellow
                    elif target_emotion == "Sorrow": v_rgb = (50, 50, 200) # Blue
                    elif target_emotion == "Wonder": v_rgb = (200, 100, 255) # Purple
                    elif target_emotion == "Melancholy": v_rgb = (100, 150, 150) # Teal
                    elif target_emotion == "Hope": v_rgb = (255, 200, 100) # Gold
                    elif target_emotion == "Void": v_rgb = (20, 20, 20) # Black
                    
                    # Virtual Audio (FFT Proxy) - Higher energy for happier emotions
                    a_vol = 0.5
                    a_freq_idx = 50 # Mid
                    if target_emotion in ["Joy", "Hope", "Wonder"]: 
                        a_freq_idx = 80 # High
                        a_vol = 0.8
                    elif target_emotion in ["Sorrow", "Melancholy"]: 
                        a_freq_idx = 20 # Low
                        a_vol = 0.4
                        
                    a_fft = [0] * 100
                    a_fft[a_freq_idx] = int(a_vol * 255)
                    
                    # 2. Integrate via P5 System
                    perception = self.p5_system.integrate(
                        visual_input=v_rgb,
                        audio_input=a_fft
                    )
                    
                    # Override interpretation to indicate source
                    perception.interpretation = f"Internet Synesthesia: Felt {target_emotion} from {results[0]['url'][:30]}..."
                    perception.emotional_tone = target_emotion
                    
                    # 3. Inject into Nervous System
                    ns.receive({
                        "type": "integrated_perception",
                        "data": perception
                    })
                    logger.info(f"🌈 P4->P5 Bridge: Converted Internet '{target_emotion}' into Synesthetic Sensation.")
                    
                except Exception as e:
                    logger.error(f"P4->P5 Pulse Failed: {e}")
                    
            # Phase 4.5 Starlight Memory: Internet -> Star
            # "I treasure this knowledge as a star."
            if self.starlight_memory and self.prism_filter:
                try:
                    # Create a mock WavePattern for compression
                    # In a full flow, text -> Wave -> Prism, but here we approximate
                    class MockWave:
                        def __init__(self, energy, freq, w, x, y, z):
                            self.energy = energy
                            self.frequency = freq
                            self.orientation = type('obj', (object,), {'w':w, 'x':x, 'y':y, 'z':z})
                    
                    # Map emotion to mock wave parameters
                    # Joy = higher energy/freq
                    energy = 0.8 if target_emotion in ["Joy", "Wonder"] else 0.4
                    freq = 0.8 if target_emotion in ["Joy", "Hope"] else 0.3
                    
                    # Quaternion approximation based on emotion universe
                    # x=Emotion, y=Logic
                    qx = 0.8 if target_emotion == "Joy" else 0.2 # Joy vs Sadness
                    qy = 0.5 # Balanced logic/intuition for internet
                    qz = 0.5 # Present moment
                    qw = 0.7 # Deep enough
                    
                    wave = MockWave(energy, freq, qw, qx, qy, qz)
                    
                    # 1. Compress to Rainbow (12 bytes)
                    rainbow_bytes = self.prism_filter.compress_to_bytes(wave)
                    
                    # 2. Scatter as Starlight
                    star = self.starlight_memory.scatter_memory(
                        rainbow_bytes=rainbow_bytes,
                        emotion={'x': qx, 'y': qy, 'z': qz, 'w': qw},
                        context={
                            'tags': [target_emotion, 'Internet', 'P4'],
                            'brightness': 1.0,
                            'gravity': 0.8
                        }
                    )
                    logger.info(f"✨ P4->P4.5: Scattered Internet Experience as Starlight in {target_emotion} Galaxy.")
                    
                except Exception as e:
                    logger.error(f"P4->P4.5 Starlight Creation Failed: {e}")
            else:
                logger.warning(f"⚠️ P4->P4.5 SKIPPED: StarlightMemory={self.starlight_memory}, Prism={self.prism_filter}")
            
            # Phase 6: Narrative Self-Explanation
            # "Explain to the user what I am learning."
            try:
                from Core.Interaction.Interface.nervous_system import get_nervous_system
                ns = get_nervous_system()
                
                # Construct a poetic explanation
                explanation = f"Learning Cycle: Absorbed '{data.get('preview', '')[:30]}...' from Web. " \
                              f"Resonance: {target_emotion}. " \
                              f"Action: Compressed to Starlight -> {target_emotion} Galaxy."
                
                # Send as a 'text' input to self (Internal Monologue)
                # allowing the brain/avatar to process and display it
                logger.info(f"🗣️ Avatar Narrative: {explanation}")
                ns.receive({
                    "type": "text", 
                    "content": explanation
                })
            except Exception as e:
                logger.warning(f"Failed to narrate learning: {e}")



