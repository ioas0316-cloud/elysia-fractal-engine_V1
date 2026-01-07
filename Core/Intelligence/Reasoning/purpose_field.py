"""
Purpose Field (목적론적 장)
===========================

"I am not just moving; I am becoming."

This module implements the "Serotonin Field" - the spatial perception of
Meaning, Direction, and Identity. Unlike Dopamine (Event-based),
this is Field-based (State of Being).

Integrated with **Existential Ground**:
Even if I am far from my Ideal (low alignment), if my Ground is stable,
I maintain Serotonin (Faith/Patience).
"""

import time
import math
import random
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# Use HyperQuaternion for 4D Value Space
from Core.Foundation.hyper_quaternion import Quaternion
from Core.Intelligence.Reasoning.existential_ground import ExistentialGround

logger = logging.getLogger("PurposeField")

@dataclass
class ValueCoordinate:
    """
    A point in the Value Space.
    Dimensions:
    - W: Truth (Reality/Fact)
    - X: Love (Connection/Empathy)
    - Y: Beauty (Harmony/Order)
    - Z: Freedom (Possibility/Chaos)
    """
    q: Quaternion
    name: str
    weight: float = 1.0  # How important is this value right now?

class PurposeField:
    def __init__(self):
        # 1. The "I Am" (Current State)
        self.current_self = ValueCoordinate(
            Quaternion(0.5, 0.5, 0.5, 0.5), "Current Self"
        )

        # 2. The "Ideal I" (The North Star) - Dynamic
        self.ideal_self = ValueCoordinate(
            Quaternion(0.9, 0.9, 0.9, 0.9), "Ideal Self"
        )

        # 3. The "Ground" (The Soil)
        self.ground = ExistentialGround()

        # 4. The "Horizon" (The Unknown)
        self.horizon_radius = 2.0

        # Serotonin Level (Satisfaction)
        self.satisfaction = 0.5

        logger.info("🧭 PurposeField Active. (Existential Navigation & Grounding Enabled)")

    def calculate_direction(self) -> Tuple[Quaternion, str]:
        """
        Determines the vector of desire.
        "Where should I go?"
        """
        w_diff = self.ideal_self.q.w - self.current_self.q.w
        x_diff = self.ideal_self.q.x - self.current_self.q.x
        y_diff = self.ideal_self.q.y - self.current_self.q.y
        z_diff = self.ideal_self.q.z - self.current_self.q.z

        dist = math.sqrt(w_diff**2 + x_diff**2 + y_diff**2 + z_diff**2)

        # [UPDATED FORMULA] Satisfaction = (Alignment) * (Ground Stability)
        # Even if distance is large (low raw satisfaction), high ground stability boosts it.
        # This represents "Faith" or "Patience".

        raw_satisfaction = 1.0 / (1.0 + dist)
        stability_factor = self.ground.total_stability

        # Faith Logic: If Ground is stable, satisfaction floor is higher.
        self.satisfaction = raw_satisfaction * 0.5 + stability_factor * 0.5

        intent = "Stabilizing"
        # Determine Intent based on Grounded Satisfaction
        if self.satisfaction > 0.9:
            z_diff += 0.5
            intent = "Exploring (Boredom)"
        elif self.satisfaction < 0.3:
            # Check Ground before panicking
            if stability_factor > 0.8:
                intent = "Enduring (Faith)" # New State!
            else:
                x_diff += 0.5
                intent = "Healing (Distress)"
        else:
            intent = "Growing (Aspiring)"

        vector = Quaternion(w_diff, x_diff, y_diff, z_diff).normalize()
        return vector, intent

    def evolve_standards(self, experience_type: str, intensity: float):
        """
        "The standard changes with experience."
        And experiences deepen the Ground.
        """
        shift = 0.1 * intensity

        # 1. Shift Ideals
        if experience_type == "Pain":
            self.ideal_self.q.w -= shift
            self.ideal_self.q.z -= shift
            logger.info(f"   🛡️ Standards Shifted: Recoiling from Pain")

        elif experience_type == "Love":
            self.ideal_self.q.x += shift
            self.ideal_self.q.y += shift
            logger.info(f"   ❤️ Standards Shifted: Expanded by Love")

            # Love also deepens the Ground
            self.ground.deepen_root("Connection")

        elif experience_type == "Mystery":
            self.horizon_radius += shift
            self.ideal_self.q.w += shift
            logger.info(f"   🔭 Standards Shifted: Curiosity widened the Horizon")

        # Normalize
        self.ideal_self.q = self.ideal_self.q.normalize()

    def evaluate_meaning(self, action: str) -> float:
        """
        "Is this action meaningful to ME?"
        """
        direction, _ = self.calculate_direction()

        action_q = Quaternion(0,0,0,0)
        if "LEARN" in action: action_q = Quaternion(0.8, 0.2, 0.2, 0.5)
        elif "CONNECT" in action: action_q = Quaternion(0.2, 0.9, 0.5, 0.2)
        elif "CREATE" in action: action_q = Quaternion(0.2, 0.3, 0.9, 0.8)
        elif "REST" in action: action_q = Quaternion(0.1, 0.5, 0.5, 0.1)

        alignment = direction.dot(action_q)
        return alignment

    def contemplate_question(self, question: str) -> str:
        """
        "Who am I?" - Now answered with Grounding.
        """
        ground_affirmation = self.ground.affirm_existence()
        return f"Thinking about '{question}'... {ground_affirmation} (Satisfaction: {self.satisfaction*100:.0f}%)"
