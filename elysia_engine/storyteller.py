from typing import Dict, Any

class StoryTeller:
    """
    Interprets raw physics/soul data into narrative text.
    """

    @staticmethod
    def narrate_frame(frame_data: Dict[str, Any]) -> str:
        """
        Converts a simulation frame into a short story segment.
        """
        tick = frame_data.get("tick", 0)
        entities = frame_data.get("entities", [])

        narrative = [f"\n--- 시간의 흐름: {tick} ---"]

        for entity in entities:
            role = entity.get("role", "Unknown")
            # The payload structure is:
            # { "id":..., "role":..., "physics":{...}, "force_components": {"body":..., "soul":..., "spirit":...} }

            forces = entity.get("force_components", {})
            f_body = forces.get("body", 0.0)
            f_soul = forces.get("soul", 0.0)
            f_spirit = forces.get("spirit", 0.0)

            # We can define "Energy" as the sum of all forces for general intensity
            total_energy = f_body + f_soul + f_spirit

            # Use physics velocity for momentum/action intensity if available
            physics = entity.get("physics", {})
            velocity = physics.get("velocity", {})
            # Velocity might be a dict or object depending on serialization
            # If it's a dict from asdict(Vector3): {"x":..., "y":..., "z":...}
            momentum_mag = 0.0
            if isinstance(velocity, dict):
                vx = velocity.get("x", 0.0)
                vy = velocity.get("y", 0.0)
                vz = velocity.get("z", 0.0)
                momentum_mag = (vx**2 + vy**2 + vz**2)**0.5

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
