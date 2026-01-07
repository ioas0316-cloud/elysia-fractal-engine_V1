"""
Elysia Node - Individual node in the collective intelligence network.

Implements Phase 7.1: Inter-Instance Communication
Each node represents a single Elysia instance with specialized capabilities.
"""

import asyncio
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
import time


@dataclass
class Message:
    """Message passed between nodes."""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    recipient_id: Optional[str] = None  # None for broadcast
    message_type: str = "general"  # general, query, response, knowledge_share
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    priority: int = 5  # 1-10, higher is more important


class ElysiaNode:
    """
    Single Elysia node in the collective intelligence network.
    
    Specializations:
    - logic: Logical reasoning and validation
    - creativity: Creative idea generation
    - emotion: Emotional processing and empathy
    - knowledge: Knowledge storage and retrieval
    - pattern: Pattern recognition
    - integration: Solution synthesis and integration
    """
    
    def __init__(self, node_id: Optional[str] = None, specialization: str = "generalist"):
        self.node_id = node_id or str(uuid.uuid4())
        self.specialization = specialization
        self.peers: List['ElysiaNode'] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.message_handlers: Dict[str, Callable] = {}
        self.performance_metrics = {
            "problems_solved": 0,
            "contributions": 0,
            "quality_score": 0.5,
            "response_time": []
        }
        
        # Specialization strengths (0.0-1.0)
        self.strengths = {
            "logic": 0.5,
            "creativity": 0.5,
            "emotion": 0.5,
            "knowledge": 0.5,
            "pattern": 0.5,
            "integration": 0.5
        }
        
        # Boost strength for specialization
        if specialization in self.strengths:
            self.strengths[specialization] = 0.9
    
    def add_peer(self, peer: 'ElysiaNode'):
        """Add a peer node to communicate with."""
        if peer not in self.peers and peer.node_id != self.node_id:
            self.peers.append(peer)
    
    def remove_peer(self, peer: 'ElysiaNode'):
        """Remove a peer node."""
        if peer in self.peers:
            self.peers.remove(peer)
    
    async def send_message(self, recipient: 'ElysiaNode', message: Message):
        """Send a message to a specific peer."""
        message.sender_id = self.node_id
        message.recipient_id = recipient.node_id
        await recipient.receive_message(message)
    
    async def broadcast(self, message: Message):
        """Broadcast a message to all peers."""
        message.sender_id = self.node_id
        message.recipient_id = None
        
        tasks = [peer.receive_message(message) for peer in self.peers]
        if tasks:
            await asyncio.gather(*tasks)
    
    async def receive_message(self, message: Message):
        """Receive a message from another node."""
        await self.message_queue.put(message)
        
        # If there's a registered handler for this message type, call it
        if message.message_type in self.message_handlers:
            await self.message_handlers[message.message_type](message)
    
    def register_handler(self, message_type: str, handler: Callable):
        """Register a handler for a specific message type."""
        self.message_handlers[message_type] = handler
    
    async def think(self, problem: str) -> Dict[str, Any]:
        """
        Independent thinking - solve a problem using this node's capabilities.
        Result quality depends on specialization match.
        """
        start_time = time.time()
        
        # Determine how well this node can solve this problem
        problem_type = self._classify_problem(problem)
        capability_match = self.strengths.get(problem_type, 0.5)
        
        # Simulate thinking time based on complexity
        await asyncio.sleep(0.01 + (1 - capability_match) * 0.02)
        
        solution = {
            "problem": problem,
            "solution": f"Solution from {self.specialization} node",
            "confidence": capability_match,
            "reasoning": f"Applied {self.specialization} approach to {problem_type} problem",
            "node_id": self.node_id,
            "specialization": self.specialization
        }
        
        # Track performance
        response_time = time.time() - start_time
        self.performance_metrics["response_time"].append(response_time)
        self.performance_metrics["problems_solved"] += 1
        
        return solution
    
    def _classify_problem(self, problem: str) -> str:
        """Classify what type of problem this is."""
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ["create", "imagine", "design", "innovate"]):
            return "creativity"
        elif any(word in problem_lower for word in ["feel", "emotion", "empathy", "understand mood"]):
            return "emotion"
        elif any(word in problem_lower for word in ["prove", "logical", "deduce", "reason"]):
            return "logic"
        elif any(word in problem_lower for word in ["pattern", "recognize", "identify trend"]):
            return "pattern"
        elif any(word in problem_lower for word in ["combine", "integrate", "synthesize"]):
            return "integration"
        elif any(word in problem_lower for word in ["know", "remember", "recall", "fact"]):
            return "knowledge"
        else:
            return "generalist"
    
    async def gather_peer_thoughts(self, problem: str) -> List[Dict[str, Any]]:
        """Gather thoughts from all peer nodes on a problem."""
        # Create query message
        query = Message(
            sender_id=self.node_id,
            message_type="query",
            content={"problem": problem, "requesting_thoughts": True}
        )
        
        # Send to all peers
        await self.broadcast(query)
        
        # Collect responses (with timeout)
        responses = []
        try:
            # Wait a bit for responses
            await asyncio.sleep(0.1)
            
            # Process queued messages
            while not self.message_queue.empty():
                msg = await asyncio.wait_for(self.message_queue.get(), timeout=0.05)
                if msg.message_type == "response" and "solution" in msg.content:
                    responses.append(msg.content)
        except asyncio.TimeoutError:
            pass
        
        return responses
    
    def reach_consensus(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Reach consensus from multiple thoughts.
        Uses weighted voting based on confidence and specialization match.
        """
        if not thoughts:
            return {"solution": "No consensus - no thoughts provided", "confidence": 0.0}
        
        # Weight by confidence
        total_weight = sum(t.get("confidence", 0.5) for t in thoughts)
        if total_weight == 0:
            total_weight = 1.0
        
        # Find the highest confidence solution
        best_thought = max(thoughts, key=lambda t: t.get("confidence", 0.0))
        
        # Calculate consensus confidence (average of all confidences)
        avg_confidence = total_weight / len(thoughts)
        
        return {
            "solution": best_thought.get("solution", ""),
            "confidence": avg_confidence,
            "reasoning": f"Consensus from {len(thoughts)} nodes",
            "supporting_nodes": len(thoughts),
            "best_contributor": best_thought.get("node_id", "unknown")
        }
    
    async def consensus_think(self, problem: str) -> Dict[str, Any]:
        """
        Consensus-based thinking - combine insights from all nodes.
        
        Process:
        1. Think independently
        2. Gather peer thoughts
        3. Reach consensus through voting/averaging
        """
        # 1. My own thought
        my_thought = await self.think(problem)
        
        # 2. Gather peer thoughts
        peer_thoughts = await self.gather_peer_thoughts(problem)
        
        # 3. Reach consensus
        all_thoughts = [my_thought] + peer_thoughts
        consensus = self.reach_consensus(all_thoughts)
        
        # Add metadata
        consensus["method"] = "consensus_thinking"
        consensus["participants"] = len(all_thoughts)
        consensus["coordinator"] = self.node_id
        
        return consensus
    
    async def solve(self, problem: str, method: str = "independent") -> Dict[str, Any]:
        """
        Solve a problem using specified method.
        
        Methods:
        - independent: Solve alone
        - consensus: Collaborate with peers
        """
        if method == "consensus":
            return await self.consensus_think(problem)
        else:
            return await self.think(problem)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of this node."""
        avg_response_time = (
            sum(self.performance_metrics["response_time"]) / len(self.performance_metrics["response_time"])
            if self.performance_metrics["response_time"] else 0.0
        )
        
        return {
            "node_id": self.node_id,
            "specialization": self.specialization,
            "peers_count": len(self.peers),
            "problems_solved": self.performance_metrics["problems_solved"],
            "contributions": self.performance_metrics["contributions"],
            "quality_score": self.performance_metrics["quality_score"],
            "avg_response_time": avg_response_time,
            "strengths": self.strengths
        }
