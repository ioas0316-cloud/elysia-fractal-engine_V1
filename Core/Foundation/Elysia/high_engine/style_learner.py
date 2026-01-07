"""
StyleLearner
------------
Analyzes high-quality dialogue examples to extract "Voice Patterns" (rhetorical styles)
and stores them in CoreMemory. This allows Elysia to "learn" how to speak
by observing good examples (or her own successful moments).
"""

import logging
import json
from typing import Optional, Dict, Any
from Project_Elysia.core_memory import CoreMemory
from Core.Foundation.gemini_api import generate_text

class StyleLearner:
    def __init__(self, core_memory: CoreMemory):
        self.core_memory = core_memory
        self.logger = logging.getLogger("StyleLearner")

    def learn_from_example(self, text: str, context_tag: str = "general"):
        """
        Analyzes the text for rhetorical devices and stores them as a pattern.
        """
        self.logger.info(f"Analyzing style of: '{text[:50]}...'")
        
        prompt = f"""Analyze the rhetorical style of the following text.
        Identify the specific "voice pattern" or "instruction" that would generate this kind of text.
        
        Text: "{text}"
        
        Examples of patterns:
        - "Use nature metaphors to describe emotions."
        - "Speak in short, punchy sentences with high contrast."
        - "Ask rhetorical questions to provoke thought."
        - "Use scientific analogies for spiritual concepts."
        
        Return ONLY the pattern description (1 sentence).
        """
        
        try:
            pattern = generate_text(prompt).strip()
            # Clean up quotes if present
            pattern = pattern.strip('"').strip("'")
            
            self.core_memory.add_voice_pattern(pattern, context_tag)
            return pattern
        except Exception as e:
            self.logger.error(f"Failed to learn style: {e}")
            return None
