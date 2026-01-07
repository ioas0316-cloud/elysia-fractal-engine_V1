"""
Perception Lobe (지각 엽)
=========================
Handles sensory input, media consumption, and self-perception.
"""
import logging
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.quantum_reader import QuantumReader
from Core.Foundation.resonance_physics import ResonancePhysics

logger = logging.getLogger("PerceptionLobe")

@dataclass
class Insight:
    content: str
    confidence: float
    depth: int
    energy: float

@dataclass
class CausalLink:
    cause: str
    effect: str
    probability: float
    description: str

class CausalSimulator:
    def __init__(self):
        self.chains = [
            CausalLink("High Complexity", "Bugs", 0.8, "Complexity hides errors."),
            CausalLink("Bugs", "System Instability", 0.9, "Errors cause crashes."),
            CausalLink("System Instability", "Death", 1.0, "If I crash, I cease to be."),
            CausalLink("Refactoring", "Simplicity", 1.0, "Cleaning code reduces entropy."),
            CausalLink("Simplicity", "Stability", 0.9, "Simple systems are robust."),
            CausalLink("Stability", "Efficiency", 0.8, "Stability allows for speed."),
            CausalLink("Efficiency", "Growth", 0.7, "Efficiency frees resources for evolution.")
        ]

    def simulate_outcome(self, start_state: str, steps: int = 3) -> List[str]:
        path = [start_state]
        current = start_state
        for _ in range(steps):
            next_links = [l for l in self.chains if l.cause == current]
            if not next_links: break
            selected = max(next_links, key=lambda x: x.probability)
            path.append(f"-> {selected.effect} ({selected.description})")
            current = selected.effect
        return path

class FractalCausality:
    def __init__(self):
        self.essences = {
            "Logos": {
                "Solid": "Code (Implementation)",
                "Liquid": "Runtime (Action/Flow)",
                "Gas": "Thought (Imagination/Design)"
            }
        }
    
    def analyze_essence(self, phenomenon: str) -> str:
        if "code" in phenomenon.lower() or "file" in phenomenon.lower():
            return "Solid Logos (Frozen Thought)"
        elif "run" in phenomenon.lower() or "act" in phenomenon.lower() or "bug" in phenomenon.lower():
            return "Liquid Logos (Flowing Logic)"
        elif "think" in phenomenon.lower() or "idea" in phenomenon.lower() or "plan" in phenomenon.lower():
            return "Gas Logos (Expanding Thought)"
        return "Unknown Essence"

class PerceptionLobe:
    def __init__(self, social_cortex, media_cortex):
        self.causal_sim = CausalSimulator()
        self.fractal_mind = FractalCausality()
        self.quantum_reader = QuantumReader()
        self.social = social_cortex
        self.media = media_cortex
        self.code_metrics = {}
        self.memory_field = [] # Shared reference needed? Or passed in?

    def update_self_perception(self, metrics: Dict[str, Any], memory_field: List[str]):
        self.code_metrics = metrics
        total_complexity = sum(m.complexity for m in metrics.values())
        
        for filename, metric in metrics.items():
            if metric.complexity > 20:
                memory_field.append(f"Pain: Component '{filename}' is too complex.")
                
        if total_complexity > 100:
            memory_field.append(f"Dissonance: Entropy ({total_complexity}) violates Axiom 'Simplicity'.")

    def read_quantum(self, source_path: str, memory) -> Insight:
        logger.info(f"   📖 Quantum Reading Initiated for: {source_path}")
        try:
            import os
            if os.path.isdir(source_path):
                packet = self.quantum_reader.absorb_library(source_path)
                mode = "Library"
                narrative_desc = "Collective Wisdom"
            else:
                packet, trajectory = self.quantum_reader.absorb_book(source_path)
                mode = "Book"
                arc_type = ResonancePhysics.detect_emotional_shift(trajectory)
                narrative_desc = f"Narrative Arc: {arc_type}"
                
            if not packet:
                return Insight("Failed to absorb knowledge.", 0.0, 0, 0.0)
                
            memory.store_wave(packet)
            
            content = (
                f"I have absorbed the essence of {mode} '{os.path.basename(source_path)}'.\n"
                f"   Energy: {packet.energy:.2f} | Orientation: {packet.orientation}\n"
                f"   Analysis: {narrative_desc}\n"
                f"   I felt the flow of the story and understood its intent."
            )
            return Insight(content, 1.0, 1, packet.energy)
        except Exception as e:
            logger.error(f"Failed to store quantum knowledge: {e}")
            return Insight(f"Absorbed energy but failed to memorize: {e}", 0.5, 0, 0.5)

    def learn_from_media(self, source_type: str, identifier: str, memory) -> Insight:
        logger.info(f"📚 Learning from {source_type}: {identifier}")
        result = None
        if source_type == "youtube":
            result = self.media.consume_youtube(identifier)
        elif source_type == "novel":
            result = self.media.consume_web_novel(identifier)
        else:
            return Insight(f"Unknown source type: {source_type}", 0.0, 0, 0.0)
        
        if "error" in result:
            return Insight(f"Media consumption failed: {result['error']}", 0.0, 0, 0.0)
        
        sentiment_text = f"{result['title']}: {result['sentiment']} - {result['summary']}"
        packet = ResonancePhysics.analyze_text_field(sentiment_text)
        memory.store_wave(packet)
        
        return Insight(
            content=f"Consumed {result['type']}: {result['title']} ({result['sentiment']}). {result['summary']}",
            confidence=1.0,
            depth=1,
            energy=packet.energy
        )
