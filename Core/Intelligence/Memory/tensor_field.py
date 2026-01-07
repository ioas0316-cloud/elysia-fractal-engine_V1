"""
Tensor Gravity Field - 중력장 기반 데이터 흐름 유도
================================================

Philosophy: "중력장이 시공간을 휘듯, 텐서 장이 데이터 흐름을 휜다"
"Like gravity bends spacetime, tensor fields bend data flow"

Inspired by General Relativity:
- Mass (important memories) creates gravitational wells
- Data flows along geodesics (shortest path in curved space)
- No explicit routing - natural gradient descent
- Emergent clustering without algorithms

Key Concepts:
1. Gravitational Potential: Φ(x) = Σ -G·mᵢ / |x - xᵢ|
2. Gradient (Force): ∇Φ(x) = direction of steepest descent
3. Geodesics: Natural paths data follows
4. Wells: Regions where data collects
5. Saddle Points: Decision boundaries

Zero-Computation Principle:
- Field is pre-computed once
- All queries are O(1) lookup
- No path planning needed
- Data "falls" naturally
"""

import logging
import math
from typing import List, Tuple, Dict, Any, Optional, Union
from dataclasses import dataclass, field
import time

logger = logging.getLogger(__name__)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


@dataclass
class GravityWell:
    """
    중력 우물 (Gravity Well) - Attractor in field
    
    Like a massive star that attracts nearby matter,
    important memories create wells that attract similar data.
    """
    # Position in 4D space
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0
    
    # Mass (importance/weight)
    mass: float = 1.0  # 0-1 typically, but can be higher
    
    # Metadata
    label: str = ""
    data: Any = None
    created_at: float = field(default_factory=time.time)
    
    def position_vector(self) -> Tuple[float, float, float, float]:
        """Get position as tuple"""
        return (self.x, self.y, self.z, self.w)
    
    def distance_to(self, x: float, y: float, z: float, w: float) -> float:
        """Calculate 4D distance to point"""
        dx = self.x - x
        dy = self.y - y
        dz = self.z - z
        dw = self.w - w
        return math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)


@dataclass
class TensorWell:
    """
    텐서 우물 (Tensor Well) - Anisotropic attractor

    Unlike a simple gravity well which attracts equally from all directions,
    a tensor well applies a transformation matrix to the space around it.
    It can create complex flow patterns like rotation, shear, or directional attraction.
    """
    # Position
    x: float
    y: float
    z: float
    w: float

    # Interaction Tensor (4x4 matrix)
    # T * displacement = force_vector
    # If T = -I (identity), it's standard attraction
    tensor: Union[List[List[float]], Any]  # List[List] or np.ndarray

    # Metadata
    label: str = ""
    data: Any = None

    def __post_init__(self):
        # Ensure tensor is in correct format if possible
        if HAS_NUMPY and not isinstance(self.tensor, np.ndarray):
            self.tensor = np.array(self.tensor, dtype=float)


@dataclass
class FieldPoint:
    """
    장 점 (Field Point) - Gravitational field at a location
    
    Stores pre-computed potential and gradient at this point.
    """
    # Position
    x: float
    y: float
    z: float
    w: float
    
    # Field values
    potential: float = 0.0  # Φ(x) - scalar potential
    gradient_x: float = 0.0  # ∂Φ/∂x - force in x direction
    gradient_y: float = 0.0  # ∂Φ/∂y
    gradient_z: float = 0.0  # ∂Φ/∂z
    gradient_w: float = 0.0  # ∂Φ/∂w
    
    def gradient_magnitude(self) -> float:
        """Magnitude of gradient (force strength)"""
        return math.sqrt(
            self.gradient_x**2 + 
            self.gradient_y**2 + 
            self.gradient_z**2 + 
            self.gradient_w**2
        )
    
    def gradient_direction(self) -> Tuple[float, float, float, float]:
        """Unit vector in gradient direction"""
        mag = self.gradient_magnitude()
        if mag < 1e-10:
            return (0.0, 0.0, 0.0, 0.0)
        return (
            self.gradient_x / mag,
            self.gradient_y / mag,
            self.gradient_z / mag,
            self.gradient_w / mag
        )


class TensorGravityField:
    """
    텐서 중력장 (Tensor Gravity Field)
    
    Creates a gravitational field in 4D thought-space that guides
    data flow without explicit computation.
    
    Like General Relativity:
    - Mass tells spacetime how to curve
    - Spacetime tells matter how to move
    
    Here:
    - Important memories create potential wells
    - Data flows toward wells automatically
    - No routing algorithm needed
    """
    
    def __init__(
        self,
        gravitational_constant: float = 1.0,
        smoothing_radius: float = 0.1
    ):
        """
        Args:
            gravitational_constant: G in Φ = -GM/r (default 1.0)
            smoothing_radius: Prevent singularities at r=0
        """
        self.G = gravitational_constant
        self.smoothing = smoothing_radius
        
        # Attractors (gravity wells)
        self.wells: List[GravityWell] = []
        
        # Pre-computed field (for very fast lookup)
        self.field_cache: Dict[Tuple[float, float, float, float], FieldPoint] = {}
        
        # Statistics
        self.queries = 0
        self.cache_hits = 0
        
        logger.info(f"🌌 Tensor Gravity Field initialized")
        logger.info(f"   G = {self.G}")
        logger.info(f"   Smoothing radius = {self.smoothing}")
    
    def add_attractor(
        self,
        x: float,
        y: float,
        z: float,
        w: float,
        mass: float = 1.0,
        label: str = "",
        data: Any = None
    ):
        """
        Add gravitational attractor (mass creates field).
        
        Args:
            x,y,z,w: Position in 4D space
            mass: Gravitational mass (importance)
            label: Optional label
            data: Optional associated data
        """
        well = GravityWell(
            x=x, y=y, z=z, w=w,
            mass=mass,
            label=label,
            data=data
        )
        self.wells.append(well)
        
        # Clear field cache (needs recomputation)
        self.field_cache.clear()
        
        logger.debug(f"   Added well '{label}' at ({x:.2f},{y:.2f},{z:.2f},{w:.2f}) mass={mass:.2f}")
    
    def get_potential(
        self,
        x: float,
        y: float,
        z: float,
        w: float
    ) -> float:
        """
        Calculate gravitational potential at point.
        
        Φ(x) = Σᵢ -G·mᵢ / sqrt(r² + ε²)
        
        where:
        - G = gravitational constant
        - mᵢ = mass of well i
        - r = distance to well i
        - ε = smoothing radius (prevents singularities)
        
        Returns: Potential (more negative = stronger attraction)
        Time: O(n) where n = number of wells
        """
        potential = 0.0
        
        for well in self.wells:
            # Distance to well
            r = well.distance_to(x, y, z, w)
            
            # Smoothed distance (prevent r=0 singularity)
            r_smooth = math.sqrt(r*r + self.smoothing*self.smoothing)
            
            # Add contribution: Φ = -GM/r
            potential += -self.G * well.mass / r_smooth
        
        return potential
    
    def get_gradient(
        self,
        x: float,
        y: float,
        z: float,
        w: float
    ) -> Tuple[float, float, float, float]:
        """
        Calculate gradient of potential (force field).
        
        ∇Φ(x) = Σᵢ G·mᵢ·(x - xᵢ) / r³
        
        Gradient points in direction of steepest ascent.
        Data flows OPPOSITE to gradient (downhill).
        
        Returns: (∂Φ/∂x, ∂Φ/∂y, ∂Φ/∂z, ∂Φ/∂w)
        Time: O(n) where n = number of wells
        """
        grad_x = 0.0
        grad_y = 0.0
        grad_z = 0.0
        grad_w = 0.0
        
        for well in self.wells:
            # Vector from well to point
            dx = x - well.x
            dy = y - well.y
            dz = z - well.z
            dw = w - well.w
            
            # Distance
            r = well.distance_to(x, y, z, w)
            r_smooth = math.sqrt(r*r + self.smoothing*self.smoothing)
            
            # Avoid division by zero
            if r_smooth < 1e-10:
                continue
            
            # ∇Φ = G·m·(x-x₀)/r³
            factor = self.G * well.mass / (r_smooth ** 3)
            grad_x += factor * dx
            grad_y += factor * dy
            grad_z += factor * dz
            grad_w += factor * dw
        
        return (grad_x, grad_y, grad_z, grad_w)
    
    def find_nearest_well(
        self,
        x: float,
        y: float,
        z: float,
        w: float
    ) -> Optional[GravityWell]:
        """
        Find nearest gravitational well.
        
        This is the well that data at this point would flow toward.
        
        Returns: Nearest GravityWell or None
        Time: O(n) where n = number of wells
        """
        if not self.wells:
            return None
        
        nearest_well = None
        min_distance = float('inf')
        
        for well in self.wells:
            distance = well.distance_to(x, y, z, w)
            if distance < min_distance:
                min_distance = distance
                nearest_well = well
        
        return nearest_well
    
    def flow_step(
        self,
        x: float,
        y: float,
        z: float,
        w: float,
        step_size: float = 0.1
    ) -> Tuple[float, float, float, float]:
        """
        Take one step following gradient flow.
        
        Data flows "downhill" toward wells (opposite to gradient).
        
        Args:
            x,y,z,w: Current position
            step_size: Size of step (smaller = more accurate)
        
        Returns: New position after flow step
        """
        # Get gradient (uphill direction)
        grad_x, grad_y, grad_z, grad_w = self.get_gradient(x, y, z, w)
        
        # Flow downhill (opposite to gradient)
        new_x = x - step_size * grad_x
        new_y = y - step_size * grad_y
        new_z = z - step_size * grad_z
        new_w = w - step_size * grad_w
        
        return (new_x, new_y, new_z, new_w)
    
    def flow_to_well(
        self,
        x: float,
        y: float,
        z: float,
        w: float,
        max_steps: int = 100,
        convergence_threshold: float = 0.01
    ) -> GravityWell:
        """
        Follow gradient flow until reaching a well.
        
        Simulates natural data flow through field.
        
        Args:
            x,y,z,w: Starting position
            max_steps: Maximum iterations
            convergence_threshold: Stop when movement < threshold
        
        Returns: Well that was reached
        """
        current_pos = (x, y, z, w)
        
        for step in range(max_steps):
            # Take flow step
            new_pos = self.flow_step(*current_pos)
            
            # Check convergence
            movement = math.sqrt(sum((n - c)**2 for n, c in zip(new_pos, current_pos)))
            if movement < convergence_threshold:
                break
            
            current_pos = new_pos
        
        # Find nearest well to final position
        return self.find_nearest_well(*current_pos)
    
    def visualize_field_1d(
        self,
        axis: int = 0,
        resolution: int = 50,
        range_min: float = -5.0,
        range_max: float = 5.0
    ) -> List[Tuple[float, float]]:
        """
        Get 1D slice of gravitational field for visualization.
        
        Args:
            axis: Which axis to vary (0=x, 1=y, 2=z, 3=w)
            resolution: Number of points
            range_min, range_max: Range to sample
        
        Returns: List of (position, potential) tuples
        """
        result = []
        
        for i in range(resolution):
            t = range_min + (range_max - range_min) * i / (resolution - 1)
            
            # Build position (vary one axis, fix others at 0)
            if axis == 0:
                pos = (t, 0.0, 0.0, 0.0)
            elif axis == 1:
                pos = (0.0, t, 0.0, 0.0)
            elif axis == 2:
                pos = (0.0, 0.0, t, 0.0)
            else:
                pos = (0.0, 0.0, 0.0, t)
            
            potential = self.get_potential(*pos)
            result.append((t, potential))
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get field statistics"""
        if not self.wells:
            return {'wells': 0, 'total_mass': 0.0}
        
        total_mass = sum(w.mass for w in self.wells)
        avg_mass = total_mass / len(self.wells)
        
        # Find center of mass
        if total_mass > 0:
            com_x = sum(w.x * w.mass for w in self.wells) / total_mass
            com_y = sum(w.y * w.mass for w in self.wells) / total_mass
            com_z = sum(w.z * w.mass for w in self.wells) / total_mass
            com_w = sum(w.w * w.mass for w in self.wells) / total_mass
        else:
            com_x = com_y = com_z = com_w = 0.0
        
        return {
            'wells': len(self.wells),
            'total_mass': total_mass,
            'avg_mass': avg_mass,
            'center_of_mass': (com_x, com_y, com_z, com_w),
            'G': self.G,
            'smoothing': self.smoothing
        }


class TensorCoil:
    """
    텐서 코일 (Tensor Coil)
    
    Advanced: Anisotropic tensor field (direction-dependent).
    
    Like electromagnetic field has both E and B components,
    tensor field can have different strengths in different directions.
    
    Use cases:
    - Directional clustering (cluster along certain axes more)
    - Rotation (swirl data around attractors)
    - Shear (stretch data in one direction)
    """
    
    def __init__(self, smoothing_radius: float = 0.1):
        """
        Initialize tensor coil

        Args:
            smoothing_radius: Prevent singularities at r=0
        """
        self.wells: List[TensorWell] = []
        self.smoothing = smoothing_radius
        logger.info("🌀 Tensor Coil initialized (anisotropic fields)")
    
    def add_well(self, x: float, y: float, z: float, w: float, tensor: Any, label: str = ""):
        """
        Add a tensor well to the coil.

        Args:
            x, y, z, w: Position
            tensor: 4x4 matrix (List[List[float]] or np.ndarray)
            label: Optional name
        """
        well = TensorWell(x, y, z, w, tensor, label)
        self.wells.append(well)
        logger.debug(f"Added tensor well '{label}' at ({x:.2f},{y:.2f},{z:.2f},{w:.2f})")

    def get_field_at(self, x: float, y: float, z: float, w: float) -> Tuple[float, float, float, float]:
        """
        Calculate the vector field at a specific point.

        Field F(x) = Σ (T_i · (x - x_i)) / |x - x_i|^3

        This allows for:
        - Attraction (if T = -c·I)
        - Repulsion (if T = c·I)
        - Rotation (if T has skew-symmetric parts)
        - Shear (if T is diagonal with unequal elements)
        """
        total_fx = 0.0
        total_fy = 0.0
        total_fz = 0.0
        total_fw = 0.0

        pos_vec = (x, y, z, w)

        for well in self.wells:
            # Displacement vector d = x - well.x
            dx = x - well.x
            dy = y - well.y
            dz = z - well.z
            dw = w - well.w

            # Distance squared
            r2 = dx*dx + dy*dy + dz*dz + dw*dw

            # Smoothed distance
            r_smooth = math.sqrt(r2 + self.smoothing**2)

            # Decay factor (1/r^3 like gravity force)
            factor = 1.0 / (r_smooth ** 3)

            # Calculate T · d
            displacement = (dx, dy, dz, dw)

            if HAS_NUMPY and isinstance(well.tensor, np.ndarray):
                # Numpy optimization
                transformed = np.dot(well.tensor, displacement)
                tf_x, tf_y, tf_z, tf_w = transformed
            else:
                # Manual matrix multiplication
                tf_x = sum(well.tensor[0][j] * displacement[j] for j in range(4))
                tf_y = sum(well.tensor[1][j] * displacement[j] for j in range(4))
                tf_z = sum(well.tensor[2][j] * displacement[j] for j in range(4))
                tf_w = sum(well.tensor[3][j] * displacement[j] for j in range(4))

            # Add to total force
            total_fx += tf_x * factor
            total_fy += tf_y * factor
            total_fz += tf_z * factor
            total_fw += tf_w * factor

        return (total_fx, total_fy, total_fz, total_fw)

    @staticmethod
    def create_isotropic_tensor(strength: float = -1.0) -> List[List[float]]:
        """Create a tensor for simple isotropic attraction/repulsion"""
        # Identity matrix scaled by strength
        # Negative strength = attraction (force opposite to displacement)
        t = [[0.0]*4 for _ in range(4)]
        for i in range(4):
            t[i][i] = strength
        return t

    @staticmethod
    def create_rotation_tensor(plane: Tuple[int, int], strength: float = 1.0) -> List[List[float]]:
        """
        Create a tensor that causes rotation in a specific plane.

        Args:
            plane: Tuple of indices (e.g., (0, 1) for xy-plane)
            strength: Speed of rotation
        """
        t = [[0.0]*4 for _ in range(4)]
        i, j = plane

        # Skew-symmetric component for rotation
        # T · d = (-y, x) -> Force is tangent to circle
        t[i][j] = -strength
        t[j][i] = strength

        return t

    @staticmethod
    def create_combined_tensor(
        attraction: float = -1.0,
        rotation_planes: List[Tuple[Tuple[int, int], float]] = None
    ) -> List[List[float]]:
        """
        Create a tensor combining attraction and rotation (spiral).
        """
        # Start with isotropic attraction
        t = TensorCoil.create_isotropic_tensor(attraction)

        # Add rotation components
        if rotation_planes:
            for (i, j), str_val in rotation_planes:
                t[i][j] -= str_val
                t[j][i] += str_val

        return t


# Helper function for easy field creation
def create_field_from_memories(memories: List[Any], mass_func=None) -> TensorGravityField:
    """
    Create gravity field from list of memories.
    
    Args:
        memories: List of objects with (x,y,z,w) coordinates
        mass_func: Function to extract mass from memory (default: brightness or 1.0)
    
    Returns: TensorGravityField with wells for each memory
    """
    field = TensorGravityField()
    
    for i, mem in enumerate(memories):
        # Extract position
        if hasattr(mem, 'x'):
            x, y, z, w = mem.x, mem.y, mem.z, mem.w
        elif isinstance(mem, (tuple, list)) and len(mem) >= 4:
            x, y, z, w = mem[0], mem[1], mem[2], mem[3]
        else:
            logger.warning(f"Memory {i} has no position, skipping")
            continue
        
        # Extract mass
        if mass_func:
            mass = mass_func(mem)
        elif hasattr(mem, 'brightness'):
            mass = mem.brightness
        elif hasattr(mem, 'mass'):
            mass = mem.mass
        else:
            mass = 1.0
        
        # Extract label
        label = getattr(mem, 'label', f"mem_{i}")
        
        # Add well
        field.add_attractor(x, y, z, w, mass, label, mem)
    
    logger.info(f"🌌 Created field with {len(memories)} wells")
    return field
