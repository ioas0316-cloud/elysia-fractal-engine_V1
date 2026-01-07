"""
Interference Solver (간섭 연산기 - Phase 3)
===========================================

"Thinking is not moving; it is vibrating into alignment."
"사고는 이동이 아니라, 정렬을 위한 진동입니다."

This module replaces the Newtonian PhysicsSolver.
It uses Phase Interference as the primary driver for cognitive evolution.
"""

import logging
import math
from typing import List, Tuple, Dict, Any
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger("InterferenceSolver")

class InterferenceSolver:
    """
    The engine of the Silent Sphere (S³).
    Instead of Gravity (Force), it uses Resonance (Alignment Depth).
    """
    
    def __init__(self):
        # The key frequency of the universe (Metabolism)
        self.key_frequency = 432.0 
        self.damping = 0.95 # Entropy/Cooling
        
    def calculate_resonance(self, thought: Quaternion, attractor: Quaternion) -> float:
        """
        Calculates the alignment (Resonance) between a thought and an attractor.
        Returns a value from -1.0 to 1.0 (Dot Product of normalized quaternions).
        """
        # Ensure normalization for spherical logic
        t_norm = thought.normalize()
        a_norm = attractor.normalize()
        
        # Alignment is the 4D Dot Product
        return t_norm.dot(a_norm)

    def step(self, thought: Quaternion, attractors: List[Tuple[Quaternion, float]], dt: float = 0.1) -> Quaternion:
        """
        A single cycle of thought evolution.
        Each attractor pulls the thought towards its phase.
        
        thought: Current phase state (Quaternion)
        attractors: List of (Target Quaternion, Mass/Importance)
        dt: Time step
        """
        # 1. Initialize result with current thought
        # We model this as 'Phase Slerp' (Spherical Linear Interpolation) 
        # but simplified for multiple interference sources.
        
        result_w, result_x, result_y, result_z = thought.w, thought.x, thought.y, thought.z
        
        total_pull = 0.0
        
        for target, mass in attractors:
            # Calculate alignment (Resonance)
            resonance = self.calculate_resonance(thought, target)
            
            # Interference Intensity (Scale by mass and distance)
            # If resonance is high (aligned), pull is stronger.
            # If resonance is low (orthogonal), pull is weak.
            # If resonance is negative (opposed), it pushes.
            
            # The pull strength is nonlinear (Higher resonance -> Exponentially stronger lock-in)
            pull_strength = mass * (resonance ** 3) * dt
            
            # Apply local rotation towards target
            # Vector interpolation (normalized later to stay on S^3)
            result_w += (target.w - thought.w) * pull_strength
            result_x += (target.x - thought.x) * pull_strength
            result_y += (target.y - thought.y) * pull_strength
            result_z += (target.z - thought.z) * pull_strength
            
            total_pull += abs(pull_strength)

        # 2. Apply Entropy (Natural drift towards Silence/Void if no resonance)
        if total_pull < 0.01:
            # Shift towards w=1 (Identity/Pure Potential)
            # result_w += (1.0 - result_w) * (1.0 - self.damping) * dt
            pass

        # 3. Final Re-normalization (S^3 Constraint)
        new_thought = Quaternion(result_w, result_x, result_y, result_z).normalize()
        
        return new_thought

    def get_interference_pattern(self, thought: Quaternion, attractors: List[Tuple[Quaternion, float]]) -> Dict[str, float]:
        """
        Analyzes the 'Interference Pattern' of the current thought.
        Identifies which attractors are currently resonating.
        """
        pattern = {}
        for target, mass in attractors:
            # In a real system, we'd need names here. Assuming names are handled elsewhere.
            res = self.calculate_resonance(thought, target)
            pattern[str(target)] = res
            
        return pattern
