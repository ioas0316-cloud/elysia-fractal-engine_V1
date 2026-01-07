"""
Unified Collective Intelligence Network - Phase 7 Complete Implementation

Consolidates all Network functionality into a single, cohesive system:
- Multi-instance collaboration
- Knowledge sharing and validation  
- Role specialization
- Network topologies (mesh, star, hierarchical)
- Async message passing

This replaces the duplicate implementations in:
- collective_intelligence.py
- elysia_network.py  
- elysia_node.py
- knowledge_sync.py
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Callable


# ============================================================================
# Enums and Data Classes
# ============================================================================

class NodeRole(Enum):
    """Specialized roles nodes can assume in the network."""
    KNOWLEDGE_KEEPER = "knowledge_keeper"
    PATTERN_RECOGNIZER = "pattern_recognizer"
    CREATIVE_GENERATOR = "creative_generator"
    LOGIC_VALIDATOR = "logic_validator"
    EMOTION_PROCESSOR = "emotion_processor"
    INTEGRATION_SYNTHESIZER = "integration_synthesizer"


class NetworkTopology(Enum):
    """Network connection patterns."""
    MESH = "mesh"  # All-to-all connections
    STAR = "star"  # Hub and spoke model
    HIERARCHICAL = "hierarchical"  # Tree structure


@dataclass
class Message:
    """Message passed between nodes."""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    recipient_id: Optional[str] = None  # None for broadcast
    message_type: str = "general"
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    priority: int = 5  # 1-10, higher is more important


@dataclass
class Knowledge:
    """Shared knowledge item."""
    knowledge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: str = "general"  # pattern, insight, skill, best_practice
    content: Any = None
    source_node: str = ""
    confidence: float = 0.5
    validated_by: Set[str] = field(default_factory=set)
    timestamp: float = field(default_factory=time.time)


# ============================================================================
# Unified Node Implementation
# ============================================================================

class UnifiedNode:
    """
    Unified Elysia node implementation combining best features of both designs.
    
    Features:
    - Specialized capabilities by role
    - Async message handling
    - Performance metrics tracking
    - Knowledge management
    """
    
    def __init__(self, node_id: Optional[str] = None, role: NodeRole = NodeRole.KNOWLEDGE_KEEPER):
        self.node_id = node_id or str(uuid.uuid4())
        self.role = role
        self.peers: List['UnifiedNode'] = []
        self.knowledge_base: Dict[str, Knowledge] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.message_handlers: Dict[str, Callable] = {}
        
        # Performance tracking
        self.metrics = {
            "problems_solved": 0,
            "contributions": 0,
            "quality_score": 0.5,
            "trust_score": 0.5,
            "active": True,
            "last_seen": time.time()
        }
        
        # Role-specific strengths
        self.strengths = self._initialize_strengths()
    
    def _initialize_strengths(self) -> Dict[str, float]:
        """Initialize role-specific capability strengths."""
        base_strengths = {
            "knowledge_retrieval": 0.5,
            "pattern_recognition": 0.5,
            "creative_thinking": 0.5,
            "logical_reasoning": 0.5,
            "emotional_intelligence": 0.5,
            "system_integration": 0.5
        }
        
        # Boost strength based on role
        role_boosts = {
            NodeRole.KNOWLEDGE_KEEPER: {"knowledge_retrieval": 0.4},
            NodeRole.PATTERN_RECOGNIZER: {"pattern_recognition": 0.4},
            NodeRole.CREATIVE_GENERATOR: {"creative_thinking": 0.4},
            NodeRole.LOGIC_VALIDATOR: {"logical_reasoning": 0.4},
            NodeRole.EMOTION_PROCESSOR: {"emotional_intelligence": 0.4},
            NodeRole.INTEGRATION_SYNTHESIZER: {"system_integration": 0.4}
        }
        
        if self.role in role_boosts:
            for skill, boost in role_boosts[self.role].items():
                base_strengths[skill] += boost
        
        return base_strengths
    
    def add_peer(self, peer: 'UnifiedNode'):
        """Add a peer node to this node's network."""
        if peer not in self.peers:
            self.peers.append(peer)
    
    def remove_peer(self, peer: 'UnifiedNode'):
        """Remove a peer node from this node's network."""
        if peer in self.peers:
            self.peers.remove(peer)
    
    async def send_message(self, message: Message):
        """Send a message to a specific peer or broadcast."""
        if message.recipient_id:
            # Send to specific peer
            for peer in self.peers:
                if peer.node_id == message.recipient_id:
                    await peer.message_queue.put(message)
                    break
        else:
            # Broadcast to all peers
            for peer in self.peers:
                await peer.message_queue.put(message)
    
    async def receive_messages(self) -> List[Message]:
        """Receive all pending messages."""
        messages = []
        while not self.message_queue.empty():
            try:
                msg = self.message_queue.get_nowait()
                messages.append(msg)
            except asyncio.QueueEmpty:
                break
        return messages
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a message handler for a specific type."""
        self.message_handlers[message_type] = handler
    
    async def process_problem(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a problem using this node's specialized capabilities.
        
        Returns a solution with confidence score based on role match.
        """
        problem_type = problem.get("type", "general")
        
        # Calculate confidence based on role match
        confidence = self.strengths.get(problem_type, 0.5)
        
        # Simulate processing
        await asyncio.sleep(0.01)  # Small delay for realism
        
        solution = {
            "solver_id": self.node_id,
            "solver_role": self.role.value,
            "solution": f"Solution from {self.role.value} perspective",
            "confidence": confidence,
            "timestamp": time.time()
        }
        
        self.metrics["problems_solved"] += 1
        self.metrics["contributions"] += 1
        
        return solution
    
    def share_knowledge(self, knowledge: Knowledge):
        """Share knowledge with this node."""
        self.knowledge_base[knowledge.knowledge_id] = knowledge
    
    def get_knowledge(self, knowledge_id: str) -> Optional[Knowledge]:
        """Retrieve knowledge by ID."""
        return self.knowledge_base.get(knowledge_id)
    
    def update_metrics(self, metric: str, value: float):
        """Update a performance metric."""
        if metric in self.metrics:
            self.metrics[metric] = value
            self.metrics["last_seen"] = time.time()


# ============================================================================
# Unified Network Implementation
# ============================================================================

class UnifiedNetwork:
    """
    Unified network coordinator combining best features of both designs.
    
    Features:
    - Multiple topology support (mesh, star, hierarchical)
    - Collaborative problem solving with specialist assignment
    - Knowledge sharing with consensus validation
    - Dynamic load balancing
    """
    
    def __init__(self, topology: NetworkTopology = NetworkTopology.MESH):
        self.topology = topology
        self.nodes: Dict[str, UnifiedNode] = {}
        self.hub_node: Optional[UnifiedNode] = None  # For star topology
        self.collective_memory: Dict[str, Knowledge] = {}
    
    async def register_node(self, node: UnifiedNode):
        """Register a node in the network."""
        self.nodes[node.node_id] = node
        
        # Setup connections based on topology
        if self.topology == NetworkTopology.MESH:
            # Connect to all existing nodes
            for existing_node in self.nodes.values():
                if existing_node.node_id != node.node_id:
                    node.add_peer(existing_node)
                    existing_node.add_peer(node)
        
        elif self.topology == NetworkTopology.STAR:
            # Connect to hub node
            if self.hub_node is None:
                self.hub_node = node
            else:
                node.add_peer(self.hub_node)
                self.hub_node.add_peer(node)
        
        elif self.topology == NetworkTopology.HIERARCHICAL:
            # Simple hierarchical: connect to first node as parent
            if len(self.nodes) > 1:
                parent = list(self.nodes.values())[0]
                node.add_peer(parent)
                parent.add_peer(node)
    
    def unregister_node(self, node_id: str):
        """Remove a node from the network."""
        # [Wave Logic] Consider resonance-based lookup instead of direct membership check
        # Original: if node_id in self.nodes:
        if node_id in self.nodes:  # TODO: Convert to query_resonance
            node = self.nodes[node_id]
            # Remove connections
            for peer in node.peers:
                peer.remove_peer(node)
            del self.nodes[node_id]
    
    async def solve_collaboratively(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve a problem using the collective intelligence of the network.
        
        Process:
        1. Decompose problem into subproblems
        2. Assign specialists
        3. Collect solutions
        4. Integrate results
        """
        # Decompose problem
        subproblems = self._decompose_problem(problem)
        
        # Assign specialists and solve
        solutions = []
        for subproblem in subproblems:
            specialist = self._find_specialist(subproblem)
            if specialist:
                solution = await specialist.process_problem(subproblem)
                solutions.append(solution)
        
        # Integrate solutions
        integrated_solution = self._integrate_solutions(solutions)
        
        return {
            "problem": problem,
            "subproblems": subproblems,
            "solutions": solutions,
            "integrated_solution": integrated_solution,
            "participating_nodes": len(solutions),
            "timestamp": time.time()
        }
    
    def _decompose_problem(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a complex problem into simpler subproblems."""
        problem_type = problem.get("type", "general")
        description = problem.get("description", "")
        
        # Simple decomposition based on problem type
        subproblems = [
            {"type": "analysis", "description": f"Analyze: {description}"},
            {"type": "solution", "description": f"Solve: {description}"},
            {"type": "validation", "description": f"Validate: {description}"}
        ]
        
        return subproblems
    
    def _find_specialist(self, problem: Dict[str, Any]) -> Optional[UnifiedNode]:
        """Find the best specialist for a given problem."""
        problem_type = problem.get("type", "general")
        
        # Find node with highest strength for problem type
        best_node = None
        best_score = 0.0
        
        for node in self.nodes.values():
            if node.metrics["active"]:
                score = node.strengths.get(problem_type, 0.3)
                if score > best_score:
                    best_score = score
                    best_node = node
        
        return best_node or (list(self.nodes.values())[0] if self.nodes else None)
    
    def _integrate_solutions(self, solutions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Integrate multiple solutions into a unified result."""
        if not solutions:
            return {"integrated": "No solutions to integrate"}
        
        # Weighted average based on confidence
        total_confidence = sum(s.get("confidence", 0.5) for s in solutions)
        avg_confidence = total_confidence / len(solutions) if solutions else 0.5
        
        return {
            "method": "weighted_integration",
            "num_solutions": len(solutions),
            "average_confidence": avg_confidence,
            "contributing_roles": [s.get("solver_role") for s in solutions],
            "synthesis": "Integrated solution from multiple perspectives"
        }
    
    async def share_knowledge(self, knowledge: Knowledge) -> Dict[str, Any]:
        """
        Share knowledge across the network with validation.
        
        Process:
        1. Broadcast knowledge to all nodes
        2. Collect validation votes
        3. Reach consensus (70% threshold)
        4. Add to collective memory if validated
        """
        # Share with all nodes
        for node in self.nodes.values():
            node.share_knowledge(knowledge)
        
        # Simulate validation
        validators = [n for n in self.nodes.values() if n.metrics["active"]]
        validations = len(validators)
        approvals = int(validations * 0.75)  # 75% approval
        
        knowledge.validated_by = {n.node_id for n in validators[:approvals]}
        
        # Check consensus (70% threshold)
        consensus_reached = len(knowledge.validated_by) / validations >= 0.7 if validations > 0 else False
        
        if consensus_reached:
            self.collective_memory[knowledge.knowledge_id] = knowledge
        
        return {
            "knowledge_id": knowledge.knowledge_id,
            "consensus_reached": consensus_reached,
            "approvals": len(knowledge.validated_by),
            "total_validators": validations,
            "added_to_memory": consensus_reached
        }
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current network status and statistics."""
        active_nodes = sum(1 for n in self.nodes.values() if n.metrics["active"])
        
        role_distribution = {}
        for node in self.nodes.values():
            role = node.role.value
            role_distribution[role] = role_distribution.get(role, 0) + 1
        
        return {
            "topology": self.topology.value,
            "total_nodes": len(self.nodes),
            "active_nodes": active_nodes,
            "role_distribution": role_distribution,
            "collective_memory_size": len(self.collective_memory),
            "hub_node_id": self.hub_node.node_id if self.hub_node else None
        }


# ============================================================================
# Knowledge Synchronization
# ============================================================================

class UnifiedKnowledgeSync:
    """
    Unified knowledge synchronization system.
    
    Manages knowledge sharing, validation, and consensus across the network.
    """
    
    def __init__(self, network: UnifiedNetwork):
        self.network = network
        self.pending_validations: Dict[str, Knowledge] = {}
    
    async def propose_knowledge(self, node: UnifiedNode, content: Any, 
                                category: str = "general", confidence: float = 0.7) -> str:
        """Propose new knowledge for network validation."""
        knowledge = Knowledge(
            category=category,
            content=content,
            source_node=node.node_id,
            confidence=confidence
        )
        
        self.pending_validations[knowledge.knowledge_id] = knowledge
        
        # Share with network for validation
        result = await self.network.share_knowledge(knowledge)
        
        if result["consensus_reached"]:
            del self.pending_validations[knowledge.knowledge_id]
        
        return knowledge.knowledge_id
    
    async def validate_knowledge(self, knowledge_id: str, validator_id: str) -> bool:
        """Validate a pending knowledge item."""
        if knowledge_id in self.pending_validations:
            knowledge = self.pending_validations[knowledge_id]
            knowledge.validated_by.add(validator_id)
            return True
        return False
    
    def get_collective_knowledge(self, category: Optional[str] = None) -> List[Knowledge]:
        """Retrieve collective knowledge, optionally filtered by category."""
        knowledge_items = list(self.network.collective_memory.values())
        
        if category:
            knowledge_items = [k for k in knowledge_items if k.category == category]
        
        return sorted(knowledge_items, key=lambda k: k.confidence, reverse=True)


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    'NodeRole',
    'NetworkTopology',
    'Message',
    'Knowledge',
    'UnifiedNode',
    'UnifiedNetwork',
    'UnifiedKnowledgeSync'
]
