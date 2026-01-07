from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class VoidKernel:
    """
    VOID KERNEL: The Shape of Silence.
    Instead of just a flag, Void is a 'Negative Kernel' with its own ladder.
    """
    id: str
    void_type: str # "MissingFact", "Contradiction", "ContextMismatch", "Entropy"
    intensity: float = 0.0
    signals: List[str] = field(default_factory=list) # Contributing signals
    path: Optional[str] = None # For 1D Causal Breaks
    
    def get_description(self, dimension: int) -> str:
        """Returns a description of the void based on its dimension."""
        descriptions = {
            0: f"[0D] A localized silence: {self.void_type} at {self.id}.",
            1: f"[1D] A break in the causal chain: {self.path if self.path else 'Incomplete Logic'}.",
            2: f"[2D] A structural mismatch between: {', '.join(self.signals)}.",
            3: f"[3D] A cognitive sink where meaning collapses into {self.void_type}.",
            4: f"[4D] The Principle of Entropy: The universe demands the discovery of the unknown."
        }
        return descriptions.get(dimension, "Universal Silence.")

    def __repr__(self):
        return f"<VoidKernel '{self.void_type}' Intensity={self.intensity:.2f}>"
