"""
Unified Experience Core (The Hippocampus)
=========================================
Synthesizes the 4 Modes of Memory into a single coherent Organ.

Layers:
1. Stream (Raw Event Log) - "What happened?"
2. Learner (Procedural/RL) - "How do I do it better?"
3. Narrator (Episodic/Semantic) - "What does it mean for my story?"
4. Wave (Ontological/Frequency) - "How does it change who I am?"

This is the central engine for 'Universal Internalization'.
"""

import time
import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from collections import defaultdict

from elysia_core import Cell, Organ

# Optional Imports (Wave Physics)
try:
    from Core.Foundation.Wave.wave_tensor import WaveTensor
except ImportError:
    WaveTensor = None

logger = logging.getLogger("UnifiedExperienceCore")

@dataclass
class ExperienceEvent:
    """The Atomic Unit of Experience"""
    id: str
    timestamp: float
    type: str  # 'action', 'thought', 'emotion', 'perception'
    content: str
    context: Dict[str, Any]
    outcome: Optional[Dict[str, Any]] = None
    feedback: float = 0.0  # -1.0 to 1.0 (Pain/Pleasure)
    embedding: Optional[List[float]] = None # For Vector Search

@Cell("ExperienceCore")
class UnifiedExperienceCore:
    def __init__(self):
        self.base_dir = Path("data/memory/experience")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Layer 1: Stream
        self.stream: List[ExperienceEvent] = []
        
        # Layer 2: Learner (Patterns)
        self.patterns: Dict[str, Dict] = {} # Pattern ID -> Score
        
        # Layer 3: Narrator (Themes)
        self.themes: Dict[str, List[str]] = defaultdict(list) # Theme -> Event IDs
        self.narrative_arc: List[str] = []
        
        # Layer 4: Wave (Self-State Frequencies)
        self.aspect_frequencies = {
            "engineer": 256.0, "artist": 432.0, "philosophical": 512.0,
            "emotional": 528.0, "creative": 852.0
        }
        self.current_state = {k: 0.5 for k in self.aspect_frequencies}
        
        self._load_state()
        logger.info("🧠 UnifiedExperienceCore (The Hippocampus) Initialized")

    def absorb(self, 
               content: str, 
               type: str = "thought", 
               context: Dict = None, 
               feedback: float = 0.0) -> Dict[str, Any]:
        """
        The Main Entry Point. Absorbs an event and processes it through all 4 layers.
        """
        if context is None: context = {}
        timestamp = time.time()
        event_id = f"exp_{int(timestamp)}_{hash(content) % 10000}"
        
        event = ExperienceEvent(event_id, timestamp, type, content, context, feedback=feedback)
        
        # 1. Stream (Log it)
        self.stream.append(event)
        
        # 2. Learner (Optimize it)
        learning_result = self._process_learning(event)
        
        # 3. Narrator (Weave it)
        narrative_result = self._process_narrative(event)
        
        # 4. Wave (Resonate it)
        wave_result = self._process_wave(event)
        
        # Auto-save occasionally
        if len(self.stream) % 10 == 0:
            self._save_state()
            
        return {
            "id": event_id,
            "learning": learning_result,
            "narrative": narrative_result,
            "wave_shift": wave_result
        }

    def _process_learning(self, event: ExperienceEvent) -> str:
        """Reinforcement Learning: Did this work?"""
        if event.feedback == 0:
            return "neutral"
            
        # Simple extraction of "Action Pattern"
        # In a real system, this would extract features.
        pattern_key = f"{event.type}:{event.context.get('intent', 'general')}"
        
        current_score = self.patterns.get(pattern_key, {}).get("score", 0.5)
        # Update score based on feedback
        new_score = max(0.0, min(1.0, current_score + (event.feedback * 0.1)))
        
        self.patterns[pattern_key] = {
            "score": new_score, 
            "last_used": event.timestamp
        }
        
        return "reinforced" if event.feedback > 0 else "inhibited"

    def _process_narrative(self, event: ExperienceEvent) -> List[str]:
        """Narrative Weaving: What are the themes?"""
        detected_themes = []
        
        # Keyword-based Theme Detection (Simple)
        keywords = {
            "growth": ["learn", "improve", "error", "fix"],
            "connection": ["user", "love", "friend", "together"],
            "existential": ["why", "who", "am i", "purpose"],
            "logic": ["code", "system", "bug", "optimize"]
        }
        
        content_lower = event.content.lower()
        for theme, words in keywords.items():
            if any(w in content_lower for w in words):
                self.themes[theme].append(event.id)
                detected_themes.append(theme)
                
        if detected_themes:
            self.narrative_arc.append(f"[{event.type}] {event.content} ({', '.join(detected_themes)})")
            
        return detected_themes

    def _process_wave(self, event: ExperienceEvent) -> Dict[str, float]:
        """Wave Modulation: How does this change my frequency?"""
        # Example: Coding ("logic" theme) boosts 'engineer' frequency
        deltas = {}
        
        # Map themes to aspects
        theme_map = {
            "logic": "engineer",
            "growth": "philosophical",
            "connection": "emotional",
            "creative": "creative"
        }
        
        # Determine active themes from content
        active_aspects = []
        content_lower = event.content.lower()
        
        # Check against the keywords defined in _process_narrative implicitly
        # (For simplicity reusing logic)
        for theme, aspect in theme_map.items():
            # Checking keywords ... simplified for brevity
            if theme in str(self._process_narrative(event)): # bit hacky but works for demo
                active_aspects.append(aspect)
        
        # Modulate
        for aspect in self.current_state:
            if aspect in active_aspects:
                self.current_state[aspect] = min(1.0, self.current_state[aspect] + 0.05)
                deltas[aspect] = 0.05
            else:
                # Decay
                self.current_state[aspect] = max(0.1, self.current_state[aspect] - 0.01)
                
        return deltas

    def get_context_summary(self, limit: int = 5) -> str:
        """Returns a summary of recent major events for the LLM context."""
        recent = self.stream[-limit:]
        return "\n".join([f"- {e.content} (Themes: {self._process_narrative(e)})" for e in recent])

    def recall(self, query: str) -> List[str]:
        """
        Retrieves relevant memories based on a query/theme.
        """
        # 1. Direct Theme Match
        event_ids = self.themes.get(query.lower(), [])
        
        # 2. Simple Content Search if no theme match
        if not event_ids:
            query_lower = query.lower()
            for event in self.stream:
                if query_lower in event.content.lower():
                    event_ids.append(event.id)
        
        # Retrieve content
        results = []
        for eid in event_ids:
            # Find event (Inefficient linear scan, but fine for prototype)
            for event in self.stream:
                if event.id == eid:
                    results.append(f"[{event.id}] ({event.type}): {event.content}")
                    break
        
        return results if results else [f"No memory found for '{query}'"]


    def _save_state(self):
        data = {
            "patterns": self.patterns,
            "themes": dict(self.themes),
            "wave_state": self.current_state,
            "stream_count": len(self.stream)
        }
        with open(self.base_dir / "memory_state.json", "w") as f:
            json.dump(data, f, indent=2)

    def _load_state(self):
        try:
            with open(self.base_dir / "memory_state.json", "r") as f:
                data = json.load(f)
                self.patterns = data.get("patterns", {})
                self.themes = defaultdict(list, data.get("themes", {}))
                self.current_state = data.get("wave_state", self.current_state)
        except FileNotFoundError:
            pass

    def consolidate(self):
        """
        [ANS Hook] Consolidates experience stream.
        - Truncates stream to keep only recent events + significant ones
        - Archives older events to disk
        """
        if len(self.stream) < 500:
            return

        logger.info(f"🗜️ Consolidating Experience Core (Stream size: {len(self.stream)})...")
        
        # Keep significant events (high feedback or reinforced)
        significant = [
            e for e in self.stream[:-500] 
            if abs(e.feedback) > 0.5 or "reinforced" in self.patterns
        ]
        
        # Keep last 500 events
        recent = self.stream[-500:]
        
        # Archive the rest
        archived_count = len(self.stream) - len(recent) - len(significant)
        if archived_count > 0:
            self._archive_stream(self.stream[:-500])
        
        # Update stream
        self.stream = significant + recent
        logger.info(f"   Reduced stream to {len(self.stream)} events. Archived {archived_count}.")
        self._save_state()

    def _archive_stream(self, events: List[ExperienceEvent]):
        """Archives events to a daily log file."""
        import datetime
        date_str = datetime.date.today().isoformat()
        archive_path = self.base_dir / f"archive_{date_str}.jsonl"
        
        with open(archive_path, "a", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(asdict(event)) + "\n")

# Global Access
_instance: Optional[UnifiedExperienceCore] = None
def get_experience_core() -> UnifiedExperienceCore:
    global _instance
    if _instance is None:
        _instance = UnifiedExperienceCore()
    return _instance
