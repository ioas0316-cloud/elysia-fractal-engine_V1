"""
Base Domain Class
=================

Base class for all knowledge domains in the P4.5 expansion.
Each domain extracts specific wave patterns from knowledge.

Philosophy:
- All knowledge is wave patterns (파동 패턴)
- Different domains resonate at different frequencies
- Cross-domain resonance creates deeper understanding
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import logging

try:
    from Core.Foundation.wave_semantic_search import WavePattern
    from Core.Foundation.hyper_quaternion import Quaternion
except ImportError:
    # Fallback for testing
    @dataclass
    class WavePattern:
        orientation: 'Quaternion'
        energy: float = 1.0
        frequency: float = 1.0
        phase: float = 0.0
        text: str = ""
        metadata: Dict[str, Any] = None
        
    @dataclass
    class Quaternion:
        w: float
        x: float
        y: float
        z: float

logger = logging.getLogger(__name__)


class BaseDomain(ABC):
    """
    Base class for all knowledge domains.
    
    Each domain:
    1. Extracts domain-specific patterns
    2. Converts to 4D wave patterns
    3. Integrates with P2.2 Wave Knowledge System
    """
    
    def __init__(self, name: str):
        self.name = name
        self.patterns = []
        logger.info(f"🌟 {name} Domain initialized")
    
    @abstractmethod
    def extract_pattern(self, content: str, metadata: Optional[Dict] = None) -> WavePattern:
        """
        Extract domain-specific wave pattern from content.
        
        Args:
            content: Text or data to analyze
            metadata: Optional metadata about the content
            
        Returns:
            WavePattern with domain-specific orientation
        """
        pass
    
    @abstractmethod
    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Perform domain-specific analysis.
        
        Args:
            content: Content to analyze
            
        Returns:
            Analysis results as dictionary
        """
        pass
    
    def get_domain_dimension(self) -> str:
        """
        Get the primary dimension this domain maps to.
        
        Returns:
            Dimension name: 'symbol', 'harmony', 'strategy', 'pattern', 'archetype'
        """
        return "generic"
    
    def create_wave_pattern(
        self,
        w: float,
        x: float, 
        y: float,
        z: float,
        energy: float = 1.0,
        frequency: float = 1.0,
        phase: float = 0.0,
        text: str = "",
        metadata: Optional[Dict] = None
    ) -> WavePattern:
        """
        Create a wave pattern with normalized quaternion orientation.
        
        Args:
            w, x, y, z: Quaternion components
            energy: Wave energy/intensity
            frequency: Wave frequency
            phase: Wave phase
            text: Associated text
            metadata: Additional metadata
            
        Returns:
            WavePattern instance
        """
        import math
        
        # Normalize quaternion
        norm = math.sqrt(w*w + x*x + y*y + z*z)
        if norm < 1e-6:
            norm = 1.0
        
        orientation = Quaternion(
            w=w/norm,
            x=x/norm,
            y=y/norm,
            z=z/norm
        )
        
        return WavePattern(
            orientation=orientation,
            energy=energy,
            frequency=frequency,
            phase=phase,
            text=text,
            metadata=metadata or {}
        )
    
    def store_pattern(self, pattern: WavePattern):
        """
        Store pattern in domain memory (FLOW MODE).
        
        Stores only wave signature, not raw text.
        Follows "빛과 물의 원리" - data flows, only patterns remain.
        """
        # Store minimal pattern info - NO RAW TEXT
        minimal_pattern = {
            'orientation': {
                'w': pattern.orientation.w,
                'x': pattern.orientation.x,
                'y': pattern.orientation.y,
                'z': pattern.orientation.z
            },
            'energy': pattern.energy,
            'frequency': pattern.frequency,
            'phase': pattern.phase,
            'text_hash': hash(pattern.text) if pattern.text else None,  # Hash only
            'timestamp': getattr(pattern, 'timestamp', None),
            'metadata_keys': list(pattern.metadata.keys()) if pattern.metadata else []
            # NO full 'text' stored!
        }
        self.patterns.append(minimal_pattern)
        logger.debug(f"Stored resonance pattern in {self.name} (hash: {minimal_pattern['text_hash']})")
    
    def query_patterns(self, query: str, top_k: int = 5) -> List[WavePattern]:
        """
        Query stored patterns (simplified version).
        
        In full implementation, this would use wave resonance matching.
        """
        # Simple text matching for now
        matches = [p for p in self.patterns if query.lower() in p.text.lower()]
        return matches[:top_k]
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', patterns={len(self.patterns)})"
