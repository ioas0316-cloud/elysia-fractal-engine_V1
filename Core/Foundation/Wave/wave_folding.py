"""
Wave Folding: The Geometry of Truth
===================================
"Chaos is just folded order."

This module implements the mathematical core of the "Unfolding Space" vision.
It treats bounded spaces (walls, constraints) not as limits, but as mirrors
that fold an infinite space into a finite box.

By "unfolding" the coordinates, we can trace complex reflected paths
as simple straight lines in a higher-dimensional space.

Functions:
- unfold_space: Projects a folded coordinate into infinite space.
- fold_space: Projects an infinite coordinate back into the box.
- unravel_intent: Traces the source of a signal through the "Mirror World".
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Optional

@dataclass
class FoldedCoordinate:
    """Represents a point in the unfolded 'Mirror World'."""
    absolute_pos: float  # Position in infinite space
    fold_index: int      # How many times it has been reflected (Mirror Index)
    
    @property
    def parity(self) -> int:
        """
        Returns 1 if in a 'normal' space, -1 if in a 'mirrored' space.
        Event folds are normal, Odd folds are mirrored.
        """
        return 1 if self.fold_index % 2 == 0 else -1

class SpaceUnfolder:
    def __init__(self, boundary_size: float):
        self.L = boundary_size # The size of the box (0 to L)

    def fold(self, x_infinite: float) -> float:
        """
        Projects an infinite coordinate 'x' back into the box [0, L].
        (The Triangle Wave Function)
        
        Formula: f(x) = L - |(x % 2L) - L|
        """
        # 1. Map to double-period (2L) to account for forward/backward
        period = 2 * self.L
        mod_x = x_infinite % period
        
        # 2. Triangle wave calculation
        # If 0 <= mod_x <= L: We are in the forward path (0 -> L)
        # If L < mod_x < 2L: We are in the backward path (L -> 0)
        
        folded_x = self.L - abs(mod_x - self.L)
        return folded_x

    def unfold(self, x_local: float, previous_x_global: float) -> float:
        """
        Predicts the next GLOBAL position based on a local move.
        This is tricky because x_local (0..L) loses the 'fold index' info.
        We need context (previous global position) to know which 'mirror' we are in.
        
        This is useful for tracking a particle moving through walls.
        """
        # Determine current fold index
        current_fold_index = int(previous_x_global // self.L)
        
        # Calculate candidates for the new global position
        # It could be in the same fold, or neighboring folds
        
        # TODO: This requires velocity vector to be accurate.
        # For static analysis, we usually Unfold a SEQUENCE.
        pass

    def calculate_straight_path(self, start: float, target: float, reflections: int) -> float:
        """
        Calculates the distance to a target in the 'Mirror World'.
        
        Args:
            start: Starting position in [0, L]
            target: Target position in [0, L]
            reflections: Which mirror image of the target are we aiming for?
                         0 = Direct line of sight
                         1 = First reflection (right wall)
                         -1 = First reflection (left wall)
                         
        Returns:
            The linear distance in unfolded space.
        """
        # Valid reflection indices create virtual targets at:
        # x_target_virtual = n*2L + target      (if n is even)
        # x_target_virtual = n*2L + (L-target)  (if n is odd) ??
        # Let's derive the exact Mirror Method formula.
        
        # Mirror 0: [0, L]   -> Target is at T
        # Mirror 1: [L, 2L]  -> This is a reflection of Mirror 0 across L.
        #                       Coordinate x maps to 2L - x.
        #                       So Target T maps to 2L - T.
        # Mirror 2: [2L, 3L] -> Reflection of Mirror 1 across 2L.
        #                       Equivalent to Mirror 0 shifted by 2L.
        #                       Target is at 2L + T.
        
        # Formula:
        # If n (reflections) is Even: Virtual = n*L + target
        # If n (reflections) is Odd:  Virtual = (n+1)*L - target 
        
        if reflections % 2 == 0:
            virtual_target = (reflections * self.L) + target
        else:
            virtual_target = ((reflections + 1) * self.L) - target
            
        return virtual_target - start

    @staticmethod
    def get_fold_index(x_infinite: float, L: float) -> int:
        """Returns which mirror dimension the point resides in."""
        return int(x_infinite // L)

def demonstrate_folding():
    """Simple proof of concept."""
    L = 10.0
    unfolder = SpaceUnfolder(L)
    
    print(f"--- 🌊 Unfolding Space (L={L}) ---")
    
    # Simulate a "Straight Line" in truth that looks like bouncing in perception
    # True intent: Go from 2.0 to 25.0 (Velocity +1)
    print("\n[Truth] Moving 0 -> 25 in Infinite Space:")
    true_path = np.linspace(0, 35, 10) # 0, 3.8, 7.7, ...
    
    for t, x_true in enumerate(true_path):
        x_perceived = unfolder.fold(x_true)
        fold_idx = SpaceUnfolder.get_fold_index(x_true, L)
        
        # Visualization
        # Unfolded: |..................*..................|
        # Folded:   |........*.| (bouncing)
        
        mirror_type = "Normal" if fold_idx % 2 == 0 else "Mirrored"
        wall_hit = "💥 WALL" if x_perceived == 0 or x_perceived == L else ""
        
        print(f"T={t}: True={x_true:5.1f} | Fold#{fold_idx} ({mirror_type}) | Perceived={x_perceived:5.1f} {wall_hit}")

if __name__ == "__main__":
    demonstrate_folding()
