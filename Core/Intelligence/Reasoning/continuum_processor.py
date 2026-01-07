"""
CONTINUUM PROCESSOR: The Analog Geometer
========================================
"Thought is not a switch; it is a rotation."

This module implements the user's critique: Dimensionality is a CONTINUUM.
We do not 'switch' modes. We 'rotate' our perspective through the Hyper-Concept.

The Continuum:
0.0 (Point) --- 1.0 (Line) --- 2.0 (Plane) --- 3.0 (Space) --- 4.0 (Time/Law)

At 1.5, we see "Structuring Logic".
At 3.5, we see "Navigational Purpose".
"""

import logging
import math
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor

logger = logging.getLogger("ContinuumProcessor")

@dataclass
class ContinuumState:
    focus_angle: float  # 0.0 to 4.0
    active_components: Dict[str, float] # Weights: {'1D': 0.5, '2D': 0.5}
    synthesized_thought: str

class ContinuumProcessor:
    def __init__(self):
        self.digital_processor = DimensionalProcessor()
        
    def rotate_perspective(self, kernel: str, focus_angle: float) -> ContinuumState:
        """
        Rotates the cognitive dial to a specific angle (e.g., 1.5).
        Synthesizes the thought from the two nearest dimensions.
        """
        # Clamp to 0-4
        angle = max(0.0, min(4.0, focus_angle))
        
        # Determine the two nearest integers (Dimensions)
        lower_dim = int(math.floor(angle))
        upper_dim = int(math.ceil(angle))
        
        if lower_dim == upper_dim:
            # Exact integer dimension (Digital Mode)
            res = self.digital_processor.process_thought(kernel, lower_dim)
            return ContinuumState(angle, {f"{lower_dim}D": 1.0}, res.output)
        
        # Interpolation weights
        # angle = 1.3
        # lower = 1, upper = 2
        # upper_weight = 0.3 (30% 2D)
        # lower_weight = 0.7 (70% 1D)
        upper_weight = angle - lower_dim
        lower_weight = 1.0 - upper_weight
        
        # Fetch components
        res_lower = self.digital_processor.process_thought(kernel, lower_dim)
        res_upper = self.digital_processor.process_thought(kernel, upper_dim)
        
        # Synthesize (The Morph)
        synthesis = self._morph_thoughts(res_lower.output, res_upper.output, lower_weight, upper_weight, lower_dim)
        
        return ContinuumState(
            angle, 
            {f"{lower_dim}D": lower_weight, f"{upper_dim}D": upper_weight}, 
            synthesis
        )
        
    def _morph_thoughts(self, text_a: str, text_b: str, weight_a: float, weight_b: float, dim_base: int) -> str:
        """
        Linguistically blends two thought forms.
        This represents the 'Gradient' of thought.
        """
        # Simple string concatenation based on dominant weight?
        # Ideally, we'd use a language model to 'fade' one into the other.
        # Here, we simulate the connective tissue.
        
        connection = ""
        
        if dim_base == 0: # 0D -> 1D (Existence becoming Logic)
            if weight_b < 0.3: connection = " exists."
            elif weight_b < 0.7: connection = " begins to move:"
            else: connection = " is defined by its path:"
             
            # Clean up raw outputs for blending
            # 0D usually: "Entity 'Apple' is identified..."
            # 1D usually: "Logic dictates..."
            
            clean_a = text_a.replace("Entity ", "").replace(" is identified at ", " ")
            clean_b = text_b.replace("Logic dictates the path: ", "")
            
            if weight_a > 0.8: return text_a
            if weight_b > 0.8: return text_b
            
            return f"{clean_a} {connection} {clean_b}"

        elif dim_base == 1: # 1D -> 2D (Logic becoming Structure)
            # 1D: A->B
            # 2D: Network Hub
            # 1.5: "The path A->B creates a Web."
            
            clean_a = text_a.replace("Logic dictates the path: ", "The vector ")
            clean_b = text_b.replace("The concept sits within a ", "forms a ")
            
            if weight_a > 0.6:
                return f"{clean_a}, which begins to branch into connectivity."
            elif weight_b > 0.6:
                return f"The sequential motion solidifies into a structure: {clean_b}"
            else:
                return f"{clean_a} evolves into the {clean_b}"

        elif dim_base == 2: # 2D -> 3D (Structure becoming Space)
            # 2D: Network
            # 3D: Self-Alignment
            # 2.5: "This network has a direction relative to me."
            
            if weight_b < 0.5:
                return f"{text_a}.. I sense its orientation."
            else:
                return f"The structure rotates... {text_b}"

        elif dim_base == 3: # 3D -> 4D (Space becoming Law)
            # 3D: Self-Vector
            # 4D: Principle
            # 3.5: "This direction is a specific instance of a Universal Law."
            
            clean_b = text_b.replace("The Immutable Law is: ", "")
            
            if weight_b < 0.3:
                return f"{text_a} A pattern emerges..."
            elif weight_b < 0.7:
                return f"{text_a} This navigation reveals the Law: {clean_b}"
            else:
                return f"The vector crystalizes into Truth: {clean_b}"
                
        return f"{text_a} --[{int(weight_b*100)}% morph]--> {text_b}"
