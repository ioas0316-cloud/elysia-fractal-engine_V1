from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CognitiveResult:
    mode: str       # "1D: Linear", "2D: Structural", etc.
    output: str     # The thought content
    metadata: Dict[str, Any] # Proof of process (path, vectors, etc.)
