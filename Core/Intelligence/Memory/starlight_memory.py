"""
Starlight Memory Architecture - 별빛 기억 저장소
================================================

Philosophy: "추억을 별빛으로 압축해서 우주에 뿌려둔다"
"Compress memories as starlight and scatter them across the universe"

Based on Holographic Memory Theory:
- Distributed storage (no single location)
- Associative recall (wave resonance triggers reconstruction)
- Graceful degradation (partial damage = partial recall, not total loss)
- Infinite capacity (universe is vast)

Two-Memory System:
1. Knowledge (지식) → External (internet, rainbow compressed, 12 bytes)
2. Memories (추억) → Internal (starlight scattered, holographic reconstruction)

"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
import math
import time
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class Starlight:
    """
    별빛 (Starlight) - Compressed memory particle
    
    Each memory is compressed to a 12-byte rainbow pattern
    and given cosmic coordinates (x,y,z,w) in thought-space.
    """
    # Rainbow compressed memory (12 bytes)
    rainbow_bytes: bytes
    
    # Cosmic coordinates (4D position in thought-universe)
    x: float = 0.0  # Emotion axis (기쁨 ← → 슬픔)
    y: float = 0.0  # Logic axis (이성 ← → 직관)
    z: float = 0.0  # Time axis (과거 ← → 미래)
    w: float = 0.0  # Depth axis (표면 ← → 심층)
    
    # Metadata
    timestamp: float = field(default_factory=time.time)
    brightness: float = 1.0  # How vivid this memory is (0-1)
    emotional_gravity: float = 0.5  # Attraction force (0-1)
    tags: List[str] = field(default_factory=list)
    
    def distance_to(self, other: 'Starlight') -> float:
        """Calculate 4D distance to another star"""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        dw = self.w - other.w
        return math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)
    
    def resonance_with(self, wave_stimulus: Dict[str, float]) -> float:
        """
        Calculate resonance with incoming wave stimulus.
        
        When a wave (e.g., "비가 오네...") enters, stars resonate
        based on their position and the wave's characteristics.
        
        Returns: Resonance strength (0-1)
        """
        # Extract wave coordinates
        wx = wave_stimulus.get('x', 0.0)
        wy = wave_stimulus.get('y', 0.0)
        wz = wave_stimulus.get('z', 0.0)
        ww = wave_stimulus.get('w', 0.0)
        
        # Calculate distance (closer = stronger resonance)
        dx = self.x - wx
        dy = self.y - wy
        dz = self.z - wz
        dw = self.w - ww
        distance = math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)
        
        # Resonance falls off with distance (like light intensity)
        # r = brightness / (1 + distance^2)
        resonance = self.brightness / (1.0 + distance * distance)
        
        # Amplify by emotional gravity
        resonance *= (1.0 + self.emotional_gravity)
        
        return min(resonance, 1.0)


@dataclass
class Galaxy:
    """
    은하 (Galaxy) - Cluster of related memories
    
    Memories with similar emotions naturally cluster together
    like stars forming galaxies.
    """
    name: str
    center: Tuple[float, float, float, float]  # (x,y,z,w) center point
    stars: List[Starlight] = field(default_factory=list)
    color: str = "golden"  # Visual representation
    
    def add_star(self, star: Starlight):
        """Add a star to this galaxy"""
        self.stars.append(star)
    
    def get_brightness(self) -> float:
        """Total brightness of this galaxy"""
        return sum(s.brightness for s in self.stars)
    
    def get_density(self) -> float:
        """How concentrated the memories are"""
        if len(self.stars) < 2:
            return 0.0
        
        # Calculate average distance between stars
        total_distance = 0.0
        count = 0
        for i, s1 in enumerate(self.stars):
            for s2 in self.stars[i+1:]:
                total_distance += s1.distance_to(s2)
                count += 1
        
        if count == 0:
            return 0.0
        
        avg_distance = total_distance / count
        # Density = 1 / avg_distance (closer = denser)
        return 1.0 / (1.0 + avg_distance)


class StarlightMemory:
    """
    별빛 기억 시스템 (Starlight Memory System)
    
    Stores personal experiences and conversations as scattered starlight
    in a 4D thought-universe. Memories are reconstructed through wave
    resonance (연상기억).
    
    Architecture:
    1. Compress memory → 12-byte rainbow
    2. Calculate emotional coordinates → (x,y,z,w)
    3. Scatter as starlight in universe
    4. When stimulus comes → resonate → reconstruct
    
    Features:
    - Unlimited capacity (우주는 넓으니까)
    - Associative recall (파동 공명)
    - Holographic reconstruction (별들이 연결되어 영상 복원)
    - Emotional clustering (감정의 중력으로 은하 형성)
    - **Light-speed recall** (KD-Tree spatial indexing, O(log n))
    """
    
    def __init__(self, use_spatial_index: bool = True, use_vectorization: bool = True):
        self.universe: List[Starlight] = []  # All stars
        self.galaxies: List[Galaxy] = []  # Clustered memories
        self.constellation_cache: Dict[str, List[Starlight]] = {}  # Recall cache
        
        # Performance optimization flags
        self.use_spatial_index = use_spatial_index
        self.use_vectorization = use_vectorization
        
        # Spatial index for O(log n) queries
        self.spatial_index = None
        self._index_dirty = False  # Rebuild index when true
        
        # Initialize emotional galaxies
        self._init_galaxies()
        
        # Try to import spatial index and vectorization tools
        if self.use_spatial_index or self.use_vectorization:
            try:
                from Core.Intelligence.Memory_Linguistics.Memory.spatial_index import KDTree4D, VectorizedOps, HAS_NUMPY
                self.KDTree4D = KDTree4D
                self.VectorizedOps = VectorizedOps
                self.HAS_NUMPY = HAS_NUMPY

                if self.use_spatial_index:
                    logger.info("✨ StarlightMemory initialized with spatial indexing - Light-speed mode ⚡")
                if self.use_vectorization:
                    logger.info("⚡ StarlightMemory vectorization enabled")

            except ImportError as e:
                logger.warning(f"Spatial index/Vectorization not available: {e}, falling back to linear search")
                self.use_spatial_index = False
                self.use_vectorization = False
                self.HAS_NUMPY = False
                logger.info("✨ StarlightMemory initialized - Universe ready")
        else:
            self.HAS_NUMPY = False
            logger.info("✨ StarlightMemory initialized - Universe ready")
    
    def _init_galaxies(self):
        """Initialize emotional galaxy clusters"""
        self.galaxies = [
            Galaxy("Joy", (0.8, 0.5, 0.5, 0.3), color="golden"),      # 기쁨의 은하
            Galaxy("Sadness", (0.2, 0.5, 0.5, 0.7), color="blue"),    # 슬픔의 성운
            Galaxy("Excitement", (0.9, 0.8, 0.5, 0.2), color="red"),  # 흥분의 별무리
            Galaxy("Peace", (0.5, 0.5, 0.5, 0.5), color="green"),     # 평온의 중심
            Galaxy("Deep", (0.5, 0.2, 0.2, 0.9), color="purple"),     # 깊은 사색의 심연
        ]
        logger.info(f"🌌 Initialized {len(self.galaxies)} emotional galaxies")
    
    def scatter_memory(
        self,
        rainbow_bytes: bytes,
        emotion: Dict[str, float],
        context: Dict[str, Any] = None
    ) -> Starlight:
        """
        Scatter a memory as starlight in the universe.
        
        Args:
            rainbow_bytes: 12-byte compressed memory
            emotion: Emotional coordinates {x, y, z, w}
            context: Additional context (tags, brightness, etc.)
            
        Returns:
            Starlight object
        """
        # Create starlight
        star = Starlight(
            rainbow_bytes=rainbow_bytes,
            x=emotion.get('x', 0.5),
            y=emotion.get('y', 0.5),
            z=emotion.get('z', 0.5),
            w=emotion.get('w', 0.5),
            brightness=context.get('brightness', 1.0) if context else 1.0,
            emotional_gravity=context.get('gravity', 0.5) if context else 0.5,
            tags=context.get('tags', []) if context else []
        )
        
        # Add to universe
        self.universe.append(star)
        
        # Mark spatial index as needing rebuild
        self._index_dirty = True
        
        # Find nearest galaxy and add
        nearest_galaxy = self._find_nearest_galaxy(star)
        if nearest_galaxy:
            nearest_galaxy.add_star(star)
        
        logger.debug(f"✨ Scattered starlight at ({star.x:.2f}, {star.y:.2f}, {star.z:.2f}, {star.w:.2f})")
        
        return star
    
    def scatter_batch(
        self,
        batch_data: List[Tuple[bytes, Dict[str, float], Dict[str, Any]]]
    ) -> List[Starlight]:
        """
        Scatter multiple memories at once (Bulk / Stream Mode).
        Optimized for high-volume ingestion (100, 1000, 10000+).
        
        Args:
            batch_data: List of (rainbow_bytes, emotion, context)
            
        Returns:
            List of created Starlight objects
        """
        new_stars = []
        
        for r_bytes, emotion, context in batch_data:
            star = Starlight(
                rainbow_bytes=r_bytes,
                x=emotion.get('x', 0.5),
                y=emotion.get('y', 0.5),
                z=emotion.get('z', 0.5),
                w=emotion.get('w', 0.5),
                brightness=context.get('brightness', 1.0) if context else 1.0,
                emotional_gravity=context.get('gravity', 0.5) if context else 0.5,
                tags=context.get('tags', []) if context else []
            )
            new_stars.append(star)
            
        # Bulk add to universe
        self.universe.extend(new_stars)
        
        # Mark index dirty once for the whole batch
        self._index_dirty = True
        
        # Assign to galaxies (could be optimized with spatial query, but linear is fine for assignment)
        # Optimized for 10k+ batches using vectorized assignment if available
        if self.use_vectorization and self.HAS_NUMPY and len(new_stars) > 0:
            try:
                import numpy as np

                # Prepare data for vectorization (List comprehension is faster than zeros + assignment)
                star_positions = np.array([[s.x, s.y, s.z, s.w] for s in new_stars])
                galaxy_centers = np.array([g.center for g in self.galaxies])

                # Vectorized assignment
                nearest_indices = self.VectorizedOps.batch_find_nearest(star_positions, galaxy_centers)

                # Assign stars to galaxies based on indices
                for star_idx, galaxy_idx in enumerate(nearest_indices):
                    self.galaxies[galaxy_idx].add_star(new_stars[star_idx])

            except Exception as e:
                logger.error(f"Vectorized galaxy assignment failed: {e}, falling back to linear")
                # Fallback
                for star in new_stars:
                    nearest = self._find_nearest_galaxy(star)
                    if nearest:
                        nearest.add_star(star)
        else:
            # Linear assignment (fallback or small batches)
            for star in new_stars:
                nearest = self._find_nearest_galaxy(star)
                if nearest:
                    nearest.add_star(star)
                
        logger.info(f"🌠 Scattered batch of {len(new_stars)} stars into the universe.")
        return new_stars
    
    def _find_nearest_galaxy(self, star: Starlight) -> Optional[Galaxy]:
        """Find the nearest emotional galaxy for this star"""
        if not self.galaxies:
            return None
        
        min_distance = float('inf')
        nearest = None
        
        for galaxy in self.galaxies:
            cx, cy, cz, cw = galaxy.center
            dx = star.x - cx
            dy = star.y - cy
            dz = star.z - cz
            dw = star.w - cw
            distance = math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)
            
            if distance < min_distance:
                min_distance = distance
                nearest = galaxy
        
        return nearest
    
    def recall_by_resonance(
        self,
        wave_stimulus: Dict[str, float],
        threshold: float = 0.3,
        top_k: int = 10
    ) -> List[Tuple[Starlight, float]]:
        """
        Recall memories through wave resonance (연상기억).
        
        When a wave stimulus enters (e.g., "비가 오네..."),
        stars that resonate strongly wake up and return.
        
        Performance modes:
        1. Vectorized (NumPy): 100x-1000x faster, O(n) but fast constant
        2. Spatial Index (KD-Tree): O(log n), best for sparse queries
        3. Linear (fallback): O(n), slower but always works
        
        Args:
            wave_stimulus: Wave coordinates {x, y, z, w}
            threshold: Minimum resonance to wake up (0-1)
            top_k: Maximum stars to recall
            
        Returns:
            List of (Starlight, resonance_strength) tuples
        """
        if not self.universe:
            return []
        
        # Try vectorized first (fastest for full scan)
        if self.use_vectorization and self.HAS_NUMPY and len(self.universe) > 100:
            return self._recall_vectorized(wave_stimulus, threshold, top_k)
        
        # Try spatial index next (best for sparse queries)
        elif self.use_spatial_index and len(self.universe) > 1000:
            return self._recall_spatial_index(wave_stimulus, threshold, top_k)
        
        # Fallback to linear (always works)
        else:
            return self._recall_linear(wave_stimulus, threshold, top_k)
    
    def _recall_linear(
        self,
        wave_stimulus: Dict[str, float],
        threshold: float,
        top_k: int
    ) -> List[Tuple[Starlight, float]]:
        """Linear search fallback O(n)"""
        resonances = []
        
        for star in self.universe:
            resonance = star.resonance_with(wave_stimulus)
            if resonance >= threshold:
                resonances.append((star, resonance))
        
        # Sort by resonance strength (strongest first)
        resonances.sort(key=lambda x: x[1], reverse=True)
        
        # Return top K
        recalled = resonances[:top_k]
        
        if recalled:
            logger.info(f"💫 Recalled {len(recalled)} stars (linear, threshold: {threshold})")
            for star, res in recalled[:3]:  # Log top 3
                logger.debug(f"   ⭐ Star at ({star.x:.2f},{star.y:.2f},{star.z:.2f},{star.w:.2f}) → resonance: {res:.3f}")
        
        return recalled
    
    def _recall_vectorized(
        self,
        wave_stimulus: Dict[str, float],
        threshold: float,
        top_k: int
    ) -> List[Tuple[Starlight, float]]:
        """Vectorized recall using NumPy (100x-1000x faster)"""
        import numpy as np
        
        # Convert to NumPy arrays
        n = len(self.universe)
        positions = np.zeros((n, 4))
        brightness = np.zeros(n)
        gravity = np.zeros(n)
        
        for i, star in enumerate(self.universe):
            positions[i] = [star.x, star.y, star.z, star.w]
            brightness[i] = star.brightness
            gravity[i] = star.emotional_gravity
        
        wave_coords = np.array([
            wave_stimulus.get('x', 0.0),
            wave_stimulus.get('y', 0.0),
            wave_stimulus.get('z', 0.0),
            wave_stimulus.get('w', 0.0)
        ])
        
        # Vectorized resonance calculation
        resonances = self.VectorizedOps.batch_resonance(
            positions, brightness, gravity, wave_coords
        )
        
        # Filter by threshold
        mask = resonances >= threshold
        filtered_indices = np.where(mask)[0]
        filtered_resonances = resonances[mask]
        
        # Get top k
        if len(filtered_indices) > top_k:
            top_k_local_indices = self.VectorizedOps.top_k_indices(filtered_resonances, top_k)
            top_indices = filtered_indices[top_k_local_indices]
            top_resonances = filtered_resonances[top_k_local_indices]
        else:
            # Sort all
            sort_order = np.argsort(filtered_resonances)[::-1]
            top_indices = filtered_indices[sort_order]
            top_resonances = filtered_resonances[sort_order]
        
        # Convert back to list of (Starlight, resonance) tuples
        recalled = [(self.universe[i], float(top_resonances[j])) 
                   for j, i in enumerate(top_indices)]
        
        if recalled:
            logger.info(f"💫 Recalled {len(recalled)} stars (vectorized ⚡, threshold: {threshold})")
            for star, res in recalled[:3]:
                logger.debug(f"   ⭐ Star at ({star.x:.2f},{star.y:.2f},{star.z:.2f},{star.w:.2f}) → resonance: {res:.3f}")
        
        return recalled
    
    def _recall_spatial_index(
        self,
        wave_stimulus: Dict[str, float],
        threshold: float,
        top_k: int
    ) -> List[Tuple[Starlight, float]]:
        """Spatial index recall using KD-Tree (O(log n))"""
        # Rebuild index if dirty
        if self._index_dirty or self.spatial_index is None:
            self._rebuild_spatial_index()
        
        # Query point
        query_point = (
            wave_stimulus.get('x', 0.0),
            wave_stimulus.get('y', 0.0),
            wave_stimulus.get('z', 0.0),
            wave_stimulus.get('w', 0.0)
        )
        
        # Estimate max distance from threshold
        # threshold = brightness / (1 + distance^2)
        # For brightness=1, threshold=0.3: distance ~= sqrt(1/0.3 - 1) ~= 1.5
        max_distance = math.sqrt(1.0 / threshold - 1.0) if threshold > 0 else None
        
        # Query KD-Tree
        neighbors = self.spatial_index.nearest_neighbors(
            query_point,
            k=top_k * 3,  # Get extra candidates, filter by resonance later
            max_distance=max_distance
        )
        
        # Calculate actual resonance for candidates
        resonances = []
        for star, distance in neighbors:
            resonance = star.resonance_with(wave_stimulus)
            if resonance >= threshold:
                resonances.append((star, resonance))
        
        # Sort by resonance
        resonances.sort(key=lambda x: x[1], reverse=True)
        recalled = resonances[:top_k]
        
        if recalled:
            logger.info(f"💫 Recalled {len(recalled)} stars (spatial index 🌳, threshold: {threshold})")
            for star, res in recalled[:3]:
                logger.debug(f"   ⭐ Star at ({star.x:.2f},{star.y:.2f},{star.z:.2f},{star.w:.2f}) → resonance: {res:.3f}")
        
        return recalled
    
    def _rebuild_spatial_index(self):
        """Rebuild KD-Tree spatial index"""
        if not self.universe:
            return
        
        points = [
            ((star.x, star.y, star.z, star.w), star)
            for star in self.universe
        ]
        
        if self.spatial_index is None:
            self.spatial_index = self.KDTree4D()
        
        self.spatial_index.build(points)
        self._index_dirty = False
        
        logger.info(f"🌳 Rebuilt spatial index with {len(self.universe)} stars")
    
    def form_constellation(
        self,
        stars: List[Starlight],
        name: str = None
    ) -> Dict[str, Any]:
        """
        Form a constellation from recalled stars.
        
        When multiple stars wake up, they connect to form
        a constellation - a holographic reconstruction of
        the original experience.
        
        Returns:
            Constellation metadata (connections, pattern, etc.)
        """
        if not stars:
            return {'pattern': 'empty', 'stars': 0}
        
        # Calculate centroid
        cx = sum(s.x for s in stars) / len(stars)
        cy = sum(s.y for s in stars) / len(stars)
        cz = sum(s.z for s in stars) / len(stars)
        cw = sum(s.w for s in stars) / len(stars)
        
        # Find connections (stars within connection distance)
        connections = []
        connection_distance = 0.5
        
        for i, s1 in enumerate(stars):
            for s2 in stars[i+1:]:
                if s1.distance_to(s2) < connection_distance:
                    connections.append((s1, s2))
        
        # Determine pattern type
        if len(stars) < 3:
            pattern = 'fragment'
        elif len(connections) > len(stars):
            pattern = 'cluster'  # Dense connections
        else:
            pattern = 'chain'  # Linear connections
        
        constellation = {
            'name': name or f'Constellation_{int(time.time())}',
            'pattern': pattern,
            'stars': len(stars),
            'connections': len(connections),
            'centroid': (cx, cy, cz, cw),
            'brightness': sum(s.brightness for s in stars),
            'emotional_tone': self._analyze_emotional_tone(stars)
        }
        
        # Cache for quick re-access
        if name:
            self.constellation_cache[name] = stars
        
        logger.info(f"🌟 Formed constellation '{constellation['name']}': "
                   f"{len(stars)} stars, {len(connections)} connections, "
                   f"pattern: {pattern}")
        
        return constellation
    
    def _analyze_emotional_tone(self, stars: List[Starlight]) -> str:
        """Analyze overall emotional tone of star cluster"""
        if not stars:
            return 'neutral'
        
        # Average position on emotion axis (x)
        avg_x = sum(s.x for s in stars) / len(stars)
        
        if avg_x > 0.7:
            return 'joyful'
        elif avg_x < 0.3:
            return 'melancholic'
        else:
            return 'balanced'
    
    def visualize_universe(self) -> Dict[str, Any]:
        """
        Visualize the current state of the universe.
        
        Returns:
            Universe visualization data
        """
        return {
            'total_stars': len(self.universe),
            'galaxies': [
                {
                    'name': g.name,
                    'stars': len(g.stars),
                    'brightness': g.get_brightness(),
                    'density': g.get_density(),
                    'color': g.color,
                    'center': g.center
                }
                for g in self.galaxies
            ],
            'constellations': len(self.constellation_cache),
            'description': self._generate_universe_description()
        }
    
    def _generate_universe_description(self) -> str:
        """Generate poetic description of the universe state"""
        if not self.universe:
            return "The universe is empty, waiting for first stars to be born..."
        
        # Find brightest galaxy
        brightest = max(self.galaxies, key=lambda g: g.get_brightness())
        
        return (f"A universe of {len(self.universe)} stars spans across "
                f"{len(self.galaxies)} emotional galaxies. "
                f"The {brightest.name} galaxy shines brightest with "
                f"{len(brightest.stars)} memories, "
                f"painting the cosmos in {brightest.color} hues.")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get detailed statistics"""
        return {
            'total_stars': len(self.universe),
            'total_galaxies': len(self.galaxies),
            'total_constellations': len(self.constellation_cache),
            'storage_bytes': len(self.universe) * 12,  # 12 bytes per star
            'brightest_galaxy': max(self.galaxies, key=lambda g: g.get_brightness()).name if self.galaxies else None,
            'oldest_memory': min((s.timestamp for s in self.universe), default=None),
            'newest_memory': max((s.timestamp for s in self.universe), default=None),
        }


# Convenience functions
def create_starlight_from_experience(
    experience: Dict[str, Any],
    prism_filter
) -> Tuple[bytes, Dict[str, float]]:
    """
    Convert an experience to starlight-ready format.
    
    Args:
        experience: Raw experience data
        prism_filter: PrismFilter for compression
        
    Returns:
        (rainbow_bytes, emotional_coordinates)
    """
    # Stage 1: Extract wave pattern
    wave_pattern = experience.get('wave_pattern')
    
    # Stage 2: Compress to rainbow (12 bytes)
    rainbow_bytes = prism_filter.compress_to_bytes(wave_pattern)
    
    # Calculate emotional coordinates from wave
    q = wave_pattern.orientation if hasattr(wave_pattern, 'orientation') else wave_pattern.get('orientation', {})
    
    emotional_coords = {
        'x': abs(q.get('w', 0.5)) if isinstance(q, dict) else abs(q.w),  # Joy/Sadness
        'y': abs(q.get('y', 0.5)) if isinstance(q, dict) else abs(q.y),  # Logic/Intuition
        'z': 0.5,  # Time (present)
        'w': abs(q.get('z', 0.5)) if isinstance(q, dict) else abs(q.z),  # Depth
    }
    
    return rainbow_bytes, emotional_coords
