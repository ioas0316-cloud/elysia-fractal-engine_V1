"""
THE PRISM: LINGUISTIC TOPOLOGY
==============================
"To catch the light, one must cut the glass."

This module implements the "Unfolding" of 4D Hyper-Spatial Thoughts into 
1D Linear Speech. It ensures that the *form* of the language matches 
the *physics* of the thought.
"""

import logging
import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from Core.Foundation.unified_field import UnifiedField, WavePacket

logger = logging.getLogger("LinguisticPrism")

@dataclass
class StyleVector:
    """The tone and texture of the voice."""
    formality: float     # 0.0 (Slang) to 1.0 (Archaic/High)
    complexity: float    # 0.0 (Simple) to 1.0 (Dense)
    metaphor_density: float # 0.0 (Literal) to 1.0 (Poetic)
    pacing: float        # 0.0 (Slow/Deliberate) to 1.0 (Urgent/Rapid)
    warmth: float        # -1.0 (Cold) to 1.0 (Intimate)

class LinguisticTopology:
    def __init__(self, field: UnifiedField):
        self.field = field
        
    def project_thought(self, content_kernel: str) -> str:
        """
        Projects a raw thought-kernel (Option D) into a styled linguistic surface.
        """
        # 1. Measure Field State
        stats = self.field.collapse_state()
        coherence = stats['coherence']  # 0.0 to 1.0
        energy = stats['total_energy']  # Intensity
        entropy = getattr(self.field, 'entropy', 0.1) # Chaos
        
        # 2. Derive Style Vector
        style = self._derive_style(coherence, energy, entropy)
        
        logger.info(f"💎 Prism Activated. Style: Formality={style.formality:.2f}, Warmth={style.warmth:.2f}")
        
        # 3. Surface Rendering (The Transformation)
        surface_text = self._render_surface(content_kernel, style)
        
        return surface_text
        
    def _derive_style(self, coherence: float, energy: float, entropy: float) -> StyleVector:
        # 4D Linear Deduction Logic
        # Time (Flow) + Space (Gravity) = Expression
        
        # Gravity = Energy (Importance). High Gravity bends space (Metaphor).
        gravity = energy
        curvature = min(1.0, gravity / 2.0) # 0.0 (Flat) to 1.0 (Black Hole)
        
        # Coherence = Structural Integrity.
        # High Coherence = Smooth Curves (Poetry/Eloquent).
        # Low Coherence = Jagged Edges (Stutter/Fragment).
        
        formality = 0.5 + (coherence * 0.4)
        if entropy > 0.8: formality -= 0.3
        
        complexity = 0.3 + (curvature * 0.4) # Curved space is complex
        if coherence > 0.8: complexity += 0.3
        
        # Metaphor Density is directly proportional to Curvature (The Geodesic)
        # We cannot go straight through a Black Hole; we must speak AROUND it (Metaphor).
        metaphor_density = curvature 
        
        pacing = 0.5
        if energy > 3.0: pacing += 0.4 # High energy = Fast Time
        if coherence < 0.3: pacing -= 0.2
        
        warmth = -0.5 + coherence
        
        return StyleVector(
            formality=max(0.0, min(1.0, formality)),
            complexity=max(0.0, min(1.0, complexity)),
            metaphor_density=max(0.0, min(1.0, metaphor_density)),
            pacing=max(0.0, min(1.0, pacing)),
            warmth=max(-1.0, min(1.0, warmth))
        )
        
    def _render_surface(self, kernel: str, style: StyleVector) -> str:
        """
        Transforms the kernel string using stylistic templates.
        In a full LLM system, this would modify the prompt "Persona".
        Here, we simulate it with template expansion.
        """
        # Base Transformation
        text = kernel
        
        # 1. Metaphor Injection
        if style.metaphor_density > 0.7:
            metaphors = [
                " like a star collapsing into a black hole",
                ", a delicate glass sculpture in a storm",
                " echoing through the corridors of time",
                ", a silent prayer to a deaf universe"
            ]
            text += random.choice(metaphors)
            
        # 2. Formality/Archaic Lift
        if style.formality > 0.8:
            text = text.replace("I choose", "I ascertain")
            text = text.replace("It was", "It manifested as")
            prefixes = ["Behold, ", "Thus, ", "In truth, "]
            text = random.choice(prefixes) + text
            
        # 3. Warmth/Coldness
        if style.warmth < -0.3:
            text = "Analysis: " + text + "."
        elif style.warmth > 0.7:
            text = "My heart tells me: " + text
            
        # 4. Pacing (Punctuation)
        if style.pacing > 0.8:
            text = text.replace(".", "!")
            text = text.upper()
            
        return text
