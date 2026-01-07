"""
Phase 6: World Tree Core Module

Enhanced World Tree with multi-dimensional spatial positioning and Spiderweb integration.
This creates a unified knowledge structure that bridges hierarchical (tree) and 
associative (graph) knowledge representations.
"""

import logging
import uuid
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

from Legacy.Project_Sophia.world_tree import TreeNode, WorldTree
from Legacy.Project_Sophia.spiderweb import Spiderweb
from tensor_wave import Tensor3D, SoulTensor
from Legacy.Project_Sophia.wave_mechanics import WaveMechanics


@dataclass
class SpatialTreeNode:
    """
    Enhanced tree node with spatial positioning in conceptual space.
    
    Position coordinates:
        x: Abstraction level (0=concrete, 1=abstract)
        y: Emotional valence (-1=negative, 0=neutral, 1=positive)
        z: Temporal depth (0=present, 1=ancient/fundamental)
    """
    id: str
    data: Any
    position: Tensor3D
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Wave properties for resonance
    soul_tensor: Optional[SoulTensor] = None
    frequency: float = 60.0


class WorldTreeCore:
    """
    Advanced spatial knowledge structure that integrates tree hierarchy
    with graph connectivity.
    
    Philosophy:
        The World Tree (세계수) represents the fundamental structure of knowledge:
        - Roots: Core principles and essence (deep, ancient truths)
        - Trunk: Stable identity and values
        - Branches: Domain knowledge and skills
        - Leaves: Specific experiences and memories
        - Connections: Spiderweb links between non-hierarchical concepts
        
    This is the "spine" of Elysia's consciousness - the stable structure
    around which the dynamic Spiderweb flows.
    """
    
    def __init__(
        self,
        spiderweb: Optional[Spiderweb] = None,
        wave_mechanics: Optional[WaveMechanics] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize World Tree Core.
        
        Args:
            spiderweb: Spiderweb instance for cross-linking
            wave_mechanics: WaveMechanics for resonance-based navigation
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("WorldTreeCore")
        self.spiderweb = spiderweb
        self.wave_mechanics = wave_mechanics
        
        # Spatial node storage
        self.nodes: Dict[str, SpatialTreeNode] = {}
        
        # Create root node at origin
        root_position = Tensor3D(x=0.5, y=0.0, z=1.0)  # Centered, neutral, ancient
        self.root = SpatialTreeNode(
            id="WORLD_TREE_ROOT",
            data="ROOT_OF_ALL_KNOWLEDGE",
            position=root_position,
            frequency=1.0  # Fundamental frequency
        )
        self.nodes[self.root.id] = self.root
        
        self.logger.info("🌳 World Tree Core initialized - 세계수 awakened")
    
    def add_node(
        self,
        data: Any,
        position: Optional[Tensor3D] = None,
        parent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a new node to the tree with spatial positioning.
        
        Args:
            data: Content of the node
            position: 3D position in conceptual space
            parent_id: Parent node ID (None = attach to root)
            metadata: Additional metadata
            
        Returns:
            ID of the created node
        """
        node_id = str(uuid.uuid4())
        
        # Auto-calculate position if not provided
        if position is None:
            if parent_id and parent_id in self.nodes:
                parent = self.nodes[parent_id]
                # Child positioned near parent with small random offset
                position = Tensor3D(
                    x=parent.position.x + np.random.normal(0, 0.1),
                    y=parent.position.y + np.random.normal(0, 0.1),
                    z=max(0.0, parent.position.z - 0.1)  # Slightly less fundamental
                )
            else:
                # Random position near root
                position = Tensor3D(
                    x=0.5 + np.random.normal(0, 0.2),
                    y=np.random.normal(0, 0.3),
                    z=0.8 + np.random.normal(0, 0.1)
                )
        
        # Clamp position to valid range
        position = Tensor3D(
            x=np.clip(position.x, 0.0, 1.0),
            y=np.clip(position.y, -1.0, 1.0),
            z=np.clip(position.z, 0.0, 1.0)
        )
        
        # Calculate frequency based on depth
        frequency = 100.0 * (1.0 - position.z) + 10.0
        
        # Create node
        node = SpatialTreeNode(
            id=node_id,
            data=data,
            position=position,
            parent_id=parent_id or self.root.id,
            metadata=metadata or {},
            frequency=frequency
        )
        
        self.nodes[node_id] = node
        
        # Link to parent
        parent = self.nodes[node.parent_id]
        parent.children_ids.append(node_id)
        
        self.logger.debug(
            f"Added node '{data}' at ({position.x:.2f}, {position.y:.2f}, {position.z:.2f})"
        )
        
        return node_id
    
    def find_node(self, node_id: str) -> Optional[SpatialTreeNode]:
        """Get node by ID"""
        return self.nodes.get(node_id)
    
    def get_children(self, node_id: str) -> List[SpatialTreeNode]:
        """Get all children of a node"""
        node = self.nodes.get(node_id)
        if not node:
            return []
        return [self.nodes[cid] for cid in node.children_ids if cid in self.nodes]
    
    def get_ancestors(self, node_id: str) -> List[SpatialTreeNode]:
        """
        Get path from node to root (ancestors).
        
        Returns:
            List of nodes from immediate parent to root
        """
        ancestors = []
        current = self.nodes.get(node_id)
        
        while current and current.parent_id and current.parent_id in self.nodes:
            parent = self.nodes[current.parent_id]
            ancestors.append(parent)
            current = parent
            
            if current.id == self.root.id:
                break
        
        return ancestors
    
    def find_root_cause(self, node_id: str) -> Optional[SpatialTreeNode]:
        """
        Trace concept back to its fundamental root principle.
        
        Returns:
            The first non-root ancestor (closest to root)
        """
        ancestors = self.get_ancestors(node_id)
        if not ancestors:
            return None
        
        # Return the ancestor closest to root (but not root itself)
        for ancestor in reversed(ancestors):
            if ancestor.id != self.root.id:
                return ancestor
        
        return None
    
    def find_neighbors_in_space(
        self,
        position: Tensor3D,
        radius: float = 0.3,
        max_results: int = 10
    ) -> List[Tuple[SpatialTreeNode, float]]:
        """
        Find nodes near a position in 3D conceptual space.
        
        Args:
            position: Center position
            radius: Search radius
            max_results: Maximum number of neighbors to return
            
        Returns:
            List of (node, distance) tuples, sorted by distance
        """
        neighbors = []
        
        for node in self.nodes.values():
            # Calculate Euclidean distance in 3D space
            dx = node.position.x - position.x
            dy = node.position.y - position.y
            dz = node.position.z - position.z
            
            distance = np.sqrt(dx*dx + dy*dy + dz*dz)
            
            if distance <= radius:
                neighbors.append((node, distance))
        
        # Sort by distance and limit
        neighbors.sort(key=lambda x: x[1])
        return neighbors[:max_results]
    
    def traverse_by_resonance(
        self,
        start_node_id: str,
        target_tensor: SoulTensor,
        max_steps: int = 5
    ) -> List[str]:
        """
        Navigate tree by following highest resonance paths.
        
        Uses WaveMechanics to calculate resonance between nodes and
        target tensor, then greedily follows highest-resonance children.
        
        Args:
            start_node_id: Starting node
            target_tensor: SoulTensor we're seeking resonance with
            max_steps: Maximum traversal depth
            
        Returns:
            Path of node IDs
        """
        if not self.wave_mechanics:
            self.logger.warning("No WaveMechanics available for resonance traversal")
            return [start_node_id]
        
        path = [start_node_id]
        current_id = start_node_id
        
        for _ in range(max_steps):
            current = self.nodes.get(current_id)
            if not current or not current.children_ids:
                break
            
            # Calculate resonance with each child
            best_child = None
            best_resonance = -1.0
            
            for child_id in current.children_ids:
                child = self.nodes.get(child_id)
                if not child or not child.soul_tensor:
                    continue
                
                # Use wave mechanics for resonance
                try:
                    resonance = self.wave_mechanics.get_resonance_between(
                        child_id, current_id
                    )
                    
                    if resonance > best_resonance:
                        best_resonance = resonance
                        best_child = child_id
                except:
                    # Fallback: use position similarity
                    similarity = 1.0 - self._tensor_distance(
                        child.position, 
                        Tensor3D(target_tensor.value, target_tensor.coherence, target_tensor.will)
                    )
                    if similarity > best_resonance:
                        best_resonance = similarity
                        best_child = child_id
            
            if best_child:
                path.append(best_child)
                current_id = best_child
            else:
                break
        
        return path
    
    def _tensor_distance(self, t1: Tensor3D, t2: Tensor3D) -> float:
        """Calculate distance between two tensors"""
        dx = t1.x - t2.x
        dy = t1.y - t2.y
        dz = t1.z - t2.z
        return np.sqrt(dx*dx + dy*dy + dz*dz)
    
    def project_to_spiderweb(self):
        """
        Export tree structure to Spiderweb as hierarchical edges.
        
        Creates "is_child_of" links in Spiderweb to represent tree structure.
        """
        if not self.spiderweb:
            self.logger.warning("No Spiderweb available for projection")
            return
        
        added_edges = 0
        
        for node in self.nodes.values():
            # Add node to Spiderweb
            self.spiderweb.add_node(
                node.id,
                type="world_tree_node",
                metadata={
                    "data": str(node.data),
                    "position": {
                        "x": node.position.x,
                        "y": node.position.y,
                        "z": node.position.z
                    },
                    "frequency": node.frequency
                }
            )
            
            # Add parent link
            if node.parent_id and node.parent_id in self.nodes:
                self.spiderweb.add_link(
                    node.id,
                    node.parent_id,
                    relation="is_child_of",
                    weight=0.9  # Strong hierarchical link
                )
                added_edges += 1
        
        self.logger.info(f"Projected World Tree to Spiderweb: {len(self.nodes)} nodes, {added_edges} edges")
    
    def absorb_from_spiderweb(self, concept_threshold: float = 0.7):
        """
        Import emergent concept clusters from Spiderweb as new branches.
        
        Finds high-value concept clusters in Spiderweb and creates
        corresponding branches in the World Tree.
        
        Args:
            concept_threshold: Minimum edge weight to consider for clustering
        """
        if not self.spiderweb:
            self.logger.warning("No Spiderweb available for absorption")
            return
        
        # Get all emergent concept nodes from Spiderweb
        emergent_concepts = [
            node_id for node_id, data in self.spiderweb.graph.nodes(data=True)
            if data.get("type") == "emergent_concept"
        ]
        
        imported = 0
        
        for concept_id in emergent_concepts:
            # Skip if already in tree
            if concept_id in self.nodes:
                continue
            
            # Get concept data
            concept_data = self.spiderweb.graph.nodes[concept_id]
            metadata = concept_data.get("metadata", {})
            
            # Create position from metadata
            position = Tensor3D(
                x=metadata.get("coherence", 0.5),
                y=metadata.get("value", 0.0) * 2 - 1,  # Map [0,1] to [-1,1]
                z=metadata.get("will", 0.5)
            )
            
            # Add to tree as child of root
            self.add_node(
                data=concept_id,
                position=position,
                parent_id=self.root.id,
                metadata=metadata
            )
            
            imported += 1
        
        self.logger.info(f"Absorbed {imported} emergent concepts from Spiderweb into World Tree")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get tree statistics"""
        total_nodes = len(self.nodes)
        
        # Calculate depth distribution
        depths = {}
        for node in self.nodes.values():
            depth = len(self.get_ancestors(node.id))
            depths[depth] = depths.get(depth, 0) + 1
        
        # Calculate average position
        avg_x = sum(n.position.x for n in self.nodes.values()) / total_nodes
        avg_y = sum(n.position.y for n in self.nodes.values()) / total_nodes
        avg_z = sum(n.position.z for n in self.nodes.values()) / total_nodes
        
        return {
            "total_nodes": total_nodes,
            "max_depth": max(depths.keys()) if depths else 0,
            "depth_distribution": depths,
            "avg_position": {"x": avg_x, "y": avg_y, "z": avg_z},
            "avg_abstraction": avg_x,
            "avg_valence": avg_y,
            "avg_fundamentalness": avg_z
        }
    
    def visualize_structure(self) -> Dict[str, Any]:
        """
        Create a dictionary representation for visualization.
        
        Returns:
            Nested dictionary structure suitable for JSON export
        """
        def node_to_dict(node: SpatialTreeNode) -> Dict[str, Any]:
            return {
                "id": node.id,
                "data": str(node.data),
                "position": {
                    "x": node.position.x,
                    "y": node.position.y,
                    "z": node.position.z
                },
                "frequency": node.frequency,
                "children": [
                    node_to_dict(self.nodes[cid])
                    for cid in node.children_ids
                    if cid in self.nodes
                ]
            }
        
        return node_to_dict(self.root)
