"""Simulation world for Elysia with multi-field dynamics and social links."""

from __future__ import annotations

import json
import logging
import math
import random
from collections import deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from cell import Cell
from Core.Foundation.Legal_Ethics.Laws.field_laws import evolve_fields
from Core.Foundation.wave_frequency_mapping import (
    WaveFrequencyMapper,
    EmotionType,
    SoundType,
    SCHUMANN_RESONANCE_HZ,
)

# ---- World Laws / Constants (tighter clamping/decay) ----
LAW_MAX_ENERGY = 2e3
LAW_MAX_HP = 1e3
LAW_FIELD_MAX = 5e2
LAW_GLOBAL_DECAY = 0.99   # applies each step to value/will fields
LAW_ENERGY_DECAY = 0.97   # passive decay per step
LAW_REPRO_THRESHOLD = 600.0
LAW_REPRO_COST = 0.55     # parent keeps this fraction, rest goes to child
LAW_MAX_SPEED = 2.0
LAW_MIN_ENERGY_TO_SURVIVE = 5.0
LAW_MAX_AGE = 3000  # ticks
LAW_RESOURCE_REGEN = 1.0
LAW_RESOURCE_CONSUME = 1.0
LAW_GRAVITY_CONST = 0.5
LAW_DENSITY_GROUP_THRESHOLD = 15
LAW_GROUP_BONUS = 0.05
LAW_EVENT_DECAY = 0.9
LAW_SPIRIT_DECAY = 0.995
LAW_BODY_DECAY = 0.993
LAW_SOUL_DECAY = 0.994
LAW_CELESTIAL_ORBIT_RADIUS = 20.0
LAW_SUN_MASS = 4.0
LAW_MOON_MASS = 1.5
LAW_WAVE_PHASE_DECAY = 0.995
LAW_WAVE_PHASE_DIFFUSION = 0.05


class World:
    """
    Grid-based world with scalar/vector fields and agent dynamics.

    Exposed attributes for legacy callers:
    - width, height
    - value_mass_field, will_field, coherence_field
    - intentional_field (H x W x 2)
    - positions, velocities, energy, is_alive_mask, id_to_idx
    - add_cell, add_connection, imprint_spiral_coil_field, apply_will_field,
      run_simulation_step, print_world_summary, harvest_snapshot
    """

    def __init__(
        self,
        width: int = 128,
        height: Optional[int] = None,
        max_cells: int = 2048,
        primordial_dna: Optional[Dict[str, Any]] = None,
        wave_mechanics: Any = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.width = int(width)
        self.height = int(height or width)
        self.max_cells = int(max_cells)
        self.primordial_dna = primordial_dna or {}
        self.wave_mechanics = wave_mechanics
        self.logger = logger or logging.getLogger("World")
        self.logger.addHandler(logging.NullHandler())

        self.tick: int = 0
        self.time_scale: float = 1.0

        self.id_to_idx: Dict[str, int] = {}
        self.idx_to_id: List[Optional[str]] = [None] * self.max_cells

        self.positions = np.zeros((self.max_cells, 3), dtype=np.float32)
        self.velocities = np.zeros_like(self.positions)
        self.energy = np.zeros(self.max_cells, dtype=np.float32)
        self.hp = np.zeros(self.max_cells, dtype=np.float32)
        self.age = np.zeros(self.max_cells, dtype=np.int32)
        self.valence = np.zeros(self.max_cells, dtype=np.float32) + 0.5
        self.arousal = np.zeros(self.max_cells, dtype=np.float32) + 0.5
        self.is_alive_mask = np.zeros(self.max_cells, dtype=bool)
        self.metadata: List[Optional[Dict[str, Any]]] = [None] * self.max_cells
        self.memory_buffers: List[Optional[deque]] = [None] * self.max_cells
        self.mass = np.ones(self.max_cells, dtype=np.float32)  # for gravity-like force
        self.group_ids: List[Optional[int]] = [None] * self.max_cells
        self.group_state: Dict[int, Dict[str, Any]] = {}
        self.group_counter: int = 0
        self.policy_gain = np.ones(self.max_cells, dtype=np.float32)
        self.rewards = np.zeros(self.max_cells, dtype=np.float32)
        self.replay_buffer: deque = deque(maxlen=5000)
        self.causal_log: List[Dict[str, Any]] = []
        self.global_policy_gain: float = 1.0
        self.last_mean_reward: float = 0.0
        self.current_intervention: Optional[str] = None

        self.value_mass_field = np.zeros((self.height, self.width), dtype=np.float32)
        self.resource_field = np.ones((self.height, self.width), dtype=np.float32) * 10.0
        self.will_field = np.zeros_like(self.value_mass_field)
        self.coherence_field = np.zeros_like(self.value_mass_field)
        self.intentional_field = np.zeros((self.height, self.width, 2), dtype=np.float32)
        self.sensory_field = np.zeros((self.height, self.width, 5), dtype=np.float32)
        self.event_reward = np.zeros_like(self.value_mass_field)
        self.event_danger = np.zeros_like(self.value_mass_field)
        # Spirit/Body/Soul triple field (axis 0: spirit, 1: body, 2: soul)
        self.soul_field = np.zeros((self.height, self.width, 3), dtype=np.float32)
        # Wave/phase field: channel 0 amplitude, channel 1 phase
        self.wave_phase_field = np.zeros((self.height, self.width, 2), dtype=np.float32)
        # Celestial bodies for large-scale law anchoring
        self.sun_pos = np.array([self.width * 0.75, self.height * 0.5], dtype=np.float32)
        self.moon_pos = np.array([self.width * 0.25, self.height * 0.5], dtype=np.float32)

        self.connections: Dict[str, Dict[str, float]] = {}
        self.freq_mapper = WaveFrequencyMapper()
        self._init_fields()

    # ------------------------------------------------------------------ #
    # Initialization helpers

    def _init_fields(self) -> None:
        grid_x, grid_y = np.meshgrid(
            np.linspace(-1.0, 1.0, self.width, dtype=np.float32),
            np.linspace(-1.0, 1.0, self.height, dtype=np.float32),
        )
        base = np.exp(-(grid_x**2 + grid_y**2) * 2.5)
        noise = 0.05 * np.random.randn(self.height, self.width).astype(np.float32)
        self.value_mass_field = (base + noise).clip(min=0.0)
        self.will_field = (0.6 + 0.1 * np.random.randn(self.height, self.width)).astype(np.float32).clip(min=0.0)
        self._init_sensory_field()
        self._refresh_fields()

    def _init_sensory_field(self) -> None:
        # Sensory map: channel 0/1 = value/will gradients (normed), 2 = crowd density placeholder,
        # 3 = danger noise, 4 = calm bias derived from peaceful frequency
        grad_val_y, grad_val_x = np.gradient(self.value_mass_field)
        grad_will_y, grad_will_x = np.gradient(self.will_field)
        grad_val = np.abs(grad_val_x) + np.abs(grad_val_y)
        grad_will = np.abs(grad_will_x) + np.abs(grad_will_y)
        grad_val = grad_val / (grad_val.max() + 1e-6)
        grad_will = grad_will / (grad_will.max() + 1e-6)
        density = np.zeros_like(self.value_mass_field)
        danger = 0.1 * np.random.rand(self.height, self.width).astype(np.float32)
        # calm bias from peace frequency color brightness
        peace = self.freq_mapper.get_emotion_frequency(EmotionType.PEACE)
        calm_bias = float(peace.frequency_hz / 1000.0)
        calm = (0.2 + calm_bias) * np.ones_like(self.value_mass_field, dtype=np.float32)
        self.sensory_field[..., 0] = grad_val
        self.sensory_field[..., 1] = grad_will
        self.sensory_field[..., 2] = density
        self.sensory_field[..., 3] = danger
        self.sensory_field[..., 4] = calm

    def _refresh_fields(self) -> None:
        grad_y, grad_x = np.gradient(self.will_field)
        vec = np.stack([-grad_x, -grad_y], axis=-1)
        norm = np.linalg.norm(vec, axis=-1, keepdims=True) + 1e-6
        self.intentional_field = (vec / norm).astype(np.float32)
        self.coherence_field = np.tanh(self.value_mass_field * self.will_field * 0.1).astype(np.float32)
        self._init_sensory_field()

    def _update_sensory_density(self, alive_idx: np.ndarray) -> None:
        density = np.zeros_like(self.value_mass_field)
        px = np.clip(self.positions[alive_idx, 0].astype(int), 0, self.width - 1)
        py = np.clip(self.positions[alive_idx, 1].astype(int), 0, self.height - 1)
        np.add.at(density, (py, px), 1)
        if density.max() > 0:
            density = density / density.max()
        self.sensory_field[..., 2] = density

    def _update_groups(self, alive_idx: np.ndarray) -> None:
        density = self.sensory_field[..., 2]
        hotspots = np.argwhere(density > (LAW_DENSITY_GROUP_THRESHOLD / max(1, alive_idx.size)))
        self.group_state.clear()
        for gid, (y, x) in enumerate(hotspots):
            self.group_state[gid] = {"center": (x, y), "members": 0, "resource": 0.0}
        for idx in alive_idx:
            x = int(np.clip(self.positions[idx, 0], 0, self.width - 1))
            y = int(np.clip(self.positions[idx, 1], 0, self.height - 1))
            assigned = None
            for gid, state in self.group_state.items():
                cx, cy = state["center"]
                if abs(x - cx) <= 2 and abs(y - cy) <= 2:
                    assigned = gid
                    break
            self.group_ids[idx] = assigned
            if assigned is not None:
                self.group_state[assigned]["members"] += 1
                self.group_state[assigned]["resource"] += self.resource_field[y, x]
                # small group bonus to will field
                self.will_field[y, x] = min(LAW_FIELD_MAX, self.will_field[y, x] + LAW_GROUP_BONUS)

    def _next_slot(self) -> Optional[int]:
        free = np.nonzero(~self.is_alive_mask)[0]
        return int(free[0]) if free.size > 0 else None

    # ------------------------------------------------------------------ #
    # Public API

    def set_time_scale(self, minutes_per_tick: float) -> None:
        self.time_scale = float(minutes_per_tick)

    def add_cell(self, concept_id: str, properties: Optional[Dict[str, Any]] = None) -> Optional[int]:
        if concept_id in self.id_to_idx:
            return self.id_to_idx[concept_id]

        slot = self._next_slot()
        if slot is None:
            self.logger.warning("No free slots left for cell '%s'", concept_id)
            return None

        props = properties or {}
        pos = props.get("position", {})
        x = float(pos.get("x", np.random.uniform(0, self.width)))
        y = float(pos.get("y", np.random.uniform(0, self.height)))
        z = float(pos.get("z", 0.0))
        energy = float(props.get("energy", props.get("hp", 100.0)))
        hp = float(props.get("hp", energy))

        self.positions[slot] = (x, y, z)
        self.velocities[slot] = 0.0
        self.energy[slot] = energy
        self.hp[slot] = hp
        self.age[slot] = 0
        self.mass[slot] = float(props.get("mass", 1.0))
        self.valence[slot] = float(props.get("valence", 0.5))
        self.arousal[slot] = float(props.get("arousal", 0.5))
        self.is_alive_mask[slot] = True
        self.metadata[slot] = {
            "dna": props.get("dna", self.primordial_dna),
            "properties": props,
        }
        self.memory_buffers[slot] = deque(maxlen=16)

        self.id_to_idx[concept_id] = slot
        self.idx_to_id[slot] = concept_id
        return slot

    def add_connection(self, head_id: str, tail_id: str, strength: float = 1.0) -> None:
        self.connections.setdefault(head_id, {})[tail_id] = float(strength)
        self.connections.setdefault(tail_id, {})[head_id] = float(strength)

    def apply_will_field(self, field_type: str, strength: float = 0.1) -> None:
        """
        Field shaper governed by decay + gentle nudges (law-based, no explosive growth).
        """
        self.will_field *= LAW_GLOBAL_DECAY
        if field_type == "entropy_stabilization":
            self.will_field += strength * 0.02
        elif field_type == "align":
            self.will_field += strength * 0.05
        self.will_field = np.clip(self.will_field, 0.0, LAW_FIELD_MAX)
        self._refresh_fields()

    def imprint_spiral_coil_field(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        turns: float = 3.0,
        strength: float = 1.0,
    ) -> None:
        theta = np.linspace(0.0, turns * 2.0 * math.pi, num=600)
        radii = np.linspace(0.0, radius, num=600)
        xs = center_x + radii * np.cos(theta)
        ys = center_y + radii * np.sin(theta)
        for x, y in zip(xs, ys):
            ix = int(np.clip(x, 0, self.width - 1))
            iy = int(np.clip(y, 0, self.height - 1))
            self.will_field[iy, ix] += strength / 200.0
            self.value_mass_field[iy, ix] += strength / 400.0
        self._refresh_fields()

    # ------------------------------------------------------------------ #
    # Simulation

    def run_simulation_step(self, dt: float = 1.0) -> Tuple[List[Cell], List[Dict[str, Any]]]:
        self.tick += 1
        dt_scaled = float(dt) * max(self.time_scale, 1.0)

        alive_idx = np.nonzero(self.is_alive_mask)[0]
        newborn_cells: List[Cell] = []
        awakening_events: List[Dict[str, Any]] = []

        if alive_idx.size == 0:
            self._decay_fields(dt_scaled)
            return newborn_cells, awakening_events

        # Update sensory density channel from current positions
        self._update_sensory_density(alive_idx)
        # Update group structures
        self._update_groups(alive_idx)
        # Random events: reward/danger patches
        self._spawn_events()
        # Update celestial positions (sun/moon) and evolve spirit/body/soul fields
        self._update_celestials()
        self._evolve_soul_axes()
        # Automated wave-phase interventions (schedule-based)
        self._auto_intervention()
        self._evolve_wave_phase()

        # Law-based field evolution (diffusion + decay + clamp)
        self.value_mass_field, self.will_field = evolve_fields(
            self.value_mass_field, self.will_field, diffusion=0.05, decay=LAW_GLOBAL_DECAY, clamp=LAW_FIELD_MAX
        )
        # Resource field regeneration and decay
        self.resource_field = np.clip(
            self.resource_field * LAW_GLOBAL_DECAY + LAW_RESOURCE_REGEN, 0.0, LAW_FIELD_MAX
        )
        # Events decay
        self.event_reward *= LAW_EVENT_DECAY
        self.event_danger *= LAW_EVENT_DECAY

        grad_val_y, grad_val_x = np.gradient(self.value_mass_field)
        grad_will_y, grad_will_x = np.gradient(self.will_field)
        field_flow_x = grad_val_x + 0.6 * grad_will_x
        field_flow_y = grad_val_y + 0.6 * grad_will_y

        px = np.clip(self.positions[alive_idx, 0].astype(int), 0, self.width - 1)
        py = np.clip(self.positions[alive_idx, 1].astype(int), 0, self.height - 1)
        senses = self.sensory_field[py, px]

        pull = np.stack([field_flow_x[py, px], field_flow_y[py, px]], axis=1)

        # Social cohesion: weak pull toward neighbors in the connection graph
        social_force = np.zeros_like(pull)
        for i, idx in enumerate(alive_idx):
            cid = self.idx_to_id[idx]
            neighbors = self.connections.get(cid, {})
            if not neighbors:
                continue
            for nid, strength in neighbors.items():
                n_idx = self.id_to_idx.get(nid)
                if n_idx is None or not self.is_alive_mask[n_idx]:
                    continue
                diff = self.positions[n_idx, :2] - self.positions[idx, :2]
                dist = np.linalg.norm(diff) + 1e-6
                social_force[i] += diff / dist * strength * 0.05

        # Gravity-like pull toward center of mass
        if alive_idx.size > 0:
            center = np.mean(self.positions[alive_idx, :2], axis=0)
            for i, idx in enumerate(alive_idx):
                diff = center - self.positions[idx, :2]
                dist = np.linalg.norm(diff) + 1e-6
                gravity = (diff / dist) * (LAW_GRAVITY_CONST * self.mass[idx] / (dist + 1.0))
                pull[i] += gravity

        # Celestial pull (sun, moon)
        for i, idx in enumerate(alive_idx):
            pos = self.positions[idx, :2]
            for body_pos, body_mass in ((self.sun_pos, LAW_SUN_MASS), (self.moon_pos, LAW_MOON_MASS)):
                diff = body_pos - pos
                dist = np.linalg.norm(diff) + 1e-3
                pull[i] += (diff / dist) * (body_mass / (dist * dist + 1.0))

        # Simple adaptive policy: agents with higher policy_gain follow fields more, lower adds noise
        adherence = np.clip(self.policy_gain[alive_idx] * self.global_policy_gain, 0.2, 3.0).reshape(-1, 1)
        noise = np.random.randn(*pull.shape) * 0.05
        pull = pull * adherence + noise * (1.0 / adherence)

        total_force = pull + social_force
        self.velocities[alive_idx, :2] += 0.08 * total_force * dt_scaled
        speed = np.linalg.norm(self.velocities[alive_idx, :2], axis=1, keepdims=True) + 1e-6
        max_speed = LAW_MAX_SPEED
        self.velocities[alive_idx, :2] = np.clip(self.velocities[alive_idx, :2], -max_speed, max_speed)

        self.positions[alive_idx, :2] += self.velocities[alive_idx, :2]
        self.positions[alive_idx, 0] = np.clip(self.positions[alive_idx, 0], 0, self.width - 1)
        self.positions[alive_idx, 1] = np.clip(self.positions[alive_idx, 1], 0, self.height - 1)
        self.age[alive_idx] += 1

        # Energy and HP updates
        gain = self.value_mass_field[py, px] * 0.02 * dt_scaled
        sense_bonus = senses[:, 0] * 0.5 * dt_scaled
        base_cost = (0.08 + 0.01 * speed.flatten()) * dt_scaled
        # Resource consumption
        consume = np.minimum(self.resource_field[py, px], LAW_RESOURCE_CONSUME * dt_scaled)
        self.resource_field[py, px] -= consume
        energy_before = self.energy[alive_idx].copy()
        self.energy[alive_idx] += gain + sense_bonus + consume - base_cost
        self.hp[alive_idx] -= 0.002 * dt_scaled
        # Apply law-based decay and clamping
        self.energy[alive_idx] *= LAW_ENERGY_DECAY
        self.energy[alive_idx] = np.clip(self.energy[alive_idx], 0.0, LAW_MAX_ENERGY)
        self.hp[alive_idx] = np.clip(self.hp[alive_idx], 0.0, LAW_MAX_HP)

        # Emotion update from sensory channels (valence: pleasantness, arousal: intensity)
        pleasant = senses[:, [0, 1]].mean(axis=1) + self.event_reward[py, px] - self.event_danger[py, px]
        intensity = np.linalg.norm(senses[:, 2:4], axis=1) + self.event_danger[py, px]
        self.valence[alive_idx] = np.clip(self.valence[alive_idx] * 0.85 + 0.15 * pleasant, 0.0, 1.0)
        self.arousal[alive_idx] = np.clip(self.arousal[alive_idx] * 0.85 + 0.15 * (intensity + speed.flatten()) * 0.5, 0.0, 1.0)

        # Reward and adaptive policy update
        reward_signal = (self.energy[alive_idx] - energy_before) + pleasant - intensity
        self.rewards[alive_idx] = reward_signal
        self.policy_gain[alive_idx] = np.clip(self.policy_gain[alive_idx] + 0.1 * reward_signal, 0.1, 3.0)

        # Causal log + replay (aggregate)
        mean_reward = float(np.mean(reward_signal)) if reward_signal.size > 0 else 0.0
        mean_val = float(self.valence[alive_idx].mean()) if alive_idx.size > 0 else 0.0
        mean_aro = float(self.arousal[alive_idx].mean()) if alive_idx.size > 0 else 0.0
        self.replay_buffer.append(
            {
                "tick": self.tick,
                "mean_reward": mean_reward,
                "valence": mean_val,
                "arousal": mean_aro,
                "intervention": self.current_intervention,
            }
        )
        self._update_global_policy(mean_reward)

        # Memory logging (short episodic buffer)
        for idx, cx, cy in zip(alive_idx, px, py):
            buf = self.memory_buffers[idx]
            if buf is None:
                buf = deque(maxlen=16)
                self.memory_buffers[idx] = buf
            buf.append(
                {
                    "tick": self.tick,
                    "pos": (int(cx), int(cy)),
                    "valence": float(self.valence[idx]),
                    "arousal": float(self.arousal[idx]),
                    "energy": float(self.energy[idx]),
                }
            )

        # Deposit influence back into fields (feedback loop)
        self.value_mass_field *= LAW_GLOBAL_DECAY
        self.will_field *= LAW_GLOBAL_DECAY
        for x_i, y_i, e in zip(px, py, self.energy[alive_idx]):
            self.value_mass_field[y_i, x_i] += max(e, 0.0) * 0.003
            self.will_field[y_i, x_i] += 0.001
        self.value_mass_field = np.clip(self.value_mass_field, 0.0, LAW_FIELD_MAX)
        self.will_field = np.clip(self.will_field, 0.0, LAW_FIELD_MAX)

        # Recompute derived fields
        self._refresh_fields()

        # Births: allowed if energy high enough and slot free
        for idx in list(alive_idx):
            if self.energy[idx] > LAW_REPRO_THRESHOLD and self._next_slot() is not None:
                child_id = f"{self.idx_to_id[idx]}_child_{self.tick}"
                child_energy = self.energy[idx] * (1.0 - LAW_REPRO_COST)
                self.energy[idx] *= LAW_REPRO_COST
                jitter = np.random.randn(2) * 1.0
                pos = {
                    "x": float(np.clip(self.positions[idx, 0] + jitter[0], 0, self.width - 1)),
                    "y": float(np.clip(self.positions[idx, 1] + jitter[1], 0, self.height - 1)),
                    "z": float(self.positions[idx, 2]),
                }
                slot = self.add_cell(child_id, {"position": pos, "energy": child_energy, "hp": child_energy})
                if slot is not None:
                    newborn = Cell(child_id, dna=self.metadata[idx]["dna"], properties={"position": pos}, energy=child_energy, hp=child_energy)
                    newborn_cells.append(newborn)
                    self.add_connection(self.idx_to_id[idx], child_id, strength=0.8)

        # Deaths
        dead_idx = np.nonzero(
            (self.energy <= 0) | (self.hp <= 0) | (self.energy < LAW_MIN_ENERGY_TO_SURVIVE) | (self.age > LAW_MAX_AGE)
        )[0]
        if dead_idx.size > 0:
            for di in dead_idx:
                cid = self.idx_to_id[di]
                if cid:
                    self.connections.pop(cid, None)
                    for neigh in list(self.connections.keys()):
                        self.connections[neigh].pop(cid, None)
                    self.id_to_idx.pop(cid, None)
                self.idx_to_id[di] = None
                self.is_alive_mask[di] = False
                self.energy[di] = 0.0
                self.hp[di] = 0.0
                self.valence[di] = 0.0
                self.arousal[di] = 0.0
                self.memory_buffers[di] = None

        return newborn_cells, awakening_events

    def _decay_fields(self, dt_scaled: float) -> None:
        decay = max(0.99, 1.0 - 0.001 * dt_scaled)
        self.value_mass_field *= decay
        self.will_field *= decay
        self.value_mass_field = np.clip(self.value_mass_field, 0.0, LAW_FIELD_MAX)
        self.will_field = np.clip(self.will_field, 0.0, LAW_FIELD_MAX)
        self._refresh_fields()

    def _spawn_events(self, reward_count: int = 5, danger_count: int = 2) -> None:
        for _ in range(reward_count):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            self.event_reward[y, x] += 1.0
        for _ in range(danger_count):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            self.event_danger[y, x] += 0.5

    def _update_celestials(self) -> None:
        # simple orbit around center
        cx, cy = self.width * 0.5, self.height * 0.5
        angle_sun = 0.01 * self.tick
        angle_moon = 0.02 * self.tick + 1.0
        self.sun_pos = np.array(
            [cx + LAW_CELESTIAL_ORBIT_RADIUS * math.cos(angle_sun), cy + LAW_CELESTIAL_ORBIT_RADIUS * math.sin(angle_sun)],
            dtype=np.float32,
        )
        self.moon_pos = np.array(
            [cx + LAW_CELESTIAL_ORBIT_RADIUS * 0.6 * math.cos(angle_moon), cy + LAW_CELESTIAL_ORBIT_RADIUS * 0.6 * math.sin(angle_moon)],
            dtype=np.float32,
        )

    def _evolve_soul_axes(self) -> None:
        # spirit/body/soul fields decay + slight boost from event reward and coherence
        self.soul_field[..., 0] = np.clip(self.soul_field[..., 0] * LAW_SPIRIT_DECAY + self.event_reward * 0.05, 0.0, 1.0)
        self.soul_field[..., 1] = np.clip(self.soul_field[..., 1] * LAW_BODY_DECAY + self.resource_field * 0.001, 0.0, 1.0)
        self.soul_field[..., 2] = np.clip(self.soul_field[..., 2] * LAW_SOUL_DECAY + self.coherence_field * 0.05, 0.0, 1.0)

    def _update_global_policy(self, mean_reward: float) -> None:
        delta = mean_reward - self.last_mean_reward
        self.global_policy_gain = float(np.clip(self.global_policy_gain + 0.5 * delta, 0.1, 3.0))
        self.last_mean_reward = mean_reward

    def set_intervention(self, label: Optional[str]) -> None:
        """Mark the current intervention label for causal logging."""
        self.current_intervention = label

    def _auto_intervention(self) -> None:
        """
        Simple schedule-based intervention:
        - every 50 ticks: phase align boost
        - every 25 ticks offset: calm alignment
        """
        if self.tick % 50 == 0:
            self.set_intervention("phase_boost")
            self.wave_phase_field[..., 0] += 0.1  # amplitude
            self.wave_phase_field[..., 1] += 0.05  # phase
        elif self.tick % 50 == 25:
            self.set_intervention("calm_align")
            self.wave_phase_field[..., 0] *= 0.98
            self.wave_phase_field[..., 1] *= 0.98
        else:
            self.set_intervention(None)

    def _evolve_wave_phase(self) -> None:
        amp = self.wave_phase_field[..., 0]
        phase = self.wave_phase_field[..., 1]
        amp_lap = (np.roll(amp, 1, 0) + np.roll(amp, -1, 0) + np.roll(amp, 1, 1) + np.roll(amp, -1, 1) - 4 * amp)
        phase_lap = (np.roll(phase, 1, 0) + np.roll(phase, -1, 0) + np.roll(phase, 1, 1) + np.roll(phase, -1, 1) - 4 * phase)
        amp = amp + LAW_WAVE_PHASE_DIFFUSION * amp_lap
        phase = phase + LAW_WAVE_PHASE_DIFFUSION * phase_lap
        amp *= LAW_WAVE_PHASE_DECAY
        phase *= LAW_WAVE_PHASE_DECAY
        # event reward nudges amplitude, danger perturbs phase
        amp += self.event_reward * 0.02
        phase -= self.event_danger * 0.01
        self.wave_phase_field[..., 0] = np.clip(amp, 0.0, 5.0)
        self.wave_phase_field[..., 1] = np.clip(phase, -3.14, 3.14)

    # ------------------------------------------------------------------ #
    # Reporting

    def print_world_summary(self) -> None:
        alive = int(self.is_alive_mask.sum())
        mean_energy = float(self.energy[self.is_alive_mask].mean()) if alive > 0 else 0.0
        mean_hp = float(self.hp[self.is_alive_mask].mean()) if alive > 0 else 0.0
        mean_val = float(self.valence[self.is_alive_mask].mean()) if alive > 0 else 0.0
        mean_aro = float(self.arousal[self.is_alive_mask].mean()) if alive > 0 else 0.0
        print(
            f"[world] tick={self.tick} alive={alive} energy_mean={mean_energy:.2f} "
            f"hp_mean={mean_hp:.2f} value_max={self.value_mass_field.max():.3f} "
            f"will_max={self.will_field.max():.3f} coherence_max={self.coherence_field.max():.3f} "
            f"valence_mean={mean_val:.2f} arousal_mean={mean_aro:.2f}"
        )

    def harvest_snapshot(self, path: str | Path) -> Dict[str, Any]:
        alive_idx = np.nonzero(self.is_alive_mask)[0]
        cells: List[Dict[str, Any]] = []
        for idx in alive_idx:
            cid = self.idx_to_id[idx] or f"cell_{idx}"
            cells.append(
                {
                    "id": cid,
                    "position": {
                        "x": float(self.positions[idx, 0]),
                        "y": float(self.positions[idx, 1]),
                        "z": float(self.positions[idx, 2]),
                    },
                    "energy": float(self.energy[idx]),
                    "hp": float(self.hp[idx]),
                    "age": int(self.age[idx]),
                    "valence": float(self.valence[idx]),
                    "arousal": float(self.arousal[idx]),
                    "memory_tail": list(self.memory_buffers[idx])[-3:] if self.memory_buffers[idx] else [],
                }
            )

        snapshot = {
            "tick": self.tick,
            "alive": len(cells),
            "fields": {
                "value_mass_max": float(self.value_mass_field.max()),
                "will_max": float(self.will_field.max()),
                "coherence_max": float(self.coherence_field.max()),
            },
            "cells": cells,
        }

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
        return snapshot


__all__ = ["World"]
