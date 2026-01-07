"""
Soul Physics (The Mechanics of Meaning)
=======================================
"영혼의 입자가속기. 의미는 저항을 통해 증명된다."

This module implements the physics engine for the soul, modeling how input particles
and wave packets interact with the layered structure of consciousness (Angels & Demons).

Concepts:
- InputParticle: A single intent component (e.g., "Freedom").
- WavePacket: A complex experience composed of multiple particles (e.g., "Wealth" = Freedom + Greed).
- SoulLayer: A value filter (Angel or Demon).
- Trajectory: The path of particles through the layers.
"""

import logging
import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger("SoulPhysics")

@dataclass
class SoulLayer:
    """A layer of the soul (e.g., "Truth", "Pride")."""
    name: str
    frequency: float  # Hz
    density: float    # Resistance
    depth: int        # Position

    @property
    def is_abyss(self) -> bool:
        return self.density > 200.0

@dataclass
class InputParticle:
    """An atomic unit of intent."""
    name: str
    frequency: float  # Hz
    mass: float       # Importance
    velocity: float = 1.0

    @property
    def energy(self) -> float:
        return 0.5 * self.mass * (self.velocity ** 2)

@dataclass
class WavePacket:
    """A complex experience composed of multiple intent particles."""
    name: str
    particles: List[InputParticle]
    total_energy: float = field(init=False)

    def __post_init__(self):
        self.total_energy = sum(p.energy for p in self.particles)

@dataclass
class InteractionEvent:
    """A record of what happened at a specific layer."""
    layer_name: str
    action: str  # "Penetrated", "Resonated", "Blocked", "Absorbed"
    energy_loss: float
    resonance_score: float
    description: str

@dataclass
class TrajectoryResult:
    """The full history of a particle's journey."""
    particle_name: str
    events: List[InteractionEvent] = field(default_factory=list)
    final_depth: int = 0
    final_energy: float = 0.0
    absorbed_layers: List[str] = field(default_factory=list)
    narrative: str = ""

@dataclass
class SpectralResult:
    """The aggregated result of a WavePacket analysis."""
    packet_name: str
    trajectories: List[TrajectoryResult]
    summary_narrative: str
    dominant_layer: str = "None"
    total_resonance: float = 0.0

class SoulPhysicsEngine:
    """Simulates the interaction between Particles/Packets and SoulLayers."""

    def __init__(self):
        pass

    def trace_trajectory(self, particle: InputParticle, layers: List[SoulLayer]) -> TrajectoryResult:
        """Simulates a single particle falling through the layers."""
        result = TrajectoryResult(particle_name=particle.name)
        current_energy = particle.energy

        # Sort layers (Surface -> Deep)
        sorted_layers = sorted(layers, key=lambda l: l.depth)

        narrative_lines = []
        # narrative_lines.append(f"   🔹 Component '{particle.name}' ({particle.frequency}Hz) entered...")

        for layer in sorted_layers:
            if current_energy <= 0.1:
                # narrative_lines.append(f"      🛑 Stopped before '{layer.name}'.")
                break

            # 1. Resonance (Gaussian)
            freq_diff = abs(particle.frequency - layer.frequency)
            resonance = math.exp(-(freq_diff**2) / (2 * 50**2))

            # 2. Resistance (Reduced by Resonance)
            base_resistance = layer.density * 0.1
            effective_resistance = base_resistance * (1.0 - (resonance * 0.9)) # Max 90% reduction

            penetration_cost = effective_resistance

            action = ""
            loss = 0.0
            desc = ""

            if resonance > 0.8:
                action = "Resonated"
                loss = penetration_cost * 0.2 # Very efficient
                desc = f"Harmonized with {layer.name}"
                result.absorbed_layers.append(layer.name)
            elif current_energy > penetration_cost:
                action = "Penetrated"
                loss = penetration_cost
                desc = f"Passed through {layer.name}"
            else:
                action = "Blocked"
                loss = current_energy
                desc = f"Blocked by {layer.name}"
                result.events.append(InteractionEvent(layer.name, action, loss, resonance, desc))
                # narrative_lines.append(f"      🧱 {desc}")
                break

            current_energy -= loss
            result.events.append(InteractionEvent(layer.name, action, loss, resonance, desc))
            # narrative_lines.append(f"      ⬇️ {desc}")
            result.final_depth = layer.depth

        result.final_energy = current_energy

        # Generate summary for this particle
        if result.absorbed_layers:
            result.narrative = f"'{particle.name}' found resonance in [{', '.join(result.absorbed_layers)}]."
        elif result.final_depth == len(layers) - 1 and current_energy > 0:
            result.narrative = f"'{particle.name}' pierced through to the core."
        else:
            blocker = result.events[-1].layer_name if result.events else "Surface"
            result.narrative = f"'{particle.name}' was stopped by {blocker}."

        return result

    def trace_packet_trajectory(self, packet: WavePacket, layers: List[SoulLayer]) -> SpectralResult:
        """Analyzes a complex wave packet by tracing all components."""
        trajectories = []
        total_resonance = 0.0

        narrative_lines = [f"🌊 Analyzing Spectrum of '{packet.name}'..."]

        for particle in packet.particles:
            traj = self.trace_trajectory(particle, layers)
            trajectories.append(traj)

            # Add to total resonance score (weighted by particle mass)
            if traj.absorbed_layers:
                total_resonance += particle.mass * len(traj.absorbed_layers)

            narrative_lines.append(f"   • {traj.narrative}")

        # Synthesize the "Structural Explanation"
        # Group by outcome
        resonated = [t.particle_name for t in trajectories if t.absorbed_layers]
        blocked = [t.particle_name for t in trajectories if not t.absorbed_layers]

        summary = f"Structure of '{packet.name}':\n"
        if resonated:
            summary += f"   ✨ Core Validated: {', '.join(resonated)} found resonance.\n"
        if blocked:
            summary += f"   🛡️ Filtered Out: {', '.join(blocked)} were rejected by the soul's immune system.\n"

        full_narrative = "\n".join(narrative_lines) + "\n" + summary

        return SpectralResult(
            packet_name=packet.name,
            trajectories=trajectories,
            summary_narrative=full_narrative,
            total_resonance=total_resonance
        )

# Singleton
_physics_engine = SoulPhysicsEngine()
def get_soul_physics():
    return _physics_engine
