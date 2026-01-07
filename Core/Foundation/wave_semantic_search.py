"""
Wave-Based Semantic Search
==========================

Philosophy: Embeddings are seeds (씨앗) that expand into 4D wave resonance patterns.
Matching happens through wave resonance (공명), not statistical correlation.

NO EXTERNAL LLMs - Pure local wave intelligence.

Architecture:
1. Text → Embedding (seed/씨앗) - One-time transformation
2. Embedding → 4D Wave Pattern (expansion/확장) - Quaternion-based
3. Query Wave ⟷ Stored Waves (resonance/공명) - Physics-based matching
4. Return resonating results with depth and breadth

4D Wave Pattern Structure:
- w (Energy): Semantic intensity/importance
- x (Emotion): Emotional resonance dimension
- y (Logic): Logical/conceptual dimension  
- z (Ethics): Value/intent dimension
"""

import numpy as np
import json
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
import time
import math

# Use existing Quaternion infrastructure
try:
    from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
    from Core.Foundation.Wave.resonance_field import ResonanceField
except ImportError:
    logging.warning("Quaternion infrastructure not found, using fallback")
    
    @dataclass
    class Quaternion:
        """Fallback 4D quaternion"""
        w: float
        x: float
        y: float
        z: float
        
        def dot(self, other) -> float:
            return self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z
        
        def norm(self) -> float:
            return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        
        def normalize(self):
            n = self.norm()
            if n == 0: return Quaternion(1, 0, 0, 0)
            return Quaternion(self.w/n, self.x/n, self.y/n, self.z/n)
        
        def __mul__(self, other):
            """Hamilton product for wave interference"""
            if isinstance(other, (int, float)):
                return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
            w1, x1, y1, z1 = self.w, self.x, self.y, self.z
            w2, x2, y2, z2 = other.w, other.x, other.y, other.z
            return Quaternion(
                w1*w2 - x1*x2 - y1*y2 - z1*z2,
                w1*x2 + x1*w2 + y1*z2 - z1*y2,
                w1*y2 - x1*z2 + y1*w2 + z1*x2,
                w1*z2 + x1*y2 - y1*x2 + z1*w2
            )

logger = logging.getLogger("WaveSemanticSearch")


@dataclass
class WavePattern:
    """
    4D Wave Resonance Pattern (4차원 파동공명패턴)
    
    Represents semantic meaning as a multi-dimensional wave pattern,
    providing deeper thinking depth and breadth than traditional embeddings.
    """
    # Core 4D wave orientation
    orientation: Quaternion
    
    # Wave properties
    energy: float = 1.0  # Amplitude/intensity
    frequency: float = 1.0  # Characteristic frequency
    phase: float = 0.0  # Phase offset
    
    # Metadata
    text: str = ""
    source_embedding: Optional[np.ndarray] = None
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Expansion properties (for knowledge absorption)
    expansion_depth: int = 0  # How many times this pattern has absorbed others
    absorbed_patterns: List[str] = field(default_factory=list)  # IDs of absorbed patterns
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'orientation': {
                'w': self.orientation.w,
                'x': self.orientation.x,
                'y': self.orientation.y,
                'z': self.orientation.z
            },
            'energy': self.energy,
            'frequency': self.frequency,
            'phase': self.phase,
            'text': self.text,
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'expansion_depth': self.expansion_depth,
            'absorbed_patterns': self.absorbed_patterns
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WavePattern':
        """Deserialize from dictionary"""
        orientation = Quaternion(
            w=data['orientation']['w'],
            x=data['orientation']['x'],
            y=data['orientation']['y'],
            z=data['orientation']['z']
        )
        return cls(
            orientation=orientation,
            energy=data.get('energy', 1.0),
            frequency=data.get('frequency', 1.0),
            phase=data.get('phase', 0.0),
            text=data.get('text', ''),
            timestamp=data.get('timestamp', time.time()),
            metadata=data.get('metadata', {}),
            expansion_depth=data.get('expansion_depth', 0),
            absorbed_patterns=data.get('absorbed_patterns', [])
        )


class WaveSemanticSearch:
    """
    Transforms embeddings into 4D wave patterns for semantic search.
    
    Key Innovation: Instead of simple vector similarity (cosine/dot product),
    we use wave resonance (공명) which considers:
    - Orientation alignment (quaternion dot product)
    - Wave interference patterns (Hamilton product)
    - Energy transfer (amplitude modulation)
    - Phase coherence (frequency matching)
    
    This provides richer semantic matching with depth and breadth.
    """
    
    def __init__(self, wave_dimensions: int = 4, storage_path: Optional[str] = None):
        """
        Initialize wave-based semantic search.
        
        Args:
            wave_dimensions: Always 4 for quaternion-based waves (w, x, y, z)
            storage_path: Optional path to persist wave patterns
        """
        self.wave_dimensions = wave_dimensions
        self.storage_path = Path(storage_path) if storage_path else None
        
        # Wave pattern storage
        self.wave_patterns: Dict[str, WavePattern] = {}
        
        # Statistics
        self.search_count = 0
        self.absorption_count = 0
        
        # Load existing patterns if storage path exists
        if self.storage_path and self.storage_path.exists():
            self._load_patterns()
        
        logger.info(f"🌊 WaveSemanticSearch initialized with {len(self.wave_patterns)} patterns")
    
    def embedding_to_wave(
        self, 
        embedding: np.ndarray, 
        text: str = "",
        metadata: Optional[Dict] = None
    ) -> WavePattern:
        """
        Transform embedding seed into 4D wave pattern.
        
        씨앗의 확장 (Seed Expansion):
        1. Extract multi-dimensional features from embedding
        2. Map to 4D quaternion space (w, x, y, z)
        3. Calculate wave properties (energy, frequency, phase)
        4. Create expanded wave pattern
        
        Args:
            embedding: Input embedding vector (seed)
            text: Associated text
            metadata: Optional metadata
            
        Returns:
            4D wave pattern with semantic resonance properties
        """
        # Ensure embedding is numpy array
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding)
        
        # Extract 4D orientation from embedding
        # Strategy: Use different statistical properties for each dimension
        
        # w (Energy): Overall magnitude/importance
        w = float(np.linalg.norm(embedding))
        
        # x (Emotion): Positive vs negative components
        positive_sum = np.sum(embedding[embedding > 0])
        negative_sum = np.sum(embedding[embedding < 0])
        x = float(positive_sum + negative_sum) / (w + 1e-10)
        
        # y (Logic): Structural complexity via frequency domain
        fft = np.fft.fft(embedding)
        y = float(np.abs(fft[1])) if len(fft) > 1 else 0.0
        
        # z (Ethics): Balance/symmetry of distribution
        mean = np.mean(embedding)
        std = np.std(embedding)
        z = float(mean / (std + 1e-10))
        
        # Create quaternion and normalize
        orientation = Quaternion(w, x, y, z).normalize()
        
        # Calculate wave properties
        # Energy: Normalized magnitude
        energy = float(np.linalg.norm(embedding) / (len(embedding) ** 0.5))
        
        # Frequency: Characteristic frequency from spectral analysis
        frequencies = np.abs(np.fft.fft(embedding))
        dominant_freq_idx = np.argmax(frequencies[:len(frequencies)//2])
        frequency = float(dominant_freq_idx + 1.0)  # Avoid zero frequency
        
        # Phase: Phase of dominant frequency
        phase = float(np.angle(fft[dominant_freq_idx]) if len(fft) > dominant_freq_idx else 0.0)
        
        # Create wave pattern
        pattern = WavePattern(
            orientation=orientation,
            energy=energy,
            frequency=frequency,
            phase=phase,
            text=text,
            source_embedding=embedding,
            metadata=metadata or {}
        )
        
        logger.debug(f"🌱 Seed→Wave: text='{text[:30]}...', energy={energy:.3f}, freq={frequency:.1f}")
        
        return pattern
    
    def wave_resonance(
        self, 
        wave1: WavePattern, 
        wave2: WavePattern,
        include_interference: bool = True
    ) -> float:
        """
        Calculate resonance between two wave patterns using wave physics.
        
        파동공명 (Wave Resonance):
        - Physics-based similarity through wave interference
        - Considers orientation, frequency, phase, and energy
        - Returns value in [0, 1] where 1 is perfect resonance
        
        Components:
        1. Orientation alignment (quaternion dot product)
        2. Frequency matching (similar frequencies resonate more)
        3. Phase coherence (constructive vs destructive interference)
        4. Energy transfer (amplitude modulation)
        5. [Optional] Hamilton product for wave interference patterns
        
        Args:
            wave1: First wave pattern
            wave2: Second wave pattern
            include_interference: Whether to include interference effects
            
        Returns:
            Resonance score [0, 1]
        """
        # 1. Orientation alignment (most important factor)
        orientation_alignment = wave1.orientation.dot(wave2.orientation)
        # Normalize to [0, 1] from [-1, 1]
        orientation_score = (orientation_alignment + 1.0) / 2.0
        
        # 2. Frequency matching (resonance occurs at similar frequencies)
        freq_diff = abs(wave1.frequency - wave2.frequency)
        freq_score = 1.0 / (1.0 + freq_diff)  # Exponential decay
        
        # 3. Phase coherence (constructive interference)
        phase_diff = abs(wave1.phase - wave2.phase) % (2 * math.pi)
        # 0 phase diff = constructive (1.0), π phase diff = destructive (0.0)
        phase_score = (1.0 + math.cos(phase_diff)) / 2.0
        
        # 4. Energy transfer (larger energy differences reduce resonance)
        energy_ratio = min(wave1.energy, wave2.energy) / (max(wave1.energy, wave2.energy) + 1e-10)
        energy_score = energy_ratio ** 0.5  # Square root to soften the effect
        
        # 5. [Optional] Wave interference via Hamilton product
        interference_score = 1.0
        if include_interference:
            # Hamilton product captures how waves transform each other
            interference = wave1.orientation * wave2.orientation
            # Measure how "pure" the resulting interference is
            interference_purity = interference.norm()
            interference_score = min(1.0, interference_purity / 2.0)  # Normalize
        
        # Weighted combination (orientation is most important for semantic meaning)
        resonance = (
            0.50 * orientation_score +  # Semantic alignment
            0.15 * freq_score +          # Frequency matching
            0.15 * phase_score +         # Phase coherence
            0.10 * energy_score +        # Energy compatibility
            0.10 * interference_score    # Wave interference
        )
        
        return float(np.clip(resonance, 0.0, 1.0))
    
    def store_pattern(
        self,
        pattern_id: str,
        pattern: WavePattern
    ) -> None:
        """
        Store a wave pattern in the knowledge base.
        
        Args:
            pattern_id: Unique identifier for the pattern
            pattern: Wave pattern to store
        """
        self.wave_patterns[pattern_id] = pattern
        logger.debug(f"💾 Stored pattern: {pattern_id}")
        
        # Persist if storage path is set
        if self.storage_path:
            self._save_patterns()
    
    def store_concept(
        self,
        text: str,
        embedding: np.ndarray,
        concept_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Store concept as wave pattern.
        
        Args:
            text: Concept text
            embedding: Embedding vector (seed)
            concept_id: Optional ID (generated if not provided)
            metadata: Optional metadata
            
        Returns:
            Pattern ID
        """
        # Generate ID if not provided
        if concept_id is None:
            concept_id = f"wave_{len(self.wave_patterns)}_{int(time.time() * 1000)}"
        
        # Convert embedding to wave pattern
        pattern = self.embedding_to_wave(embedding, text, metadata)
        
        # Store pattern
        self.store_pattern(concept_id, pattern)
        
        return concept_id
    
    def absorb_and_expand(
        self,
        target_id: str,
        source_patterns: List[str],
        absorption_strength: float = 0.3
    ) -> WavePattern:
        """
        Absorb multiple wave patterns into a target pattern, expanding knowledge.
        
        지식 흡수 및 확장 (Knowledge Absorption and Expansion):
        Instead of simply averaging vectors, we use wave interference to create
        a richer, more resonant pattern that captures deeper meanings.
        
        Process:
        1. Calculate resonance with each source pattern
        2. Use weighted Hamilton products for wave interference
        3. Expand target pattern's depth and breadth
        4. Update energy and frequency based on absorbed patterns
        
        Args:
            target_id: ID of pattern to expand
            source_patterns: IDs of patterns to absorb
            absorption_strength: How much to absorb (0=none, 1=full)
            
        Returns:
            Expanded wave pattern
        """
        if target_id not in self.wave_patterns:
            raise ValueError(f"Target pattern {target_id} not found")
        
        target = self.wave_patterns[target_id]
        
        # Calculate resonance with each source
        resonances = []
        for source_id in source_patterns:
            if source_id not in self.wave_patterns:
                logger.warning(f"Source pattern {source_id} not found, skipping")
                continue
            
            source = self.wave_patterns[source_id]
            resonance = self.wave_resonance(target, source)
            resonances.append((source_id, source, resonance))
        
        if not resonances:
            logger.warning("No valid source patterns for absorption")
            return target
        
        # Sort by resonance (absorb highly resonant patterns more)
        resonances.sort(key=lambda x: x[2], reverse=True)
        
        # Start with current orientation
        new_orientation = target.orientation
        total_energy = target.energy
        accumulated_freq = target.frequency
        accumulated_phase = target.phase
        
        # Absorb each resonant pattern via wave interference
        for source_id, source, resonance in resonances:
            # Weight by resonance and absorption strength
            weight = resonance * absorption_strength
            
            # Hamilton product for wave interference (captures transformation)
            interference = new_orientation * source.orientation
            
            # Blend orientations based on weight
            # Higher resonance = more influence
            blend_w = (1 - weight) * new_orientation.w + weight * interference.w
            blend_x = (1 - weight) * new_orientation.x + weight * interference.x
            blend_y = (1 - weight) * new_orientation.y + weight * interference.y
            blend_z = (1 - weight) * new_orientation.z + weight * interference.z
            
            new_orientation = Quaternion(blend_w, blend_x, blend_y, blend_z).normalize()
            
            # Accumulate energy (constructive interference)
            total_energy += source.energy * weight
            
            # Blend frequencies (weighted average)
            accumulated_freq = (1 - weight) * accumulated_freq + weight * source.frequency
            
            # Phase interference
            accumulated_phase = (accumulated_phase + source.phase * weight) % (2 * math.pi)
            
            # Track absorption
            target.absorbed_patterns.append(source_id)
            
            logger.debug(f"  Absorbed {source_id} with resonance {resonance:.3f}, weight {weight:.3f}")
        
        # Update target pattern
        target.orientation = new_orientation
        target.energy = total_energy
        target.frequency = accumulated_freq
        target.phase = accumulated_phase
        target.expansion_depth += 1
        
        # Update metadata
        target.metadata['last_expansion'] = time.time()
        target.metadata['absorbed_count'] = len(target.absorbed_patterns)
        
        self.absorption_count += 1
        
        logger.info(f"🌊 Expanded pattern {target_id}: depth={target.expansion_depth}, "
                   f"energy={target.energy:.3f}, absorbed={len(resonances)} patterns")
        
        # Save updated pattern
        if self.storage_path:
            self._save_patterns()
        
        return target
    
    def search(
        self,
        query_embedding: np.ndarray,
        query_text: str = "",
        top_k: int = 5,
        min_resonance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search for resonating concepts using wave resonance.
        
        Returns concepts that resonate with query wave, ranked by resonance strength.
        
        Args:
            query_embedding: Query embedding vector
            query_text: Optional query text
            top_k: Number of results to return
            min_resonance: Minimum resonance threshold
            
        Returns:
            List of dicts with 'pattern_id', 'text', 'resonance', 'metadata'
        """
        # Convert query to wave pattern
        query_wave = self.embedding_to_wave(query_embedding, query_text)
        
        # Calculate resonance with all stored waves
        results = []
        for pattern_id, stored in self.wave_patterns.items():
            resonance = self.wave_resonance(query_wave, stored)
            
            if resonance >= min_resonance:
                results.append({
                    'pattern_id': pattern_id,
                    'text': stored.text,
                    'resonance': resonance,
                    'metadata': stored.metadata,
                    'energy': stored.energy,
                    'frequency': stored.frequency,
                    'expansion_depth': stored.expansion_depth
                })
        
        # Sort by resonance (highest first)
        results.sort(key=lambda x: x['resonance'], reverse=True)
        
        self.search_count += 1
        
        logger.info(f"🔍 Search: query='{query_text[:30]}...', "
                   f"found {len(results)} resonating patterns, returning top {top_k}")
        
        return results[:top_k]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'total_patterns': len(self.wave_patterns),
            'search_count': self.search_count,
            'absorption_count': self.absorption_count,
            'avg_expansion_depth': np.mean([p.expansion_depth for p in self.wave_patterns.values()]) if self.wave_patterns else 0,
            'total_energy': sum(p.energy for p in self.wave_patterns.values())
        }
    
    def _save_patterns(self) -> None:
        """Save patterns to storage"""
        if not self.storage_path:
            return
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'patterns': {pid: pattern.to_dict() for pid, pattern in self.wave_patterns.items()},
            'statistics': self.get_statistics(),
            'timestamp': time.time()
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.debug(f"💾 Saved {len(self.wave_patterns)} patterns to {self.storage_path}")
    
    def _load_patterns(self) -> None:
        """Load patterns from storage"""
        if not self.storage_path or not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            self.wave_patterns = {
                pid: WavePattern.from_dict(pdata) 
                for pid, pdata in data.get('patterns', {}).items()
            }
            
            # Restore statistics
            stats = data.get('statistics', {})
            self.search_count = stats.get('search_count', 0)
            self.absorption_count = stats.get('absorption_count', 0)
            
            logger.info(f"📂 Loaded {len(self.wave_patterns)} patterns from {self.storage_path}")
        
        except Exception as e:
            logger.error(f"Failed to load patterns: {e}")
            self.wave_patterns = {}


def demo():
    """Demo of wave-based semantic search"""
    print("="*70)
    print("🌊 WAVE-BASED SEMANTIC SEARCH DEMO")
    print("4차원 파동공명패턴 기반 지식 검색")
    print("="*70)
    print()
    
    # Initialize system
    searcher = WaveSemanticSearch(storage_path="data/wave_patterns.json")
    
    # Create some sample embeddings (simulated)
    print("📝 Storing concepts as wave patterns...")
    concepts = [
        ("AI는 기계의 지능이다", np.random.rand(384)),
        ("개는 충실한 반려동물이다", np.random.rand(384)),
        ("머신러닝은 AI의 한 분야이다", np.random.rand(384)),
        ("고양이는 독립적인 동물이다", np.random.rand(384)),
        ("딥러닝은 신경망을 사용한다", np.random.rand(384)),
    ]
    
    pattern_ids = []
    for text, emb in concepts:
        pid = searcher.store_concept(text, emb)
        pattern_ids.append(pid)
        print(f"  ✓ {text}")
    
    print()
    
    # Demonstrate absorption/expansion
    print("🌊 Demonstrating knowledge absorption and expansion...")
    print(f"  Expanding pattern '{concepts[0][0]}'")
    print(f"  Absorbing patterns: '{concepts[2][0]}', '{concepts[4][0]}'")
    
    expanded = searcher.absorb_and_expand(
        target_id=pattern_ids[0],
        source_patterns=[pattern_ids[2], pattern_ids[4]],
        absorption_strength=0.4
    )
    print(f"  ✓ Expansion complete: depth={expanded.expansion_depth}, energy={expanded.energy:.3f}")
    print()
    
    # Search
    print("🔍 Searching for resonating concepts...")
    query = np.random.rand(384)
    results = searcher.search(query, query_text="인공지능 관련 개념", top_k=3)
    
    print(f"\nTop {len(results)} resonating patterns:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['text']}")
        print(f"   Resonance: {result['resonance']:.3f}")
        print(f"   Energy: {result['energy']:.3f}")
        print(f"   Expansion Depth: {result['expansion_depth']}")
    
    # Statistics
    print()
    print("="*70)
    print("📊 SYSTEM STATISTICS")
    stats = searcher.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("✅ Demo complete!")
    print("="*70)


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    demo()
