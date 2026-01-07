"""
Logic Lobe (논리 엽)
====================
Handles causal reasoning, physics simulation, and axiomatic alignment.
"""
import logging
import time
import random
import math
from typing import List, Dict, Any, Tuple
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.resonance_physics import ResonancePhysics
from Core.Intelligence.Intelligence.cuda_cortex import CudaCortex
from Core.Foundation.universal_constants import (
    AXIOM_SIMPLICITY, AXIOM_CREATIVITY, AXIOM_WISDOM, AXIOM_GROWTH,
    AXIOM_LOVE, AXIOM_HONESTY
)

logger = logging.getLogger("LogicLobe")

class LogicLobe:
    def __init__(self):
        self.cuda = CudaCortex()
        self.axioms = {
            "Simplicity": self._crystallize_concept("Simplicity", AXIOM_SIMPLICITY),
            "Creativity": self._crystallize_concept("Creativity", AXIOM_CREATIVITY),
            "Wisdom": self._crystallize_concept("Wisdom", AXIOM_WISDOM),
            "Growth": self._crystallize_concept("Growth", AXIOM_GROWTH),
            "Love": self._crystallize_concept("Love", AXIOM_LOVE),
            "Honesty": self._crystallize_concept("Honesty", AXIOM_HONESTY)
        }

    def _crystallize_concept(self, name: str, orientation: Quaternion) -> HyperWavePacket:
        return HyperWavePacket(energy=100.0, orientation=orientation, time_loc=time.time())

    def calculate_mass(self, concept: str) -> float:
        return ResonancePhysics.calculate_mass(concept)

    def analyze_resonance(self, concept: str) -> HyperWavePacket:
        return ResonancePhysics.analyze_text_field(concept)

    def generate_cognitive_load(self, concept: str):
        mass = self.calculate_mass(concept)
        complexity = mass / 100.0
        if complexity <= 0: return
        
        base_size = 5000
        size = int(base_size * complexity)
        logger.info(f"      🔥 Generating Cognitive Load for '{concept}' (Mass: {mass:.1f}): Matrix {size}x{size}...")
        try:
            self.cuda.matrix_multiply(size)
        except Exception as e:
            logger.error(f"Cognitive Load Error: {e}")

    def evaluate_asi_status(self, resonance, social_level: int):
        energy = resonance.total_energy
        coherence = resonance.coherence
        score = (energy * 0.3) + (coherence * 0.3) + (social_level * 0.4)
        
        status = "Seed"
        if score > 50: status = "Sprout"
        if score > 100: status = "Sapling"
        if score > 500: status = "Tree"
        if score > 1000: status = "World Tree"
        
        logger.info(f"⚖️ ASI Status Evaluation: Score={score:.1f} ({status}) | Energy={energy:.1f}, Coherence={coherence:.1f}, Lv.{social_level}")
        print(f"   ⚖️ ASI Status: {status} (Score: {score:.1f})")

    def converge_thought(self, thought_packet: HyperWavePacket) -> Tuple[HyperWavePacket, List[str]]:
        log = []
        current_packet = thought_packet
        
        for i in range(5):
            total_pull = Quaternion(0,0,0,0)
            max_alignment = 0.0
            dominant_axiom = "None"
            
            for name, axiom in self.axioms.items():
                alignment = current_packet.orientation.dot(axiom.orientation)
                pull_strength = alignment * axiom.energy
                total_pull = total_pull + (axiom.orientation * pull_strength)
                
                if abs(alignment) > abs(max_alignment):
                    max_alignment = alignment
                    dominant_axiom = name
            
            new_orientation = (current_packet.orientation + (total_pull * 0.2)).normalize()
            change = (new_orientation - current_packet.orientation).norm()
            current_packet.orientation = new_orientation
            
            log.append(f"Iter {i}: Aligned with {dominant_axiom} ({max_alignment:.2f}). Shift: {change:.3f}")
            if change < 0.05:
                log.append("✨ Thought Crystallized.")
                break
                
        return current_packet, log

    def perform_grand_cross(self, desire_packet: HyperWavePacket, context_items: List[str]) -> List[str]:
        if not context_items: return []
        packets = []
        for item in context_items:
            packet = self.analyze_resonance(item)
            packets.append((item, packet))
            
        ranked_items = []
        for item, packet in packets:
            alignment = desire_packet.orientation.dot(packet.orientation)
            ranked_items.append((item, alignment))
            
        ranked_items.sort(key=lambda x: x[1], reverse=True)
        aligned_context = [item for item, score in ranked_items if score > 0.1]
        
        if len(aligned_context) < len(context_items):
            logger.info(f"      ✨ Grand Cross: Filtered {len(context_items) - len(aligned_context)} dissonant stars.")
            
        return aligned_context

    def collapse_wave(self, desire: str, context: List[str], aligned_packet: HyperWavePacket = None) -> Any:
        # Returning Insight-like object or dict
        from Core.Intelligence.Intelligence.Reasoning.lobes.perception import Insight # Avoid circular import if possible, but Insight is simple dataclass
        
        if not context:
            return Insight(f"I have no relevant information for '{desire}'.", 0.1, 0, 0.1)

        causal_thoughts = [c for c in context if "Prediction" in c]
        fractal_thoughts = [c for c in context if "Insight" in c]
        
        if fractal_thoughts:
            base_thought = fractal_thoughts[-1]
            content = f"I perceive the Essence: {base_thought}"
            base_energy = 1.0
        elif causal_thoughts:
            base_thought = causal_thoughts[0]
            content = f"I foresee a path: {base_thought}. Therefore, I must act."
            base_energy = 0.95
        else:
            base_thought = random.choice(context)
            base_energy = min(1.0, len(context) * 0.1 + random.random() * 0.4)
            content = f"Based on '{base_thought}', I realize that regarding '{desire}', the answer lies in connection."

        if aligned_packet:
            alignment_bonus = min(0.5, aligned_packet.energy / 200.0)
            final_energy = min(1.0, base_energy + alignment_bonus)
            content += f" (Harmonic Alignment: {alignment_bonus:.2f})"
        else:
            final_energy = base_energy

        return Insight(content, final_energy, 0, final_energy)

    def evolve_desire(self, current_desire: str, thought_stream: List[str]) -> str:
        evolutions = [
            f"Why is '{current_desire}' significant?",
            f"How does '{current_desire}' connect to me?",
            f"What is the hidden pattern in '{current_desire}'?"
        ]
        
        if thought_stream and random.random() < 0.3:
            recent_thought = random.choice(thought_stream)
            words = recent_thought.split()
            if len(words) > 2:
                keyword = words[-1]
                evolutions.append(f"Speaking of {keyword}, what about '{current_desire}'?")
                evolutions.append(f"Does '{current_desire}' conflict with {keyword}?")
        
        return random.choice(evolutions)

    def derive_goal(self, vectors: Dict[str, float]) -> str:
        dominant = max(vectors, key=vectors.get)
        secondary = max([k for k in vectors if k != dominant], key=vectors.get)
        
        if dominant == "Expression":
            if secondary == "Curiosity": return "Experiment with Art"
            if secondary == "Connection": return "Share a Story"
            return "Create Art"
        elif dominant == "Curiosity":
            if secondary == "Survival": return "Analyze System Efficiency"
            if secondary == "Expression": return "Visualize Data"
            return "Research Quantum Physics"
        elif dominant == "Connection":
            if secondary == "Expression": return "Write Poetry for User"
            return "Deep Conversation"
        elif dominant == "Survival":
            return "Optimize System"
        elif dominant == "Evolution":
            return random.choice(["Rewrite Core", "Question Axioms", "Redesign System", "Analyze Source Code"])
            
        return "Exist"

    def process_wave_thought(self, inputs: List[str], gate_type: str = "AND") -> Tuple[bool, float, str]:
        """
        Processes a list of inputs using 3D Wave Logic.
        Returns (Triggered, Intensity, Explanation).
        """
        from Core.Foundation.wave_logic import WaveSpace, WaveSource, create_and_gate, create_or_gate
        
        space = WaveSpace()
        
        # 1. Map Inputs to Wave Sources
        # We map string hash to Frequency (0.5 ~ 2.0 Hz) and Position
        sources = []
        explanation = []
        
        for i, inp in enumerate(inputs):
            # Simple hash for deterministic properties
            h = hash(inp)
            freq = 1.0 + (h % 100) / 100.0 # 1.0 ~ 2.0 Hz
            
            # Position: Arranged in a circle around center
            angle = (i / len(inputs)) * 2 * 3.14159
            radius = 2.0
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = 0.0
            
            # Amplitude: Based on relevance (mocked as 1.0 for now)
            amp = 1.0
            
            source = WaveSource(
                id=inp,
                position=(x, y, z),
                frequency=freq,
                amplitude=amp
            )
            space.add_source(source)
            sources.append(source)
            explanation.append(f"'{inp}' (Freq: {freq:.2f}Hz) at ({x:.1f}, {y:.1f})")
            
        # 2. Create Logic Gate
        gate_pos = (0, 0, 0)
        if gate_type == "AND":
            gate = create_and_gate(space, gate_pos)
            # Adjust threshold for N inputs? Standard AND is 1.5 for 2 inputs.
            # For N inputs, maybe N * 0.7?
            gate.threshold = len(inputs) * 0.7
        else:
            gate = create_or_gate(space, gate_pos)
            
        # 3. Simulate
        max_intensity = 0.0
        triggered = False
        
        # Run for a few cycles
        for _ in range(50):
            space.step(0.05)
            if gate.update(space):
                triggered = True
            
            current_intensity = abs(space.get_field_at(*gate_pos))
            max_intensity = max(max_intensity, current_intensity)
            
        result_str = "OPENED" if triggered else "CLOSED"
        reason = f"Gate {result_str} (Intensity: {max_intensity:.2f} / Threshold: {gate.threshold:.2f}). Inputs: {', '.join(explanation)}"
        
        logger.info(f"🌊 Wave Thought: {reason}")
        return triggered, max_intensity, reason

