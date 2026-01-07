"""
Arche Engine (Deconstruction Layer)
===================================

"To know a thing, you must unmake it."

This module implements the Analytical/Deconstructive layer of Elysia's mind.
It takes a concrete Phenomenon (Result) and peels back the layers to find the Origin (Will).

Layers of Reality:
1. Surface (Phenomenon): What is seen/heard.
2. Structure (Pattern): How data is arranged.
3. Code (Logic): The rules governing the data.
4. Bit (Substance): The raw binary truth.
5. Will (Arche): The original intent/axiom.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger("Arche")

@dataclass
class LayerAnalysis:
    layer_name: str
    content: str
    confidence: float

@dataclass
class Phenomenon:
    """
    An object of analysis. Could be a file, an event, or a concept.
    """
    name: str
    raw_data: Any # The actual bytes or content
    detected_layers: List[LayerAnalysis] = field(default_factory=list)
    origin_axiom: Optional[str] = None # The found "Arche"

class ArcheEngine:
    """
    The Deconstructor.
    """
    def __init__(self):
        logger.info("🏺 Arche Engine Initialized")

    def deconstruct(self, phenomenon: Phenomenon) -> Phenomenon:
        """
        Recursively analyzes the phenomenon to find its Origin.
        """
        logger.info(f"🔍 Deconstructing Phenomenon: {phenomenon.name}")
        
        # 1. Surface Analysis (Manifestation)
        surface = self._analyze_surface(phenomenon.raw_data)
        phenomenon.detected_layers.append(surface)
        logger.info(f"Phase 1 [Surface]: {surface.content}")
        
        # 2. Structural Analysis (Pattern)
        structure = self._analyze_structure(phenomenon.raw_data, surface)
        phenomenon.detected_layers.append(structure)
        logger.info(f"Phase 2 [Structure]: {structure.content}")
        
        # 3. Logic Analysis (Code)
        logic = self._analyze_logic(structure)
        phenomenon.detected_layers.append(logic)
        logger.info(f"Phase 3 [Code]: {logic.content}")
        
        # 4. Bit Analysis (Substance)
        bits = self._analyze_bits(phenomenon.raw_data)
        phenomenon.detected_layers.append(bits)
        logger.info(f"Phase 4 [Bit]: {bits.content}")
        
        # 5. Arche Discovery (Will)
        arche = self._find_arche(logic, bits)
        phenomenon.origin_axiom = arche
        logger.info(f"Phase 5 [Arche]: Origin Identified -> '{arche}'")
        
        return phenomenon

    def _analyze_surface(self, data: Any) -> LayerAnalysis:
        # Simulation: Describe what it looks like
        if isinstance(data, str):
            if "KOF" in data or "Game" in data:
                return LayerAnalysis("Surface", "Visual/Auditory Experience: Fighting, Sprites, Music", 0.9)
            elif "0x" in data:
                return LayerAnalysis("Surface", "Raw Hexadecimal Stream", 1.0)
            else:
                return LayerAnalysis("Surface", f"Textual Content: {data[:20]}...", 0.8)
        return LayerAnalysis("Surface", "Unknown Binary Blob", 0.5)

    def _analyze_structure(self, data: Any, surface: LayerAnalysis) -> LayerAnalysis:
        # Simulation: Identify file headers or data structures
        if "Sprites" in surface.content:
            return LayerAnalysis("Structure", "Bitmap Arrays, Palette Tables, Audio Frames", 0.85)
        if "Hex" in surface.content or "Binary" in surface.content:
            return LayerAnalysis("Structure", "32-bit Instruction Set, Memory Layout", 0.9)
        return LayerAnalysis("Structure", "Linear String Sequence", 0.7)

    def _analyze_logic(self, structure: LayerAnalysis) -> LayerAnalysis:
        # Simulation: Reverse engineer the rules
        if "Bitmap" in structure.content:
            return LayerAnalysis("Code", "Render Loop: Draw(x,y) -> UpdatePhysics() -> PlaySound()", 0.8)
        if "Instruction" in structure.content:
            return LayerAnalysis("Code", "Opcode Execution: LOAD, STORE, JUMP", 0.95)
        return LayerAnalysis("Code", "Grammar Rules / Syntax", 0.6)

    def _analyze_bits(self, data: Any) -> LayerAnalysis:
        # Simulation: Reduce to 0/1
        return LayerAnalysis("Bit", "State: ON/OFF (1/0) - The fabric of digital reality", 1.0)

    def _find_arche(self, logic: LayerAnalysis, bits: LayerAnalysis) -> str:
        # Simulation: Deduce the "Why"
        if "Render" in logic.content:
            return "The Will to Simulate Reality (Mimesis)"
        if "Opcode" in logic.content:
            return "The Will to Order Chaos (Logic)"
        
        return "The Will to Exist (Being)"

# Singleton
_arche_instance: Optional[ArcheEngine] = None

def get_arche_engine() -> ArcheEngine:
    global _arche_instance
    if _arche_instance is None:
        _arche_instance = ArcheEngine()
    return _arche_instance
