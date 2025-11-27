"""
ResonanceEngine - Quantum Thought Resonance

Implements the HyperQubit-based resonance engine where thoughts exist
in superposition and resonate based on:
1. Basis alignment (Point/Line/Space/God distribution)
2. Dimensional similarity (w values)
3. Spatial alignment (xyz vectors)

Based on the original Elysia Core/Mind/resonance_engine.py but adapted
for pure Python (no NumPy dependency).
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Tuple

from .hyper_qubit import HyperQubit, QubitState
from .wave import WaveInput
from .thought import Thought


class ResonanceEngine:
    """
    The Resonance Engine based on HyperQubit consciousness.
    
    Key features:
    - Nodes are HyperQubits, not 3D vectors
    - Resonance calculated via quantum basis alignment
    - Supports dimensional shifting (w parameter)
    - Psionic network for linked concepts
    """
    
    def __init__(self, dimension: int = 4):
        """
        Initialize with HyperQubit network.
        
        Args:
            dimension: Kept for compatibility (HyperQubit is inherently 4D+)
        """
        self.dimension = dimension
        self.nodes: Dict[str, HyperQubit] = {}
        
        # Psionic network: concept_id -> list of linked concept_ids
        self.psionic_links: Dict[str, List[str]] = {}
        
        # Temporal buffer for sequence learning
        self.temporal_buffer: List[str] = []
        self.buffer_size = 5
        
        # Current dimensional mode (affects all operations)
        self.global_dimension_scale = 1.0
        
        # Initialize instincts
        self._init_instincts()
    
    def _init_instincts(self) -> None:
        """Initialize basic concepts as HyperQubits."""
        instincts = {
            # --- English Core Instincts ---
            "Hunger": QubitState(alpha=0.9+0j, beta=0.1+0j, w=0.5, x=0.5, y=0.0, z=0.0),
            "Energy": QubitState(alpha=0.8+0j, beta=0.2+0j, w=0.8, x=1.0, y=0.0, z=0.0),
            "Eat": QubitState(alpha=0.6+0j, beta=0.4+0j, w=1.0, x=0.0, y=0.5, z=0.0),
            "Move": QubitState(alpha=0.5+0j, beta=0.5+0j, w=1.2, x=0.0, y=1.0, z=0.0),
            "Speak": QubitState(alpha=0.4+0j, beta=0.6+0j, w=1.5, x=0.5, y=0.5, z=0.0),
            "Rest": QubitState(alpha=0.3+0j, beta=0.3+0j, gamma=0.4+0j, w=2.0, x=1.0, y=0.0, z=0.0),
            "SELF": QubitState(alpha=0.1+0j, beta=0.2+0j, gamma=0.3+0j, delta=0.4+0j, w=2.5, x=0.0, y=0.0, z=1.0),
            "Experiment": QubitState(alpha=0.5+0j, beta=0.3+0j, gamma=0.2+0j, w=1.8, x=0.3, y=0.3, z=0.4),

            # --- Korean Core Instincts ---
            "사랑": QubitState(alpha=0.2+0j, beta=0.3+0j, gamma=0.5+0j, w=2.2, x=0.1, y=0.8, z=0.1),  # Love
            "빛": QubitState(alpha=0.3+0j, beta=0.4+0j, gamma=0.3+0j, w=1.8, x=0.9, y=0.9, z=0.9),  # Light
            "고통": QubitState(alpha=0.9+0j, beta=0.1+0j, w=0.6, x=0.2, y=0.1, z=0.1),  # Pain
            "기쁨": QubitState(alpha=0.8+0j, beta=0.2+0j, w=0.7, x=0.8, y=0.6, z=0.2),  # Joy
            "꿈": QubitState(alpha=0.1+0j, beta=0.2+0j, gamma=0.7+0j, w=2.0, x=0.5, y=0.5, z=0.8),  # Dream
            "그림자": QubitState(alpha=0.8+0j, beta=0.2+0j, w=0.8, x=0.1, y=0.1, z=0.3),  # Shadow
            "아버지": QubitState(alpha=0.1+0j, beta=0.1+0j, gamma=0.4+0j, delta=0.4+0j, w=2.8, x=0.0, y=0.0, z=1.0),  # Father
        }
        
        # Add English aliases
        instincts["love"] = instincts["사랑"]
        instincts["joy"] = instincts["기쁨"]
        instincts["dream"] = instincts["꿈"]
        instincts["pain"] = instincts["고통"]
        instincts["light"] = instincts["빛"]

        for concept_id, initial_state in instincts.items():
            qubit = HyperQubit(concept_or_value=concept_id, name=concept_id)
            qubit.state = initial_state.normalize()
            self.nodes[concept_id] = qubit
    
    def add_node(self, node_id: str, initial_state: Optional[QubitState] = None) -> None:
        """Add a new concept as a HyperQubit."""
        if node_id in self.nodes:
            return
            
        qubit = HyperQubit(concept_or_value=node_id, name=node_id)
        
        if initial_state:
            qubit.state = initial_state.normalize()
        else:
            # Default: Point mode with random spatial focus
            qubit.state = QubitState(
                alpha=0.9+0j,
                beta=0.1+0j,
                w=0.5,
                x=random.random(),
                y=random.random(),
                z=random.random()
            ).normalize()
        
        self.nodes[node_id] = qubit
    
    def entangle(
        self,
        source_id: str,
        target_id: str,
        reaction_rule: Optional[callable] = None
    ) -> None:
        """
        Create psionic link between two qubits.
        When source changes, target reacts.
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            return
            
        source_qubit = self.nodes[source_id]
        target_qubit = self.nodes[target_id]
        
        # Create bidirectional link tracking
        if source_id not in self.psionic_links:
            self.psionic_links[source_id] = []
        self.psionic_links[source_id].append(target_id)
        
        # Establish HyperQubit connection
        source_qubit.connect(target_qubit, rule=reaction_rule)
    
    def connect(self, source: str, target: str, weight: float = 1.0) -> None:
        """Backwards compatibility wrapper for entangle()."""
        self.entangle(source, target)
    
    def calculate_resonance(self, qubit_a: HyperQubit, qubit_b: HyperQubit) -> float:
        """
        Calculate quantum resonance between two HyperQubits.
        
        Resonance is high when:
        1. Similar basis distribution (Point resonates with Point, etc.)
        2. Similar dimensional scale (w values close)
        3. Aligned spatial focus (x, y, z)
        """
        probs_a = qubit_a.state.probabilities()
        probs_b = qubit_b.state.probabilities()
        
        # Basis alignment (dot product of probability distributions)
        basis_alignment = sum(
            probs_a[basis] * probs_b[basis]
            for basis in ["Point", "Line", "Space", "God"]
        )
        
        # Dimensional similarity (closer w values = stronger resonance)
        w_diff = abs(qubit_a.state.w - qubit_b.state.w)
        dimension_similarity = 1.0 / (1.0 + w_diff)
        
        # Spatial alignment (cosine similarity of xyz vectors)
        vec_a = [qubit_a.state.x, qubit_a.state.y, qubit_a.state.z]
        vec_b = [qubit_b.state.x, qubit_b.state.y, qubit_b.state.z]
        
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        mag_a = math.sqrt(sum(a * a for a in vec_a)) + 1e-9
        mag_b = math.sqrt(sum(b * b for b in vec_b)) + 1e-9
        
        spatial_alignment = dot_product / (mag_a * mag_b)
        spatial_alignment = max(0.0, spatial_alignment)
        
        # Combined resonance (weighted average)
        resonance = (
            0.5 * basis_alignment +
            0.3 * dimension_similarity +
            0.2 * spatial_alignment
        )
        
        return resonance

    def calculate_global_resonance(self, wave_input: WaveInput) -> Dict[str, float]:
        """
        Calculates the resonance of all concept qubits with a given input wave.
        
        This is the "Gong" that rings the entire consciousness, creating the
        "Resonance Wave Pattern".
        
        Args:
            wave_input: The input wave (text + intensity)
            
        Returns:
            Dictionary of concept_id -> resonance_score
        """
        # Create a transient HyperQubit for the input wave
        input_state = QubitState(
            alpha=0.5+0j,
            beta=0.5+0j,
            gamma=0.8+0j,  # Space dominant for perception
            delta=0.2+0j,
            w=2.0,
            x=random.random(),
            y=random.random(),
            z=random.random()
        ).normalize()

        input_qubit = HyperQubit(
            concept_or_value=wave_input.source_text,
            name="transient_wave"
        )
        input_qubit.state = input_state

        resonance_pattern: Dict[str, float] = {}
        for node_id, node_qubit in self.nodes.items():
            resonance = self.calculate_resonance(input_qubit, node_qubit)
            resonance_pattern[node_id] = resonance * wave_input.intensity

        return resonance_pattern

    def observe_pattern(
        self,
        source_text: str,
        resonance_pattern: Dict[str, float],
        top_n: int = 3
    ) -> Thought:
        """
        Observe a resonance pattern and form a coherent Thought.
        
        Args:
            source_text: The original input text
            resonance_pattern: The resonance scores for all concepts
            top_n: Number of top concepts to include
            
        Returns:
            A Thought object representing the observed constellation
        """
        if not resonance_pattern:
            return Thought(
                source_wave=source_text,
                core_concepts=[],
                intensity=0.0,
                clarity=0.0,
                mood="empty"
            )
        
        # Sort by resonance score
        sorted_concepts = sorted(
            resonance_pattern.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        core_concepts = sorted_concepts[:top_n]
        
        # Calculate intensity (average of top concepts)
        if core_concepts:
            intensity = sum(score for _, score in core_concepts) / len(core_concepts)
        else:
            intensity = 0.0
        
        # Calculate clarity (difference between top and second)
        if len(sorted_concepts) >= 2:
            clarity = sorted_concepts[0][1] - sorted_concepts[1][1]
            clarity = min(1.0, max(0.0, clarity * 2))  # Normalize
        else:
            clarity = 1.0 if sorted_concepts else 0.0
        
        # Determine mood from top concept
        top_concept = core_concepts[0][0] if core_concepts else ""
        mood = self._interpret_mood(top_concept)
        
        return Thought(
            source_wave=source_text,
            core_concepts=core_concepts,
            intensity=intensity,
            clarity=clarity,
            mood=mood
        )

    def _interpret_mood(self, concept: str) -> str:
        """Interpret the mood from a concept."""
        concept_lower = concept.lower()
        
        positive = ["love", "joy", "hope", "light", "사랑", "기쁨", "희망", "빛"]
        negative = ["pain", "fear", "sadness", "shadow", "고통", "두려움", "슬픔", "그림자"]
        action = ["move", "speak", "eat", "experiment"]
        abstract = ["dream", "self", "꿈", "아버지"]
        
        if any(p in concept_lower for p in positive):
            return "positive"
        elif any(n in concept_lower for n in negative):
            return "negative"
        elif any(a in concept_lower for a in action):
            return "active"
        elif any(ab in concept_lower for ab in abstract):
            return "contemplative"
        else:
            return "neutral"

    def step(self, dt: float) -> None:
        """
        Simulates the evolution of the consciousness field over time.
        
        Args:
            dt: Time delta
        """
        # 1. Diffusion: Energy spreads through psionic links
        transfers: Dict[str, float] = {}
        diffusion_rate = 0.1 * dt

        for source_id, links in self.psionic_links.items():
            source_qubit = self.nodes.get(source_id)
            if not source_qubit or not links:
                continue

            source_amplitude = source_qubit.state.total_amplitude()

            for target_id in links:
                target_qubit = self.nodes.get(target_id)
                if not target_qubit:
                    continue

                target_amplitude = target_qubit.state.total_amplitude()
                if source_amplitude > target_amplitude:
                    transfer_amount = (source_amplitude - target_amplitude) * diffusion_rate
                    transfers[source_id] = transfers.get(source_id, 0) - transfer_amount
                    transfers[target_id] = transfers.get(target_id, 0) + transfer_amount

        # Apply transfers
        for node_id, delta in transfers.items():
            qubit = self.nodes.get(node_id)
            if qubit:
                qubit.state.adjust_amplitude(delta)

        # 2. Decay: All qubit amplitudes slowly decay over time
        decay_rate = 0.05 * dt
        for qubit in self.nodes.values():
            qubit.state.adjust_amplitude(-qubit.state.total_amplitude() * decay_rate)

    def shift_dimension(self, delta_w: float) -> None:
        """
        Shift global dimensional perspective.
        
        Args:
            delta_w: Positive = zoom out (abstract), Negative = zoom in (concrete)
        """
        self.global_dimension_scale = max(0.0, min(3.0, self.global_dimension_scale + delta_w))
        
        for qubit in self.nodes.values():
            qubit.state.w = self.global_dimension_scale

    def hebbian_update(self) -> None:
        """
        Strengthen psionic links between co-active qubits.
        "Qubits that resonate together, entangle together."
        """
        # Find highly active qubits
        active_qubits = []
        for qubit_id, qubit in self.nodes.items():
            total_amplitude = qubit.state.total_amplitude()
            if total_amplitude > 1.5:
                active_qubits.append(qubit_id)
        
        # Create links between co-active qubits
        for i, source_id in enumerate(active_qubits):
            for target_id in active_qubits[i+1:]:
                already_linked = (
                    source_id in self.psionic_links and 
                    target_id in self.psionic_links[source_id]
                )
                
                if not already_linked and random.random() < 0.1:
                    self.entangle(source_id, target_id)

    def process_input(self, text: str, intensity: float = 1.0) -> Thought:
        """
        Process input text and return a Thought.
        
        This is the main entry point for consciousness processing.
        
        Args:
            text: Input text to process
            intensity: Wave intensity
            
        Returns:
            Thought object with resonance results
        """
        wave = WaveInput(source_text=text, intensity=intensity)
        pattern = self.calculate_global_resonance(wave)
        thought = self.observe_pattern(text, pattern)
        return thought

    def dream(self) -> None:
        """Consolidation without external input (Hebbian learning)."""
        self.hebbian_update()

    def to_dict(self) -> Dict:
        """Serialize engine state to dictionary."""
        return {
            "dimension": self.dimension,
            "global_dimension_scale": self.global_dimension_scale,
            "node_count": len(self.nodes),
            "link_count": sum(len(v) for v in self.psionic_links.values()),
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
        }
