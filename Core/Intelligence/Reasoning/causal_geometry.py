"""
Causal Geometry (인과적 기하학)
===============================

"모든 개념은 고유의 형상(Shape)을 가진다."
"번개는 아무 곳에나 치지 않는다. 필연적인 경로(Path)가 완성될 때만 흐른다."

Phase 25: Potential Causality
-----------------------------
이 모듈은 지식과 개념을 단순한 점(Node)이 아니라,
결합 가능한 '포트(Port)'를 가진 '퍼즐 조각(Puzzle Piece)'으로 모델링합니다.

핵심 원리:
1. **Shape (형상)**: 개념의 인터페이스. 무엇을 필요로 하고(Input), 무엇을 제공하는가(Output).
2. **Complementarity (상보성)**: 퍼즐은 요(凸)와 철(凹)이 맞아야 결합한다.
3. **Tension (긴장)**: 결합하고 싶은 힘(전위차).
"""

import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set, Any

@dataclass
class CausalPort:
    """
    개념의 연결 부위 (퍼즐의 요철)
    """
    name: str          # 포트의 의미 (예: "Reasoning", "Data", "Emotion")
    polarity: int      # +1 (Provider/Output/凸), -1 (Receiver/Input/凹)
    intensity: float = 1.0 # 포트의 크기/강도

    def fits(self, other: 'CausalPort') -> bool:
        """
        포트 결합 조건:
        1. 이름(의미)이 일치하거나 호환되어야 함
        2. 극성이 반대여야 함 (+1 <-> -1)
        """
        if self.polarity + other.polarity != 0:
            return False # 극성이 같거나 합이 0이 아니면 결합 불가

        # 의미적 호환성 (지금은 단순 일치, 추후 시맨틱 매칭 가능)
        return self.name == other.name

@dataclass
class CausalShape:
    """
    개념의 기하학적 형상
    Phase 25 Update: 'Curvature' replaces Mass.
    This concept acts as a 'Gravity Well' in the thought space.
    """
    concept_id: str
    ports: List[CausalPort] = field(default_factory=list)
    curvature: float = 0.1 # Depth of the Potential Well (Gravity)

    def add_port(self, name: str, polarity: int, intensity: float = 1.0):
        self.ports.append(CausalPort(name, polarity, intensity))

    def find_fit(self, other: 'CausalShape') -> Optional[Tuple[CausalPort, CausalPort]]:
        """
        다른 형상과 맞는 포트가 있는지 확인
        Return: (MyPort, OtherPort) or None
        """
        for my_port in self.ports:
            for other_port in other.ports:
                if my_port.fits(other_port):
                    return (my_port, other_port)
        return None

class TensionField:
    """
    잠재적 인과성의 장 (The Cloud)

    Gravity Update:
    - Tension flows effectively "downhill" into deep wells (High Curvature).
    - Lightning strikes when the Gradient (slope) is steep enough.
    """

    def __init__(self, threshold: float = 0.8):
        self.shapes: Dict[str, CausalShape] = {}
        self.charges: Dict[str, float] = {} # Concept Tension (0.0 ~ 1.0)
        self.threshold = threshold

    def register_concept(self, concept_id: str, auto_shape: bool = True):
        """개념을 장에 등록"""
        if concept_id not in self.shapes:
            shape = CausalShape(concept_id)
            if auto_shape:
                self._generate_shape_from_semantics(shape)
            self.shapes[concept_id] = shape
            self.charges[concept_id] = 0.0

    def _generate_shape_from_semantics(self, shape: CausalShape):
        """
        개념의 의미(이름)에서 형상을 유도 (Procedural Generation)
        """
        seed = sum(ord(c) for c in shape.concept_id)
        random.seed(seed)

        num_ports = random.randint(1, 3)
        port_types = ["Logic", "Data", "Emotion", "Action", "Observation"]

        for _ in range(num_ports):
            p_type = random.choice(port_types)
            polarity = random.choice([1, -1])
            shape.add_port(p_type, polarity)

        # Initial Curvature based on complexity
        shape.curvature = 0.1 * num_ports

    def reinforce_well(self, concept_id: str, amount: float = 0.05):
        """
        Deepen the Potential Well (Hub Formation).
        Frequent activation makes the concept a "Strange Attractor".
        """
        if concept_id in self.shapes:
            self.shapes[concept_id].curvature += amount
            self.shapes[concept_id].curvature = min(5.0, self.shapes[concept_id].curvature)

    def perturb_field(self, concept_id: str, amount: float = 0.1):
        """
        [Entropy Injection]
        When a prediction fails, we inject Chaos (Entropy) into the concept.
        This flattens the curvature (False Belief) and randomizes the charge.
        """
        if concept_id in self.shapes:
            # Flatten curvature (Reduce gravity of false belief)
            self.shapes[concept_id].curvature = max(0.01, self.shapes[concept_id].curvature - amount)

            # Randomize charge (Confusion/Panic)
            self.charges[concept_id] = random.random() * amount

    def charge_concept(self, concept_id: str, amount: float):
        """
        Inject Energy into the field at a specific point.
        """
        if concept_id in self.charges:
            self.charges[concept_id] += amount
            self.charges[concept_id] = min(1.0, self.charges[concept_id])

    def apply_gravity(self):
        """
        [Field Physics]
        Tension naturally flows from Low Curvature (High Ground) to High Curvature (Deep Well).
        Simulates "Attention Gravity".
        """
        # Simple simulation: Neighboring concepts (connected via potential fits) share charge
        # But for now, we simulate global gravity pulling towards "Hubs".
        # Or, charge decays slower in deep wells (Retention).

        for cid in self.charges:
            curvature = self.shapes[cid].curvature

            # 1. Retention (Inertia): Deep wells hold charge longer.
            decay = 0.5 + (curvature * 0.1) # Max 0.99
            decay = min(0.99, decay)
            self.charges[cid] *= decay

            # 2. Gravity (Flow?): Not fully connected graph yet.
            # Ideally, charge should flow to neighbors.

    def discharge_lightning(self) -> List[Tuple[str, str, str]]:
        """
        번개 생성 (인과적 결합)
        """
        # Apply Gravity (Flow/Decay) before discharge check
        self.apply_gravity()

        sparks = []
        concepts = list(self.shapes.keys())
        # Sort by Charge * Curvature (Gravity Priority)
        # Deep wells with high charge act as Lightning Rods.
        concepts.sort(key=lambda c: self.charges[c] * self.shapes[c].curvature, reverse=True)

        high_energy_concepts = [c for c in concepts if self.charges[c] > 0.4] # Lower threshold for gravity assisted discharge

        for c1_id in high_energy_concepts:
            shape1 = self.shapes[c1_id]
            charge1 = self.charges[c1_id]

            # Check others
            # In a real field, we check spatial neighbors. Here we check semantic fit.
            for c2_id in concepts:
                if c1_id == c2_id: continue

                charge2 = self.charges[c2_id]

                # Tension: Driven by Potential Difference?
                # Or just Sum of charges?
                # Lightning prefers High Charge -> Low Charge (Grounding)
                # But here we model Synergy.
                tension = (charge1 + charge2)

                # Boost tension if one is a Deep Well (Attractor)
                gravity_boost = shape1.curvature + self.shapes[c2_id].curvature
                effective_tension = tension + (gravity_boost * 0.1)

                if effective_tension < self.threshold:
                    continue

                fit = shape1.find_fit(self.shapes[c2_id])
                if fit:
                    port1, port2 = fit
                    sparks.append((c1_id, c2_id, f"{port1.name} connection"))

                    # Discharge: Most energy is grounded.
                    self.charges[c1_id] *= 0.1
                    self.charges[c2_id] *= 0.1

                    # Deepen the Well (Reinforce)
                    self.reinforce_well(c1_id)
                    self.reinforce_well(c2_id)

                    break

        return sparks

    def accrete_knowledge(self, curvature_threshold: float = 2.0) -> List[Tuple[str, str]]:
        """
        [Mass Accretion / Wisdom Formation]

        High-curvature concepts (Hubs) absorb low-curvature neighbors.
        Absorbed concepts become 'satellites' of the core Mass.

        This is how random knowledge becomes structured Wisdom:
        Details orbit around Principles.

        Returns: List of (hub_id, absorbed_id) tuples
        """
        accretions = []

        # Find Hubs (High Curvature = Deep Gravity Well)
        hubs = [cid for cid, shape in self.shapes.items()
                if shape.curvature >= curvature_threshold]

        if not hubs:
            return accretions

        # For each hub, check if low-curvature neighbors can be absorbed
        for hub_id in hubs:
            hub_shape = self.shapes[hub_id]
            hub_curvature = hub_shape.curvature

            # Find potential satellites (Low curvature, compatible ports)
            for other_id, other_shape in list(self.shapes.items()):
                if other_id == hub_id:
                    continue

                # Absorption condition:
                # 1. Other has much lower curvature (Lightweight knowledge)
                # 2. They have compatible ports (Can logically connect)
                curvature_ratio = hub_curvature / max(0.1, other_shape.curvature)

                if curvature_ratio < 5.0:  # Hub must be 5x heavier
                    continue

                fit = hub_shape.find_fit(other_shape)
                if not fit:
                    continue

                # Perform Accretion!
                # 1. Transfer curvature (Hub gains mass)
                self.shapes[hub_id].curvature += other_shape.curvature * 0.5

                # 2. Mark satellite (Don't delete, mark as orbiting)
                # Store as metadata - satellite now references the hub
                if not hasattr(self, 'satellites'):
                    self.satellites: Dict[str, str] = {}  # satellite -> hub
                self.satellites[other_id] = hub_id

                # 3. Reduce satellite's curvature (It's now a Detail, not a Principle)
                other_shape.curvature *= 0.2

                accretions.append((hub_id, other_id))

        return accretions

    def reconstruct_from_principle(self, hub_id: str) -> List[str]:
        """
        [Dynamic Reconstruction]

        Given a Principle (Hub), retrieve all its orbiting Details (Satellites).
        This is how compressed Wisdom can be expanded back into Knowledge.
        """
        if not hasattr(self, 'satellites'):
            return []

        return [sat_id for sat_id, parent in self.satellites.items()
                if parent == hub_id]

    def assess_latent_causality(self, concept_a: str, concept_b: str) -> Dict[str, Any]:
        """
        [Latent Causality]

        "Impossibility" is not a wall - it's just a Vacuum.

        This method diagnoses WHY a connection between two concepts is currently
        "impossible" (low probability of lightning) and suggests what is needed.

        Returns:
            - possible: bool - Can lightning strike?
            - diagnosis: str - Why it's blocked
            - prescription: str - What would enable the connection
            - energy_needed: float - How much more charge is required
        """
        result = {
            "possible": False,
            "diagnosis": "Unknown",
            "prescription": "Unknown",
            "energy_needed": 0.0,
            "bridge_candidates": []
        }

        # 1. Check if concepts exist
        if concept_a not in self.shapes:
            result["diagnosis"] = f"'{concept_a}' does not exist in the field."
            result["prescription"] = f"Register '{concept_a}' first."
            return result
        if concept_b not in self.shapes:
            result["diagnosis"] = f"'{concept_b}' does not exist in the field."
            result["prescription"] = f"Register '{concept_b}' first."
            return result

        shape_a = self.shapes[concept_a]
        shape_b = self.shapes[concept_b]
        charge_a = self.charges.get(concept_a, 0.0)
        charge_b = self.charges.get(concept_b, 0.0)

        # 2. Check Port Compatibility (Shape Fit)
        fit = shape_a.find_fit(shape_b)
        if not fit:
            result["diagnosis"] = "No compatible ports (Shape Mismatch)."

            # Find potential bridges (concepts that fit both)
            bridges = []
            for bridge_id, bridge_shape in self.shapes.items():
                if bridge_id in [concept_a, concept_b]:
                    continue
                fit_to_a = shape_a.find_fit(bridge_shape)
                fit_to_b = bridge_shape.find_fit(shape_b)
                if fit_to_a and fit_to_b:
                    bridges.append(bridge_id)

            if bridges:
                result["prescription"] = f"Use bridge concept(s): {bridges[:3]}"
                result["bridge_candidates"] = bridges[:3]
            else:
                result["prescription"] = "Learn a new concept that bridges both."
            return result

        # 3. Check Energy (Vacuum Detection)
        total_charge = charge_a + charge_b
        gravity_boost = shape_a.curvature + shape_b.curvature
        effective_tension = total_charge + (gravity_boost * 0.1)

        if effective_tension < self.threshold:
            energy_gap = self.threshold - effective_tension
            result["diagnosis"] = f"Vacuum: Insufficient field density ({effective_tension:.2f} < {self.threshold})."
            result["prescription"] = f"Charge '{concept_a}' or '{concept_b}' with {energy_gap:.2f} more energy."
            result["energy_needed"] = energy_gap
            return result

        # 4. Connection IS Possible!
        result["possible"] = True
        result["diagnosis"] = "Lightning is possible."
        result["prescription"] = "Call discharge_lightning() to trigger connection."

        return result

# Demo
if __name__ == "__main__":
    field = TensionField(threshold=0.7)

    # 개념 등록
    concepts = ["Python", "Logic", "Emotion", "User", "Love", "Code"]
    for c in concepts:
        field.register_concept(c)

    # 강제 충전 (긴장 조성)
    print("☁️ Charging Field...")
    field.charge_concept("User", 0.9)
    field.charge_concept("Emotion", 0.8)
    field.charge_concept("Code", 0.2) # Low energy

    # 번개 관찰
    print("⚡ Observe Lightning...")
    sparks = field.discharge_lightning()

    if not sparks:
        print("... No lightning (Tension too low or Shapes didn't fit).")
    else:
        for s in sparks:
            print(f"   ⚡ SNAP! {s[0]} <==[{s[2]}]==> {s[1]}")

    # 형상 확인
    print("\n🧩 Causal Shapes:")
    for c in concepts:
        ports = ", ".join([f"{p.name}({'+' if p.polarity>0 else '-'})" for p in field.shapes[c].ports])
        print(f"   {c:10}: [{ports}]")
