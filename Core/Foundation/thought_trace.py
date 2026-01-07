"""
Thought Trace (Cognitive History)
=================================

"To knwo thyself is to know the path of thy thought."

This module defines the data structures for recording the history of a thought.
It allows Elysia to introspect not just on *what* she thinks, but *how* she thought it.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import time
import logging

@dataclass
class CognitiveEvent:
    """
    A single step in the processing of a thought.
    """
    timestamp: float
    engine: str       # e.g., "WaveEngine", "LogosEngine", "ArcheEngine"
    action: str       # e.g., "Genesis", "Ascension", "Deconstruction"
    detail: str       # Description of what happened
    confidence: float = 1.0

    def __repr__(self):
        return f"[{time.strftime('%H:%M:%S', time.localtime(self.timestamp))}] {self.engine}.{self.action}: {self.detail}"

@dataclass
class ThoughtTrace:
    """
    The complete history of a thought's life.
    """
    events: List[CognitiveEvent] = field(default_factory=list)
    origin_id: str = "Unknown"
    
    def add_event(self, engine: str, action: str, detail: str, confidence: float = 1.0):
        event = CognitiveEvent(
            timestamp=time.time(),
            engine=engine,
            action=action,
            detail=detail,
            confidence=confidence
        )
        self.events.append(event)
        
    def get_narrative(self) -> str:
        """
        Generates a human-readable story of this thought.
        """
        if not self.events:
            return "This thought appeared from the void without history."
            
        narrative = "Cognitive History:\n"
        for i, event in enumerate(self.events):
            narrative += f"  {i+1}. {event.engine} performed '{event.action}': {event.detail}\n"
        return narrative.strip()

# Mixin for Thinking Classes to use
class Tracable:
    def __init__(self):
        self.trace = ThoughtTrace()

    def add_trace(self, engine: str, action: str, detail: str):
        if not hasattr(self, 'trace'):
            self.trace = ThoughtTrace()
        self.trace.add_event(engine, action, detail)
