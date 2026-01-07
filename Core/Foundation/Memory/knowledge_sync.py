"""
Knowledge Sync - Node-to-node knowledge sharing and synchronization.

Implements Phase 7.2: Knowledge Sharing Protocol
Enables nodes to share discoveries, validate knowledge, and maintain collective memory.
"""

import asyncio
import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Discovery:
    """A new piece of knowledge discovered by a node."""
    discovery_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Dict[str, Any] = field(default_factory=dict)
    source_node_id: str = ""
    timestamp: float = field(default_factory=time.time)
    confidence: float = 0.5
    category: str = "general"  # pattern, insight, skill, best_practice
    validations: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "discovery_id": self.discovery_id,
            "content": self.content,
            "source_node_id": self.source_node_id,
            "timestamp": self.timestamp,
            "confidence": self.confidence,
            "category": self.category,
            "validation_count": len(self.validations)
        }


class KnowledgeSync:
    """
    System for synchronizing knowledge across network nodes.
    Manages knowledge sharing, validation, and collective memory.
    """
    
    def __init__(self):
        self.shared_knowledge: Dict[str, Discovery] = {}
        self.validation_threshold = 0.6  # Minimum confidence for acceptance
        self.consensus_threshold = 0.7  # Minimum agreement for consensus
    
    def evaluate_confidence(self, discovery: Discovery) -> float:
        """
        Evaluate confidence in a discovery.
        Based on source reliability and content quality.
        """
        # Base confidence from the discovery itself
        base_confidence = discovery.confidence
        
        # Adjust based on validations if any
        if discovery.validations:
            validation_scores = [v.get("confidence", 0.5) for v in discovery.validations]
            avg_validation = sum(validation_scores) / len(validation_scores)
            # Blend original confidence with validation feedback
            return (base_confidence + avg_validation) / 2
        
        return base_confidence
    
    async def request_validations(self, discovery: Discovery, validators: List[Any]) -> List[Dict[str, Any]]:
        """
        Request other nodes to validate a discovery.
        
        Args:
            discovery: The discovery to validate
            validators: List of validator nodes
        
        Returns:
            List of validation results
        """
        validations = []
        
        for validator in validators:
            # Simulate validation process
            validation_confidence = await self._validate_discovery(validator, discovery)
            
            validations.append({
                "validator_id": getattr(validator, 'node_id', str(uuid.uuid4())),
                "confidence": validation_confidence,
                "timestamp": time.time()
            })
        
        return validations
    
    async def _validate_discovery(self, validator: Any, discovery: Discovery) -> float:
        """Validate a discovery using a validator node."""
        # Simple validation: check if content makes sense
        # In real implementation, this would use the validator's capabilities
        
        # Simulate processing time
        await asyncio.sleep(0.01)
        
        # Base validation on discovery's original confidence with some variation
        base = discovery.confidence
        import random
        variation = random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, base + variation))
    
    def has_consensus(self, validations: List[Dict[str, Any]]) -> bool:
        """
        Check if validations reach consensus.
        
        Consensus requires:
        1. At least 2 validations
        2. Average confidence above threshold
        """
        if len(validations) < 2:
            return False
        
        avg_confidence = sum(v.get("confidence", 0.0) for v in validations) / len(validations)
        return avg_confidence >= self.consensus_threshold
    
    async def share_discovery(self, discovery: Discovery, validators: List[Any] = None):
        """
        Share a new discovery with the network.
        
        Process:
        1. Evaluate confidence
        2. Request validations
        3. Check consensus
        4. Broadcast if consensus reached
        """
        # 1. Evaluate confidence
        confidence = self.evaluate_confidence(discovery)
        
        # 2. Request validations if validators provided
        if validators:
            validations = await self.request_validations(discovery, validators)
            discovery.validations = validations
            
            # Update confidence based on validations
            confidence = self.evaluate_confidence(discovery)
        
        # 3. Check consensus
        if discovery.validations:
            has_consensus = self.has_consensus(discovery.validations)
        else:
            # If no validations, accept if confidence is high enough
            has_consensus = confidence >= self.validation_threshold
        
        # 4. Broadcast if consensus reached
        if has_consensus:
            await self.broadcast_knowledge(discovery)
            return True
        
        return False
    
    async def broadcast_knowledge(self, discovery: Discovery):
        """Broadcast validated knowledge to the entire network."""
        # Store in shared knowledge base
        self.shared_knowledge[discovery.discovery_id] = discovery
        
        # In a real implementation, this would send to all nodes
        # For now, just record it
        discovery.content["broadcast_time"] = time.time()
    
    async def gather_all_memories(self, nodes: List[Any]) -> List[Dict[str, Any]]:
        """
        Gather memories/experiences from all nodes.
        
        Args:
            nodes: List of network nodes
        
        Returns:
            Combined list of all memories
        """
        all_memories = []
        
        for node in nodes:
            # Get node's knowledge base
            if hasattr(node, 'knowledge_base'):
                for key, value in node.knowledge_base.items():
                    all_memories.append({
                        "source_node": getattr(node, 'node_id', 'unknown'),
                        "key": key,
                        "content": value,
                        "timestamp": time.time()
                    })
        
        return all_memories
    
    def merge_memories(self, all_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge memories from all nodes into unified collective memory.
        
        Process:
        1. Remove duplicates
        2. Resolve contradictions
        3. Rank by importance
        """
        if not all_memories:
            return {}
        
        # 1. Deduplicate by key
        memory_by_key = {}
        for memory in all_memories:
            key = memory.get("key", "")
            if key:
                if key not in memory_by_key:
                    memory_by_key[key] = []
                memory_by_key[key].append(memory)
        
        # 2. Resolve contradictions by majority or recency
        unified_memory = {}
        for key, memories in memory_by_key.items():
            if len(memories) == 1:
                # No conflict
                unified_memory[key] = memories[0]["content"]
            else:
                # Multiple values - use most recent
                most_recent = max(memories, key=lambda m: m.get("timestamp", 0))
                unified_memory[key] = most_recent["content"]
        
        # 3. Add metadata
        result = {
            "memories": unified_memory,
            "total_entries": len(unified_memory),
            "sources": len(set(m.get("source_node") for m in all_memories)),
            "merged_at": time.time()
        }
        
        return result
    
    async def collective_memory(self, nodes: List[Any]) -> Dict[str, Any]:
        """
        Create collective memory from all nodes.
        Integrates experiences and knowledge from entire network.
        """
        # Gather memories from all nodes
        all_memories = await self.gather_all_memories(nodes)
        
        # Merge into unified memory
        unified_memory = self.merge_memories(all_memories)
        
        return unified_memory
    
    def get_shared_knowledge(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all shared knowledge, optionally filtered by category.
        """
        knowledge_list = []
        
        for discovery in self.shared_knowledge.values():
            if category is None or discovery.category == category:
                knowledge_list.append(discovery.to_dict())
        
        return knowledge_list
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about knowledge sharing."""
        total_knowledge = len(self.shared_knowledge)
        
        # Count by category
        by_category = {}
        for discovery in self.shared_knowledge.values():
            cat = discovery.category
            by_category[cat] = by_category.get(cat, 0) + 1
        
        # Average confidence
        if self.shared_knowledge:
            avg_confidence = sum(
                self.evaluate_confidence(d) for d in self.shared_knowledge.values()
            ) / len(self.shared_knowledge)
        else:
            avg_confidence = 0.0
        
        return {
            "total_knowledge": total_knowledge,
            "by_category": by_category,
            "avg_confidence": avg_confidence,
            "validation_threshold": self.validation_threshold,
            "consensus_threshold": self.consensus_threshold
        }
