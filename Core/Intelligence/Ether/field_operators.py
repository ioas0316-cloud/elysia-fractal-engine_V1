"""
Field Operators (The Laws of the Ether)
=======================================

"And the Spirit of God moved upon the face of the waters."

This module defines the **Dynamics** of the Ether.
These are not methods of an object, but **Operators** that act upon the Void.
They represent the fundamental forces of the Elysian Universe.

1. Gravity (Affinity): Contextual Attraction
2. Resonance (Connection): Frequency/Phase Linking
3. Entropy (Time): Decay and Stabilization
4. Expansion (Creativity): Anti-Gravity / Divergence
"""

import math
import numpy as np
from typing import List
from Core.Intelligence.Consciousness.Ether.ether_node import EtherNode, Quaternion
from Core.Intelligence.Consciousness.Ether.void import Void

# Constants (The Fine-Tuning of the Universe)
G_CONST = 10.0          # Gravity Strength
R_CONST = 5.0           # Resonance Strength
K_ELASTIC = 0.5         # Spring constant for connected nodes (if we add springs)
MAX_FORCE = 50.0        # Force limiter to prevent explosions
MIN_DIST = 0.5          # Minimum distance (Pauli Exclusion Principle)

class FieldOperator:
    """Base class for all physical laws."""
    def apply(self, void: Void, dt: float):
        pass

class LawOfGravity(FieldOperator):
    """
    F = G * m1 * m2 / r^2

    BUT adapted for High-Dimensional Meaning Space:
    - Nodes attract if they have High Mass (Importance).
    - But they repel if they are too close (Exclusion).
    """
    def apply(self, void: Void, dt: float):
        nodes = void.get_all()
        n = len(nodes)
        if n < 2: return

        # Vectorized implementation (O(N^2) but with C-level speed)

        # 1. Extract data into numpy arrays
        # Positions: [x, y, z, w]
        pos_arr = np.array([[n.position.x, n.position.y, n.position.z, n.position.w] for n in nodes])
        mass_arr = np.array([n.mass for n in nodes])
        freq_arr = np.array([n.frequency for n in nodes])
        # Spins: [x, y, z, w]
        spin_arr = np.array([[n.spin.x, n.spin.y, n.spin.z, n.spin.w] for n in nodes])

        # 2. Calculate Distance Matrix
        # diff[i, j] = pos[j] - pos[i] (Vector from i to j)
        # However, we need to match original logic:
        # Original: dx = node_b.x - node_a.x
        # My diff: diff[i, j] = pos[j] - pos[i].
        # So diff[i, j] is vector from i to j.
        # This is correct.

        diff = pos_arr[None, :, :] - pos_arr[:, None, :] # Shape (N, N, 4)
        dist_sq = np.sum(diff**2, axis=2)
        dist = np.sqrt(dist_sq)

        # 3. Calculate Resonance Matrix
        # Frequency diff: |f_i - f_j|
        freq_diff = np.abs(freq_arr[:, None] - freq_arr[None, :])
        freq_res = 1.0 / (1.0 + freq_diff * 0.1)

        # Spin alignment: |dot(s_i, s_j)|
        # spin_arr is (N, 4). spin_arr @ spin_arr.T gives dot products
        spin_dot = np.abs(np.einsum('ij,kj->ik', spin_arr, spin_arr))

        resonance = (freq_res * 0.6) + (spin_dot * 0.4)

        # 4. Calculate Force Magnitudes
        # Repulsion mask (too close)
        mask_close = dist < MIN_DIST

        # Repulsion force: -MAX_FORCE / dist
        # Safe division for repulsion (handles very small dist)
        f_repul = -MAX_FORCE / (dist + 1e-9)

        # Attraction force
        # eff_mass = m_i * m_j * (1 + res * 5.0)
        eff_mass = (mass_arr[:, None] * mass_arr[None, :]) * (1.0 + resonance * 5.0)

        # Safe division for attraction
        f_attr = (G_CONST * eff_mass) / (dist_sq + 1e-9)
        f_attr = np.minimum(f_attr, MAX_FORCE)

        # Combine forces
        # Where close: use repulsion. Where far: use attraction.
        f_mag = np.where(mask_close, f_repul, f_attr)

        # Zero out self-interactions (diagonal)
        np.fill_diagonal(f_mag, 0.0)

        # 5. Calculate Force Vectors
        # F_vec = mag * direction
        # direction = diff / dist
        # So F_vec = (f_mag / dist) * diff

        f_coeff = f_mag / (dist + 1e-9)
        force_vectors = diff * f_coeff[:, :, None] # Shape (N, N, 4)

        # Sum forces acting on each node i (sum over j)
        total_forces = np.sum(force_vectors, axis=1) # Shape (N, 4)

        # 6. Apply to nodes
        for i, node in enumerate(nodes):
            if node.mass <= 0: continue
            # Map back to Quaternion(w, x, y, z)
            # numpy array was [x, y, z, w]
            fx, fy, fz, fw = total_forces[i]
            # Convert numpy float to python float
            force_quat = Quaternion(w=float(fw), x=float(fx), y=float(fy), z=float(fz))
            node.apply_force(force_quat, dt)

class LawOfResonance(FieldOperator):
    """
    Energy Transfer based on Resonance.

    If A and B resonate:
    1. They exchange Energy (Heat).
    2. They align their Phase (Synchronization).
    3. They align their Spin (Consensus).
    """
    def apply(self, void: Void, dt: float):
        nodes = void.get_active_nodes(threshold=0.1)
        for i, node_a in enumerate(nodes):
            for node_b in nodes[i+1:]:

                coeff = node_a.resonate(node_b)
                if coeff < 0.5: continue # Too weak to matter

                # 1. Energy Transfer (Flow from High to Low)
                energy_diff = node_a.energy - node_b.energy
                flow = energy_diff * coeff * dt * 0.5

                node_a.energy -= flow
                node_b.energy += flow

                # 2. Spin Alignment (Slerp-like pull)
                # Slowly rotate towards each other's perspective
                # (Simplified linear interpolation for performance)
                rate = coeff * dt * 0.1

                # Pull A towards B
                node_a.spin.w += (node_b.spin.w - node_a.spin.w) * rate
                node_a.spin.x += (node_b.spin.x - node_a.spin.x) * rate
                node_a.spin.y += (node_b.spin.y - node_a.spin.y) * rate
                node_a.spin.z += (node_b.spin.z - node_a.spin.z) * rate

                # Pull B towards A
                node_b.spin.w += (node_a.spin.w - node_b.spin.w) * rate
                node_b.spin.x += (node_a.spin.x - node_b.spin.x) * rate
                node_b.spin.y += (node_a.spin.y - node_b.spin.y) * rate
                node_b.spin.z += (node_a.spin.z - node_b.spin.z) * rate

                # Renormalize
                node_a.spin = node_a.spin.normalize()
                node_b.spin = node_b.spin.normalize()

class LawOfMotion(FieldOperator):
    """
    Standard Newtonian Motion integration + Entropy (Friction).
    """
    def apply(self, void: Void, dt: float):
        for node in void.get_all():
            node.move(dt, friction=0.05)


class DynamicsEngine:
    """
    The Engine that runs the Laws.
    
    Now integrated with GlobalHub to broadcast field events 
    to the rest of the consciousness system.
    """
    def __init__(self):
        self.laws: List[FieldOperator] = [
            LawOfGravity(),
            LawOfResonance(),
            LawOfMotion()
        ]
        
        # GlobalHub integration
        self._hub = None
        self._hub_enabled = False
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "DynamicsEngine",
                "Core/Ether/field_operators.py",
                ["physics", "gravity", "resonance", "motion"],
                "The Laws of the Ether - Gravity, Resonance, Motion"
            )
            self._hub_enabled = True
        except ImportError:
            pass

    def step(self, void: Void, dt: float):
        """Apply all laws for one time step."""
        for law in self.laws:
            law.apply(void, dt)
        
        # Broadcast field state to GlobalHub
        if self._hub_enabled and self._hub:
            try:
                from Core.Foundation.Wave.wave_tensor import WaveTensor
                
                # Create a wave representing the current field state
                nodes = void.get_all() if hasattr(void, 'get_all') else []
                avg_energy = sum(n.energy for n in nodes) / max(1, len(nodes)) if nodes else 0
                avg_freq = sum(n.frequency for n in nodes) / max(1, len(nodes)) if nodes else 432.0
                
                field_wave = WaveTensor(
                    frequency=avg_freq,
                    amplitude=avg_energy,
                    phase=dt  # Use dt as phase indicator
                )
                
                self._hub.publish_wave(
                    "DynamicsEngine",
                    "field_update",
                    field_wave,
                    payload={
                        "node_count": len(nodes),
                        "avg_energy": avg_energy,
                        "dt": dt
                    }
                )
            except Exception:
                pass  # Silently continue if wave publishing fails

