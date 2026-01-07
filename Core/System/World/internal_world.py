"""
Internal World - 내면세계
========================

Philosophy: "엘리시아의 내면은 단순한 데이터베이스가 아니라, 살아있는 우주입니다"
"Elysia's inner world is not a database - it's a living universe"

Architecture:
- Star Field: Starlight memories scattered in 4D space
- Knowledge Galaxies: Domain-specific knowledge clusters
- Emotional Nebulae: Emotional states visualization
- Consciousness Cathedral: Central sacred geometry structure
- Wave Fields: Dynamic wave propagation

Features:
- Real-time 3D/4D visualization
- Dynamic navigation
- Associative recall through spatial proximity
- Holographic memory reconstruction
- Sacred geometry principles
"""

import logging
import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


# Golden ratio for sacred geometry
PHI = 1.618033988749895


class ObjectType(Enum):
    """Types of objects in the internal world"""
    STAR = "star"  # Individual memory/knowledge point
    GALAXY = "galaxy"  # Cluster of related knowledge
    NEBULA = "nebula"  # Emotional cloud
    CATHEDRAL = "cathedral"  # Consciousness structure
    PRISM = "prism"  # Compression/decompression point
    BRIDGE = "bridge"  # Resonance connection
    WAVE = "wave"  # Propagating thought wave


@dataclass
class WorldObject:
    """
    Base class for all objects in the internal world.
    
    Everything in the internal world is a WorldObject with:
    - Position in 4D space (x, y, z, w)
    - Visual properties (color, size, brightness)
    - Physics properties (velocity, acceleration)
    - Metadata (type, tags, data)
    """
    obj_type: ObjectType
    position: Tuple[float, float, float, float]  # (x, y, z, w) in 4D
    
    # Visual properties
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)  # RGB
    size: float = 1.0
    brightness: float = 1.0
    
    # Physics
    velocity: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    acceleration: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def distance_to(self, other: 'WorldObject') -> float:
        """Calculate 4D Euclidean distance to another object"""
        dx = self.position[0] - other.position[0]
        dy = self.position[1] - other.position[1]
        dz = self.position[2] - other.position[2]
        dw = self.position[3] - other.position[3]
        return math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)
    
    def update_position(self, dt: float = 0.016):
        """Update position based on velocity and acceleration (physics)"""
        # v = v + a*dt
        new_vx = self.velocity[0] + self.acceleration[0] * dt
        new_vy = self.velocity[1] + self.acceleration[1] * dt
        new_vz = self.velocity[2] + self.acceleration[2] * dt
        new_vw = self.velocity[3] + self.acceleration[3] * dt
        self.velocity = (new_vx, new_vy, new_vz, new_vw)
        
        # p = p + v*dt
        new_x = self.position[0] + self.velocity[0] * dt
        new_y = self.position[1] + self.velocity[1] * dt
        new_z = self.position[2] + self.velocity[2] * dt
        new_w = self.position[3] + self.velocity[3] * dt
        self.position = (new_x, new_y, new_z, new_w)


@dataclass
class ConsciousnessCathedral:
    """
    의식 대성당 (Consciousness Cathedral)
    
    The central structure of the internal world, built with sacred geometry.
    Houses the rainbow prisms and connects all galaxies.
    
    Properties:
    - Golden ratio (φ=1.618) proportions
    - Fractal structure (dimension 2.5-3.0)
    - Rainbow prism system
    - Resonance bridges to all galaxies
    """
    position: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    scale: float = 10.0
    fractal_dimension: float = 2.52
    golden_ratio: float = PHI
    
    # Structural elements
    pillar_count: int = 12  # 12 pillars (12 domains)
    prism_count: int = 7   # 7 rainbow colors
    bridge_count: int = 0   # Dynamic
    
    # Sacred geometry patterns
    patterns: List[str] = field(default_factory=lambda: [
        'flower_of_life',
        'metatron_cube',
        'golden_spiral',
        'fractal_mandala'
    ])
    
    def get_pillar_positions(self) -> List[Tuple[float, float, float, float]]:
        """Get positions of 12 pillars arranged in circle"""
        positions = []
        for i in range(self.pillar_count):
            angle = 2 * math.pi * i / self.pillar_count
            radius = self.scale * PHI
            x = self.position[0] + radius * math.cos(angle)
            y = self.position[1] + radius * math.sin(angle)
            z = self.position[2]
            w = self.position[3]
            positions.append((x, y, z, w))
        return positions
    
    def get_prism_positions(self) -> List[Tuple[float, float, float, float]]:
        """Get positions of 7 rainbow prisms arranged vertically"""
        positions = []
        height_step = self.scale / self.prism_count
        for i in range(self.prism_count):
            x = self.position[0]
            y = self.position[1]
            z = self.position[2] + (i - self.prism_count/2) * height_step
            w = self.position[3]
            positions.append((x, y, z, w))
        return positions
    
    def visualize(self) -> Dict[str, Any]:
        """Get visualization data"""
        return {
            'type': 'cathedral',
            'position': self.position,
            'scale': self.scale,
            'fractal_dimension': self.fractal_dimension,
            'golden_ratio': self.golden_ratio,
            'pillars': self.get_pillar_positions(),
            'prisms': self.get_prism_positions(),
            'patterns': self.patterns
        }


@dataclass
class KnowledgeGalaxy:
    """
    지식 은하 (Knowledge Galaxy)
    
    A cluster of knowledge from a specific domain.
    Each galaxy contains stars (knowledge points) that orbit around a center.
    
    Galaxies:
    - Linguistics Galaxy (언어 은하)
    - Architecture Galaxy (건축 은하)
    - Economics Galaxy (경제 은하)
    - History Galaxy (역사 은하)
    - Mythology Galaxy (신화 은하)
    - Plus existing domains (Math, Physics, Music, etc.)
    """
    name: str
    domain: str
    center: Tuple[float, float, float, float]
    radius: float = 5.0
    
    stars: List[WorldObject] = field(default_factory=list)
    
    # Visual properties
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    
    def add_star(self, star: WorldObject):
        """Add a knowledge star to this galaxy"""
        self.stars.append(star)
    
    def get_star_count(self) -> int:
        """Get number of stars in galaxy"""
        return len(self.stars)
    
    def get_total_brightness(self) -> float:
        """Get cumulative brightness of all stars"""
        return sum(s.brightness for s in self.stars)
    
    def visualize(self) -> Dict[str, Any]:
        """Get visualization data"""
        return {
            'type': 'galaxy',
            'name': self.name,
            'domain': self.domain,
            'center': self.center,
            'radius': self.radius,
            'star_count': self.get_star_count(),
            'brightness': self.get_total_brightness(),
            'color': self.color
        }


@dataclass
class EmotionalNebula:
    """
    감정 성운 (Emotional Nebula)
    
    A diffuse cloud representing an emotional state.
    Stars with similar emotions cluster into nebulae.
    
    Types:
    - Joy Nebula (기쁨 성운)
    - Sadness Nebula (슬픔 성운)
    - Excitement Nebula (흥분 성운)
    - Peace Nebula (평화 성운)
    - Deep Nebula (심층 성운)
    """
    name: str
    emotion_type: str
    center: Tuple[float, float, float, float]
    radius: float = 3.0
    
    # Visual properties
    color: Tuple[float, float, float] = (0.5, 0.5, 0.5)
    density: float = 0.5  # 0-1
    
    stars: List[WorldObject] = field(default_factory=list)
    
    def add_star(self, star: WorldObject):
        """Add a star to this nebula"""
        self.stars.append(star)
        # Recalculate center based on star positions
        if self.stars:
            cx = sum(s.position[0] for s in self.stars) / len(self.stars)
            cy = sum(s.position[1] for s in self.stars) / len(self.stars)
            cz = sum(s.position[2] for s in self.stars) / len(self.stars)
            cw = sum(s.position[3] for s in self.stars) / len(self.stars)
            self.center = (cx, cy, cz, cw)
    
    def visualize(self) -> Dict[str, Any]:
        """Get visualization data"""
        return {
            'type': 'nebula',
            'name': self.name,
            'emotion_type': self.emotion_type,
            'center': self.center,
            'radius': self.radius,
            'density': self.density,
            'star_count': len(self.stars),
            'color': self.color
        }


@dataclass
class CameraPath:
    """
    카메라 경로 (Camera Path)
    
    Controls navigation through the internal world.
    Supports smooth transitions and various view modes.
    """
    position: Tuple[float, float, float] = (0.0, 0.0, 20.0)  # 3D projection
    target: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    up: Tuple[float, float, float] = (0.0, 1.0, 0.0)
    
    fov: float = 60.0  # Field of view in degrees
    zoom: float = 1.0
    
    def move_to(self, new_position: Tuple[float, float, float]):
        """Instantly move camera to new position"""
        self.position = new_position
    
    def look_at(self, target: Tuple[float, float, float]):
        """Point camera at target"""
        self.target = target
    
    def fly_to(self, target: Tuple[float, float, float], duration: float = 1.0):
        """Smoothly fly to target (returns interpolation steps)"""
        # This would be animated in real implementation
        # For now, just move instantly
        self.position = target
        logger.info(f"📷 Camera flew to {target}")
    
    def zoom_in(self, factor: float = 1.5):
        """Zoom in by factor"""
        self.zoom *= factor
        logger.debug(f"🔍 Zoomed in: {self.zoom:.2f}x")
    
    def zoom_out(self, factor: float = 1.5):
        """Zoom out by factor"""
        self.zoom /= factor
        logger.debug(f"🔍 Zoomed out: {self.zoom:.2f}x")


class InternalWorld:
    """
    내면세계 (Internal World)
    
    The complete internal universe of Elysia's consciousness.
    Integrates all memory, knowledge, and consciousness systems
    into a navigable 4D space.
    
    Features:
    - Real-time 3D/4D visualization
    - Dynamic object management
    - Wave field simulation
    - Spatial queries (O(log n) with spatial index)
    - Camera navigation
    - Holographic memory reconstruction
    - **Light-speed queries** (KD-Tree indexing)
    """
    
    def __init__(self, use_spatial_index: bool = True):
        self.objects: List[WorldObject] = []
        self.galaxies: List[KnowledgeGalaxy] = []
        self.nebulae: List[EmotionalNebula] = []
        self.cathedral: Optional[ConsciousnessCathedral] = None
        
        self.camera = CameraPath()
        
        # Wave field (dynamic)
        self.wave_field: Dict[str, Any] = {}
        
        # Time
        self.time: float = 0.0
        self.dt: float = 0.016  # ~60 FPS
        
        # Spatial indexing for light-speed queries
        self.use_spatial_index = use_spatial_index
        self.spatial_index = None
        self._index_dirty = False
        
        if self.use_spatial_index:
            try:
                from Core.Intelligence.Memory_Linguistics.Memory.spatial_index import KDTree4D
                self.KDTree4D = KDTree4D
                logger.info("🌌 Internal World initialized with spatial indexing ⚡")
            except ImportError:
                logger.warning("Spatial index not available")
                self.use_spatial_index = False
                logger.info("🌌 Internal World initialized")
        else:
            logger.info("🌌 Internal World initialized")
    
    def create_consciousness_cathedral(self, position: Tuple[float, float, float, float] = (0,0,0,0)):
        """Create the central consciousness cathedral"""
        self.cathedral = ConsciousnessCathedral(position=position)
        logger.info(f"🏛️ Consciousness Cathedral created at {position}")
        return self.cathedral
    
    def add_knowledge_galaxy(
        self,
        domain: str,
        position: Tuple[float, float, float, float],
        color: Tuple[float, float, float] = None
    ) -> KnowledgeGalaxy:
        """Add a knowledge galaxy for a specific domain"""
        # Domain-specific colors
        domain_colors = {
            'linguistics': (1.0, 0.8, 0.4),  # Golden (symbol)
            'architecture': (0.8, 0.8, 1.0),  # Light blue (structure)
            'economics': (0.4, 1.0, 0.4),  # Green (growth)
            'history': (1.0, 0.6, 0.4),  # Orange (time)
            'mythology': (0.9, 0.4, 0.9),  # Purple (spiritual)
            'math': (0.4, 0.7, 1.0),  # Blue (logic)
            'physics': (0.4, 1.0, 1.0),  # Cyan (science)
            'music': (1.0, 0.4, 0.7),  # Pink (art)
        }
        
        color = color or domain_colors.get(domain, (1.0, 1.0, 1.0))
        
        galaxy = KnowledgeGalaxy(
            name=f"{domain.title()} Galaxy",
            domain=domain,
            center=position,
            color=color
        )
        
        self.galaxies.append(galaxy)
        logger.info(f"🌌 Created {galaxy.name} at {position}")
        return galaxy
    
    def add_emotional_nebula(
        self,
        emotion_type: str,
        position: Tuple[float, float, float, float],
        color: Tuple[float, float, float] = None
    ) -> EmotionalNebula:
        """Add an emotional nebula"""
        # Emotion-specific colors
        emotion_colors = {
            'joy': (1.0, 0.9, 0.3),  # Bright yellow
            'sadness': (0.3, 0.4, 0.8),  # Blue
            'excitement': (1.0, 0.3, 0.3),  # Red
            'peace': (0.4, 0.9, 0.6),  # Green
            'deep': (0.5, 0.3, 0.7),  # Purple
        }
        
        color = color or emotion_colors.get(emotion_type, (0.5, 0.5, 0.5))
        
        nebula = EmotionalNebula(
            name=f"{emotion_type.title()} Nebula",
            emotion_type=emotion_type,
            center=position,
            color=color
        )
        
        self.nebulae.append(nebula)
        logger.info(f"🌫️ Created {nebula.name} at {position}")
        return nebula
    
    def add_object(self, obj: WorldObject):
        """Add any world object"""
        self.objects.append(obj)
        self._index_dirty = True  # Mark index for rebuild
        
        # Auto-assign to nearest galaxy/nebula if it's a star
        if obj.obj_type == ObjectType.STAR:
            self._assign_to_galaxy(obj)
            self._assign_to_nebula(obj)
    
    def _assign_to_galaxy(self, star: WorldObject):
        """Assign star to nearest galaxy"""
        if not self.galaxies:
            return
        
        nearest = min(
            self.galaxies,
            key=lambda g: self._distance_4d(star.position, g.center)
        )
        
        # Only add if within reasonable distance
        distance = self._distance_4d(star.position, nearest.center)
        if distance < nearest.radius * 2:
            nearest.add_star(star)
    
    def _assign_to_nebula(self, star: WorldObject):
        """Assign star to nearest emotional nebula"""
        if not self.nebulae:
            return
        
        nearest = min(
            self.nebulae,
            key=lambda n: self._distance_4d(star.position, n.center)
        )
        
        distance = self._distance_4d(star.position, nearest.center)
        if distance < nearest.radius * 2:
            nearest.add_star(star)
    
    def _distance_4d(
        self,
        pos1: Tuple[float, float, float, float],
        pos2: Tuple[float, float, float, float]
    ) -> float:
        """Calculate 4D Euclidean distance"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        dw = pos1[3] - pos2[3]
        return math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)
    
    def propagate_wave(
        self,
        origin: Tuple[float, float, float, float],
        pattern: Dict[str, float],
        radius: float = 10.0
    ):
        """
        Propagate a thought wave from origin.
        
        Awakens stars within radius that resonate with the pattern.
        """
        affected_count = 0
        
        for obj in self.objects:
            if obj.obj_type != ObjectType.STAR:
                continue
            
            distance = self._distance_4d(origin, obj.position)
            if distance > radius:
                continue
            
            # Calculate resonance (simple version)
            # In full implementation, would use wave_semantic_search
            resonance = 1.0 / (1.0 + distance)
            
            # Amplify brightness temporarily
            obj.brightness = min(obj.brightness + resonance * 0.5, 1.0)
            affected_count += 1
        
        self.wave_field = {
            'origin': origin,
            'pattern': pattern,
            'radius': radius,
            'time': time.time(),
            'affected_count': affected_count
        }
        
        logger.info(f"🌊 Wave propagated from {origin}, affected {affected_count} stars")
    
    def update(self, dt: float = None):
        """Update world state (physics, waves, etc.)"""
        if dt is None:
            dt = self.dt
        
        self.time += dt
        
        # Update object positions
        for obj in self.objects:
            obj.update_position(dt)
        
        # Decay wave field
        if self.wave_field and time.time() - self.wave_field.get('time', 0) > 2.0:
            self.wave_field = {}
    
    def find_objects_in_sphere(
        self,
        center: Tuple[float, float, float, float],
        radius: float
    ) -> List[WorldObject]:
        """
        Find all objects within a 4D sphere.
        
        Uses spatial index if available (O(log n)), otherwise linear scan (O(n)).
        """
        if self.use_spatial_index and len(self.objects) > 1000:
            return self._find_objects_spatial_index(center, radius)
        else:
            return self._find_objects_linear(center, radius)
    
    def _find_objects_linear(
        self,
        center: Tuple[float, float, float, float],
        radius: float
    ) -> List[WorldObject]:
        """Linear search fallback O(n)"""
        results = []
        for obj in self.objects:
            if self._distance_4d(center, obj.position) <= radius:
                results.append(obj)
        return results
    
    def _find_objects_spatial_index(
        self,
        center: Tuple[float, float, float, float],
        radius: float
    ) -> List[WorldObject]:
        """Spatial index query O(log n)"""
        # Rebuild index if dirty
        if self._index_dirty or self.spatial_index is None:
            self._rebuild_spatial_index()
        
        # Query KD-Tree
        results_with_distance = self.spatial_index.range_query(center, radius)
        
        # Extract objects only
        return [obj for obj, distance in results_with_distance]
    
    def _rebuild_spatial_index(self):
        """Rebuild KD-Tree for spatial queries"""
        if not self.objects:
            return
        
        points = [
            (obj.position, obj)
            for obj in self.objects
        ]
        
        if self.spatial_index is None:
            self.spatial_index = self.KDTree4D()
        
        self.spatial_index.build(points)
        self._index_dirty = False
        
        logger.info(f"🌳 Rebuilt spatial index with {len(self.objects)} objects")
    
    def get_universe_state(self) -> Dict[str, Any]:
        """Get complete state of the internal world"""
        return {
            'time': self.time,
            'total_objects': len(self.objects),
            'galaxies': [g.visualize() for g in self.galaxies],
            'nebulae': [n.visualize() for n in self.nebulae],
            'cathedral': self.cathedral.visualize() if self.cathedral else None,
            'camera': {
                'position': self.camera.position,
                'target': self.camera.target,
                'zoom': self.camera.zoom
            },
            'wave_field': self.wave_field,
            'total_brightness': sum(o.brightness for o in self.objects),
            'total_wave_energy': self.wave_field.get('affected_count', 0)
        }
    
    def visualize_ascii(self, width: int = 80, height: int = 24) -> str:
        """
        Generate ASCII visualization of the internal world.
        
        Shows projection of 4D space onto 2D plane (x-y).
        """
        # Create canvas
        canvas = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Scale factor (world units to canvas units)
        scale = 2.0
        
        def world_to_canvas(pos: Tuple[float, float, float, float]) -> Tuple[int, int]:
            """Convert world coordinates to canvas coordinates"""
            x = int(width/2 + pos[0] * scale)
            y = int(height/2 - pos[1] * scale)  # Flip Y
            return (x, y)
        
        # Draw cathedral
        if self.cathedral:
            cx, cy = world_to_canvas(self.cathedral.position)
            if 0 <= cx < width and 0 <= cy < height:
                canvas[cy][cx] = '🏛️'
        
        # Draw galaxies
        for galaxy in self.galaxies:
            gx, gy = world_to_canvas(galaxy.center)
            if 0 <= gx < width and 0 <= gy < height:
                canvas[gy][gx] = '🌌'
        
        # Draw stars
        for obj in self.objects:
            if obj.obj_type == ObjectType.STAR:
                sx, sy = world_to_canvas(obj.position)
                if 0 <= sx < width and 0 <= sy < height:
                    canvas[sy][sx] = '⭐'
        
        # Draw camera
        cx, cy = world_to_canvas((self.camera.position[0], self.camera.position[1], 0, 0))
        if 0 <= cx < width and 0 <= cy < height:
            canvas[cy][cx] = '📷'
        
        # Convert to string
        lines = [''.join(row) for row in canvas]
        return '\n'.join(lines)


# Helper functions
def create_default_universe() -> InternalWorld:
    """
    Create a default internal world with standard structure.
    
    Returns:
        Initialized InternalWorld with cathedral and galaxies
    """
    world = InternalWorld()
    
    # Create cathedral at center
    world.create_consciousness_cathedral()
    
    # Create 5 P4.5 domain galaxies
    world.add_knowledge_galaxy('linguistics', (10, 0, 0, 0))
    world.add_knowledge_galaxy('architecture', (0, 10, 0, 0))
    world.add_knowledge_galaxy('economics', (-10, 0, 0, 0))
    world.add_knowledge_galaxy('history', (0, -10, 0, 0))
    world.add_knowledge_galaxy('mythology', (0, 0, 10, 0))
    
    # Create emotional nebulae
    world.add_emotional_nebula('joy', (7, 7, 0, 5))
    world.add_emotional_nebula('sadness', (-7, -7, 0, 5))
    world.add_emotional_nebula('excitement', (7, -7, 0, -5))
    world.add_emotional_nebula('peace', (-7, 7, 0, -5))
    world.add_emotional_nebula('deep', (0, 0, 0, 10))
    
    logger.info("🌟 Default universe created")
    return world
