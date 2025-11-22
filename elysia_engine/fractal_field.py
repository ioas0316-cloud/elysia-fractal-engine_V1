from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

from .entities import Entity
from .physics import Attractor
from .chronos import ChronoField
from .topology import GravityPath
from .math_utils import Vector3


@dataclass
class ConceptNode(Entity):
    """
    Level 0: Point.
    A single data point or idea.
    """
    dimension: int = 0


@dataclass
class ConceptLine(Entity):
    """
    Level 1: Line.
    Formed by 2+ Nodes. Acts as a Path/TensorCoil.
    """
    dimension: int = 1
    nodes: List[ConceptNode] = field(default_factory=list)

    def to_gravity_path(self) -> GravityPath:
        """Transforms this concept line into a physical Gravity Path."""
        points = [n.physics.position for n in self.nodes]
        return GravityPath(points=points, radius=5.0)


@dataclass
class ConceptPlane(Entity):
    """
    Level 2: Plane/Field.
    Formed by resonating Lines. Acts as a ChronoField or Surface.
    """
    dimension: int = 2
    lines: List[ConceptLine] = field(default_factory=list)

    def to_chrono_field(self) -> ChronoField:
        """
        Transforms this plane into a Time Dilation Field.
        The logic is: A stable plane of ideas creates its own 'Time'.
        """
        # Center is average of all nodes
        total_pos = Vector3(0,0,0)
        count = 0
        for line in self.lines:
            for node in line.nodes:
                total_pos = total_pos + node.physics.position
                count += 1

        center = total_pos * (1.0/count) if count > 0 else Vector3(0,0,0)
        return ChronoField(position=center, radius=20.0, time_scale=2.0)


@dataclass
class ConceptSpace(Entity):
    """
    Level 3: Space/Law.
    Formed by stacked Planes. Acts as a Fundamental Law (Attractor/Gravity Well).
    """
    dimension: int = 3
    planes: List[ConceptPlane] = field(default_factory=list)

    def to_attractor(self) -> Attractor:
        """
        Transforms this space into a massive Attractor (The Truth).
        """
        # Center...
        return Attractor(id=self.id, position=self.physics.position, mass=10000.0)


class FractalEvolver:
    """
    Manages the ascension of concepts from Point -> Line -> Plane -> Space.
    """
    def evolve(self, entities: List[Entity]) -> Optional[Entity]:
        """
        Checks if a group of entities can fuse into a higher dimension.
        """
        # Simplistic logic:
        # 2 Nodes close -> Line
        # 3 Lines parallel -> Plane
        # 2 Planes stacked -> Space
        pass
        return None
