"""
LiteraryCortex (The Hyper-Storyteller)
======================================
"Stories are the resonance of the Void observing itself."

This module is responsible for narrative generation using the HYPER-QUBIT paradigm.
It no longer picks "random templates" but grows stories from a "Seed Resonance".
"""

import random
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

# Core Systems
from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.nervous_system import get_nervous_system
from Core.Foundation.Wave.infinite_hyperquaternion import InfiniteHyperQubit, create_infinite_qubit
from Core.Intelligence.Intelligence.logos_engine import LogosEngine

logger = logging.getLogger("LiteraryCortex")

@dataclass
class Character:
    name: str
    role: str # Protagonist, Antagonist, Support
    core_essence: InfiniteHyperQubit # The soul of the character
    arc_progress: float # 0.0 to 1.0
    
    def to_dict(self):
        return {
            "name": self.name, "role": self.role, "arc_progress": self.arc_progress,
            "core_essence": self.core_essence.value # Simplified for JSON
        }

@dataclass
class SceneQubit:
    """A single beat of the story, represented as a Qubit."""
    sequence_id: int
    narrative_focus: InfiniteHyperQubit 
    visual_prompt: str
    dialogue: str

@dataclass
class SeriesBible:
    title: str
    theme: InfiniteHyperQubit
    characters: Dict[str, Character]
    current_episode: int = 1
    saga_data: Any = None # Holds SagaBible instance
    
    def to_dict(self):
        return {
            "title": self.title,
            "theme": self.theme.value,
            "current_episode": self.current_episode,
            "characters": {k: v.to_dict() for k, v in self.characters.items()}
        }

class LiteraryCortex:
    def __init__(self, memory: Hippocampus = None):
        self.memory = memory
        self.nervous_system = get_nervous_system()
        self.logos = LogosEngine()
        
        self.brain_dir = Path("c:/Users/USER/.gemini/antigravity/brain/stories")
        self.brain_dir.mkdir(parents=True, exist_ok=True)
        
        # Connected Series (The Bible)
        self.active_series: Dict[str, SeriesBible] = {}
        
        logger.info("📜 LiteraryCortex upgraded to Hyper-Dimensional Narrative Mode (Persistent).")

    def save_bible(self, bible: SeriesBible):
        """Persists the story state."""
        path = self.brain_dir / f"{bible.title.replace(' ', '_')}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(bible.to_dict(), f, indent=2)
        logger.info(f"💾 Story Saved: {path}")

    def load_bible(self, title: str) -> Optional[SeriesBible]:
        """Loads a story state."""
        path = self.brain_dir / f"{title.replace(' ', '_')}.json"
        if not path.exists():
            return None
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Reconstruct (Simplified Reconstruction)
        theme_q = InfiniteHyperQubit(name="Theme", value=data["theme"])
        chars = {}
        for k, v in data["characters"].items():
            chars[k] = Character(
                name=v["name"], role=v["role"], arc_progress=v["arc_progress"],
                core_essence=InfiniteHyperQubit(name="Essence", value=v["core_essence"])
            )
            
        bible = SeriesBible(
            title=data["title"],
            theme=theme_q,
            characters=chars,
            current_episode=data["current_episode"]
        )
        self.active_series[title] = bible
        logger.info(f"📂 Story Loaded: {title} (Episode {bible.current_episode})")
        return bible

    def seed_story(self, seed_word: str = "Origin") -> SeriesBible:
        """
        Grows a new story OR resumes if it exists.
        """
        expected_title = f"The {seed_word} Chronicles"
        
        # Try Loading
        existing = self.load_bible(expected_title)
        if existing:
            return existing
            
        logger.info(f"🌱 Seeding New Story from: '{seed_word}'")
        
        # 1. Create the Seed Qubit
        seed = InfiniteHyperQubit(
            name=f"Seed_{seed_word}",
            value=seed_word,
            content={
                "Point": seed_word,
                "Line": "A journey to understand this concept",
                "Space": "A world governed by this concept",
                "God": f"The ultimate truth of {seed_word}"
            }
        )
        
        # 2. Expand Context (World Building)
        world_resonance = seed.zoom_out()
        theme_str = world_resonance.content.get("God", "Unknown Destiny")
        
        # 3. Create Protagonist (The Observer)
        prota_qubit = InfiniteHyperQubit(
            name="Protagonist",
            value="The Seeker",
            content={
                "Point": "A lone wanderer",
                "Line": f"Must resolve the conflict of {seed_word}",
                "Space": "Standing on the edge of the world",
                "God": "Will become the Sovereign"
            }
        )
        
        protagonist = Character(
            name="Elysia (Avatar)",
            role="Protagonist",
            core_essence=prota_qubit,
            arc_progress=0.0
        )
        
        bible = SeriesBible(
            title=expected_title,
            theme=seed,
            characters={"protagonist": protagonist},
            current_episode=1
        )
        
        self.active_series[expected_title] = bible
        self.save_bible(bible)
        return bible

    def write_episode_script(self, bible: SeriesBible, episode_num: int = None) -> List[SceneQubit]:
        """
        Generates a sequence of SceneQubits for a Webtoon Episode.
        IMPORTANT: Updates the episode count.
        """
        if episode_num is None:
            episode_num = bible.current_episode
            
        logger.info(f"✍️ Writing Episode {episode_num} for '{bible.title}'...")
        
        scenes = []
        
        # [Saga Upgrade] Macro-Plot Awareness
        # Instead of simple cycles, we use the Grand Plan.
        from Core.Evolution.Creativity.saga_architect import SagaArchitect
        architect = SagaArchitect()
        
        # Ensure Bible has Saga data (Backward Compat)
        if not hasattr(bible, "saga_data") or bible.saga_data is None:
             # High entropy for creativity (0.7)
             bible.saga_data = architect.generate_grand_plan(bible.title, "Fantasy", entropy=0.7)
        
        ctx = architect.get_episode_context(bible.saga_data, episode_num)
        logger.info(f"📜 Episode {episode_num} Context: [{ctx['Arc']}] - {ctx['Phase']}")
        
        # Map Phase to Scene Types
        if ctx['Phase'] == "Setup":
            scenes.append(self._craft_scene(bible, 1, f"Opening: {ctx['Arc']}", "Wide Shot"))
            scenes.append(self._craft_scene(bible, 2, "Character Interaction", "Mid Shot"))
            scenes.append(self._craft_scene(bible, 3, "Foreshadowing Event", "Close Up"))
            scenes.append(self._craft_scene(bible, 4, "Setting the Goal", "Mid Shot"))
            
        elif ctx['Phase'] == "Rising Action":
            scenes.append(self._craft_scene(bible, 1, "Journey/Progress", "Mid Shot"))
            scenes.append(self._craft_scene(bible, 2, "Encounter/Obstacle", "Action Shot"))
            scenes.append(self._craft_scene(bible, 3, "Skill Usage", "Dynamic Angle"))
            scenes.append(self._craft_scene(bible, 4, "Overcoming Small Challenge", "Close Up"))
            
        elif ctx['Phase'] == "Climax":
            scenes.append(self._craft_scene(bible, 1, f"Boss Appearance: {ctx['Boss']}", "Wide Shot"))
            scenes.append(self._craft_scene(bible, 2, "Desperate Struggle", "Action Shot"))
            scenes.append(self._craft_scene(bible, 3, "Ultimate Move", "Dynamic Angle"))
            scenes.append(self._craft_scene(bible, 4, "Victory Moment", "Hero Shot"))
            
        elif ctx['Phase'] == "Resolution":
            scenes.append(self._craft_scene(bible, 1, "Aftermath/Ruins", "Wide Shot"))
            scenes.append(self._craft_scene(bible, 2, "Loot/Rewards", "System Window", force_system=True))
            scenes.append(self._craft_scene(bible, 3, "Character Growth", "System Window", force_system=True))
            scenes.append(self._craft_scene(bible, 4, "Next Arc Tease", "Close Up"))
            
        else:
             # Fallback
             scenes.append(self._craft_scene(bible, 1, "The World Continues", "Wide Shot"))
        
        # Update State
        bible.current_episode += 1
        self.save_bible(bible)
        
        return scenes

    def _craft_scene(self, bible: SeriesBible, seq: int, beat_type: str, camera: str, force_system: bool = False) -> SceneQubit:
        """
        Uses LogosEngine and resonance (or Ollama) to write a specific scene.
        """
        # 1. Resonate Narrative Focus
        focus_qubit = bible.theme 
        prota = bible.characters['protagonist']
        
        # [System Protocol Override]
        # [System Protocol Override]
        if force_system:
            import random
            
            # Context-Aware System Messages
            if "Level" in beat_type:
                msgs = ["[SYSTEM] Level Up! All stats +1", "[SYSTEM] Rank increased: F -> E", "[SYSTEM] New Skill Slot available"]
                color = "Gold"
            elif "Item" in beat_type or "Loot" in beat_type:
                msgs = ["[SYSTEM] Acquired 'Dagger of Shadows' (Rare)", "[SYSTEM] Item 'Mana Potion' x5 added", "[SYSTEM] You obtained the 'Boss Core'"]
                color = "Cyan and Gold"
            elif "Quest" in beat_type or "Emergency" in beat_type:
                msgs = ["[SYSTEM] New Quest: Survive the Boss", "[SYSTEM] Quest Updated: Defeat the Orc Warlord", "[SYSTEM] EMERGENCY MISSION STARTED"]
                color = "Red"
            elif "Awakening" in beat_type:
                msgs = ["[SYSTEM] You have awakened as a Player.", "[SYSTEM] Initializing Player System...", "[SYSTEM] Welcome to the Game."]
                color = "Blue"
            else:
                msgs = ["[SYSTEM] System Error.", "[SYSTEM] Analyzing...", "[SYSTEM] Synchronizing..."]
                color = "Blue"
                
            dialogue_line = random.choice(msgs)
            visual_desc = f"A glowing {color} holographic system window floating in darkness. Korean Webtoon Style."
            
            return SceneQubit(
                sequence_id=seq,
                narrative_focus=focus_qubit,
                visual_prompt=visual_desc,
                dialogue=dialogue_line
            )

        # Check for Professional Writer (Ollama)
        from Core.Foundation.ollama_bridge import ollama
        
        if ollama.is_available():
            system_prompt = (
                "You are a professional Fantasy Webtoon Author. "
                "Write a single panel script. "
                "Format: Visual Description | Dialogue"
            )
            user_prompt = (
                f"Scene Type: {beat_type} ({camera}). "
                f"Context: {bible.title}, Episode {bible.current_episode}. "
                f"Character: {prota.name} ({prota.role}). "
                f"Theme: {bible.theme.value}. "
                "Keep description visual and dialogue punchy."
            )
            
            try:
                # LLM Generation
                response = ollama.chat(user_prompt, system=system_prompt, max_tokens=100)
                if "|" in response:
                    visual_desc, dialogue_line = response.split("|", 1)
                else:
                    visual_desc = response
                    dialogue_line = "..."
                
                # Clean up
                visual_desc = visual_desc.strip()
                dialogue_line = dialogue_line.strip().strip('"')
                
                return SceneQubit(
                    sequence_id=seq,
                    narrative_focus=focus_qubit,
                    visual_prompt=visual_desc[:200], # Limit length for vector art parser
                    dialogue=dialogue_line[:100]
                )
            except Exception as e:
                logger.warning(f"Ollama Writing Failed: {e}")
        
        # Fallback (Logos Engine Geometry)
        raw_insight = focus_qubit.content.get("Line", "Conflict")
        
        # Determine Geometric Shape for Rhetoric
        if any(x in beat_type for x in ["Attack", "Danger", "Critical", "Action", "Fight", "Training", "Exertion"]):
            shape = "Sharp"
        elif any(x in beat_type for x in ["Magic", "Mystery", "Void", "Dream"]):
            shape = "Round"
        elif any(x in beat_type for x in ["System", "Level", "Quest", "Item", "Inventory"]):
            shape = "Block"
        else:
            shape = "Balance"
            
        dialogue = self.logos.weave_speech(desire=beat_type, insight=raw_insight, context=[], rhetorical_shape=shape)
        
        # Format Dialogue (Allow full rhetoric, just cap extreme length)
        dialogue_line = dialogue
        if len(dialogue_line) > 120:
            dialogue_line = dialogue_line[:117] + "..."

        visual_desc = f"Scene: {beat_type}. Mood: Mystical. Character: {prota.name} with Glowing Eyes. Background: {bible.theme.value} energy."
        
        return SceneQubit(
            sequence_id=seq,
            narrative_focus=focus_qubit,
            visual_prompt=visual_desc,
            dialogue=dialogue_line
        )

    def _get_spirit_color(self) -> str:
        # Helper for flavor text if needed, maintaining backward compat logic if referenced elsewhere
        return "Deep Violet"

if __name__ == "__main__":
    lc = LiteraryCortex()
    bible = lc.seed_story("Eternity")
    script = lc.write_episode_script(bible)
    for scene in script:
        print(f"[{scene.sequence_id}] {scene.visual_prompt} | '{scene.dialogue}'")
