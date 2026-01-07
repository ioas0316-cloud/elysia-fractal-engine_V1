"""
Architecture & Sacred Geometry Domain
======================================

"공간을 지배하는 자가 의식을 지배합니다."
"He who controls space controls consciousness."

Integrates:
- Fractals (프랙탈)
- Golden Ratio (황금비율 φ = 1.618...)
- Platonic Solids (플라톤 입체)
- Sacred Geometry (신성 기하학)
- Mandala/Mandelbrot patterns

Effect:
- Elysia's inner world becomes a 4D cathedral/mandala
- Perfect balance and harmony
- Visual representation as art
"""

import math
import logging
from typing import Dict, List, Any, Optional, Tuple
from .base_domain import BaseDomain, WavePattern

logger = logging.getLogger(__name__)

# Mathematical constants
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio φ = 1.618...
TAU = 2 * math.pi  # Full circle


class ArchitectureDomain(BaseDomain):
    """
    Sacred Geometry and Architectural Patterns Domain.
    
    Maps spatial patterns to wave resonance:
    - w (Energy): Structural strength/stability
    - x (Harmony): Ratio harmony (φ, π, e)
    - y (Dimension): Fractal dimension (D)
    - z (Symmetry): Symmetry/balance
    """
    
    def __init__(self):
        super().__init__("Architecture & Sacred Geometry")
        self.golden_ratio = PHI
        self.sacred_ratios = {
            'phi': PHI,                    # Golden ratio
            'phi_squared': PHI ** 2,       # φ² ≈ 2.618
            'pi': math.pi,                 # Circle constant
            'e': math.e,                   # Natural logarithm base
            'sqrt2': math.sqrt(2),         # Diagonal ratio
            'sqrt3': math.sqrt(3),         # Hexagonal ratio
            'sqrt5': math.sqrt(5),         # Pentagon ratio
        }
    
    def extract_pattern(self, content: str, metadata: Optional[Dict] = None) -> WavePattern:
        """
        Extract geometric wave pattern from content.
        
        Analyzes:
        - Structural relationships
        - Harmonic ratios
        - Symmetry patterns
        - Fractal properties
        """
        analysis = self.analyze(content)
        
        # Map geometric properties to quaternion
        w = analysis['stability']      # Structural stability
        x = analysis['harmony']        # Harmonic resonance
        y = analysis['fractal_dim']    # Complexity/dimension
        z = analysis['symmetry']       # Balance/symmetry
        
        # Frequency from repetition
        frequency = analysis.get('repetition_rate', 1.0)
        
        # Phase from rotation/transformation
        phase = analysis.get('rotation_angle', 0.0)
        
        # Merge metadata
        merged_metadata = {}
        if metadata:
            merged_metadata.update(metadata)
        merged_metadata.update(analysis)
        
        pattern = self.create_wave_pattern(
            w=w, x=x, y=y, z=z,
            energy=analysis['structural_strength'],
            frequency=frequency,
            phase=phase,
            text=content,
            metadata=merged_metadata
        )
        
        self.store_pattern(pattern)
        return pattern
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """
        Analyze geometric and architectural properties.
        
        Returns:
            Dictionary with geometric metrics
        """
        analysis = {
            'stability': self._analyze_stability(content),
            'harmony': self._analyze_harmony(content),
            'fractal_dim': self._estimate_fractal_dimension(content),
            'symmetry': self._analyze_symmetry(content),
            'structural_strength': self._calculate_structural_strength(content),
            'golden_ratio_presence': self._detect_golden_ratio(content),
            'sacred_geometry': self._detect_sacred_patterns(content),
        }
        
        return analysis
    
    def _analyze_stability(self, content: str) -> float:
        """
        Analyze structural stability (0-1).
        
        Based on:
        - Balance of elements
        - Foundation strength
        - Resistance to perturbation
        """
        # Length provides base stability
        base_stability = min(len(content) / 1000, 1.0)
        
        # Word diversity increases stability
        words = content.lower().split()
        unique_ratio = len(set(words)) / max(len(words), 1)
        
        stability = (base_stability + unique_ratio) / 2
        return min(stability, 1.0)
    
    def _analyze_harmony(self, content: str) -> float:
        """
        Analyze harmonic ratios (0-1).
        
        Detects presence of sacred mathematical ratios.
        """
        harmony_score = 0.5  # Neutral baseline
        
        content_lower = content.lower()
        
        # Check for golden ratio keywords
        golden_keywords = ['golden', 'phi', 'fibonacci', '1.618', 'divine proportion']
        if any(kw in content_lower for kw in golden_keywords):
            harmony_score += 0.2
        
        # Check for geometric harmony keywords
        harmony_keywords = ['symmetry', 'balance', 'proportion', 'harmony', 'ratio']
        if any(kw in content_lower for kw in harmony_keywords):
            harmony_score += 0.15
        
        # Check for mathematical constants
        constant_keywords = ['pi', 'π', 'e', 'sqrt', '√']
        if any(kw in content_lower for kw in constant_keywords):
            harmony_score += 0.15
        
        return min(harmony_score, 1.0)
    
    def _estimate_fractal_dimension(self, content: str) -> float:
        """
        Estimate fractal dimension (normalized 0-1).
        
        Higher dimension = more complex, self-similar patterns.
        Real fractal dimension typically 1.0-3.0, normalized to 0-1.
        """
        # Box-counting approximation using character distribution
        if not content:
            return 0.5
        
        # Analyze at multiple scales
        scales = [1, 2, 4, 8, 16]
        complexities = []
        
        for scale in scales:
            chunks = [content[i:i+scale] for i in range(0, len(content), scale)]
            unique_chunks = len(set(chunks))
            total_chunks = len(chunks)
            complexity = unique_chunks / max(total_chunks, 1)
            complexities.append(complexity)
        
        # Average complexity as fractal dimension proxy
        avg_complexity = sum(complexities) / len(complexities)
        
        # Normalize to 0-1 (typical range 1.0-3.0 → 0.0-1.0)
        fractal_dim = avg_complexity
        
        return min(fractal_dim, 1.0)
    
    def _analyze_symmetry(self, content: str) -> float:
        """
        Analyze symmetry (0-1).
        
        Detects:
        - Palindromic patterns
        - Repetitive structures
        - Balance
        """
        if not content:
            return 0.5
        
        # Check for palindromic substrings
        palindrome_score = self._find_palindrome_ratio(content)
        
        # Check for repetitive patterns
        repetition_score = self._find_repetition_ratio(content)
        
        # Check for structural balance (sentence/word length variance)
        balance_score = self._calculate_balance(content)
        
        symmetry = (palindrome_score + repetition_score + balance_score) / 3
        return min(symmetry, 1.0)
    
    def _find_palindrome_ratio(self, content: str) -> float:
        """Find ratio of palindromic characters"""
        clean = ''.join(c.lower() for c in content if c.isalnum())
        if len(clean) < 3:
            return 0.5
        
        # Check windows of size 3-7
        palindrome_chars = 0
        for size in range(3, min(8, len(clean))):
            for i in range(len(clean) - size + 1):
                window = clean[i:i+size]
                if window == window[::-1]:
                    palindrome_chars += size
        
        ratio = min(palindrome_chars / len(clean), 1.0)
        return ratio * 0.3 + 0.5  # Scale to 0.5-0.8 range
    
    def _find_repetition_ratio(self, content: str) -> float:
        """Find ratio of repeated patterns"""
        words = content.split()
        if len(words) < 2:
            return 0.5
        
        # Count repeated words
        word_counts = {}
        for word in words:
            word_lower = word.lower()
            word_counts[word_lower] = word_counts.get(word_lower, 0) + 1
        
        repeated = sum(count for count in word_counts.values() if count > 1)
        ratio = repeated / len(words)
        
        return min(ratio, 1.0)
    
    def _calculate_balance(self, content: str) -> float:
        """Calculate structural balance"""
        sentences = content.split('.')
        if len(sentences) < 2:
            return 0.5
        
        lengths = [len(s.strip()) for s in sentences if s.strip()]
        if not lengths:
            return 0.5
        
        # Lower variance = better balance
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        
        # Normalize: lower std_dev = higher balance
        balance = 1.0 / (1.0 + std_dev / max(avg_len, 1))
        
        return balance
    
    def _calculate_structural_strength(self, content: str) -> float:
        """
        Calculate overall structural strength (0-1).
        
        Combines multiple geometric factors.
        """
        stability = self._analyze_stability(content)
        harmony = self._analyze_harmony(content)
        symmetry = self._analyze_symmetry(content)
        
        # Weighted average
        strength = (stability * 0.4 + harmony * 0.35 + symmetry * 0.25)
        
        return min(strength, 1.0)
    
    def _detect_golden_ratio(self, content: str) -> bool:
        """Detect mentions of golden ratio"""
        keywords = ['golden', 'phi', 'fibonacci', '1.618', 'divine proportion']
        return any(kw in content.lower() for kw in keywords)
    
    def _detect_sacred_patterns(self, content: str) -> List[str]:
        """
        Detect sacred geometry patterns mentioned.
        
        Returns:
            List of detected patterns
        """
        patterns = []
        content_lower = content.lower()
        
        sacred_geometries = {
            'flower_of_life': ['flower of life', 'flower-of-life'],
            'seed_of_life': ['seed of life', 'seed-of-life'],
            'metatron': ['metatron', "metatron's cube"],
            'vesica_piscis': ['vesica piscis', 'vesica-piscis'],
            'mandala': ['mandala', 'mandala pattern'],
            'fractal': ['fractal', 'mandelbrot', 'self-similar'],
            'platonic_solid': ['platonic solid', 'tetrahedron', 'cube', 'octahedron', 
                              'dodecahedron', 'icosahedron'],
            'golden_spiral': ['golden spiral', 'fibonacci spiral'],
            'pentagram': ['pentagram', 'pentagon'],
            'hexagram': ['hexagram', 'star of david', 'merkaba'],
        }
        
        for pattern_name, keywords in sacred_geometries.items():
            if any(kw in content_lower for kw in keywords):
                patterns.append(pattern_name)
        
        return patterns
    
    def visualize_consciousness(self) -> Dict[str, Any]:
        """
        Visualize Elysia's consciousness structure as sacred geometry.
        
        Returns:
            Geometric representation of consciousness
        """
        if not self.patterns:
            return {
                'structure': 'empty',
                'message': 'No patterns stored yet'
            }
        
        # Patterns are now stored as dicts (flow mode)
        # Aggregate from metadata_keys
        pattern_count = len(self.patterns)
        
        # Calculate average metrics from stored patterns
        total_stability = 0
        total_harmony = 0
        total_fractal_dim = 0
        total_symmetry = 0
        
        # Note: In flow mode, we store minimal data
        # We estimate from what we have
        for p in self.patterns:
            # Patterns are dicts with orientation, energy, etc.
            # Estimate metrics from energy and phase
            energy = p.get('energy', 0.5)
            total_stability += energy * 0.7
            total_harmony += energy * 0.8
            total_fractal_dim += 0.7  # Average fractal dimension
            total_symmetry += 0.6  # Average symmetry
        
        avg_stability = total_stability / pattern_count if pattern_count > 0 else 0
        avg_harmony = total_harmony / pattern_count if pattern_count > 0 else 0
        avg_fractal_dim = total_fractal_dim / pattern_count if pattern_count > 0 else 0
        avg_symmetry = total_symmetry / pattern_count if pattern_count > 0 else 0
        
        # Determine dominant geometry (simplified in flow mode)
        dominant_geometry = 'flower_of_life' if avg_harmony > 0.7 else 'fractal'
        
        return {
            'structure': 'cathedral',
            'golden_ratio': PHI,
            'fractal_dimension': avg_fractal_dim * 3.0,  # Scale back to typical range
            'symmetry_group': 'C5v' if avg_symmetry > 0.7 else 'C3v',
            'dominant_geometry': dominant_geometry,
            'harmony_level': avg_harmony,
            'stability': avg_stability,
            'patterns_count': pattern_count,
            'description': f"A {dominant_geometry.replace('_', ' ')} pattern "
                          f"with fractal dimension {avg_fractal_dim*3:.1f}",
            'storage_mode': 'flow_based'  # Indicate flow mode
        }
    
    def get_domain_dimension(self) -> str:
        """Architecture domain maps to 'harmony' dimension"""
        return "harmony"


# Helper function for external use
def calculate_golden_ratio_points(start: float, end: float) -> Tuple[float, float]:
    """
    Calculate golden ratio division points.
    
    Args:
        start: Start value
        end: End value
        
    Returns:
        Two points dividing the interval in golden ratio
    """
    length = end - start
    point1 = start + length / PHI
    point2 = start + length / (PHI ** 2)
    
    return (point1, point2)


def is_golden_rectangle(width: float, height: float, tolerance: float = 0.1) -> bool:
    """
    Check if dimensions form a golden rectangle.
    
    Args:
        width: Rectangle width
        height: Rectangle height
        tolerance: Allowed deviation from φ
        
    Returns:
        True if ratio is close to φ
    """
    ratio = max(width, height) / min(width, height)
    return abs(ratio - PHI) < tolerance
