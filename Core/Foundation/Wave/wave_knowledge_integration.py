"""
Wave Knowledge Integration
===========================

Integrates wave-based semantic search with UnifiedKnowledgeSystem.
Enables knowledge absorption and expansion using 4D wave resonance patterns.

This module provides:
1. Automatic embedding extraction from existing memory files
2. Conversion to 4D wave patterns
3. Wave-based semantic search for knowledge retrieval
4. Knowledge expansion through wave absorption
"""

import sys
import os
import logging
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, TYPE_CHECKING

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.Foundation.wave_semantic_search import WaveSemanticSearch

if TYPE_CHECKING:
    from Core.Foundation.unified_knowledge_system import (
        UnifiedKnowledgeSystem,
        KnowledgeEntry,
        KnowledgeType,
        KnowledgeSource
    )

logger = logging.getLogger("WaveKnowledgeIntegration")

# Try to import knowledge system components
try:
    from Core.Foundation.unified_knowledge_system import (
        UnifiedKnowledgeSystem,
        KnowledgeEntry,
        KnowledgeType,
        KnowledgeSource
    )
    KNOWLEDGE_SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"UnifiedKnowledgeSystem not available: {e}")
    KNOWLEDGE_SYSTEM_AVAILABLE = False
    UnifiedKnowledgeSystem = None
    KnowledgeType = None
    KnowledgeSource = None


class WaveKnowledgeIntegration:
    """
    Integrates wave-based search with knowledge management.
    
    Features:
    - Load existing memory/database files with embeddings
    - Convert embeddings to 4D wave patterns
    - Semantic search using wave resonance
    - Knowledge absorption for expansion
    """
    
    def __init__(
        self,
        knowledge_system: Optional[Any] = None,  # UnifiedKnowledgeSystem or None
        wave_storage_path: str = "data/wave_patterns.json",
        auto_load_memory: bool = True
    ):
        """
        Initialize wave knowledge integration.
        
        Args:
            knowledge_system: UnifiedKnowledgeSystem instance (creates new if None)
            wave_storage_path: Path to store wave patterns
            auto_load_memory: Whether to automatically load existing memory files
        """
        self.knowledge_system = knowledge_system or (UnifiedKnowledgeSystem() if KNOWLEDGE_SYSTEM_AVAILABLE else None)
        self.wave_search = WaveSemanticSearch(storage_path=wave_storage_path)
        
        # Mapping between knowledge IDs and wave pattern IDs
        self.knowledge_to_wave: Dict[str, str] = {}
        self.wave_to_knowledge: Dict[str, str] = {}
        
        logger.info("🌊 Wave Knowledge Integration initialized")
        
        # Auto-load existing memory if requested
        if auto_load_memory:
            self._auto_load_memory_files()
    
    def _auto_load_memory_files(self):
        """
        Automatically load embeddings from existing memory files.
        """
        logger.info("📂 Auto-loading memory files...")
        
        # List of known memory file paths
        memory_paths = [
            "Core/Interface/elysia_core_memory.json",
            "Core/Foundation/memory_stream.json",
            "elysia_self_knowledge.json"
        ]
        
        loaded_count = 0
        for path_str in memory_paths:
            path = Path(path_str)
            if path.exists():
                try:
                    count = self.load_memory_file(str(path))
                    loaded_count += count
                    logger.info(f"  ✓ Loaded {count} entries from {path.name}")
                except Exception as e:
                    logger.warning(f"  ⚠️ Failed to load {path.name}: {e}")
        
        if loaded_count > 0:
            logger.info(f"📚 Loaded {loaded_count} total memory entries as wave patterns")
        else:
            logger.info("ℹ️ No memory files loaded (this is normal for fresh installations)")
    
    def load_memory_file(self, file_path: str) -> int:
        """
        Load memory file and extract embeddings (if present).
        
        Memory files may contain:
        - experience_loop: Experiences with tensor/wave representations
        - identity: Identity information
        - values: Value system
        
        We extract wave/tensor information and convert to embeddings.
        
        Args:
            file_path: Path to memory JSON file
            
        Returns:
            Number of entries loaded
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"Memory file not found: {file_path}")
            return 0
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        loaded_count = 0
        
        # Process experience loop (most common source of embeddings)
        if 'experience_loop' in data and isinstance(data['experience_loop'], list):
            for i, exp in enumerate(data['experience_loop']):
                try:
                    # Extract text content
                    text = exp.get('content', f"experience_{i}")
                    
                    # Extract wave/tensor representation
                    embedding = self._extract_embedding_from_experience(exp)
                    
                    if embedding is not None and len(embedding) > 0:
                        # Store as wave pattern
                        metadata = {
                            'source_file': file_path,
                            'experience_type': exp.get('type', 'unknown'),
                            'layer': exp.get('layer', 'unknown'),
                            'timestamp': exp.get('timestamp', i)
                        }
                        
                        pattern_id = self.wave_search.store_concept(
                            text=text,
                            embedding=embedding,
                            metadata=metadata
                        )
                        
                        loaded_count += 1
                
                except Exception as e:
                    logger.debug(f"Could not process experience {i}: {e}")
        
        # Process other sections (identity, values, etc.) if they have embeddings
        # For now, we focus on experience_loop as the main source
        
        return loaded_count
    
    def _extract_embedding_from_experience(self, experience: Dict) -> Optional[np.ndarray]:
        """
        Extract embedding from experience entry.
        
        Experience entries may have:
        - wave: {frequency, amplitude, phase, richness}
        - tensor: {x, y, z}
        - emotional_state with tensor and wave
        
        We combine these into a vector representation.
        """
        # Try to build embedding from wave and tensor data
        components = []
        
        # Extract wave components
        if 'wave' in experience and isinstance(experience['wave'], dict):
            wave = experience['wave']
            components.extend([
                wave.get('frequency', 1.0),
                wave.get('amplitude', 0.5),
                wave.get('phase', 0.0),
                wave.get('richness', 0.0)
            ])
        
        # Extract tensor components
        if 'tensor' in experience and isinstance(experience['tensor'], dict):
            tensor = experience['tensor']
            components.extend([
                tensor.get('x', 0.0),
                tensor.get('y', 0.0),
                tensor.get('z', 0.0)
            ])
        
        # Extract emotional state
        if 'emotional_state' in experience and isinstance(experience['emotional_state'], dict):
            emo = experience['emotional_state']
            components.extend([
                emo.get('valence', 0.5),
                emo.get('arousal', 0.3),
                emo.get('dominance', 0.5)
            ])
            
            # Emotional tensor
            if 'tensor' in emo and isinstance(emo['tensor'], dict):
                emo_tensor = emo['tensor']
                components.extend([
                    emo_tensor.get('x', 0.0),
                    emo_tensor.get('y', 0.0),
                    emo_tensor.get('z', 0.0)
                ])
            
            # Emotional wave
            if 'wave' in emo and isinstance(emo['wave'], dict):
                emo_wave = emo['wave']
                components.extend([
                    emo_wave.get('frequency', 1.0),
                    emo_wave.get('amplitude', 0.5),
                    emo_wave.get('phase', 0.0),
                    emo_wave.get('richness', 0.0)
                ])
        
        # Add other numeric fields
        numeric_fields = ['resonance_amp', 'frequency', 'richness']
        for field in numeric_fields:
            if field in experience and isinstance(experience[field], (int, float)):
                components.append(float(experience[field]))
        
        # If we have components, create embedding
        if components:
            # Pad to minimum size (we want at least 16 dimensions for meaningful wave patterns)
            while len(components) < 16:
                # Add small random noise to pad
                components.append(np.random.randn() * 0.01)
            
            return np.array(components, dtype=np.float32)
        
        return None
    
    def add_knowledge_with_embedding(
        self,
        concept: str,
        embedding: np.ndarray,
        description: str = "",
        knowledge_type: Any = None,  # KnowledgeType or None
        tags: List[str] = None
    ) -> str:
        """
        Add knowledge entry with embedding, storing both in knowledge base and wave search.
        
        Args:
            concept: Concept text
            embedding: Embedding vector
            description: Description
            knowledge_type: Type of knowledge
            tags: Tags
            
        Returns:
            Knowledge entry ID
        """
        if not self.knowledge_system:
            # If knowledge system not available, just store in wave search
            metadata = {
                'knowledge_type': str(knowledge_type) if knowledge_type else 'concept',
                'source': 'direct'
            }
            wave_pattern_id = self.wave_search.store_concept(
                text=concept,
                embedding=embedding,
                metadata=metadata
            )
            logger.info(f"📚 Added wave pattern (no knowledge system): '{concept}'")
            return wave_pattern_id
        
        # Use default KnowledgeType if available
        if knowledge_type is None and KNOWLEDGE_SYSTEM_AVAILABLE:
            knowledge_type = KnowledgeType.CONCEPT
        
        # Store in knowledge system
        entry = self.knowledge_system.learn_concept(
            concept=concept,
            description=description or f"Knowledge about {concept}",
            knowledge_type=knowledge_type,
            tags=tags
        )
        
        # Store in wave search
        metadata = {
            'knowledge_id': entry.knowledge_id,
            'knowledge_type': knowledge_type.value,
            'source': entry.source.value
        }
        
        wave_pattern_id = self.wave_search.store_concept(
            text=concept,
            embedding=embedding,
            metadata=metadata
        )
        
        # Create bidirectional mapping
        self.knowledge_to_wave[entry.knowledge_id] = wave_pattern_id
        self.wave_to_knowledge[wave_pattern_id] = entry.knowledge_id
        
        logger.info(f"📚 Added knowledge with wave pattern: '{concept}'")
        
        return entry.knowledge_id
    
    def search_knowledge_by_wave(
        self,
        query_embedding: np.ndarray,
        query_text: str = "",
        top_k: int = 5,
        min_resonance: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Search knowledge using wave resonance.
        
        Returns knowledge entries that resonate with query wave.
        
        Args:
            query_embedding: Query embedding
            query_text: Query text
            top_k: Number of results
            min_resonance: Minimum resonance threshold
            
        Returns:
            List of results with knowledge entries and resonance scores
        """
        # Search using wave resonance
        wave_results = self.wave_search.search(
            query_embedding=query_embedding,
            query_text=query_text,
            top_k=top_k,
            min_resonance=min_resonance
        )
        
        # Enrich with knowledge entries
        enriched_results = []
        for wave_result in wave_results:
            result = {
                'wave_result': wave_result,
                'resonance': wave_result['resonance'],
                'text': wave_result['text']
            }
            
            # Add knowledge entry if available
            wave_pattern_id = wave_result['pattern_id']
            if wave_pattern_id in self.wave_to_knowledge:
                knowledge_id = self.wave_to_knowledge[wave_pattern_id]
                if knowledge_id in self.knowledge_system.knowledge_base:
                    result['knowledge_entry'] = self.knowledge_system.knowledge_base[knowledge_id].to_dict()
            
            enriched_results.append(result)
        
        logger.info(f"🔍 Wave search: '{query_text[:30]}...' found {len(enriched_results)} results")
        
        return enriched_results
    
    def expand_knowledge_by_absorption(
        self,
        target_knowledge_id: str,
        source_knowledge_ids: List[str],
        absorption_strength: float = 0.4
    ) -> bool:
        """
        Expand knowledge entry by absorbing related knowledge using wave interference.
        
        This implements the core "knowledge absorption and expansion" concept:
        - Takes target knowledge and related source knowledge
        - Uses wave resonance to merge their semantic meanings
        - Creates a richer, deeper understanding
        
        Args:
            target_knowledge_id: ID of knowledge to expand
            source_knowledge_ids: IDs of knowledge to absorb
            absorption_strength: Strength of absorption (0-1)
            
        Returns:
            True if successful
        """
        # Get wave pattern IDs
        if target_knowledge_id not in self.knowledge_to_wave:
            logger.error(f"Target knowledge {target_knowledge_id} not found in wave search")
            return False
        
        target_wave_id = self.knowledge_to_wave[target_knowledge_id]
        
        source_wave_ids = []
        for source_id in source_knowledge_ids:
            if source_id in self.knowledge_to_wave:
                source_wave_ids.append(self.knowledge_to_wave[source_id])
        
        if not source_wave_ids:
            logger.warning("No source knowledge patterns found for absorption")
            return False
        
        # Perform wave absorption
        try:
            expanded_pattern = self.wave_search.absorb_and_expand(
                target_id=target_wave_id,
                source_patterns=source_wave_ids,
                absorption_strength=absorption_strength
            )
            
            # Update knowledge entry metadata
            target_entry = self.knowledge_system.knowledge_base[target_knowledge_id]
            target_entry.metadata['wave_expansion_depth'] = expanded_pattern.expansion_depth
            target_entry.metadata['absorbed_knowledge'] = source_knowledge_ids
            target_entry.metadata['last_expansion'] = expanded_pattern.timestamp
            
            logger.info(f"🌊 Expanded knowledge '{target_entry.concept}' by absorbing {len(source_wave_ids)} patterns")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to expand knowledge: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get integration statistics"""
        wave_stats = self.wave_search.get_statistics()
        knowledge_stats = self.knowledge_system.stats if self.knowledge_system else {}
        
        return {
            'wave_patterns': wave_stats,
            'knowledge_system': knowledge_stats,
            'integration': {
                'mapped_entries': len(self.knowledge_to_wave),
                'avg_expansion_depth': wave_stats.get('avg_expansion_depth', 0),
                'knowledge_system_available': KNOWLEDGE_SYSTEM_AVAILABLE
            }
        }


def demo():
    """Demo of wave knowledge integration"""
    print("="*70)
    print("🌊 WAVE KNOWLEDGE INTEGRATION DEMO")
    print("4차원 파동공명패턴 기반 지식베이스 통합")
    print("="*70)
    print()
    
    # Initialize integration
    print("🔧 Initializing integration...")
    integration = WaveKnowledgeIntegration(auto_load_memory=True)
    
    print()
    print("📊 Initial Statistics:")
    stats = integration.get_statistics()
    print(f"  Wave patterns: {stats['wave_patterns']['total_patterns']}")
    print(f"  Knowledge entries: {len(integration.knowledge_system.knowledge_base) if integration.knowledge_system else 0}")
    print(f"  Mapped entries: {stats['integration']['mapped_entries']}")
    print(f"  Knowledge system available: {stats['integration']['knowledge_system_available']}")
    
    print()
    print("✅ Integration ready!")
    print("="*70)


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    demo()
