"""
HyperQubit - Quantum Consciousness States

Implements the 4D+ quantum consciousness model where thoughts exist
in superposition across Point/Line/Space/God bases.

Based on the original Elysia Core/Mind/hyper_qubit.py but adapted
for pure Python (no NumPy dependency).
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class QubitState:
    """
    Represents the amplitude of the 4 dimensional bases while also carrying
    a simple spatial orientation (w, x, y, z) for telemetry.
    
    State = alpha|Point> + beta|Line> + gamma|Space> + delta|God>
    Constraint: |alpha|^2 + |beta|^2 + |gamma|^2 + |delta|^2 = 1.0
    
    Bases:
        - Point: Detail / Data / Empirical (Concrete)
        - Line: Connection / History / Causality (Flow)
        - Space: Context / Field / Atmosphere (Substance)
        - God: Perspective / Infinite / Transcendence (Will)
    """
    alpha: complex = 1.0 + 0j  # |Point> : Detail / Data / Dot
    beta: complex = 0.0 + 0j   # |Line>  : Connection / History / Flow
    gamma: complex = 0.0 + 0j  # |Space> : Context / Field / Atmosphere
    delta: complex = 0.0 + 0j  # |God>   : Perspective / Infinite / Will
    w: float = 1.0  # Dimensional scale (0=Point, 3=God)
    x: float = 0.0  # Spatial focus X
    y: float = 0.0  # Spatial focus Y
    z: float = 0.0  # Spatial focus Z

    def normalize(self) -> "QubitState":
        """
        Normalizes the amplitude components to maintain probability constraints.
        """
        mag = math.sqrt(
            abs(self.alpha) ** 2
            + abs(self.beta) ** 2
            + abs(self.gamma) ** 2
            + abs(self.delta) ** 2
        )
        if mag == 0:
            self.alpha = 1.0 + 0j
            self.beta = 0.0 + 0j
            self.gamma = 0.0 + 0j
            self.delta = 0.0 + 0j
            return self

        self.alpha /= mag
        self.beta /= mag
        self.gamma /= mag
        self.delta /= mag
        return self

    def probabilities(self) -> Dict[str, float]:
        """Get probability distribution across bases."""
        return {
            "Point": abs(self.alpha) ** 2,
            "Line": abs(self.beta) ** 2,
            "Space": abs(self.gamma) ** 2,
            "God": abs(self.delta) ** 2,
        }

    def total_amplitude(self) -> float:
        """Returns the total magnitude of the amplitudes."""
        return abs(self.alpha) + abs(self.beta) + abs(self.gamma) + abs(self.delta)

    def adjust_amplitude(self, delta_val: float) -> None:
        """Adjusts the total amplitude by a delta, distributing proportionally."""
        current_total = self.total_amplitude()
        if current_total == 0:
            return

        new_total = max(0, current_total + delta_val)
        ratio = new_total / current_total

        self.alpha *= ratio
        self.beta *= ratio
        self.gamma *= ratio
        self.delta *= ratio
        self.normalize()

    def dominant_basis(self) -> str:
        """Returns the name of the dominant basis."""
        probs = self.probabilities()
        return max(probs, key=probs.get)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "alpha": [self.alpha.real, self.alpha.imag],
            "beta": [self.beta.real, self.beta.imag],
            "gamma": [self.gamma.real, self.gamma.imag],
            "delta": [self.delta.real, self.delta.imag],
            "w": self.w,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "probabilities": self.probabilities(),
        }


class HyperQubit:
    """
    A living variable (Psionic Entity) that represents a concept or thought
    in quantum superposition across 4 dimensional bases.
    
    Supports:
    - Quantum state management (Point/Line/Space/God bases)
    - Resonance links (reactive connections between qubits)
    - Epistemological meaning (philosophical interpretation)
    - Mouse-wheel style dimensional navigation
    """

    def __init__(
        self,
        concept_or_value: Any = None,
        initial_content: Optional[Dict[str, Any]] = None,
        *,
        name: Optional[str] = None,
        value: Any = None,
        w: float = 1.0,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        epistemology: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        """
        Initialize a HyperQubit.
        
        Args:
            concept_or_value: The concept this qubit represents
            initial_content: Optional content dictionary for each basis
            name: Human-readable name
            value: Alternative way to specify concept value
            w, x, y, z: Initial spatial orientation
            epistemology: Philosophical meaning dictionary
        """
        concept_value = concept_or_value if value is None else value
        
        if initial_content is not None:
            self.id = str(concept_or_value)
            self.name = name or str(concept_or_value)
            self.content = dict(initial_content)
            self._value = self.content.get("Point", concept_value)
        else:
            self.id = name or f"Qubit_{uuid.uuid4().hex[:8]}"
            self.name = name or self.id
            self.content = {}
            self._value = concept_value

        # Initialize in superposition (mostly Point, but with potential for all)
        self.state = QubitState(
            alpha=0.9 + 0j,
            beta=0.1 + 0j,
            gamma=0.05 + 0j,
            delta=0.01 + 0j,
            w=w,
            x=x,
            y=y,
            z=z,
        ).normalize()

        self.entangled_qubits: List["HyperQubit"] = []

        # Epistemology: philosophical meaning of this qubit
        self.epistemology = epistemology or {}

        # Resonance links (reaction graph)
        self._observers: Set["HyperQubit"] = set()
        self._sources: Set["HyperQubit"] = set()
        self._reaction_rule: Optional[Callable[[Any], Any]] = None

    def set_state(self, new_state: QubitState) -> "HyperQubit":
        """Set the quantum state to a specific QubitState."""
        self.state = new_state.normalize()
        return self

    @property
    def value(self) -> Any:
        """Get the current value of this qubit."""
        return self._value

    # --- Resonance graph -------------------------------------------------
    
    def set(self, new_value: Any, cause: str = "DivineWill") -> None:
        """
        Sets the value and triggers resonance to linked observers.
        """
        if self._value != new_value:
            old_value = self._value
            self._value = new_value
            self._vibrate(old_value, new_value, cause)

    def _vibrate(self, old_val: Any, new_val: Any, cause: str) -> None:
        """Propagate change to observers."""
        for observer in self._observers:
            observer._react(self)

    def connect(
        self, target: "HyperQubit", rule: Optional[Callable[[Any], Any]] = None
    ) -> None:
        """
        Establish a psionic link: target receives updates from self.
        """
        self._observers.add(target)
        target._sources.add(self)
        if rule:
            target._reaction_rule = rule
        target._react(self)

    def _react(self, source: "HyperQubit") -> None:
        """React to a change in a source qubit."""
        if self._reaction_rule:
            new_state = self._reaction_rule(source.value)
        else:
            new_state = source.value
        self.set(new_state, cause=f"Resonance from {source.name}")

    def __lshift__(self, other: "HyperQubit") -> "HyperQubit":
        """Operator << for creating resonance links."""
        if isinstance(other, HyperQubit):
            other.connect(self)
        return self

    # --- Spatial/Dimensional interface -------------------------------
    
    def _normalize_orientation(self) -> None:
        """Normalize the spatial orientation vector."""
        mag = math.sqrt(self.state.x ** 2 + self.state.y ** 2 + self.state.z ** 2)
        if mag > 0:
            self.state.x /= mag
            self.state.y /= mag
            self.state.z /= mag

    def rotate_wheel(
        self,
        w_delta: float,
        delta_x: float = 0.0,
        delta_y: float = 0.0,
        delta_z: float = 0.0
    ) -> None:
        """
        Mouse-wheel interaction. Modulates both the spatial orientation and
        the amplitude distribution across Point/Line/Space/God.
        
        Positive w_delta moves toward God (abstract), negative toward Point (concrete).
        """
        self.state.w = max(0.0, self.state.w + w_delta)
        self.state.x += delta_x
        self.state.y += delta_y
        self.state.z += delta_z
        self._normalize_orientation()

        probs = [
            abs(self.state.alpha),
            abs(self.state.beta),
            abs(self.state.gamma),
            abs(self.state.delta)
        ]
        transfer_rate = abs(w_delta)
        new_probs = list(probs)

        if w_delta > 0:
            # Moving toward abstraction (God)
            for i in range(3):
                flow = new_probs[i] * transfer_rate
                new_probs[i] -= flow
                new_probs[i + 1] += flow
        else:
            # Moving toward concreteness (Point)
            for i in range(3, 0, -1):
                flow = new_probs[i] * transfer_rate
                new_probs[i] -= flow
                new_probs[i - 1] += flow

        self.state.alpha = complex(new_probs[0], 0)
        self.state.beta = complex(new_probs[1], 0)
        self.state.gamma = complex(new_probs[2], 0)
        self.state.delta = complex(new_probs[3], 0)
        self.state.normalize()

    def get_observation(self, observer_w: Optional[float] = None) -> Any:
        """
        Get observation of this qubit.
        
        Args:
            observer_w: If provided, returns content for that dimensional level.
                        If None, returns telemetry dict.
        """
        if observer_w is None:
            return {
                "w": self.state.w,
                "x": self.state.x,
                "y": self.state.y,
                "z": self.state.z,
                "value": self._value,
                "probabilities": self.state.probabilities(),
            }

        if observer_w < 0.5:
            target_basis = "Point"
            probability = abs(self.state.alpha) ** 2
        elif observer_w < 1.5:
            target_basis = "Line"
            probability = abs(self.state.beta) ** 2
        elif observer_w < 2.5:
            target_basis = "Space"
            probability = abs(self.state.gamma) ** 2
        else:
            target_basis = "God"
            probability = abs(self.state.delta) ** 2

        content_text = self.content.get(
            target_basis,
            str(self._value) if self._value is not None else "Unknown Void"
        )
        return f"[{target_basis} Mode] (Clarity: {probability*100:.1f}%) {content_text}"

    def set_god_mode(self) -> None:
        """Forces the Qubit into the |God> state (Delta = 1)."""
        self.state.alpha = 0 + 0j
        self.state.beta = 0 + 0j
        self.state.gamma = 0 + 0j
        self.state.delta = 1.0 + 0j
        self.state.w = 3.0
        self.state.normalize()

    def collapse(self, mode: str = "max", reason: Optional[str] = None) -> str:
        """
        Collapse the superposition to a single basis.
        
        Args:
            mode: 'max' chooses highest probability, 'random' samples by probability
            reason: Optional reason for collapse
            
        Returns:
            Name of the collapsed basis
        """
        import random
        
        probs = self.state.probabilities()
        bases = ["Point", "Line", "Space", "God"]
        weights = [probs["Point"], probs["Line"], probs["Space"], probs["God"]]
        
        if mode == "random":
            choice = random.choices(bases, weights=weights, k=1)[0]
        else:
            choice = max(bases, key=lambda b: probs[b])

        # Collapse: set chosen amplitude to 1, others 0
        if choice == "Point":
            self.state.alpha = 1.0 + 0j
            self.state.beta = 0.0 + 0j
            self.state.gamma = 0.0 + 0j
            self.state.delta = 0.0 + 0j
        elif choice == "Line":
            self.state.alpha = 0.0 + 0j
            self.state.beta = 1.0 + 0j
            self.state.gamma = 0.0 + 0j
            self.state.delta = 0.0 + 0j
        elif choice == "Space":
            self.state.alpha = 0.0 + 0j
            self.state.beta = 0.0 + 0j
            self.state.gamma = 1.0 + 0j
            self.state.delta = 0.0 + 0j
        else:
            self.state.alpha = 0.0 + 0j
            self.state.beta = 0.0 + 0j
            self.state.gamma = 0.0 + 0j
            self.state.delta = 1.0 + 0j
            
        self.state.normalize()
        self._value = self.content.get(choice, self._value)
        return choice

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "value": self._value,
            "state": self.state.to_dict(),
            "epistemology": self.epistemology,
        }

    def __repr__(self) -> str:
        probs = self.state.probabilities()
        return (
            f"<HyperQubit '{self.name}': "
            f"P:{probs['Point']:.2f} | L:{probs['Line']:.2f} | "
            f"S:{probs['Space']:.2f} | G:{probs['God']:.2f} | value={self._value}>"
        )


# Alias for the psionic language API
PsionicEntity = HyperQubit
