from typing import Dict, Any, List, Optional
import math
from dataclasses import asdict

from .tensor import SoulTensor
from .entities import Entity

class StoryTeller:
    """
    Interprets raw physics/soul data into narrative text.
    """

    @staticmethod
    def create_intent_soul(text: str) -> SoulTensor:
        """
        Converts text into a SoulTensor (Intent).
        The text defines the Frequency (Color) and Amplitude (Mass) of the intent.
        """
        text = text.lower()

        # Tensor Resonance Map
        # Format: "word": (Frequency, Amplitude, Phase_Offset)
        lexicon = {
            # Red / Combat (100-300 Hz)
            "fight": (150.0, 50.0, 0.0),
            "attack": (180.0, 60.0, 0.0),
            "kill": (250.0, 80.0, 0.0),
            "destroy": (200.0, 90.0, 0.0),
            "power": (120.0, 40.0, 0.0),

            # Green / Peace (20-50 Hz)
            "love": (40.0, 50.0, 0.0),
            "heal": (30.0, 40.0, 0.0),
            "protect": (45.0, 70.0, 0.0),
            "help": (35.0, 30.0, 0.0),
            "peace": (25.0, 20.0, 0.0),

            # Blue / Sorrow / Gravity (< 20 Hz)
            "sad": (10.0, 30.0, 0.0),
            "cry": (15.0, 40.0, 0.0),
            "wait": (5.0, 10.0, 0.0),

            # White/Violet / Magic (> 300 Hz)
            "magic": (400.0, 30.0, math.pi),
            "think": (350.0, 20.0, math.pi / 2),
            "focus": (320.0, 40.0, math.pi / 4),
            "void": (500.0, 100.0, 0.0),
        }

        total_freq = 0.0
        total_amp = 10.0 # Base mass
        total_phase = 0.0
        match_count = 0

        words = text.split()
        for word in words:
            # Simple partial matching
            for key, (freq, amp, phase) in lexicon.items():
                if key in word:
                    total_freq += freq
                    total_amp += amp
                    total_phase += phase
                    match_count += 1
                    break

        if match_count > 0:
            avg_freq = total_freq / match_count
            avg_phase = total_phase / match_count
        else:
            avg_freq = 10.0 # Default to noise
            avg_phase = 0.0

        # Create the SoulTensor
        soul = SoulTensor(
            amplitude=total_amp,
            frequency=avg_freq,
            phase=avg_phase,
            spin=1.0 if avg_freq < 300 else -1.0
        )

        return soul

    @staticmethod
    def create_intent_entity(text: str, entity_id: str = "UserIntent") -> Entity:
        """
        Converts text into a physical Entity with a SoulTensor.
        """
        soul = StoryTeller.create_intent_soul(text)

        # Position defaults to (0,0,0)
        entity = Entity(id=entity_id, soul=soul, role="Intent")
        return entity

    @staticmethod
    def narrate_frame(frame_data: Dict[str, Any]) -> str:
        """
        Converts a simulation frame into a short story segment.
        """
        tick = frame_data.get("tick", 0)
        entities = frame_data.get("entities", [])

        narrative = [f"\n--- 시간의 흐름: {tick} ---"]

        for entity_data in entities:
            # Flexible handling of entity_data (dict or object)
            role = entity_data.get("role", "Unknown") if isinstance(entity_data, dict) else getattr(entity_data, "role", "Unknown")

            # Extract forces if available
            forces = {}
            if isinstance(entity_data, dict):
                forces = entity_data.get("force_components", {})
            elif hasattr(entity_data, "force_components"):
                forces = entity_data.force_components

            f_body = forces.get("body", 0.0)
            f_soul = forces.get("soul", 0.0)
            f_spirit = forces.get("spirit", 0.0)

            total_energy = f_body + f_soul + f_spirit

            desc = StoryTeller._describe_state(role, total_energy, f_body, f_soul, f_spirit)
            narrative.append(f"[{role}] {desc}")

        return "\n".join(narrative)

    @staticmethod
    def to_llm_system_prompt(entity_payload: Dict[str, Any]) -> str:
        """
        Generates a formatted string for LLM System Prompts.
        Input: Entity payload (from export_persona_snapshot)
        Output: Structured state description
        """
        role = entity_payload.get("role", "Entity")
        forces = entity_payload.get("force_components", {})
        f_body = forces.get("body", 0.0)
        f_soul = forces.get("soul", 0.0)
        f_spirit = forces.get("spirit", 0.0)

        # Interpret state for AI
        body_state = "Weak" if f_body < 0.3 else ("Energetic" if f_body > 0.7 else "Stable")
        soul_state = "Detached" if f_soul < 0.3 else ("Connected" if f_soul > 0.7 else "Neutral")
        spirit_state = "Uncertain" if f_spirit < 0.3 else ("Determined" if f_spirit > 0.7 else "Focused")

        prompt = (
            f"[System State Injection]\n"
            f"Role: {role}\n"
            f"Current Condition:\n"
            f"- Body (Physical): {body_state} ({f_body:.2f})\n"
            f"- Soul (Emotional): {soul_state} ({f_soul:.2f})\n"
            f"- Spirit (Will): {spirit_state} ({f_spirit:.2f})\n"
            f"Instruction: Act according to these internal energy levels."
        )
        return prompt

    @staticmethod
    def parse_intent(text: str) -> Dict[str, float]:
        """
        Translates natural language intent into force modifiers.
        Input: User text (e.g. "I want to fight")
        Output: Force modifiers {"body": 0.5, "soul": 0.0, "spirit": 0.0}
        """
        text = text.lower()
        forces = {"body": 0.0, "soul": 0.0, "spirit": 0.0}

        # Body Keywords: Physicality, aggression, movement
        body_keywords = ["fight", "attack", "kill", "destroy", "run", "move", "strength", "power", "muscle", "physical"]
        # Soul Keywords: Emotion, connection, healing, protection
        soul_keywords = ["love", "help", "protect", "heal", "feel", "connect", "bond", "friend", "empathy", "care"]
        # Spirit Keywords: Will, intellect, planning, magic, destiny
        spirit_keywords = ["think", "plan", "wait", "focus", "magic", "will", "destiny", "create", "analyze", "wisdom"]

        for word in body_keywords:
            if word in text:
                forces["body"] += 0.2

        for word in soul_keywords:
            if word in text:
                forces["soul"] += 0.2

        for word in spirit_keywords:
            if word in text:
                forces["spirit"] += 0.2

        # Normalize to max 1.0 per axis (soft cap)
        for key in forces:
            forces[key] = min(forces[key], 1.0)

        return forces

    @staticmethod
    def _describe_state(role: str, energy: float, f_body: float, f_soul: float, f_spirit: float) -> str:
        """
        Generates a sentence based on role and physics state.
        """
        # Determine dominant force
        dominant_val = f_body
        dominant_type = "body"

        if f_soul > dominant_val:
            dominant_val = f_soul
            dominant_type = "soul"
        if f_spirit > dominant_val:
            dominant_val = f_spirit
            dominant_type = "spirit"

        # Action based on role + dominant force
        action = ""

        if role.lower() == "warrior":
            if dominant_type == "body":
                action = "근육이 팽팽해지며 힘이 솟아납니다. (Body↑)"
            elif dominant_type == "soul":
                action = "동료들을 지키겠다는 마음이 불타오릅니다. (Soul↑)"
            else: # Spirit
                action = "전사의 명예를 위해 검을 다잡습니다. (Spirit↑)"

        elif role.lower() == "mage":
            if dominant_type == "body":
                action = "지팡이를 쥔 손에 힘이 들어갑니다. (Body↑)"
            elif dominant_type == "soul":
                action = "대기 중의 마나와 깊은 교감을 나눕니다. (Soul↑)"
            else: # Spirit
                action = "고대의 주문을 읊조리며 집중합니다. (Spirit↑)"

        elif role.lower() == "priest":
            if dominant_type == "body":
                action = "고된 순례길에도 지치지 않는 체력을 보입니다. (Body↑)"
            elif dominant_type == "soul":
                action = "따스한 눈빛으로 상처 입은 이들을 바라봅니다. (Soul↑)"
            else: # Spirit
                action = "신의 목소리에 귀 기울이며 기도합니다. (Spirit↑)"

        else:
            # Generic fallback
            if dominant_type == "body":
                action = f"강한 생명력이 느껴집니다. (Body={f_body:.2f})"
            elif dominant_type == "soul":
                action = f"감정이 풍부해집니다. (Soul={f_soul:.2f})"
            else:
                action = f"깊은 생각에 잠깁니다. (Spirit={f_spirit:.2f})"

        return action
