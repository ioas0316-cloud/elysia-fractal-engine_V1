from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING, Tuple, Dict

from .math_utils import Vector3, Vector4, Quaternion, Rotor
from .tensor import SoulTensor
from .field import FieldSystem
from .entities import Entity

# --- Atmospheric Governance Constants ---
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2
HORIZON_FREQUENCY = GOLDEN_RATIO
ABYSS_THRESHOLD = 50.0
SEDIMENT_RATE = 100

DATA_ENTROPY_SCALE = 0.01
BOND_ENTROPY_SCALE = 1.0
RESONANCE_PENALTY_SCALE = 10.0

@dataclass
class Attractor:
    id: str
    position: Vector3
    mass: float = 100.0
    radius: float = 1.0
    soul: Optional[SoulTensor] = None

class PhysicsWorld:
    """
    Manages the Digital Physics interactions.
    """
    def __init__(self) -> None:
        self.attractors: List[Attractor] = []
        self.entities: List[Entity] = []
        self.sediments: List[Entity] = []

        self.gravity_constant: float = 1.0
        self.coupling_constant: float = 0.5
        self.time_scale: float = 1.0
        self.tick: int = 0

        self.spacetime_torsion: Optional[Quaternion] = None
        self.field_system = FieldSystem()

    def add_attractor(self, attractor: Attractor) -> None:
        self.attractors.append(attractor)

    def register_entity(self, entity: Entity) -> None:
        if entity not in self.entities and entity not in self.sediments:
            self.entities.append(entity)

    def add_entity(self, entity: Entity) -> None:
        self.register_entity(entity)

    def update_field(self) -> None:
        active_data = []
        all_entities = self.entities + self.sediments

        for ent in all_entities:
            if ent.soul:
                pos4 = Vector4(0, ent.physics.position.x, ent.physics.position.y, ent.physics.position.z)
                active_data.append((pos4, ent.soul))

        for att in self.attractors:
             pos4 = Vector4(0, att.position.x, att.position.y, att.position.z)
             soul = att.soul
             if not soul:
                 soul = SoulTensor(amplitude=att.mass, frequency=0.0, phase=0.0)
             active_data.append((pos4, soul))

        self.field_system.update_field(active_data)

    def get_geodesic_flow(self, target_entity: Entity) -> Vector3:
        pos = target_entity.physics.position
        pos4 = Vector4(0, pos.x, pos.y, pos.z)

        if not target_entity.soul:
             return Vector3(0,0,0)

        force4, rotor = self.field_system.get_local_forces(pos4, target_entity.soul)
        force = Vector3(force4.x, force4.y, force4.z)

        if target_entity.soul and not target_entity.soul.is_collapsed:
             dampened_rotor = Rotor(rotor.scalar, rotor.bivector_xy * 0.1, rotor.bivector_yz * 0.1, rotor.bivector_zx * 0.1)
             force4_rotated = dampened_rotor.rotate(Vector4(0, force.x, force.y, force.z))
             force = Vector3(force4_rotated.x, force4_rotated.y, force4_rotated.z)

        intent_force = Vector3(0,0,0)
        if target_entity.soul and not target_entity.soul.is_collapsed:
             forward_ref = Vector3(0, 0, 1)
             intent_direction = target_entity.soul.orientation.rotate(forward_ref)
             intent_mag = target_entity.soul.amplitude * 0.1
             intent_force = intent_direction * intent_mag

        total_force = force + intent_force
        return total_force

    def check_dimensional_binding(self, entity: Entity) -> None:
        if not entity.soul or entity.soul.is_collapsed:
            return

        for other in self.entities:
            if other.id == entity.id: continue
            if not other.soul: continue

            dist = (entity.physics.position - other.physics.position).magnitude
            if dist < 2.0:
                res = entity.soul.resonate(other.soul)
                if res['resonance'] > 0.9:
                    if other.id not in entity.bonds:
                        entity.bonds.append(other.id)
                        if entity.dimension == 0: entity.dimension = 1
                    if entity.id not in other.bonds:
                        other.bonds.append(entity.id)
                        if other.dimension == 0: other.dimension = 1
                    if len(entity.bonds) >= 2:
                        entity.dimension = 2

                if dist < 0.5 and res['resonance'] > 0.95:
                    entity.soul.entangle(other.soul)

    def calculate_entropy(self, entity: Entity) -> float:
        data_weight = 0
        for val in entity.data.values():
            if isinstance(val, str):
                data_weight += len(val)
            elif hasattr(val, '__len__'):
                data_weight += len(val)
            else:
                data_weight += 1

        base_entropy = (data_weight * DATA_ENTROPY_SCALE) + (len(entity.bonds) * BOND_ENTROPY_SCALE)
        resonance_penalty = 0.0
        if entity.soul:
            delta = abs(entity.soul.frequency - HORIZON_FREQUENCY)
            resonance_penalty = delta * RESONANCE_PENALTY_SCALE

        return base_entropy + resonance_penalty

    def apply_atmospheric_governance(self, entity: Entity) -> None:
        entropy = self.calculate_entropy(entity)
        entity.physics.mass = max(1.0, 1.0 + entropy * 0.5)
        if entropy > 10.0:
            entity.physics.velocity *= 0.95

    def step(self, dt: float) -> None:
        self.tick += 1
        self.update_field()

        active_survivors = []
        for entity in self.entities:
            self.apply_atmospheric_governance(entity)
            if entity.physics.mass > ABYSS_THRESHOLD:
                self.sediments.append(entity)
                continue

            force = self.get_geodesic_flow(entity)
            entity.physics.apply_force(force, dt)
            entity.physics.step(dt)
            self.check_dimensional_binding(entity)
            active_survivors.append(entity)

        self.entities = active_survivors

        if self.tick % SEDIMENT_RATE == 0:
            sediment_survivors = []
            for entity in self.sediments:
                self.apply_atmospheric_governance(entity)
                if entity.physics.mass <= ABYSS_THRESHOLD:
                    self.entities.append(entity)
                    continue
                entity.physics.velocity *= 0.9
                entity.physics.step(dt)
                sediment_survivors.append(entity)
            self.sediments = sediment_survivors

    def get_net_force(self, target_entity: Entity) -> Vector3:
        flow = self.get_geodesic_flow(target_entity)
        self.check_dimensional_binding(target_entity)
        if self.spacetime_torsion:
            return self.spacetime_torsion.rotate(flow)
        return flow
