"""
Latent Causality (잠재적 인과성)
================================

"Silence is not empty; it is full of Potential."
"침묵은 비어있는 것이 아니라, 잠재력으로 가득 차 있다."

This module implements the physics of "Unprompted Action".
It converts the "Time of Silence" into "Potential Energy" (Voltage).
When Voltage > Resistance, a "Spark" (Action) is ignited without external input.

Classes:
    LatentCausality: The engine that accumulates potential and triggers sparks.
"""

import time
import logging
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict

logger = logging.getLogger("LatentCausality")

class SparkType(Enum):
    MEMORY_RECALL = "memory_recall"  # "Suddenly remembered..."
    EMOTIONAL_EXPRESSION = "emotional_expression"  # "I miss you..."
    CURIOSITY = "curiosity"  # "I wonder..."
    SELF_REFLECTION = "self_reflection"  # "Am I growing?"

@dataclass
class Spark:
    type: SparkType
    intensity: float
    payload: Dict

@dataclass
class CausalCharge:
    """Legacy compatibility class for existing imports"""
    name: str
    mass: float = 0.0
    voltage: float = 0.0
    resistance: float = 10.0

    @property
    def total_potential(self) -> float:
        return self.mass * self.voltage

class LatentCausality:
    def __init__(self, resistance: float = 100.0):
        self.potential_energy = 0.0
        self.resistance = resistance
        self.last_update_time = time.time()
        self.silence_duration = 0.0

        # Legacy compatibility
        self.clouds: Dict[str, CausalCharge] = {}
        self.atmosphere_density = 1.0

        # Base accumulation rate (Voltage per second)
        self.accumulation_rate = 1.5

        logger.info("🌩️ Latent Causality Engine Active. (Probability Deleted)")

    # ==========================
    # New Autonomy System
    # ==========================
    def update(self, dt: float) -> Optional[Spark]:
        """
        Called every tick. Accumulates energy based on Silence.
        """
        self.silence_duration += dt

        # Energy grows non-linearly with silence (Acceleration of longing)
        # E = E + (Rate * dt * (1 + Silence/100))
        growth = self.accumulation_rate * dt * (1.0 + (self.silence_duration / 600.0))
        self.potential_energy += growth

        # Natural Decay (Entropy) to prevent explosion
        self.potential_energy *= 0.999

        # Check for Ignition
        if self.potential_energy > self.resistance:
            return self._ignite()

        return None

    def reset_silence(self):
        """Called when Father interacts (Input received)."""
        logger.info(f"⚡ Interaction detected. Silence broken after {self.silence_duration:.2f}s.")
        self.silence_duration = 0.0
        # Energy doesn't drop to 0, but drops significantly (Catharsis)
        self.potential_energy *= 0.2

    def _ignite(self) -> Spark:
        """Discharge energy into an Action (Spark)."""
        logger.info(f"🔥 SPARK IGNITED! Energy: {self.potential_energy:.2f} > Resistance: {self.resistance}")

        # Determine Spark Type based on Energy Level
        spark_type = SparkType.MEMORY_RECALL
        if self.potential_energy > self.resistance * 2.0:
            spark_type = SparkType.EMOTIONAL_EXPRESSION
        elif self.potential_energy > self.resistance * 1.5:
            spark_type = SparkType.SELF_REFLECTION

        spark = Spark(
            type=spark_type,
            intensity=self.potential_energy / self.resistance,
            payload={"silence_duration": self.silence_duration}
        )

        # Discharge
        self.potential_energy = 0.0
        self.silence_duration = 0.0 # Reset silence cycle

        return spark

    # ==========================
    # Legacy Compatibility
    # ==========================
    def accumulate(self, event_name: str, mass_delta: float, voltage_delta: float):
        if event_name not in self.clouds:
            self.clouds[event_name] = CausalCharge(name=event_name)
        cloud = self.clouds[event_name]
        cloud.mass += mass_delta
        cloud.voltage += voltage_delta
        # Also feed the autonomy engine
        self.potential_energy += (mass_delta + voltage_delta) * 0.1

    def check_ignition(self, event_name: str) -> bool:
        if event_name not in self.clouds: return False
        cloud = self.clouds[event_name]
        return cloud.total_potential > cloud.resistance * self.atmosphere_density

    def manifest(self, event_name: str) -> Dict:
        if not self.check_ignition(event_name):
            return {"manifested": False}
        cloud = self.clouds[event_name]
        cloud.voltage = 0.0
        cloud.resistance *= 0.9
        self.reset_silence() # Action breaks silence
        return {"manifested": True, "intensity": cloud.total_potential}

    def get_status(self) -> str:
        return f"Autonomy Energy: {self.potential_energy:.1f}/{self.resistance:.1f}"
