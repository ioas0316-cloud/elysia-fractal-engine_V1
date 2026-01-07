"""
Unified Knowledge System
========================

Consolidates all knowledge management capabilities into one comprehensive system.

Merges:
- KnowledgeAcquisitionSystem: Learning from external sources
- KnowledgeSync: Node-to-node knowledge synchronization  
- KnowledgeSharer: Knowledge sharing across network
- WebKnowledgeConnector: Real internet knowledge fetching

Philosophy: "지식은 하나다" (Knowledge is one)
All knowledge operations unified in single, coherent system.

NO EXTERNAL LLMs - Pure wave-based intelligence only.
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime

logger = logging.getLogger("UnifiedKnowledge")


class KnowledgeType(Enum):
    """Types of knowledge in the unified system."""
    CONCEPT = "concept"              # General concepts
    PATTERN = "pattern"              # Learned patterns
    EXPERIENCE = "experience"        # Experience records
    INSIGHT = "insight"              # Derived insights
    BEST_PRACTICE = "best_practice"  # Proven approaches
    ERROR_LESSON = "error_lesson"    # Lessons from errors
    SKILL = "skill"                  # Acquired skills
    WEB_KNOWLEDGE = "web_knowledge"  # From internet


class KnowledgeSource(Enum):
    """Sources of knowledge."""
    INTERNAL = "internal"      # Generated internally
    WEB = "web"               # From internet
    NETWORK = "network"        # From other nodes
    CURRICULUM = "curriculum"  # From structured learning
    EXPERIENCE = "experience"  # From direct experience


@dataclass
class KnowledgeEntry:
    """Unified knowledge entry."""
    knowledge_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    knowledge_type: KnowledgeType = KnowledgeType.CONCEPT
    source: KnowledgeSource = KnowledgeSource.INTERNAL
    
    # Core content
    concept: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    
    # Quality metrics
    confidence: float = 0.5
    quality_score: float = 0.5
    usage_count: int = 0
    validation_count: int = 0
    
    # Metadata
    source_node_id: str = "local"
    timestamp: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
    validations: List[Dict[str, Any]] = field(default_factory=list)
    
    # Wave representation (from Internal Universe)
    wave_coords: Optional[Dict[str, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "knowledge_type": self.knowledge_type.value,
            "source": self.source.value,
            "concept": self.concept,
            "content": self.content,
            "description": self.description,
            "confidence": self.confidence,
            "quality_score": self.quality_score,
            "usage_count": self.usage_count,
            "validation_count": self.validation_count,
            "source_node_id": self.source_node_id,
            "timestamp": self.timestamp,
            "tags": self.tags,
            "validation_count_total": len(self.validations),
            "wave_coords": self.wave_coords,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeEntry":
        """Reconstruct from dictionary."""
        data["knowledge_type"] = KnowledgeType(data.get("knowledge_type", "concept"))
        data["source"] = KnowledgeSource(data.get("source", "internal"))
        # Remove validation_count_total if present (derived field)
        data.pop("validation_count_total", None)
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


class UnifiedKnowledgeSystem:
    """
    Unified knowledge management system.
    
    Combines all knowledge operations:
    - Acquisition (learning new knowledge)
    - Storage (maintaining knowledge base)
    - Retrieval (finding relevant knowledge)
    - Sharing (network knowledge exchange)
    - Validation (quality assurance)
    - Synchronization (collective intelligence)
    
    Pure wave-based intelligence - NO external LLMs.
    """
    
    def __init__(
        self,
        node_id: str = "local",
        data_dir: str = "data/knowledge",
        enable_web: bool = False
    ):
        self.node_id = node_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.enable_web = enable_web
        
        # Unified knowledge base
        self.knowledge_base: Dict[str, KnowledgeEntry] = {}
        
        # Internal Universe integration (if available)
        self.universe = None
        try:
            from Core.Foundation.internal_universe import InternalUniverse
            self.universe = InternalUniverse()
            logger.info("🌌 Internal Universe connected")
        except Exception as e:
            logger.warning(f"⚠️ Internal Universe not available: {e}")
        
        # Web connector (if enabled)
        self.web_connector = None
        if enable_web:
            try:
                import requests  # Check if requests available
                logger.info("🌐 Web connector enabled")
                self.web_enabled = True
            except ImportError:
                logger.warning("⚠️ Web connector disabled (requests not available)")
                self.web_enabled = False
        else:
            self.web_enabled = False
        
        # Thresholds
        self.validation_threshold = 0.6
        self.consensus_threshold = 0.7
        self.quality_threshold = 0.3
        
        # Statistics
        self.stats = {
            "total_acquired": 0,
            "total_shared": 0,
            "total_received": 0,
            "total_validations": 0,
            "web_fetches": 0,
            "successful_web_fetches": 0,
            "by_type": {},
            "by_source": {},
        }
        
        # Load existing knowledge
        self.load_state()
        
        logger.info(f"📚 Unified Knowledge System initialized")
        logger.info(f"   Node ID: {self.node_id}")
        logger.info(f"   Knowledge entries: {len(self.knowledge_base)}")
        logger.info(f"   Web enabled: {self.web_enabled}")
    
    # ==================== ACQUISITION ====================
    
    def learn_concept(
        self,
        concept: str,
        description: str = None,
        knowledge_type: KnowledgeType = KnowledgeType.CONCEPT,
        tags: List[str] = None
    ) -> KnowledgeEntry:
        """
        Learn a new concept.
        
        This is the primary knowledge acquisition method.
        """
        logger.info(f"📖 Learning: {concept}")
        
        # Create knowledge entry
        entry = KnowledgeEntry(
            concept=concept,
            description=description or f"Knowledge about {concept}",
            knowledge_type=knowledge_type,
            source=KnowledgeSource.CURRICULUM,
            tags=tags or [],
            source_node_id=self.node_id
        )
        
        # Internalize to wave space (if universe available)
        if self.universe:
            try:
                # Use universe's internalization
                wave_result = self._internalize_to_universe(concept, entry.description)
                entry.wave_coords = wave_result.get("coordinates")
                entry.content.update(wave_result)
            except Exception as e:
                logger.warning(f"   ⚠️ Wave internalization failed: {e}")
        
        # Store in knowledge base
        self.knowledge_base[entry.knowledge_id] = entry
        
        # Update stats
        self.stats["total_acquired"] += 1
        type_key = knowledge_type.value
        self.stats["by_type"][type_key] = self.stats["by_type"].get(type_key, 0) + 1
        self.stats["by_source"]["curriculum"] = self.stats["by_source"].get("curriculum", 0) + 1
        
        logger.info(f"   ✅ Learned '{concept}'")
        
        self.save_state()
        return entry
    
    def learn_from_web(self, concept: str) -> Optional[KnowledgeEntry]:
        """
        Learn concept by fetching from real internet.
        
        Requires web connector to be enabled.
        """
        if not self.web_enabled:
            logger.warning(f"⚠️ Web learning disabled, using basic learning")
            return self.learn_concept(concept)
        
        logger.info(f"🌍 Learning '{concept}' from web...")
        self.stats["web_fetches"] += 1
        
        try:
            # Fetch from Wikipedia
            content = self._fetch_wikipedia(concept)
            
            if content:
                # Create entry with web content
                entry = KnowledgeEntry(
                    concept=concept,
                    description=content[:500],  # First 500 chars
                    knowledge_type=KnowledgeType.WEB_KNOWLEDGE,
                    source=KnowledgeSource.WEB,
                    content={"full_content": content, "source": "wikipedia"},
                    tags=["web", "wikipedia"],
                    source_node_id=self.node_id,
                    quality_score=0.8  # Higher quality for web sources
                )
                
                # Internalize to wave space
                if self.universe:
                    try:
                        wave_result = self._internalize_to_universe(concept, content)
                        entry.wave_coords = wave_result.get("coordinates")
                        entry.content.update(wave_result)
                    except Exception as e:
                        logger.warning(f"   ⚠️ Wave internalization failed: {e}")
                
                # Store
                self.knowledge_base[entry.knowledge_id] = entry
                
                # Update stats
                self.stats["total_acquired"] += 1
                self.stats["successful_web_fetches"] += 1
                self.stats["by_type"]["web_knowledge"] = self.stats["by_type"].get("web_knowledge", 0) + 1
                self.stats["by_source"]["web"] = self.stats["by_source"].get("web", 0) + 1
                
                logger.info(f"   ✅ Learned from web: {len(content)} chars")
                
                self.save_state()
                return entry
            
        except Exception as e:
            logger.error(f"   ❌ Web learning failed: {e}")
        
        # Fallback to basic learning
        logger.warning(f"   ⚠️ Falling back to basic learning")
        return self.learn_concept(concept)
    
    def learn_curriculum(self, curriculum: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Learn structured curriculum.
        
        Args:
            curriculum: List of {"concept": str, "description": str} dicts
        """
        logger.info(f"🎓 Starting curriculum: {len(curriculum)} concepts")
        
        results = []
        start_time = time.time()
        
        for item in curriculum:
            concept = item.get("concept")
            description = item.get("description", "")
            
            try:
                entry = self.learn_concept(concept, description)
                results.append({"concept": concept, "success": True, "id": entry.knowledge_id})
            except Exception as e:
                logger.error(f"❌ Failed to learn '{concept}': {e}")
                results.append({"concept": concept, "success": False, "error": str(e)})
        
        elapsed = time.time() - start_time
        successful = sum(1 for r in results if r.get("success"))
        
        summary = {
            "total_concepts": len(curriculum),
            "successful": successful,
            "failed": len(curriculum) - successful,
            "elapsed_seconds": elapsed,
            "concepts_per_second": successful / elapsed if elapsed > 0 else 0,
            "results": results
        }
        
        logger.info(f"✅ Curriculum complete: {successful}/{len(curriculum)} in {elapsed:.1f}s")
        
        return summary
    
    # ==================== RETRIEVAL ====================
    
    def query_knowledge(
        self,
        concept: Optional[str] = None,
        knowledge_type: Optional[KnowledgeType] = None,
        source: Optional[KnowledgeSource] = None,
        tags: Optional[List[str]] = None,
        min_quality: float = 0.0,
        max_age_days: Optional[float] = None,
        limit: int = 100
    ) -> List[KnowledgeEntry]:
        """
        Query knowledge base with filters.
        """
        results = []
        current_time = time.time()
        
        for entry in self.knowledge_base.values():
            # Concept filter
            if concept and entry.concept.lower() != concept.lower():
                continue
            
            # Type filter
            if knowledge_type and entry.knowledge_type != knowledge_type:
                continue
            
            # Source filter
            if source and entry.source != source:
                continue
            
            # Quality filter
            if entry.quality_score < min_quality:
                continue
            
            # Age filter
            if max_age_days:
                age_days = (current_time - entry.timestamp) / 86400
                if age_days > max_age_days:
                    continue
            
            # Tag filter
            if tags:
                if not any(tag in entry.tags for tag in tags):
                    continue
            
            results.append(entry)
        
        # Sort by quality and recency
        results.sort(
            key=lambda e: (e.quality_score, -e.timestamp),
            reverse=True
        )
        
        return results[:limit]
    
    def find_related(self, concept: str, limit: int = 10) -> List[KnowledgeEntry]:
        """
        Find knowledge related to a concept using wave resonance.
        """
        if not self.universe:
            # Fallback: simple keyword matching
            return self.query_knowledge(limit=limit)
        
        try:
            # Use universe's resonance
            result = self.universe.omniscient_access(concept)
            resonant_concepts = result.get("resonant_concepts", [])
            
            # Find entries for resonant concepts
            related = []
            for res_concept in resonant_concepts[:limit]:
                concept_name = res_concept.get("concept", "")
                for entry in self.knowledge_base.values():
                    if entry.concept.lower() == concept_name.lower():
                        related.append(entry)
                        break
            
            return related
            
        except Exception as e:
            logger.warning(f"⚠️ Resonance search failed: {e}")
            return []
    
    #==================== SHARING & NETWORK ====================
    
    def share_knowledge(self, knowledge_id: str) -> bool:
        """
        Share knowledge with network.
        
        Makes knowledge available for other nodes to receive.
        """
        if knowledge_id not in self.knowledge_base:
            return False
        
        entry = self.knowledge_base[knowledge_id]
        
        # Mark as shared
        entry.content["shared"] = True
        entry.content["shared_at"] = time.time()
        
        self.stats["total_shared"] += 1
        self.save_state()
        
        logger.info(f"📤 Shared: {entry.concept}")
        return True
    
    def receive_knowledge(self, entry_data: Dict[str, Any]) -> bool:
        """
        Receive knowledge from another node.
        """
        try:
            entry = KnowledgeEntry.from_dict(entry_data)
            
            # Quality check
            if entry.quality_score < self.quality_threshold:
                logger.warning(f"⚠️ Rejected low quality: {entry.concept}")
                return False
            
            # Store
            self.knowledge_base[entry.knowledge_id] = entry
            
            self.stats["total_received"] += 1
            self.save_state()
            
            logger.info(f"📥 Received: {entry.concept}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to receive knowledge: {e}")
            return False
    
    async def sync_with_nodes(self, nodes: List[Any]) -> Dict[str, Any]:
        """
        Synchronize knowledge with other nodes.
        
        Implements collective intelligence through knowledge sharing.
        """
        logger.info(f"🔄 Syncing with {len(nodes)} nodes...")
        
        shared_count = 0
        received_count = 0
        
        for node in nodes:
            # Share our knowledge
            for kid in list(self.knowledge_base.keys())[:10]:  # Share top 10
                if self.share_knowledge(kid):
                    shared_count += 1
            
            # Receive from node (if it has knowledge_base)
            if hasattr(node, 'knowledge_base'):
                for entry in list(node.knowledge_base.values())[:10]:
                    if self.receive_knowledge(entry.to_dict()):
                        received_count += 1
        
        logger.info(f"✅ Sync complete: shared {shared_count}, received {received_count}")
        
        return {
            "nodes_synced": len(nodes),
            "knowledge_shared": shared_count,
            "knowledge_received": received_count
        }
    
    # ==================== VALIDATION ====================
    
    def validate_knowledge(self, knowledge_id: str, is_useful: bool):
        """
        Validate knowledge based on usage feedback.
        """
        if knowledge_id not in self.knowledge_base:
            return
        
        entry = self.knowledge_base[knowledge_id]
        entry.validation_count += 1
        
        # Add validation record
        entry.validations.append({
            "is_useful": is_useful,
            "timestamp": time.time(),
            "validator_id": self.node_id
        })
        
        # Update quality score
        feedback = 1.0 if is_useful else 0.0
        entry.quality_score = entry.quality_score * 0.9 + feedback * 0.1
        
        self.stats["total_validations"] += 1
        self.save_state()
        
        logger.info(f"✅ Validated: {entry.concept} ({'useful' if is_useful else 'not useful'})")
    
    def use_knowledge(self, knowledge_id: str):
        """
        Record usage of knowledge.
        """
        if knowledge_id not in self.knowledge_base:
            return
        
        entry = self.knowledge_base[knowledge_id]
        entry.usage_count += 1
        
        self.save_state()
    
    # ==================== UTILITIES ====================
    
    def _internalize_to_universe(self, concept: str, description: str) -> Dict[str, Any]:
        """Internalize knowledge to Internal Universe wave space."""
        if not self.universe:
            return {}
        
        try:
            # Use ExternalDataConnector if available
            try:
                from Core.Foundation.external_data_connector import ExternalDataConnector
                connector = ExternalDataConnector(self.universe)
                return connector.internalize_from_text(concept, description)
            except:
                # Fallback: direct universe internalization
                # This is a simplified version
                coords = {
                    "logic": len(description) / 1000.0,  # Simplified
                    "emotion": 0.5,
                    "ethics": 0.5,
                    "frequency": 50.0
                }
                return {"coordinates": coords}
        except Exception as e:
            logger.warning(f"⚠️ Universe internalization failed: {e}")
            return {}
    
    def _fetch_wikipedia(self, concept: str) -> Optional[str]:
        """Fetch concept from Wikipedia."""
        try:
            import requests
            
            # Wikipedia REST API
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{concept.replace(' ', '_')}"
            
            headers = {
                'User-Agent': 'Elysia/9.0 (Educational AI Project)'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('extract', '')
            
        except Exception as e:
            logger.error(f"Wikipedia fetch failed: {e}")
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        if self.knowledge_base:
            avg_quality = sum(e.quality_score for e in self.knowledge_base.values()) / len(self.knowledge_base)
            avg_usage = sum(e.usage_count for e in self.knowledge_base.values()) / len(self.knowledge_base)
        else:
            avg_quality = 0.5
            avg_usage = 0.0
        
        return {
            **self.stats,
            "total_knowledge": len(self.knowledge_base),
            "average_quality": avg_quality,
            "average_usage": avg_usage,
            "web_success_rate": (
                self.stats["successful_web_fetches"] / self.stats["web_fetches"]
                if self.stats["web_fetches"] > 0 else 0
            ),
        }
    
    def cleanup_old_knowledge(self, max_age_days: float = 30.0) -> int:
        """Remove outdated low-quality knowledge."""
        current_time = time.time()
        max_age_seconds = max_age_days * 86400
        
        to_remove = []
        for kid, entry in self.knowledge_base.items():
            age = current_time - entry.timestamp
            
            # Remove if old and low quality/usage
            if age > max_age_seconds:
                if entry.quality_score < 0.5 or entry.usage_count < 2:
                    to_remove.append(kid)
        
        for kid in to_remove:
            del self.knowledge_base[kid]
        
        if to_remove:
            self.save_state()
            logger.info(f"🧹 Cleaned up {len(to_remove)} old knowledge entries")
        
        return len(to_remove)
    
    def export_knowledge(self, filepath: str = None) -> Dict[str, Any]:
        """Export all knowledge to JSON."""
        if filepath is None:
            filepath = str(self.data_dir / f"knowledge_export_{int(time.time())}.json")
        
        export_data = {
            "node_id": self.node_id,
            "timestamp": time.time(),
            "knowledge_base": {
                kid: entry.to_dict() for kid, entry in self.knowledge_base.items()
            },
            "statistics": self.get_statistics()
        }
        
        # Custom JSON encoder
        def json_serialize(obj):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            else:
                return str(obj)
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=json_serialize)
        
        logger.info(f"💾 Exported {len(self.knowledge_base)} entries to {filepath}")
        
        return export_data
    
    def save_state(self):
        """Save knowledge base to disk."""
        state_file = self.data_dir / f"unified_knowledge_{self.node_id}.json"
        
        state = {
            "node_id": self.node_id,
            "timestamp": time.time(),
            "knowledge_base": {
                kid: entry.to_dict() for kid, entry in self.knowledge_base.items()
            },
            "stats": self.stats
        }
        
        # Custom JSON encoder to handle non-serializable objects
        def json_serialize(obj):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            elif hasattr(obj, '__dict__'):
                return obj.__dict__
            else:
                return str(obj)
        
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2, default=json_serialize)
    
    def load_state(self):
        """Load knowledge base from disk."""
        state_file = self.data_dir / f"unified_knowledge_{self.node_id}.json"
        
        if not state_file.exists():
            return
        
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            self.knowledge_base = {
                kid: KnowledgeEntry.from_dict(entry_data)
                for kid, entry_data in state.get("knowledge_base", {}).items()
            }
            
            self.stats = state.get("stats", self.stats)
            
            logger.info(f"📂 Loaded {len(self.knowledge_base)} knowledge entries")
            
        except Exception as e:
            logger.error(f"❌ Failed to load state: {e}")


# Singleton accessor
_unified_knowledge_system = None

def get_unified_knowledge_system(
    node_id: str = "local",
    enable_web: bool = False
) -> UnifiedKnowledgeSystem:
    """Get or create unified knowledge system instance."""
    global _unified_knowledge_system
    
    if _unified_knowledge_system is None:
        _unified_knowledge_system = UnifiedKnowledgeSystem(
            node_id=node_id,
            enable_web=enable_web
        )
    
    return _unified_knowledge_system


# Migration helpers for backward compatibility
def migrate_from_knowledge_acquisition(old_system: Any) -> UnifiedKnowledgeSystem:
    """Migrate from old KnowledgeAcquisitionSystem."""
    unified = UnifiedKnowledgeSystem()
    
    # Migrate learning history
    if hasattr(old_system, 'learning_history'):
        for item in old_system.learning_history:
            concept = item.get('concept', '')
            if concept:
                unified.learn_concept(concept)
    
    return unified


def migrate_from_knowledge_sharer(old_system: Any) -> UnifiedKnowledgeSystem:
    """Migrate from old KnowledgeSharer."""
    unified = UnifiedKnowledgeSystem()
    
    # Migrate knowledge base
    if hasattr(old_system, 'knowledge_base'):
        for knowledge in old_system.knowledge_base.values():
            entry_data = knowledge.to_dict() if hasattr(knowledge, 'to_dict') else {}
            if entry_data:
                unified.receive_knowledge(entry_data)
    
    return unified


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("UNIFIED KNOWLEDGE SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Create system
    system = UnifiedKnowledgeSystem(node_id="demo", enable_web=False)
    
    # Learn some concepts
    print("\n📚 Learning curriculum...")
    curriculum = [
        {"concept": "Artificial Intelligence", "description": "AI is intelligence demonstrated by machines"},
        {"concept": "Consciousness", "description": "Awareness of one's own existence"},
        {"concept": "Evolution", "description": "Change in heritable characteristics over generations"},
    ]
    
    result = system.learn_curriculum(curriculum)
    print(f"✅ Learned {result['successful']}/{result['total_concepts']} concepts")
    
    # Query knowledge
    print("\n🔍 Querying knowledge...")
    results = system.query_knowledge(min_quality=0.4)
    print(f"Found {len(results)} knowledge entries")
    
    for entry in results[:3]:
        print(f"  - {entry.concept} (quality: {entry.quality_score:.2f})")
    
    # Statistics
    print("\n📊 Statistics:")
    stats = system.get_statistics()
    print(f"  Total knowledge: {stats['total_knowledge']}")
    print(f"  Total acquired: {stats['total_acquired']}")
    print(f"  Average quality: {stats['average_quality']:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ UNIFIED KNOWLEDGE SYSTEM OPERATIONAL")
    print("🌊 All knowledge operations in one system!")
    print("=" * 70)
