"""
Story Generation System - Phase 10

Creates creative narratives with world-building, character development,
and emotional arc optimization.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random


class StoryStyle(Enum):
    """Story genres and styles"""
    FANTASY = "fantasy"
    SCIENCE_FICTION = "science_fiction"
    MYSTERY = "mystery"
    ROMANCE = "romance"
    HORROR = "horror"
    ADVENTURE = "adventure"
    DRAMA = "drama"


class EmotionType(Enum):
    """Emotional states in narrative"""
    JOY = "joy"
    SADNESS = "sadness"
    FEAR = "fear"
    ANGER = "anger"
    SURPRISE = "surprise"
    TENSION = "tension"
    RELIEF = "relief"
    HOPE = "hope"


@dataclass
class World:
    """Story world/setting"""
    name: str
    description: str
    rules: List[str] = field(default_factory=list)
    locations: List[Dict[str, Any]] = field(default_factory=list)
    technology_level: str = "medieval"
    magic_system: Optional[Dict[str, Any]] = None
    cultural_elements: List[str] = field(default_factory=list)


@dataclass
class Character:
    """Story character"""
    name: str
    role: str  # protagonist, antagonist, supporting
    personality: List[str] = field(default_factory=list)
    background: str = ""
    goals: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    arc: Optional[str] = None  # character development arc


@dataclass
class PlotPoint:
    """Single plot point in the story"""
    sequence: int
    event: str
    characters_involved: List[str]
    location: str
    emotional_tone: EmotionType
    importance: float  # 0.0 to 1.0


@dataclass
class Scene:
    """Individual story scene"""
    plot_point: PlotPoint
    narrative: str
    dialogue: List[Dict[str, str]] = field(default_factory=list)
    emotion_intensity: float = 0.5
    pacing: str = "medium"  # slow, medium, fast


@dataclass
class Story:
    """Complete story structure"""
    world: World
    characters: List[Character]
    plot: List[PlotPoint]
    scenes: List[Scene]
    title: str = "Untitled"
    themes: List[str] = field(default_factory=list)
    tone: str = "balanced"
    word_count: int = 0


class StoryGenerator:
    """
    Creative Story Generation System
    
    Generates complete narratives with:
    - World building
    - Character creation
    - Plot construction
    - Scene writing
    - Consistency verification
    - Emotional arc optimization
    """
    
    def __init__(self):
        self.world_templates = self._init_world_templates()
        self.character_archetypes = self._init_character_archetypes()
        self.plot_structures = self._init_plot_structures()
    
    def _init_world_templates(self) -> Dict[str, Dict]:
        """Initialize world-building templates"""
        return {
            "fantasy": {
                "technology": "medieval",
                "common_rules": ["Magic exists", "Multiple races", "Ancient prophecies"],
                "locations": ["Castle", "Forest", "Mountain", "Village"]
            },
            "science_fiction": {
                "technology": "advanced",
                "common_rules": ["FTL travel", "AI exists", "Space colonies"],
                "locations": ["Spaceship", "Space station", "Colony planet", "Research lab"]
            },
            "mystery": {
                "technology": "modern",
                "common_rules": ["Crime has occurred", "Clues are hidden", "Truth is obscured"],
                "locations": ["Crime scene", "Police station", "Suspect's home", "Dark alley"]
            }
        }
    
    def _init_character_archetypes(self) -> Dict[str, Dict]:
        """Initialize character archetypes"""
        return {
            "hero": {
                "traits": ["brave", "determined", "compassionate"],
                "arc": "growth through adversity"
            },
            "mentor": {
                "traits": ["wise", "experienced", "patient"],
                "arc": "passing the torch"
            },
            "villain": {
                "traits": ["ambitious", "ruthless", "cunning"],
                "arc": "corruption or redemption"
            },
            "trickster": {
                "traits": ["clever", "unpredictable", "charming"],
                "arc": "finding purpose"
            }
        }
    
    def _init_plot_structures(self) -> Dict[str, List[str]]:
        """Initialize narrative structures"""
        return {
            "three_act": [
                "Setup - Introduce world and characters",
                "Confrontation - Rising conflict and challenges",
                "Resolution - Climax and conclusion"
            ],
            "hero_journey": [
                "Ordinary World",
                "Call to Adventure",
                "Refusal of the Call",
                "Meeting the Mentor",
                "Crossing the Threshold",
                "Tests and Trials",
                "Approach to Innermost Cave",
                "Ordeal",
                "Reward",
                "The Road Back",
                "Resurrection",
                "Return with Elixir"
            ]
        }
    
    async def generate_story(
        self,
        prompt: str,
        style: str = "fantasy",
        length: str = "short"
    ) -> Dict[str, Any]:
        """
        Generate a complete story from a prompt
        
        Args:
            prompt: Story seed/concept
            style: Genre/style (fantasy, sci-fi, etc.)
            length: short, medium, long
        
        Returns:
            Complete story structure with metadata
        """
        print(f"🎨 Generating {style} story from prompt: '{prompt}'")
        
        # 1. Build world
        world = await self.build_world(prompt, style)
        print(f"🌍 Built world: {world.name}")
        
        # 2. Create characters
        characters = await self.create_characters(world, prompt)
        print(f"👥 Created {len(characters)} characters")
        
        # 3. Construct plot
        plot = await self.construct_plot(world, characters, prompt, length)
        print(f"📖 Constructed plot with {len(plot)} plot points")
        
        # 4. Write scenes
        scenes = []
        for i, plot_point in enumerate(plot):
            scene = await self.write_scene(plot_point, characters, world)
            scenes.append(scene)
            print(f"✍️  Scene {i+1}/{len(plot)} written")
        
        # 5. Ensure consistency
        story = Story(
            world=world,
            characters=characters,
            plot=plot,
            scenes=scenes
        )
        story = await self.ensure_consistency(story)
        print("✅ Consistency verified")
        
        # 6. Optimize emotional arc
        story = await self.optimize_emotional_arc(story)
        print("🎭 Emotional arc optimized")
        
        # 7. Extract metadata
        story.title = await self.generate_title(story, prompt)
        story.themes = self.extract_themes(story)
        story.tone = self.analyze_tone(story)
        story.word_count = self.count_words(story)
        
        return {
            "world": {
                "name": world.name,
                "description": world.description,
                "rules": world.rules,
                "locations": world.locations,
                "technology_level": world.technology_level
            },
            "characters": [
                {
                    "name": c.name,
                    "role": c.role,
                    "personality": c.personality,
                    "background": c.background
                }
                for c in characters
            ],
            "plot": [
                {
                    "sequence": p.sequence,
                    "event": p.event,
                    "emotional_tone": p.emotional_tone.value
                }
                for p in plot
            ],
            "full_story": self.format_story(story),
            "meta": {
                "title": story.title,
                "themes": story.themes,
                "tone": story.tone,
                "complexity": self.measure_complexity(story),
                "word_count": story.word_count
            }
        }
    
    async def build_world(self, prompt: str, style: str) -> World:
        """Build the story world from prompt and style"""
        template = self.world_templates.get(style, self.world_templates["fantasy"])
        
        # Generate world name
        world_name = self._generate_world_name(prompt, style)
        
        # Create world description
        description = f"A {style} world where {prompt.lower()}. "
        description += f"Technology level: {template['technology']}. "
        
        # Setup locations
        locations = [
            {"name": loc, "description": f"A key {loc.lower()} in the story"}
            for loc in template["locations"][:3]
        ]
        
        return World(
            name=world_name,
            description=description,
            rules=template["common_rules"][:2],
            locations=locations,
            technology_level=template["technology"]
        )
    
    async def create_characters(self, world: World, prompt: str) -> List[Character]:
        """Generate story characters"""
        characters = []
        
        # Protagonist
        hero = Character(
            name=self._generate_character_name("hero"),
            role="protagonist",
            personality=["brave", "curious", "determined"],
            background=f"A person from {world.name} seeking to understand {prompt.lower()}",
            goals=["Discover the truth", "Overcome challenges"],
            fears=["Failure", "Loss"]
        )
        characters.append(hero)
        
        # Antagonist
        villain = Character(
            name=self._generate_character_name("villain"),
            role="antagonist",
            personality=["cunning", "powerful", "mysterious"],
            background=f"An opposing force in {world.name}",
            goals=["Prevent the hero", "Maintain power"],
            fears=["Defeat", "Exposure"]
        )
        characters.append(villain)
        
        # Supporting character
        mentor = Character(
            name=self._generate_character_name("mentor"),
            role="supporting",
            personality=["wise", "kind", "experienced"],
            background=f"A guide in {world.name}",
            goals=["Help the hero", "Pass on knowledge"],
            fears=["Hero's failure", "Being too late"]
        )
        characters.append(mentor)
        
        return characters
    
    async def construct_plot(
        self,
        world: World,
        characters: List[Character],
        prompt: str,
        length: str
    ) -> List[PlotPoint]:
        """Construct the story plot"""
        # Determine number of plot points based on length
        num_points = {"short": 5, "medium": 8, "long": 12}.get(length, 5)
        
        # Use three-act structure
        plot_points = []
        
        # Act 1: Setup
        plot_points.append(PlotPoint(
            sequence=1,
            event=f"Introduction to {world.name} and {characters[0].name}",
            characters_involved=[characters[0].name],
            location=world.locations[0]["name"],
            emotional_tone=EmotionType.HOPE,
            importance=0.8
        ))
        
        plot_points.append(PlotPoint(
            sequence=2,
            event=f"The inciting incident: {prompt} becomes urgent",
            characters_involved=[c.name for c in characters[:2]],
            location=world.locations[0]["name"],
            emotional_tone=EmotionType.SURPRISE,
            importance=1.0
        ))
        
        # Act 2: Confrontation
        for i in range(3, num_points - 1):
            emotions = [EmotionType.TENSION, EmotionType.FEAR, EmotionType.HOPE]
            # Sample characters safely
            sample_size = min(2, len(characters))
            selected_chars = random.sample(characters, sample_size) if len(characters) > 0 else []
            
            plot_points.append(PlotPoint(
                sequence=i,
                event=f"Challenge {i-2}: Facing obstacles in the quest",
                characters_involved=[c.name for c in selected_chars],
                location=random.choice(world.locations)["name"],
                emotional_tone=random.choice(emotions),
                importance=0.6 + (i / num_points) * 0.3
            ))
        
        # Act 3: Resolution
        plot_points.append(PlotPoint(
            sequence=num_points - 1,
            event="The climactic confrontation",
            characters_involved=[c.name for c in characters],
            location=world.locations[-1]["name"],
            emotional_tone=EmotionType.TENSION,
            importance=1.0
        ))
        
        plot_points.append(PlotPoint(
            sequence=num_points,
            event="Resolution and new understanding",
            characters_involved=[characters[0].name],
            location=world.locations[0]["name"],
            emotional_tone=EmotionType.RELIEF,
            importance=0.9
        ))
        
        return plot_points
    
    async def write_scene(
        self,
        plot_point: PlotPoint,
        characters: List[Character],
        world: World
    ) -> Scene:
        """Write a narrative scene from a plot point"""
        # Create narrative text
        narrative = f"In {plot_point.location}, {plot_point.event}. "
        narrative += f"The {plot_point.emotional_tone.value} was palpable. "
        
        # Add character interactions
        char_dict = {c.name: c for c in characters}
        involved_chars = [char_dict.get(name) for name in plot_point.characters_involved if name in char_dict]
        
        if involved_chars:
            narrative += f"{involved_chars[0].name} "
            if len(involved_chars) > 1:
                narrative += f"confronted {involved_chars[1].name}. "
            else:
                narrative += "stood alone, contemplating the situation. "
        
        # Generate simple dialogue
        dialogue = []
        if len(involved_chars) >= 2:
            dialogue.append({
                "speaker": involved_chars[0].name,
                "line": f"We must address {plot_point.event.lower()}."
            })
            dialogue.append({
                "speaker": involved_chars[1].name,
                "line": "I understand. Let us proceed with caution."
            })
        
        return Scene(
            plot_point=plot_point,
            narrative=narrative,
            dialogue=dialogue,
            emotion_intensity=plot_point.importance,
            pacing="medium"
        )
    
    async def ensure_consistency(self, story: Story) -> Story:
        """Verify and fix story consistency"""
        # Check character continuity
        all_mentioned = set()
        for scene in story.scenes:
            all_mentioned.update(scene.plot_point.characters_involved)
        
        # Verify all mentioned characters exist
        character_names = {c.name for c in story.characters}
        for name in all_mentioned:
            if name not in character_names:
                print(f"⚠️  Warning: Character '{name}' mentioned but not defined")
        
        # Check location continuity
        defined_locations = {loc["name"] for loc in story.world.locations}
        for scene in story.scenes:
            if scene.plot_point.location not in defined_locations:
                # Add missing location
                story.world.locations.append({
                    "name": scene.plot_point.location,
                    "description": f"A location in {story.world.name}"
                })
        
        return story
    
    async def optimize_emotional_arc(self, story: Story) -> Story:
        """Optimize the emotional journey of the story"""
        # Ensure emotional variety
        emotions_used = [scene.plot_point.emotional_tone for scene in story.scenes]
        
        # Check for emotional monotony
        if len(set(emotions_used)) < 3:
            print("💡 Diversifying emotional tones")
            # Add more emotional variety in middle scenes
            for i, scene in enumerate(story.scenes[1:-1], 1):
                if i % 2 == 0:
                    # Alternate emotions for better pacing
                    available = [e for e in EmotionType if e != scene.plot_point.emotional_tone]
                    scene.plot_point.emotional_tone = random.choice(available)
        
        # Ensure climax has highest emotional intensity
        if len(story.scenes) > 2:
            climax_scene = story.scenes[-2]  # Second to last is usually climax
            climax_scene.emotion_intensity = 1.0
            climax_scene.pacing = "fast"
        
        return story
    
    async def generate_title(self, story: Story, prompt: str) -> str:
        """Generate a title for the story"""
        # Use key elements
        hero = next((c for c in story.characters if c.role == "protagonist"), None)
        if hero:
            return f"The {story.world.name} Chronicles: {hero.name}'s Journey"
        return f"Tales from {story.world.name}"
    
    def extract_themes(self, story: Story) -> List[str]:
        """Extract themes from the story"""
        themes = []
        
        # Analyze plot for common themes
        plot_text = " ".join(p.event.lower() for p in story.plot)
        
        if "discover" in plot_text or "truth" in plot_text:
            themes.append("Discovery")
        if "confront" in plot_text or "challenge" in plot_text:
            themes.append("Overcoming Adversity")
        if "friend" in plot_text or "together" in plot_text:
            themes.append("Friendship")
        if "power" in plot_text or "control" in plot_text:
            themes.append("Power and Responsibility")
        
        return themes or ["Adventure", "Growth"]
    
    def analyze_tone(self, story: Story) -> str:
        """Analyze the overall tone of the story"""
        emotions = [scene.plot_point.emotional_tone for scene in story.scenes]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Determine dominant emotion
        dominant = max(emotion_counts, key=emotion_counts.get)
        
        tone_map = {
            EmotionType.JOY: "optimistic",
            EmotionType.SADNESS: "melancholic",
            EmotionType.FEAR: "suspenseful",
            EmotionType.TENSION: "dramatic",
            EmotionType.HOPE: "uplifting"
        }
        
        return tone_map.get(dominant, "balanced")
    
    def measure_complexity(self, story: Story) -> float:
        """Measure story complexity (0.0 to 1.0)"""
        factors = [
            len(story.characters) / 10,  # Character count
            len(story.plot) / 15,  # Plot points
            len(story.world.rules) / 5,  # World complexity
            len(story.themes) / 5  # Theme depth
        ]
        return min(sum(factors) / len(factors), 1.0)
    
    def count_words(self, story: Story) -> int:
        """Count total words in story"""
        total = 0
        for scene in story.scenes:
            total += len(scene.narrative.split())
            for dialogue in scene.dialogue:
                total += len(dialogue["line"].split())
        return total
    
    def format_story(self, story: Story) -> str:
        """Format story as readable text"""
        output = []
        output.append(f"# {story.title}\n")
        output.append(f"## World: {story.world.name}\n")
        output.append(f"{story.world.description}\n")
        
        output.append("\n## Characters\n")
        for char in story.characters:
            output.append(f"- **{char.name}** ({char.role}): {char.background}")
        
        output.append("\n## Story\n")
        for i, scene in enumerate(story.scenes, 1):
            output.append(f"\n### Scene {i}: {scene.plot_point.event}\n")
            output.append(f"{scene.narrative}\n")
            if scene.dialogue:
                output.append("\nDialogue:")
                for line in scene.dialogue:
                    output.append(f'- {line["speaker"]}: "{line["line"]}"')
        
        return "\n".join(output)
    
    def _generate_world_name(self, prompt: str, style: str) -> str:
        """Generate a world name"""
        prefixes = {
            "fantasy": ["Aether", "Mythral", "Eldar", "Nova"],
            "science_fiction": ["Neo", "Cyber", "Stellar", "Quantum"],
            "mystery": ["Shadow", "Crimson", "Obsidian", "Noir"]
        }
        suffixes = {
            "fantasy": ["ia", "heim", "dor", "rion"],
            "science_fiction": ["Prime", "Station", "Nexus", "Core"],
            "mystery": ["City", "Falls", "Heights", "Bay"]
        }
        
        prefix = random.choice(prefixes.get(style, prefixes["fantasy"]))
        suffix = random.choice(suffixes.get(style, suffixes["fantasy"]))
        return f"{prefix}{suffix}"
    
    def _generate_character_name(self, archetype: str) -> str:
        """Generate a character name"""
        first_names = {
            "hero": ["Aria", "Kael", "Luna", "Zephyr", "Nova"],
            "villain": ["Malachar", "Ravenna", "Mordex", "Nyx", "Vex"],
            "mentor": ["Aldric", "Celeste", "Orin", "Sage", "Elder"]
        }
        
        names = first_names.get(archetype, ["Alex", "Jordan", "Morgan"])
        return random.choice(names)
