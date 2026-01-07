"""
Music Composition System - Phase 10

Creates emotional music with music theory, melody, harmony, and rhythm generation.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import random
import math


class MusicStyle(Enum):
    """Music genres and styles"""
    CLASSICAL = "classical"
    JAZZ = "jazz"
    ELECTRONIC = "electronic"
    AMBIENT = "ambient"
    ROCK = "rock"
    FOLK = "folk"


class MusicEmotion(Enum):
    """Emotional qualities in music"""
    JOYFUL = "joyful"
    MELANCHOLIC = "melancholic"
    ENERGETIC = "energetic"
    PEACEFUL = "peaceful"
    TENSE = "tense"
    ROMANTIC = "romantic"
    MYSTERIOUS = "mysterious"


class Note:
    """Musical note representation"""
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self, pitch: int, duration: float = 1.0, velocity: int = 64):
        self.pitch = pitch  # MIDI note number (0-127)
        self.duration = duration  # In beats
        self.velocity = velocity  # Volume (0-127)
    
    @property
    def name(self) -> str:
        """Get note name (e.g., 'C4')"""
        octave = (self.pitch // 12) - 1
        note_idx = self.pitch % 12
        return f"{self.NOTE_NAMES[note_idx]}{octave}"
    
    def __repr__(self):
        return f"Note({self.name}, dur={self.duration}, vel={self.velocity})"


@dataclass
class Scale:
    """Musical scale"""
    root: int  # MIDI note
    intervals: List[int]  # Semitone intervals
    name: str = ""
    
    def get_notes(self, octaves: int = 2) -> List[int]:
        """Get all notes in scale across octaves"""
        notes = []
        for octave in range(octaves):
            for interval in self.intervals:
                notes.append(self.root + interval + (12 * octave))
        return notes


@dataclass
class Chord:
    """Musical chord"""
    root: int  # Root note MIDI number
    intervals: List[int]  # Intervals from root
    name: str = ""
    
    def get_notes(self) -> List[int]:
        """Get all notes in chord"""
        return [self.root + interval for interval in self.intervals]


@dataclass
class Melody:
    """Musical melody"""
    notes: List[Note] = field(default_factory=list)
    key: str = "C"
    scale_type: str = "major"


@dataclass
class Harmony:
    """Harmonic progression"""
    chords: List[Chord] = field(default_factory=list)
    progression_name: str = ""


@dataclass
class Rhythm:
    """Rhythmic pattern"""
    pattern: List[float] = field(default_factory=list)  # Beat timings
    tempo: int = 120  # BPM
    time_signature: Tuple[int, int] = (4, 4)


@dataclass
class Instrumentation:
    """Instrument arrangement"""
    melody_instrument: str = "piano"
    harmony_instruments: List[str] = field(default_factory=list)
    rhythm_instruments: List[str] = field(default_factory=list)
    parts: Dict[str, List[Note]] = field(default_factory=dict)


@dataclass
class Composition:
    """Complete musical composition"""
    melody: Melody
    harmony: Harmony
    rhythm: Rhythm
    instrumentation: Instrumentation
    key: str = "C"
    tempo: int = 120
    time_signature: Tuple[int, int] = (4, 4)
    emotion: MusicEmotion = MusicEmotion.PEACEFUL
    duration_bars: int = 8


class MusicComposer:
    """
    Music Composition System
    
    Creates music with:
    - Emotion-based music theory
    - Melody generation
    - Harmony generation
    - Rhythm patterns
    - Instrument arrangement
    """
    
    def __init__(self):
        self.scales = self._init_scales()
        self.chord_progressions = self._init_chord_progressions()
        self.emotion_mappings = self._init_emotion_mappings()
        self.instruments = self._init_instruments()
    
    def _init_scales(self) -> Dict[str, Scale]:
        """Initialize musical scales"""
        return {
            "major": Scale(60, [0, 2, 4, 5, 7, 9, 11], "Major"),
            "minor": Scale(60, [0, 2, 3, 5, 7, 8, 10], "Natural Minor"),
            "pentatonic_major": Scale(60, [0, 2, 4, 7, 9], "Major Pentatonic"),
            "pentatonic_minor": Scale(60, [0, 3, 5, 7, 10], "Minor Pentatonic"),
            "blues": Scale(60, [0, 3, 5, 6, 7, 10], "Blues"),
            "dorian": Scale(60, [0, 2, 3, 5, 7, 9, 10], "Dorian"),
            "phrygian": Scale(60, [0, 1, 3, 5, 7, 8, 10], "Phrygian")
        }
    
    def _init_chord_progressions(self) -> Dict[str, List[str]]:
        """Initialize common chord progressions"""
        return {
            "pop": ["I", "V", "vi", "IV"],  # C-G-Am-F
            "jazz": ["ii", "V", "I"],  # Dm-G-C
            "blues": ["I", "I", "I", "I", "IV", "IV", "I", "I", "V", "IV", "I", "V"],
            "sad": ["vi", "IV", "I", "V"],  # Am-F-C-G
            "epic": ["i", "VI", "III", "VII"],  # Am-F-C-G in minor
        }
    
    def _init_emotion_mappings(self) -> Dict[MusicEmotion, Dict]:
        """Map emotions to musical parameters"""
        return {
            MusicEmotion.JOYFUL: {
                "key": "major",
                "tempo": 140,
                "scale": "major",
                "progression": "pop"
            },
            MusicEmotion.MELANCHOLIC: {
                "key": "minor",
                "tempo": 72,
                "scale": "minor",
                "progression": "sad"
            },
            MusicEmotion.ENERGETIC: {
                "key": "major",
                "tempo": 160,
                "scale": "pentatonic_major",
                "progression": "pop"
            },
            MusicEmotion.PEACEFUL: {
                "key": "major",
                "tempo": 60,
                "scale": "pentatonic_major",
                "progression": "jazz"
            },
            MusicEmotion.TENSE: {
                "key": "minor",
                "tempo": 110,
                "scale": "phrygian",
                "progression": "epic"
            },
            MusicEmotion.ROMANTIC: {
                "key": "major",
                "tempo": 80,
                "scale": "major",
                "progression": "sad"
            },
            MusicEmotion.MYSTERIOUS: {
                "key": "minor",
                "tempo": 90,
                "scale": "dorian",
                "progression": "jazz"
            }
        }
    
    def _init_instruments(self) -> Dict[str, int]:
        """Initialize MIDI instrument map"""
        return {
            "piano": 0,
            "guitar": 24,
            "violin": 40,
            "flute": 73,
            "strings": 48,
            "synth": 80,
            "bass": 32,
            "drums": 128  # Percussion
        }
    
    async def compose_music(
        self,
        emotion: str,
        style: str = "classical",
        duration_bars: int = 8
    ) -> Dict[str, Any]:
        """
        Compose music based on emotion and style
        
        Args:
            emotion: Target emotion (joyful, melancholic, etc.)
            style: Music style (classical, jazz, etc.)
            duration_bars: Length in bars
        
        Returns:
            Complete composition with metadata
        """
        print(f"🎵 Composing {style} music with {emotion} emotion")
        
        # Parse emotion
        try:
            emotion_enum = MusicEmotion(emotion.lower())
        except ValueError:
            emotion_enum = MusicEmotion.PEACEFUL
        
        # 1. Apply music theory
        key_data = self.select_key_for_emotion(emotion_enum)
        tempo = self.select_tempo_for_emotion(emotion_enum)
        time_signature = self.select_time_signature(style)
        
        print(f"🎼 Key: {key_data['note_name']} {key_data['scale_type']}, Tempo: {tempo} BPM")
        
        # 2. Generate melody
        melody = await self.generate_melody(key_data, emotion_enum, duration_bars)
        print(f"🎹 Generated melody with {len(melody.notes)} notes")
        
        # 3. Generate harmony
        harmony = await self.generate_harmony(melody, key_data)
        print(f"🎸 Generated harmony with {len(harmony.chords)} chords")
        
        # 4. Generate rhythm
        rhythm = await self.generate_rhythm(tempo, time_signature, duration_bars)
        print(f"🥁 Generated rhythm pattern")
        
        # 5. Arrange instruments
        instrumentation = await self.arrange_instruments(
            melody, harmony, rhythm, style
        )
        print(f"🎺 Arranged {len(instrumentation.parts)} instrument parts")
        
        # 6. Create composition object
        composition = Composition(
            melody=melody,
            harmony=harmony,
            rhythm=rhythm,
            instrumentation=instrumentation,
            key=key_data['note_name'],
            tempo=tempo,
            time_signature=time_signature,
            emotion=emotion_enum,
            duration_bars=duration_bars
        )
        
        # 7. Evaluate emotion match
        emotion_match = self.evaluate_emotion_match(composition, emotion_enum)
        
        return {
            "composition": {
                "melody_notes": [note.name for note in melody.notes],
                "chord_progression": [chord.name for chord in harmony.chords],
                "instruments": list(instrumentation.parts.keys())
            },
            "score": self.generate_text_score(composition),
            "analysis": {
                "key": key_data['note_name'],
                "scale": key_data['scale_type'],
                "tempo": tempo,
                "time_signature": f"{time_signature[0]}/{time_signature[1]}",
                "emotion_match": emotion_match,
                "complexity": self.calculate_complexity(composition)
            }
        }
    
    def select_key_for_emotion(self, emotion: MusicEmotion) -> Dict[str, Any]:
        """Select musical key based on emotion"""
        mapping = self.emotion_mappings[emotion]
        
        # Select root note (C for simplicity, can be randomized)
        root_midi = 60  # Middle C
        note_name = Note(root_midi).name[:-1]  # Remove octave
        
        return {
            "root_midi": root_midi,
            "note_name": note_name,
            "scale_type": mapping["scale"],
            "mode": mapping["key"]
        }
    
    def select_tempo_for_emotion(self, emotion: MusicEmotion) -> int:
        """Select tempo (BPM) based on emotion"""
        return self.emotion_mappings[emotion]["tempo"]
    
    def select_time_signature(self, style: str) -> Tuple[int, int]:
        """Select time signature based on style"""
        signatures = {
            "classical": (4, 4),
            "jazz": (4, 4),
            "electronic": (4, 4),
            "ambient": (4, 4),
            "rock": (4, 4),
            "folk": (3, 4)  # Waltz
        }
        return signatures.get(style, (4, 4))
    
    async def generate_melody(
        self,
        key_data: Dict[str, Any],
        emotion: MusicEmotion,
        duration_bars: int
    ) -> Melody:
        """Generate a melodic line"""
        scale_type = key_data["scale_type"]
        scale = self.scales[scale_type]
        scale.root = key_data["root_midi"]
        
        # Get available notes
        available_notes = scale.get_notes(octaves=2)
        
        # Generate notes based on emotion
        notes = []
        beats_per_bar = 4
        total_beats = duration_bars * beats_per_bar
        
        current_beat = 0
        while current_beat < total_beats:
            # Select note from scale
            pitch = random.choice(available_notes)
            
            # Vary duration based on emotion
            if emotion in [MusicEmotion.ENERGETIC, MusicEmotion.JOYFUL]:
                duration = random.choice([0.5, 1.0])  # Shorter, faster notes
            elif emotion in [MusicEmotion.PEACEFUL, MusicEmotion.MELANCHOLIC]:
                duration = random.choice([1.0, 2.0])  # Longer, slower notes
            else:
                duration = 1.0
            
            # Vary velocity
            velocity = random.randint(60, 100)
            
            notes.append(Note(pitch, duration, velocity))
            current_beat += duration
        
        return Melody(
            notes=notes,
            key=key_data["note_name"],
            scale_type=scale_type
        )
    
    async def generate_harmony(self, melody: Melody, key_data: Dict[str, Any]) -> Harmony:
        """Generate harmonic chord progression"""
        # Get chord progression for the emotion
        root = key_data["root_midi"]
        scale_type = key_data["scale_type"]
        
        # Use simple progression
        if "minor" in scale_type:
            progression_name = "sad"
        else:
            progression_name = "pop"
        
        # Build chords
        chords = []
        chord_intervals = {
            "major": [0, 4, 7],  # Major triad
            "minor": [0, 3, 7]   # Minor triad
        }
        
        # Create 4 chords for progression
        scale = self.scales[scale_type]
        scale.root = root
        scale_notes = scale.get_notes(octaves=1)
        
        # Adjust scale degrees based on scale size
        num_notes = len(scale_notes)
        if num_notes >= 7:
            scale_degrees = [0, 2, 4, 5]  # I, ii, iii, IV for 7-note scales
        elif num_notes >= 5:
            scale_degrees = [0, 1, 2, 3]  # Use first 4 notes for pentatonic
        else:
            scale_degrees = [0, 1, 2, 0]  # Fallback for very small scales
        
        for degree in scale_degrees:
            if degree < len(scale_notes):
                chord_root = scale_notes[degree]
            else:
                chord_root = scale_notes[0]  # Fallback to root
                
            intervals = chord_intervals["major"] if "major" in scale_type else chord_intervals["minor"]
            
            chord = Chord(
                root=chord_root,
                intervals=intervals,
                name=f"{Note(chord_root).name[:-1]} {'major' if 'major' in scale_type else 'minor'}"
            )
            chords.append(chord)
        
        return Harmony(
            chords=chords,
            progression_name=progression_name
        )
    
    async def generate_rhythm(
        self,
        tempo: int,
        time_signature: Tuple[int, int],
        duration_bars: int
    ) -> Rhythm:
        """Generate rhythmic pattern"""
        beats_per_bar = time_signature[0]
        
        # Generate simple beat pattern
        pattern = []
        for bar in range(duration_bars):
            for beat in range(beats_per_bar):
                pattern.append(bar * beats_per_bar + beat)
        
        return Rhythm(
            pattern=pattern,
            tempo=tempo,
            time_signature=time_signature
        )
    
    async def arrange_instruments(
        self,
        melody: Melody,
        harmony: Harmony,
        rhythm: Rhythm,
        style: str
    ) -> Instrumentation:
        """Arrange instruments for the composition"""
        instrumentation = Instrumentation()
        
        # Select instruments based on style
        if style == "classical":
            instrumentation.melody_instrument = "violin"
            instrumentation.harmony_instruments = ["piano", "strings"]
        elif style == "jazz":
            instrumentation.melody_instrument = "piano"
            instrumentation.harmony_instruments = ["bass", "piano"]
            instrumentation.rhythm_instruments = ["drums"]
        elif style == "electronic":
            instrumentation.melody_instrument = "synth"
            instrumentation.harmony_instruments = ["synth"]
            instrumentation.rhythm_instruments = ["drums"]
        else:
            instrumentation.melody_instrument = "piano"
            instrumentation.harmony_instruments = ["strings"]
        
        # Assign melody to lead instrument
        instrumentation.parts[instrumentation.melody_instrument] = melody.notes
        
        # Create harmony parts (simplified - play chord roots)
        for harm_inst in instrumentation.harmony_instruments:
            harmony_notes = []
            for chord in harmony.chords:
                # Use chord root as bass note
                harmony_notes.append(Note(chord.root, 4.0, 70))  # Whole note
            instrumentation.parts[harm_inst] = harmony_notes
        
        return instrumentation
    
    def evaluate_emotion_match(
        self,
        composition: Composition,
        target_emotion: MusicEmotion
    ) -> float:
        """Evaluate how well composition matches target emotion"""
        target_mapping = self.emotion_mappings[target_emotion]
        
        score = 0.0
        
        # Check tempo match
        tempo_diff = abs(composition.tempo - target_mapping["tempo"])
        tempo_score = max(0, 1.0 - (tempo_diff / 100))
        score += tempo_score * 0.4
        
        # Check scale match
        if composition.melody.scale_type == target_mapping["scale"]:
            score += 0.3
        
        # Check complexity (energetic = complex, peaceful = simple)
        complexity = self.calculate_complexity(composition)
        if target_emotion in [MusicEmotion.ENERGETIC, MusicEmotion.JOYFUL]:
            score += complexity * 0.3
        else:
            score += (1 - complexity) * 0.3
        
        return min(score, 1.0)
    
    def calculate_complexity(self, composition: Composition) -> float:
        """Calculate composition complexity (0.0 to 1.0)"""
        factors = [
            len(composition.melody.notes) / 50,  # Note count
            len(composition.harmony.chords) / 10,  # Chord count
            len(composition.instrumentation.parts) / 5  # Instrument count
        ]
        return min(sum(factors) / len(factors), 1.0)
    
    def generate_text_score(self, composition: Composition) -> str:
        """Generate a text-based musical score"""
        lines = []
        lines.append(f"Title: {composition.emotion.value.title()} Composition")
        lines.append(f"Key: {composition.key}")
        lines.append(f"Tempo: {composition.tempo} BPM")
        lines.append(f"Time Signature: {composition.time_signature[0]}/{composition.time_signature[1]}")
        lines.append("")
        
        lines.append("Melody:")
        melody_line = " ".join([note.name for note in composition.melody.notes[:16]])  # First bar
        lines.append(f"  {melody_line}...")
        lines.append("")
        
        lines.append("Chord Progression:")
        for i, chord in enumerate(composition.harmony.chords, 1):
            lines.append(f"  {i}. {chord.name}")
        lines.append("")
        
        lines.append("Instrumentation:")
        for instrument in composition.instrumentation.parts.keys():
            lines.append(f"  - {instrument.title()}")
        
        return "\n".join(lines)
    
    async def synthesize_audio(self, composition: Composition) -> bytes:
        """
        Synthesize audio from composition (placeholder)
        
        In a real implementation, this would use a library like:
        - mido (MIDI)
        - pydub (audio processing)
        - sounddevice (playback)
        """
        # Placeholder for actual audio synthesis
        print("🔊 Audio synthesis would happen here (placeholder)")
        return b""  # Empty bytes as placeholder
