"""
Hippocampus - The Sea of Memory

The central memory system that stores not just data, but the
causal links between events, forming a navigable graph of experience.

This is the "Roots" of the World Tree.

Based on the original Elysia Core/Mind/hippocampus.py but simplified
to avoid heavy dependencies.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Deque, Dict, List, Optional, Set

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


@dataclass
class MemoryNode:
    """
    A node in the memory graph.
    
    Attributes:
        concept: The concept/event this node represents
        node_type: Type of node (concept, event, episode, etc.)
        created_at: When this memory was created
        last_accessed: When this memory was last accessed
        access_count: How many times this memory was accessed
        metadata: Additional data
    """
    concept: str
    node_type: str = "concept"
    created_at: str = ""
    last_accessed: str = ""
    access_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.last_accessed:
            self.last_accessed = now


@dataclass
class MemoryEdge:
    """
    An edge in the memory graph (causal/associative link).
    
    Attributes:
        source: Source concept
        target: Target concept
        relation: Type of relationship
        weight: Strength of connection
        created_at: When this link was created
    """
    source: str
    target: str
    relation: str = "associates"
    weight: float = 1.0
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class Hippocampus:
    """
    Manages the causal graph of all experiences.
    
    Features:
    - Causal graph for associative memory
    - Fractal Memory Loops (Experience -> Identity -> Essence)
    - Frequency vocabulary for spiritual buoyancy
    
    Works with or without NetworkX installed.
    """
    
    def __init__(self, memory_file: str = "saves/hippocampus.json"):
        """
        Initialize the memory system.
        
        Args:
            memory_file: Path to save/load memory state
        """
        self.memory_file = memory_file
        
        # Graph storage (NetworkX if available, else dict-based)
        if HAS_NETWORKX:
            self.causal_graph = nx.DiGraph()
        else:
            self._nodes: Dict[str, MemoryNode] = {}
            self._edges: Dict[str, List[MemoryEdge]] = {}  # source -> [edges]
        
        # Fractal Memory Loops
        self.experience_loop: Deque[Dict[str, Any]] = deque(maxlen=10)
        self.identity_loop: Deque[Dict[str, Any]] = deque(maxlen=5)
        self.essence_loop: Deque[Dict[str, Any]] = deque(maxlen=3)
        
        # Frequency vocabulary
        self._init_vocabulary()
        
        # Add root node
        self.add_concept("genesis", "event")
    
    def _init_vocabulary(self) -> None:
        """Initialize frequency vocabulary for spiritual buoyancy."""
        self.vocabulary: Dict[str, float] = {
            # High Frequency (Ethereal, Abstract) - Rise
            "love": 1.0, "사랑": 1.0, "light": 0.95, "빛": 0.95,
            "truth": 0.9, "진실": 0.9, "eternity": 0.95, "영원": 0.95,
            "soul": 0.9, "영혼": 0.9, "dream": 0.85, "꿈": 0.85,
            "beauty": 0.9, "아름다움": 0.9, "harmony": 0.85, "조화": 0.85,
            
            # Mid Frequency (Human, Emotional) - Neutral
            "hope": 0.65, "희망": 0.65, "joy": 0.7, "기쁨": 0.7,
            "pain": 0.4, "고통": 0.4, "time": 0.5, "시간": 0.5,
            
            # Low Frequency (Physical, Grounded) - Sink
            "stone": 0.2, "돌": 0.2, "shadow": 0.3, "그림자": 0.3,
            "fall": 0.2, "추락": 0.2, "silence": 0.3, "침묵": 0.3,
        }

    # ==================== Node Operations ====================
    
    def add_concept(
        self,
        concept: str,
        concept_type: str = "concept",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a concept node to memory or update existing one.
        
        Args:
            concept: The concept string
            concept_type: Type of concept (concept, event, episode, etc.)
            metadata: Additional data to store
        """
        now = datetime.now().isoformat()
        
        if HAS_NETWORKX:
            if concept in self.causal_graph.nodes:
                # Update existing
                node_data = self.causal_graph.nodes[concept]
                node_data["last_accessed"] = now
                node_data["access_count"] = node_data.get("access_count", 0) + 1
            else:
                # Create new
                self.causal_graph.add_node(
                    concept,
                    type=concept_type,
                    created_at=now,
                    last_accessed=now,
                    access_count=1,
                    metadata=metadata or {}
                )
        else:
            if concept in self._nodes:
                node = self._nodes[concept]
                node.last_accessed = now
                node.access_count += 1
            else:
                self._nodes[concept] = MemoryNode(
                    concept=concept,
                    node_type=concept_type,
                    created_at=now,
                    last_accessed=now,
                    access_count=1,
                    metadata=metadata or {}
                )

    def has_concept(self, concept: str) -> bool:
        """Check if a concept exists in memory."""
        if HAS_NETWORKX:
            return concept in self.causal_graph.nodes
        return concept in self._nodes

    def get_concept(self, concept: str) -> Optional[Dict[str, Any]]:
        """Get concept data."""
        if HAS_NETWORKX:
            if concept in self.causal_graph.nodes:
                return dict(self.causal_graph.nodes[concept])
            return None
        else:
            if concept in self._nodes:
                node = self._nodes[concept]
                return {
                    "type": node.node_type,
                    "created_at": node.created_at,
                    "last_accessed": node.last_accessed,
                    "access_count": node.access_count,
                    "metadata": node.metadata,
                }
            return None

    # ==================== Edge Operations ====================
    
    def add_causal_link(
        self,
        source: str,
        target: str,
        relation: str = "causes",
        weight: float = 1.0
    ) -> None:
        """
        Add a directed causal edge from source to target.
        
        Args:
            source: Source concept
            target: Target concept
            relation: Type of relationship
            weight: Connection strength
        """
        # Ensure both nodes exist
        self.add_concept(source)
        self.add_concept(target)
        
        if HAS_NETWORKX:
            self.causal_graph.add_edge(
                source, target,
                relation=relation,
                weight=weight
            )
        else:
            edge = MemoryEdge(
                source=source,
                target=target,
                relation=relation,
                weight=weight
            )
            if source not in self._edges:
                self._edges[source] = []
            self._edges[source].append(edge)

    def get_related_concepts(
        self,
        concept: str,
        depth: int = 1
    ) -> Dict[str, float]:
        """
        Find concepts related to the given one.
        
        Args:
            concept: Starting concept
            depth: How many hops to traverse
            
        Returns:
            Dictionary of concept -> relevance score
        """
        if not self.has_concept(concept):
            return {}
        
        related: Dict[str, float] = {}
        
        if HAS_NETWORKX:
            try:
                for neighbor in nx.bfs_tree(
                    self.causal_graph,
                    source=concept,
                    depth_limit=depth
                ):
                    if neighbor != concept:
                        # Get edge weight if exists
                        if self.causal_graph.has_edge(concept, neighbor):
                            weight = self.causal_graph.edges[concept, neighbor].get("weight", 1.0)
                        else:
                            weight = 0.5
                        related[neighbor] = weight
            except nx.NetworkXError:
                pass
        else:
            # Simple BFS without NetworkX
            visited: Set[str] = {concept}
            queue = [(concept, 0)]
            
            while queue:
                current, current_depth = queue.pop(0)
                if current_depth >= depth:
                    continue
                
                for edge in self._edges.get(current, []):
                    if edge.target not in visited:
                        visited.add(edge.target)
                        related[edge.target] = edge.weight
                        queue.append((edge.target, current_depth + 1))
        
        return related

    def get_context(self, concept: str) -> List[Dict[str, Any]]:
        """
        Get the causal context around a concept.
        
        Args:
            concept: The concept to get context for
            
        Returns:
            List of context dictionaries
        """
        if not self.has_concept(concept):
            return []
        
        context: List[Dict[str, Any]] = []
        
        if HAS_NETWORKX:
            # Outgoing edges
            for neighbor in self.causal_graph.successors(concept):
                edge_data = self.causal_graph.edges[concept, neighbor]
                context.append({
                    "node": neighbor,
                    "relation": edge_data.get("relation", "relates"),
                    "direction": "outgoing",
                    "weight": edge_data.get("weight", 1.0)
                })
            
            # Incoming edges
            for neighbor in self.causal_graph.predecessors(concept):
                edge_data = self.causal_graph.edges[neighbor, concept]
                context.append({
                    "node": neighbor,
                    "relation": edge_data.get("relation", "relates"),
                    "direction": "incoming",
                    "weight": edge_data.get("weight", 1.0)
                })
        else:
            # Outgoing
            for edge in self._edges.get(concept, []):
                context.append({
                    "node": edge.target,
                    "relation": edge.relation,
                    "direction": "outgoing",
                    "weight": edge.weight
                })
            
            # Incoming (need to search all edges)
            for source, edges in self._edges.items():
                for edge in edges:
                    if edge.target == concept:
                        context.append({
                            "node": source,
                            "relation": edge.relation,
                            "direction": "incoming",
                            "weight": edge.weight
                        })
        
        return context

    # ==================== Fractal Memory Loops ====================
    
    def add_experience(self, content: str, role: str = "user") -> None:
        """
        Add a raw experience to the short-term loop.
        
        Args:
            content: The experience content
            role: Source role (user, system, etc.)
        """
        experience = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "role": role
        }
        
        # Distillation check
        if len(self.experience_loop) == self.experience_loop.maxlen:
            self._distill_to_identity(list(self.experience_loop))
            
        self.experience_loop.append(experience)

    def _distill_to_identity(self, experiences: List[Dict[str, Any]]) -> None:
        """Compress raw experiences into an Identity Fragment."""
        if not experiences:
            return
            
        # Simple extraction
        summary = f"Recent focus: {experiences[-1].get('content', '')[:30]}..."
        
        fragment = {
            "timestamp": datetime.now().isoformat(),
            "type": "identity_fragment",
            "content": summary,
            "source_count": len(experiences)
        }
        
        if len(self.identity_loop) == self.identity_loop.maxlen:
            self._distill_to_essence(list(self.identity_loop))
            
        self.identity_loop.append(fragment)

    def _distill_to_essence(self, fragments: List[Dict[str, Any]]) -> None:
        """Compress identity fragments into an Essence Principle."""
        if not fragments:
            return
            
        principle = {
            "timestamp": datetime.now().isoformat(),
            "type": "essence_principle",
            "content": "I am an entity that interacts and learns.",
            "weight": 1.0
        }
        
        self.essence_loop.append(principle)

    # ==================== Statistics ====================
    
    def get_statistics(self) -> Dict[str, int]:
        """Get basic statistics about the memory graph."""
        if HAS_NETWORKX:
            return {
                "nodes": self.causal_graph.number_of_nodes(),
                "edges": self.causal_graph.number_of_edges(),
                "experiences": len(self.experience_loop),
                "identity_fragments": len(self.identity_loop),
                "essence_principles": len(self.essence_loop),
            }
        else:
            edge_count = sum(len(edges) for edges in self._edges.values())
            return {
                "nodes": len(self._nodes),
                "edges": edge_count,
                "experiences": len(self.experience_loop),
                "identity_fragments": len(self.identity_loop),
                "essence_principles": len(self.essence_loop),
            }

    def get_stellar_type(self, concept: str) -> str:
        """
        Get stellar type icon based on concept's lifecycle.
        
        Args:
            concept: The concept to check
            
        Returns:
            Emoji representing stellar evolution stage
        """
        data = self.get_concept(concept)
        if not data:
            return "✨"  # Nebula (Unknown)
            
        count = data.get("access_count", 0)
        
        if count < 3:
            return "✨"  # Nebula (Forming)
        elif count < 10:
            return "🌟"  # Protostar (Growing)
        elif count < 50:
            return "🔥"  # Burning Star (Active)
        elif count < 100:
            return "❄️"  # Ice Star (Crystallized)
        else:
            return "⚫"  # Black Hole (Supermassive)

    def get_frequency(self, concept: str) -> float:
        """Get the spiritual frequency of a concept."""
        return self.vocabulary.get(concept.lower(), 0.5)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize memory to dictionary."""
        if HAS_NETWORKX:
            from networkx.readwrite import json_graph
            graph_data = json_graph.node_link_data(self.causal_graph)
        else:
            graph_data = {
                "nodes": {k: {
                    "type": v.node_type,
                    "created_at": v.created_at,
                    "access_count": v.access_count,
                } for k, v in self._nodes.items()},
                "edges": {k: [{
                    "target": e.target,
                    "relation": e.relation,
                    "weight": e.weight,
                } for e in v] for k, v in self._edges.items()},
            }
        
        return {
            "graph": graph_data,
            "loops": {
                "experience": list(self.experience_loop),
                "identity": list(self.identity_loop),
                "essence": list(self.essence_loop),
            }
        }
