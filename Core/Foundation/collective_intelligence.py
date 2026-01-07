"""
Collective Intelligence Network - Multi-instance collaboration system.

Enables multiple Elysia instances to work together, share knowledge, and
solve problems collectively through distributed processing.
"""

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class NodeRole(Enum):
    """Roles that network nodes can assume."""
    COORDINATOR = "coordinator"  # Orchestrates tasks
    SPECIALIST = "specialist"    # Specialized expertise
    GENERALIST = "generalist"    # Broad knowledge
    LEARNER = "learner"          # Learning-focused
    VALIDATOR = "validator"      # Quality control


@dataclass
class NetworkNode:
    """Represents a node in the collective intelligence network."""
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: NodeRole = NodeRole.GENERALIST
    specialization: Optional[str] = None
    capabilities: List[str] = field(default_factory=list)
    trust_score: float = 0.5  # 0.0 to 1.0
    active: bool = True
    last_seen: float = field(default_factory=time.time)
    contributions: int = 0
    quality_score: float = 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "role": self.role.value,
            "specialization": self.specialization,
            "capabilities": self.capabilities,
            "trust_score": self.trust_score,
            "active": self.active,
            "last_seen": self.last_seen,
            "contributions": self.contributions,
            "quality_score": self.quality_score,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NetworkNode":
        data["role"] = NodeRole(data["role"])
        return cls(**data)


@dataclass
class CollaborativeTask:
    """A task distributed across network nodes."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    required_capabilities: List[str] = field(default_factory=list)
    priority: float = 0.5
    created_at: float = field(default_factory=time.time)
    assigned_nodes: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"  # pending, in_progress, completed, failed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "required_capabilities": self.required_capabilities,
            "priority": self.priority,
            "created_at": self.created_at,
            "assigned_nodes": self.assigned_nodes,
            "results": self.results,
            "status": self.status,
        }


class CollectiveIntelligence:
    """
    Manages collective intelligence network for multi-instance collaboration.
    
    Features:
    - Node discovery and registration
    - Dynamic role assignment
    - Task distribution and coordination
    - Result aggregation and consensus
    - Trust and quality scoring
    """
    
    def __init__(self, node_id: Optional[str] = None, data_dir: str = "data/network"):
        self.node_id = node_id or str(uuid.uuid4())
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Network state
        self.nodes: Dict[str, NetworkNode] = {}
        self.tasks: Dict[str, CollaborativeTask] = {}
        self.my_node: NetworkNode = NetworkNode(
            node_id=self.node_id,
            role=NodeRole.GENERALIST,
            capabilities=["thinking", "learning", "reflection"]
        )
        self.nodes[self.node_id] = self.my_node
        
        # Network statistics
        self.stats = {
            "total_nodes": 1,
            "active_nodes": 1,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_quality": 0.5,
            "network_uptime": time.time(),
        }
        
        self.load_state()
    
    def register_node(self, node: NetworkNode) -> bool:
        """Register a new node in the network."""
        if node.node_id in self.nodes:
            return False
        
        self.nodes[node.node_id] = node
        self.stats["total_nodes"] = len(self.nodes)
        self.stats["active_nodes"] = sum(1 for n in self.nodes.values() if n.active)
        
        self.save_state()
        return True
    
    def unregister_node(self, node_id: str) -> bool:
        """Remove a node from the network."""
        if node_id not in self.nodes or node_id == self.node_id:
            return False
        
        del self.nodes[node_id]
        self.stats["total_nodes"] = len(self.nodes)
        self.stats["active_nodes"] = sum(1 for n in self.nodes.values() if n.active)
        
        self.save_state()
        return True
    
    def find_capable_nodes(self, capabilities: List[str], min_trust: float = 0.3) -> List[NetworkNode]:
        """Find nodes with specific capabilities and minimum trust score."""
        capable_nodes = []
        
        for node in self.nodes.values():
            if not node.active or node.trust_score < min_trust:
                continue
            
            # Check if node has all required capabilities
            has_all = all(cap in node.capabilities for cap in capabilities)
            if has_all:
                capable_nodes.append(node)
        
        # Sort by trust score and quality score
        capable_nodes.sort(
            key=lambda n: (n.trust_score + n.quality_score) / 2,
            reverse=True
        )
        
        return capable_nodes
    
    async def create_task(
        self,
        description: str,
        required_capabilities: List[str],
        priority: float = 0.5
    ) -> CollaborativeTask:
        """Create a new collaborative task."""
        task = CollaborativeTask(
            description=description,
            required_capabilities=required_capabilities,
            priority=priority
        )
        
        self.tasks[task.task_id] = task
        
        # Assign to capable nodes
        capable_nodes = self.find_capable_nodes(required_capabilities)
        if capable_nodes:
            task.assigned_nodes = [n.node_id for n in capable_nodes[:3]]  # Limit to 3 nodes
            task.status = "in_progress"
        
        self.save_state()
        return task
    
    async def distribute_task(self, task: CollaborativeTask) -> Dict[str, Any]:
        """Distribute task to assigned nodes and collect results."""
        results = {}
        
        for node_id in task.assigned_nodes:
            if node_id not in self.nodes:
                continue
            
            node = self.nodes[node_id]
            
            # Simulate node processing (in real implementation, would send to node)
            result = await self._simulate_node_processing(node, task)
            results[node_id] = result
            
            # Update node stats
            node.contributions += 1
            node.last_seen = time.time()
        
        task.results = results
        task.status = "completed"
        self.stats["tasks_completed"] += 1
        
        self.save_state()
        return results
    
    async def _simulate_node_processing(
        self,
        node: NetworkNode,
        task: CollaborativeTask
    ) -> Dict[str, Any]:
        """Simulate a node processing a task."""
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Generate result based on node role and capabilities
        quality = node.quality_score
        
        result = {
            "node_id": node.node_id,
            "role": node.role.value,
            "quality": quality,
            "confidence": 0.7 + (quality * 0.3),
            "output": f"Result from {node.role.value} node",
            "processing_time": 0.1,
        }
        
        return result
    
    async def aggregate_results(self, task: CollaborativeTask) -> Dict[str, Any]:
        """Aggregate results from multiple nodes using consensus."""
        if not task.results:
            return {"error": "No results to aggregate"}
        
        # Calculate consensus
        qualities = [r.get("quality", 0.5) for r in task.results.values()]
        confidences = [r.get("confidence", 0.5) for r in task.results.values()]
        
        consensus = {
            "task_id": task.task_id,
            "num_contributors": len(task.results),
            "average_quality": sum(qualities) / len(qualities) if qualities else 0.5,
            "average_confidence": sum(confidences) / len(confidences) if confidences else 0.5,
            "individual_results": task.results,
            "consensus_reached": len(task.results) >= 2,
        }
        
        # Update network quality score
        if qualities:
            self.stats["average_quality"] = (
                self.stats["average_quality"] * 0.9 + consensus["average_quality"] * 0.1
            )
        
        return consensus
    
    def update_node_trust(self, node_id: str, feedback: float):
        """Update trust score for a node based on feedback."""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        
        # Moving average with decay
        node.trust_score = node.trust_score * 0.9 + feedback * 0.1
        node.trust_score = max(0.0, min(1.0, node.trust_score))
        
        self.save_state()
    
    def rebalance_network(self):
        """Dynamically rebalance node roles based on performance."""
        # Identify high-performing nodes
        sorted_nodes = sorted(
            [n for n in self.nodes.values() if n.node_id != self.node_id],
            key=lambda n: (n.quality_score + n.trust_score) / 2,
            reverse=True
        )
        
        # Promote top performers to specialist/coordinator roles
        for i, node in enumerate(sorted_nodes[:3]):
            if i == 0 and node.quality_score > 0.8:
                node.role = NodeRole.COORDINATOR
            elif node.quality_score > 0.7:
                node.role = NodeRole.SPECIALIST
        
        # Demote low performers
        for node in sorted_nodes[-3:]:
            if node.quality_score < 0.4:
                node.role = NodeRole.LEARNER
        
        self.save_state()
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get comprehensive network statistics."""
        active_nodes = [n for n in self.nodes.values() if n.active]
        
        role_distribution = {}
        for node in active_nodes:
            role_distribution[node.role.value] = role_distribution.get(node.role.value, 0) + 1
        
        return {
            **self.stats,
            "role_distribution": role_distribution,
            "active_nodes_detail": [n.to_dict() for n in active_nodes],
            "pending_tasks": sum(1 for t in self.tasks.values() if t.status == "pending"),
            "in_progress_tasks": sum(1 for t in self.tasks.values() if t.status == "in_progress"),
        }
    
    def save_state(self):
        """Save network state to disk."""
        state = {
            "node_id": self.node_id,
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()},
            "tasks": {tid: t.to_dict() for tid, t in self.tasks.items()},
            "stats": self.stats,
        }
        
        state_file = self.data_dir / "collective_intelligence_state.json"
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load network state from disk."""
        state_file = self.data_dir / "collective_intelligence_state.json"
        if not state_file.exists():
            return
        
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
            
            self.nodes = {
                nid: NetworkNode.from_dict(ndata)
                for nid, ndata in state.get("nodes", {}).items()
            }
            
            # Ensure my node is in the network
            if self.node_id not in self.nodes:
                self.nodes[self.node_id] = self.my_node
            
            self.stats = state.get("stats", self.stats)
            
        except Exception as e:
            print(f"Error loading collective intelligence state: {e}")
