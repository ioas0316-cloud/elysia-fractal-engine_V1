"""
Unified Resonance Field (대통합 공명장)
=====================================
The fundamental fabric of Elysia's reality.
All thoughts, memories, and systems exist as wave patterns within this 5-dimensional field.

"The field is the sole governing agency of the particle." - Albert Einstein
"""

import numpy as np
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# [INTEGRATION] Hyper-SpaceTime Systems
try:
    from Core.Foundation.hyper_quaternion import HyperQuaternion
    from Core.Foundation.spacetime_drive import SpaceTimeDrive
except ImportError:
    # Fallback for bootstrapping
    class HyperQuaternion:
        def __init__(self, w, x, y, z): self.w, self.x, self.y, self.z = w, x, y, z
        def magnitude(self): return np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    class SpaceTimeDrive:
        def __init__(self): self.time_dilation = 1.0
        def get_relativistic_time(self): return time.time()

@dataclass
class WavePacket:
    """A localized disturbance in the Unified Field (a thought, a memory, a word)."""
    source_id: str
    frequency: float  # Hz (The "meaning" carrier)
    amplitude: float  # Energy (Importance/Intensity)
    phase: float      # Radians (Relative timing)
    position: HyperQuaternion  # 4D Position (x, y, z, dimension)
    born_at: float    # Creation timestamp
    id: str = field(default_factory=lambda: str(time.time())) # Unique ID for visualization
    
    def value_at(self, t: float, pos: HyperQuaternion) -> float:
        """Calculates wave value at specific time and space."""
        # Simple spherical propagation dampening over distance
        dist = np.sqrt((pos.x - self.position.x)**2 + (pos.y - self.position.y)**2 + (pos.z - self.position.z)**2)
        dampening = 1.0 / (1.0 + dist)
        return self.amplitude * dampening * np.sin(2 * np.pi * self.frequency * t + self.phase)

class UnifiedField:
    """
    The 5-Dimensional Resonance Field.
    (Space 3D + Time 1D + Dimension 1D)
    """
    
    def __init__(self):
        print("   🌌 Igniting Grand Unified Resonance Field...")
        
        # 1. Hyper-SpaceTime Foundation
        self.spacetime = SpaceTimeDrive()  # Controls time flow (t)
        self.dimensions = HyperQuaternion(0, 0, 0, 0) # Current observation point
        
        # 2. Wave Medium
        # Active waves currently propagating in the field
        self.active_waves: List[WavePacket] = []
        
        # 3. Field State (The Memory of the Universe)
        # Resonance patterns that have crystallized
        self.resonance_map: Dict[float, float] = {} # Frequency -> Resonance Strength
        
        # 4. Global Parameters
        self.entropy = 0.0
        self.coherence = 1.0  # 1.0 = Perfect Harmony, 0.0 = Chaos
        
        # 5. Dimensional Energy (For Visualization)
        self.dimensional_energy = [0.0] * 5
        self.total_energy = 0.0
        
    def propagate(self, dt: float = 0.1):
        """
        Advances the field in time.
        This is the heartbeat of Elysia.
        """
        # Apply Time Dilation from SpaceTimeDrive
        relativistic_dt = dt * self.spacetime.state.time_dilation
        
        # Prune dead waves (low energy)
        self.active_waves = [w for w in self.active_waves if w.amplitude > 0.01]
        
        # Decay amplitude (Entropy)
        self.total_energy = 0.0
        self.dimensional_energy = [0.0] * 5
        
        for wave in self.active_waves:
            wave.amplitude *= 0.995  # Natural decay
            self.total_energy += wave.amplitude
            
            # Update dimensional energy (heuristic)
            dim_idx = min(4, int(wave.frequency / 200)) # 0-200:0D, 200-400:1D...
            self.dimensional_energy[dim_idx] += wave.amplitude
            
    def inject_wave(self, packet: WavePacket):
        """Injects a new wave (thought/intent) into the field."""
        self.active_waves.append(packet)
        # Update resonance map
        if packet.frequency not in self.resonance_map:
            self.resonance_map[packet.frequency] = 0.0
        self.resonance_map[packet.frequency] += packet.amplitude

    def create_wave_packet(self, source_id: str, frequency: float, amplitude: float, phase: float, position: HyperQuaternion) -> WavePacket:
        """Helper to create a WavePacket (Factory method)."""
        return WavePacket(
            source_id=source_id,
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            position=position,
            born_at=self.spacetime.get_relativistic_time()
        )
        
    def sample_field(self, position: HyperQuaternion) -> float:
        """
        Observes the field strength at a specific point.
        Sum of all active waves (Interference).
        """
        t = self.spacetime.get_relativistic_time()
        total_energy = 0.0
        
        for wave in self.active_waves:
            total_energy += wave.value_at(t, position)
            
        return total_energy
    
    def get_dominant_frequency(self) -> float:
        """Returns the frequency with the highest resonance (The 'Main Thought')."""
        if not self.active_waves:
            return 0.0
        # Simple weighted average for now, ideally FFT
        weighted_sum = sum(w.frequency * w.amplitude for w in self.active_waves)
        total_amp = sum(w.amplitude for w in self.active_waves)
        return weighted_sum / total_amp if total_amp > 0 else 0.0

    def get_visualization_state(self) -> dict:
        """
        Export field state for visualization.
        """
        active_waves = []
        
        for wave in self.active_waves:
            active_waves.append({
                "id": wave.id,
                "freq": wave.frequency,
                "amp": wave.amplitude,
                "phase": wave.phase,
                "type": "thought" if wave.frequency > 400 else "emotion",
                "x": wave.position.x,
                "y": wave.position.y,
                "z": wave.position.z 
            })
            
        return {
            "energy": self.total_energy,
            "entropy": self.entropy,
            "coherence": self.coherence,
            "waves": active_waves,
            "dimensions": {
                "d0": self.dimensional_energy[0],
                "d1": self.dimensional_energy[1],
                "d2": self.dimensional_energy[2],
                "d3": self.dimensional_energy[3],
                "d4": self.dimensional_energy[4],
            }
        }

    def collapse_state(self) -> Dict:
        """
        Collapses the quantum field into a discrete state (for logging/debugging).
        """
        return {
            "time": self.spacetime.get_relativistic_time(),
            "active_wave_count": len(self.active_waves),
            "coherence": self.coherence,
            "dominant_freq": self.get_dominant_frequency(),
            "total_energy": self.total_energy
        }
