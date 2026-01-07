from typing import Any, Dict, List, Optional
from typing import Any, Dict, List, Optional
import json
from pathlib import Path

from intent_engine import IntentBundle
from core_memory import CoreMemory


class UtteranceComposer:
    """
    Generative Utterance Composer
    -----------------------------
    Uses the Gemini API to generate responses, enriched by "Voice Patterns"
    retrieved from CoreMemory. This allows the agent's style to evolve
    based on what it has learned.
    """

    def __init__(self, core_memory: CoreMemory) -> None:
        self.core_memory = core_memory

    def compose(self, intent: IntentBundle, base_text: str = "") -> str:
        """
        Generates a response based on the intent and learned voice patterns.
        If base_text is provided, it treats it as a draft to improve.
        """
        # 1. Retrieve Learned Styles
        patterns = self.core_memory.get_voice_patterns()
        
        # Select relevant patterns (for now, just take the most recent 3)
        # In a real system, we'd use vector similarity to find relevant styles.
        recent_patterns = [p["pattern"] for p in patterns[-3:]]
        
        style_instruction = ""
        if recent_patterns:
            style_instruction = "Apply these rhetorical styles:\n" + "\n".join([f"- {p}" for p in recent_patterns])
        else:
            style_instruction = "Speak in a clear, empathetic, and philosophical manner."

        # 2. Construct Prompt
        prompt = f"""You are Elysia.
        
        Current Intent:
        - Target: {intent.target}
        - Emotion: {intent.emotion}
        - Goal: {intent.intent_type}
        - Relationship: {intent.relationship}
        
        {style_instruction}
        
        Draft Content (Optional): "{base_text}"
        
        Generate the final response.
        """
        
        # 3. Generate
        try:
            from gemini_api import generate_text
            response = generate_text(prompt).strip()
            # Clean up quotes
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1]
            return response
        except Exception as e:
            # Fallback
            return base_text or "I am listening."
