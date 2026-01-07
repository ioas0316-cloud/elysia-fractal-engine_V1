"""
Knowledge Sharing System - Enable knowledge transfer across network nodes.

Allows Elysia instances to share learned patterns, experiences, and insights
with other nodes in the collective intelligence network.
"""

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class KnowledgeType(Enum):
    """Types of knowledge that can be shared."""
    PATTERN = "pattern"            # Learned patterns
    EXPERIENCE = "experience"      # Experience records
    INSIGHT = "insight"            # Derived insights
    BEST_PRACTICE = "best_practice"  # Proven approaches
    ERROR_LESSON = "error_lesson"  # Lessons from errors
    SKILL = "skill"                # Acquired skills


@dataclass
class SharedKnowledge:
    """Represents a piece of knowledge shared across the network."""
    knowledge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    knowledge_type: KnowledgeType = KnowledgeType.INSIGHT
    content: Dict[str, Any] = field(default_factory=dict)
    source_node_id: str = ""
    timestamp: float = field(default_factory=time.time)
    quality_score: float = 0.5
    usage_count: int = 0
    validation_count: int = 0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "knowledge_type": self.knowledge_type.value,
            "content": self.content,
            "source_node_id": self.source_node_id,
            "timestamp": self.timestamp,
            "quality_score": self.quality_score,
            "usage_count": self.usage_count,
            "validation_count": self.validation_count,
            "tags": self.tags,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SharedKnowledge":
        data["knowledge_type"] = KnowledgeType(data["knowledge_type"])
        return cls(**data)


class KnowledgeSharer:
    """
    Manages knowledge sharing across the collective intelligence network.
    
    Features:
    - Knowledge publication and subscription
    - Quality-based filtering
    - Usage tracking
    - Knowledge validation and rating
    - Automatic knowledge decay for outdated info
    """
    
    def __init__(self, node_id: str, data_dir: str = "data/network"):
        self.node_id = node_id
        self.data_dir = Path(data_dir) / "knowledge"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Knowledge repository
        self.knowledge_base: Dict[str, SharedKnowledge] = {}
        self.subscriptions: Set[KnowledgeType] = set(KnowledgeType)
        
        # Statistics
        self.stats = {
            "total_shared": 0,
            "total_received": 0,
            "total_validations": 0,
            "average_quality": 0.5,
            "knowledge_by_type": {},
        }
        
        self.load_state()
    
    def share_knowledge(
        self,
        knowledge_type: KnowledgeType,
        content: Dict[str, Any],
        tags: List[str] = None,
        quality_score: float = 0.5
    ) -> SharedKnowledge:
        """Share new knowledge with the network."""
        knowledge = SharedKnowledge(
            knowledge_type=knowledge_type,
            content=content,
            source_node_id=self.node_id,
            quality_score=quality_score,
            tags=tags or [],
        )
        
        self.knowledge_base[knowledge.knowledge_id] = knowledge
        self.stats["total_shared"] += 1
        
        # Update type statistics
        type_key = knowledge_type.value
        self.stats["knowledge_by_type"][type_key] = (
            self.stats["knowledge_by_type"].get(type_key, 0) + 1
        )
        
        self.save_state()
        return knowledge
    
    def receive_knowledge(self, knowledge: SharedKnowledge) -> bool:
        """Receive knowledge from another node."""
        # Check if we're subscribed to this type
        if knowledge.knowledge_type not in self.subscriptions:
            return False
        
        # Check quality threshold
        if knowledge.quality_score < 0.3:
            return False
        
        # Add to knowledge base
        self.knowledge_base[knowledge.knowledge_id] = knowledge
        self.stats["total_received"] += 1
        
        self.save_state()
        return True
    
    def query_knowledge(
        self,
        knowledge_type: Optional[KnowledgeType] = None,
        tags: Optional[List[str]] = None,
        min_quality: float = 0.0,
        max_age_days: Optional[float] = None
    ) -> List[SharedKnowledge]:
        """Query knowledge base with filters."""
        results = []
        current_time = time.time()
        
        for knowledge in self.knowledge_base.values():
            # Type filter
            if knowledge_type and knowledge.knowledge_type != knowledge_type:
                continue
            
            # Quality filter
            if knowledge.quality_score < min_quality:
                continue
            
            # Age filter
            if max_age_days:
                age_days = (current_time - knowledge.timestamp) / 86400
                if age_days > max_age_days:
                    continue
            
            # Tag filter
            if tags:
                if not any(tag in knowledge.tags for tag in tags):
                    continue
            
            results.append(knowledge)
        
        # Sort by quality and recency
        results.sort(
            key=lambda k: (k.quality_score, -k.timestamp),
            reverse=True
        )
        
        return results
    
    def validate_knowledge(self, knowledge_id: str, is_useful: bool):
        """Validate a piece of knowledge based on usage."""
        if knowledge_id not in self.knowledge_base:
            return
        
        knowledge = self.knowledge_base[knowledge_id]
        knowledge.validation_count += 1
        
        # Update quality score
        feedback = 1.0 if is_useful else 0.0
        knowledge.quality_score = (
            knowledge.quality_score * 0.9 + feedback * 0.1
        )
        
        self.stats["total_validations"] += 1
        self.save_state()
    
    def use_knowledge(self, knowledge_id: str):
        """Record usage of a piece of knowledge."""
        if knowledge_id not in self.knowledge_base:
            return
        
        knowledge = self.knowledge_base[knowledge_id]
        knowledge.usage_count += 1
        
        self.save_state()
    
    def find_best_practices(
        self,
        context: Dict[str, Any],
        min_usage: int = 3,
        min_quality: float = 0.7
    ) -> List[SharedKnowledge]:
        """Find best practices matching a given context."""
        best_practices = self.query_knowledge(
            knowledge_type=KnowledgeType.BEST_PRACTICE,
            min_quality=min_quality
        )
        
        # Filter by usage
        best_practices = [
            bp for bp in best_practices
            if bp.usage_count >= min_usage
        ]
        
        # Score by relevance to context (simple keyword matching)
        context_str = " ".join(str(v).lower() for v in context.values())
        
        scored_practices = []
        for practice in best_practices:
            content_str = " ".join(str(v).lower() for v in practice.content.values())
            
            # Simple relevance score based on common words
            common_words = set(context_str.split()) & set(content_str.split())
            relevance = len(common_words) / max(len(context_str.split()), 1)
            
            scored_practices.append((practice, relevance))
        
        # Sort by relevance and quality
        scored_practices.sort(
            key=lambda x: (x[1], x[0].quality_score),
            reverse=True
        )
        
        return [p for p, _ in scored_practices]
    
    def cleanup_old_knowledge(self, max_age_days: float = 30.0):
        """Remove outdated knowledge from the base."""
        current_time = time.time()
        max_age_seconds = max_age_days * 86400
        
        to_remove = []
        for kid, knowledge in self.knowledge_base.items():
            age = current_time - knowledge.timestamp
            
            # Remove if too old and low quality/usage
            if age > max_age_seconds:
                if knowledge.quality_score < 0.5 or knowledge.usage_count < 2:
                    to_remove.append(kid)
        
        for kid in to_remove:
            del self.knowledge_base[kid]
        
        if to_remove:
            self.save_state()
        
        return len(to_remove)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge sharing statistics."""
        if self.knowledge_base:
            avg_quality = sum(k.quality_score for k in self.knowledge_base.values()) / len(self.knowledge_base)
            avg_usage = sum(k.usage_count for k in self.knowledge_base.values()) / len(self.knowledge_base)
        else:
            avg_quality = 0.5
            avg_usage = 0.0
        
        return {
            **self.stats,
            "total_knowledge": len(self.knowledge_base),
            "current_average_quality": avg_quality,
            "average_usage_count": avg_usage,
            "knowledge_by_type": {
                k_type.value: sum(1 for k in self.knowledge_base.values() if k.knowledge_type == k_type)
                for k_type in KnowledgeType
            },
        }
    
    def save_state(self):
        """Save knowledge base to disk."""
        state = {
            "node_id": self.node_id,
            "knowledge_base": {
                kid: k.to_dict() for kid, k in self.knowledge_base.items()
            },
            "subscriptions": [s.value for s in self.subscriptions],
            "stats": self.stats,
        }
        
        state_file = self.data_dir / f"knowledge_sharer_{self.node_id}.json"
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
    
    def load_state(self):
        """Load knowledge base from disk."""
        state_file = self.data_dir / f"knowledge_sharer_{self.node_id}.json"
        if not state_file.exists():
            return
        
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
            
            self.knowledge_base = {
                kid: SharedKnowledge.from_dict(kdata)
                for kid, kdata in state.get("knowledge_base", {}).items()
            }
            
            self.subscriptions = {
                KnowledgeType(s) for s in state.get("subscriptions", [])
            }
            
            self.stats = state.get("stats", self.stats)
            
        except Exception as e:
            print(f"Error loading knowledge sharer state: {e}")
