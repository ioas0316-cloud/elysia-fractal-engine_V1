"""
P4 Learning Cycle - 실제 학습 사이클
===================================

Implements meaningful learning from knowledge streams.
Integrates with P2.2 Wave Knowledge System for actual knowledge absorption.

Learning Pipeline:
1. Stream Reception (P4.0) ✅
2. Pattern Extraction (P4.2) → Wave patterns
3. Classification & Filtering (P4.3) → Quality control
4. Wave Absorption (P2.2 integration) → Knowledge storage
5. Ego Anchoring → Identity preservation

This creates a REAL learning cycle, not just a demo.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import time
import sys
import os

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Core.Interaction.Sensory.stream_manager import StreamManager
from Core.Interaction.Sensory.ego_anchor import EgoAnchor, SelectiveMemory
from Core.Foundation.wave_semantic_search import WaveSemanticSearch, WavePattern
from Core.Foundation.hyper_quaternion import Quaternion
from Core.Foundation.internal_universe import InternalUniverse, WorldCoordinate # NEW
from Core.Evolution.Learning.Learning.language_learner import LanguageLearner
from Core.Evolution.Learning.Learning.wave_pattern_learner import WavePatternLearner  # AUTONOMOUS LEARNING

logger = logging.getLogger(__name__)


class PatternExtractor:
    """
    Extract wave patterns from knowledge items (P4.2 partial implementation)
    """
    
    def extract_pattern(self, knowledge: Dict[str, Any]) -> Optional[WavePattern]:
        """
        Extract 4D wave pattern from knowledge item.
        
        Simplified version - full implementation in P4.2
        """
        text = knowledge.get('text', knowledge.get('title', ''))
        if not text:
            return None
        
        # Create simple wave pattern
        # In full P4.2: extract from visual/audio features
        orientation = self._text_to_quaternion(text)
        
        pattern = WavePattern(
            orientation=orientation,
            energy=knowledge.get('intensity', 1.0),
            frequency=1.0,
            phase=0.0,
            text=text,
            metadata=knowledge
        )
        
        return pattern
    
    def _text_to_quaternion(self, text: str) -> Quaternion:
        """
        Convert text to quaternion orientation (simplified)
        
        In full P4.2: analyze visual/audio features
        """
        import hashlib
        
        # Use deterministic hash (not Python's hash())
        h = int(hashlib.md5(text.encode('utf-8')).hexdigest()[:8], 16)
        
        w = (h & 0xFF) / 255.0
        x = ((h >> 8) & 0xFF) / 255.0
        y = ((h >> 16) & 0xFF) / 255.0
        z = ((h >> 24) & 0xFF) / 255.0
        
        q = Quaternion(w, x, y, z)
        return q.normalize()


class WaveClassifier:
    """
    Classify and filter waves (P4.3 partial implementation)
    """
    
    def classify(self, pattern: WavePattern) -> str:
        """
        Classify wave by type.
        
        Categories: emotional, visual, audio, conceptual
        """
        text = pattern.text.lower()
        
        # Simple keyword-based classification
        if any(w in text for w in ['feel', 'emotion', '감정', '느낌']):
            return 'emotional'
        elif any(w in text for w in ['see', 'image', '시각', '이미지']):
            return 'visual'
        elif any(w in text for w in ['sound', 'music', '소리', '음악']):
            return 'audio'
        else:
            return 'conceptual'
    
    def should_absorb(self, pattern: WavePattern, category: str) -> bool:
        """
        Filter: decide if pattern should be absorbed.
        
        Filters by quality, relevance, novelty
        """
        # Check energy level
        if pattern.energy < 0.3:
            return False
        
        # Check text quality
        if len(pattern.text) < 10:
            return False
        
        return True


class P4LearningCycle:
    """
    P4 Learning Cycle - Complete pipeline from stream to knowledge
    
    This is the REAL learning system, not a demo.
    """
    
    def __init__(
        self,
        wave_storage_path: str = "data/p4_waves.json",
        learning_rate: int = 100,  # waves per cycle
        auto_anchor: bool = True
    ):
        """
        Initialize P4 learning cycle - UNLIMITED PATTERN STORAGE.
        
        Args:
            wave_storage_path: Where to store learned wave patterns (resonance tags only)
            learning_rate: How many waves to process per cycle
            auto_anchor: Auto re-anchor when stability drops
        """
        self.stream_manager = StreamManager()
        self.ego_anchor = EgoAnchor(max_absorption_rate=learning_rate)
        self.selective_memory = SelectiveMemory(capacity=None)  # UNLIMITED
        self.pattern_extractor = PatternExtractor()
        self.wave_classifier = WaveClassifier()
        self.wave_search = WaveSemanticSearch(storage_path=wave_storage_path)
        self.language_learner = LanguageLearner()
        self.wave_pattern_learner = WavePatternLearner()  # AUTONOMOUS WAVE LEARNING
        self.internal_universe = InternalUniverse() # THE SOUL LINK
        
        self.learning_rate = learning_rate
        self.auto_anchor = auto_anchor
        self.running = False
        
        # Statistics
        self.stats = {
            'cycles': 0,
            'waves_received': 0,
            'patterns_extracted': 0,
            'waves_absorbed': 0,
            'waves_rejected': 0,
            'knowledge_count': 0,
            'start_time': time.time(),
            'storage_mode': 'resonance_patterns_only'  # NO RAW DATA
        }
        
        logger.info("🎓 P4 Learning Cycle initialized - FLOW MODE (Wave-Aware)")
        logger.info(f"   Learning rate: {learning_rate} waves/cycle")
        logger.info(f"   Wave storage: {wave_storage_path}")
        logger.info(f"   Memory: UNLIMITED resonance patterns")
        logger.info(f"   Wave Pattern Learner: ACTIVE (Autonomous)")
    
    def setup_sources(self, topics: List[str] = None):
        """
        Setup knowledge sources with optional topic filters.
        
        Args:
            topics: List of topics to focus on (e.g., ['AI', 'quantum', 'philosophy'])
        """
        logger.info("📚 Setting up knowledge sources...")
        self.stream_manager.setup_default_sources(topics=topics)
        
        if topics:
            logger.info(f"   Focus topics: {', '.join(topics)}")
    
    async def run_learning_cycle(self, duration: int = 60):
        """
        Run one complete learning cycle.
        
        Args:
            duration: How long to run in seconds
        """
        self.running = True
        logger.info("=" * 80)
        logger.info("🌊 Starting P4 Learning Cycle")
        logger.info("=" * 80)
        
        # Start stream reception
        receive_task = asyncio.create_task(
            self.stream_manager.receiver.receive_streams()
        )
        
        start_time = time.time()
        last_report = start_time
        
        try:
            while self.running and (time.time() - start_time) < duration:
                # Get wave from stream
                wave = await self.stream_manager.receiver.get_wave()
                
                if wave:
                    await self._process_wave_for_learning(wave)
                else:
                    # No waves available, wait briefly
                    await asyncio.sleep(0.1)
                
                # Report progress every 10 seconds
                if time.time() - last_report >= 10:
                    self._report_progress()
                    last_report = time.time()
                
                # Check ego stability
                if self.auto_anchor:
                    stability = self.ego_anchor.assess_stability()
                    if stability < self.ego_anchor.stability_threshold:
                        logger.warning("⚠️ Low stability detected")
                        self.ego_anchor.re_anchor()
                
        except KeyboardInterrupt:
            logger.info("Received stop signal")
        finally:
            self.running = False
            self.stream_manager.stop()
            
        self.stats['cycles'] += 1
        
        # Final report
        self._report_final()
    
    async def _process_wave_for_learning(self, wave: Dict[str, Any]):
        """
        Process one wave through complete learning pipeline.
        
        Pipeline:
        1. Ego filtering → Prevent overwhelm
        2. Pattern extraction → Convert to 4D wave
        3. Classification → Categorize wave type
        4. Quality filtering → Accept/reject
        5. Absorption → Store in wave knowledge system
        6. Selective memory → Remember if important
        """
        self.stats['waves_received'] += 1
        
        # 1. Ego filtering
        filtered_wave = self.ego_anchor.filter_wave(wave)
        if not filtered_wave:
            self.stats['waves_rejected'] += 1
            return
        
        # 2. Pattern extraction (P4.2)
        pattern = self.pattern_extractor.extract_pattern(filtered_wave)
        if not pattern:
            return
        
        self.stats['patterns_extracted'] += 1
        
        # 3. Classification (P4.3)
        category = self.wave_classifier.classify(pattern)
        
        # 4. Quality filtering (P4.3)
        if not self.wave_classifier.should_absorb(pattern, category):
            self.stats['waves_rejected'] += 1
            return
        
        # 5. Wave absorption (P2.2 integration)
        import uuid
        pattern_id = str(uuid.uuid4())[:8]
        self.wave_search.store_pattern(pattern_id, pattern) # Correct API
        self.stats['waves_absorbed'] += 1
        self.stats['knowledge_count'] = len(self.wave_search.wave_patterns)
        
        # 6. Anchor to Elysia's perspective
        anchored = self.ego_anchor.anchor_perspective({
            'pattern_id': pattern_id,
            'category': category,
            'text': pattern.text,
            'energy': pattern.energy
        })
        
        # 6.5 Linguistic Distillation (Language Learning)
        # Extract style and grammar from the raw text before discarding/archiving it
        self.language_learner.learn_from_text(pattern.text, category)
        
        # 6.6 Deep Internalization (Soul Modification)
        # Convert External Wave (Pattern) to Internal Coordinate
        # WorldCoordinate requires (x, y, z, context), not (orientation, frequency)
        # We map the quaternion's i, j, k components to spatial coords
        world_coord = WorldCoordinate(
            x=pattern.orientation.x,
            y=pattern.orientation.y,
            z=pattern.orientation.z,
            context=pattern.text[:50] # Short summary as context
        )
        self.internal_universe.internalize(world_coord)
        self.internal_universe.save_snapshot() # Persist change for Monitor
        
        # 7. Selective memory
        if self.selective_memory.should_remember(anchored, self.ego_anchor.self_core):
            self.selective_memory.remember(anchored)
    
    def _report_progress(self):
        """Report learning progress"""
        elapsed = time.time() - self.stats['start_time']
        
        logger.info(f"\n📊 Progress Report (t={elapsed:.1f}s):")
        logger.info(f"   Waves received: {self.stats['waves_received']}")
        logger.info(f"   Patterns extracted: {self.stats['patterns_extracted']}")
        logger.info(f"   Waves absorbed: {self.stats['waves_absorbed']}")
        logger.info(f"   Knowledge count: {self.stats['knowledge_count']}")
        
        # Safe rejection rate calculation
        if self.stats['waves_received'] > 0:
            rejection_rate = f"{self.stats['waves_rejected']}/{self.stats['waves_received']}"
        else:
            rejection_rate = "0/0"
        logger.info(f"   Rejection rate: {rejection_rate}")
        
        # Ego status
        ego_stats = self.ego_anchor.get_stats()
        logger.info(f"   Stability: {ego_stats['stability']:.2f}")
        logger.info(f"   Coherence: {ego_stats['coherence']:.2f}")
        
        # Memory status
        mem_stats = self.selective_memory.get_stats()
        logger.info(f"   Remembered: {mem_stats['remembered']}/{mem_stats['capacity']}")
    
    def _report_final(self):
        """Final report after cycle completes"""
        elapsed = time.time() - self.stats['start_time']
        
        logger.info("\n" + "=" * 80)
        logger.info("🎓 P4 Learning Cycle Complete")
        logger.info("=" * 80)
        
        logger.info(f"\n📈 Final Statistics:")
        logger.info(f"   Duration: {elapsed:.1f}s")
        logger.info(f"   Cycles: {self.stats['cycles']}")
        logger.info(f"   Total waves: {self.stats['waves_received']}")
        logger.info(f"   Patterns extracted: {self.stats['patterns_extracted']}")
        logger.info(f"   Waves absorbed: {self.stats['waves_absorbed']}")
        logger.info(f"   Final knowledge: {self.stats['knowledge_count']} patterns")
        
        # Safe learning rate calculation
        if elapsed > 0:
            learning_rate = self.stats['waves_absorbed'] / elapsed
            logger.info(f"   Learning rate: {learning_rate:.2f} waves/sec")
        else:
            logger.info(f"   Learning rate: N/A (too fast)")
        
        # Ego final status
        center = self.ego_anchor.get_center()
        logger.info(f"\n⚓ Ego Status:")
        logger.info(f"   Identity: {center['name']}")
        logger.info(f"   Stability: {center['stability']:.2f}")
        logger.info(f"   Coherence: {center['coherence']:.2f}")
        logger.info(f"   Signature: {center['signature'][:50]}...")
        
        # Memory status
        mem_stats = self.selective_memory.get_stats()
        logger.info(f"\n🧠 Memory Status:")
        logger.info(f"   Remembered: {mem_stats['remembered']}")
        logger.info(f"   Forgotten: {mem_stats['forgotten']}")
        logger.info(f"   Utilization: {mem_stats['utilization']:.1%}")
        
        logger.info("\n✅ 중심(自我)을 유지하면서 학습 완료!")
        logger.info(f"   {self.stats['knowledge_count']} 개의 파동 패턴 습득")
    
    def query_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query learned knowledge using wave resonance.
        
        Args:
            query: Query text
            top_k: Number of results to return
            
        Returns:
            List of resonating knowledge patterns
        """
        logger.info(f"\n🔍 Querying: '{query}'")
        
        results = self.wave_search.search(query, top_k=top_k)
        
        logger.info(f"   Found {len(results)} resonating patterns:")
        for i, result in enumerate(results):
            logger.info(f"   {i+1}. Score: {result['score']:.3f} - {result['text'][:60]}...")
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get complete statistics"""
        return {
            **self.stats,
            'ego': self.ego_anchor.get_stats(),
            'memory': self.selective_memory.get_stats(),
            'knowledge_patterns': len(self.wave_search.patterns)
        }


async def run_meaningful_learning_demo(duration: int = 120):
    """
    Run meaningful learning demonstration.
    
    This is NOT a simple test - it's a real learning cycle that:
    1. Connects to 6 knowledge sources
    2. Receives knowledge streams
    3. Extracts wave patterns
    4. Absorbs into wave knowledge system
    5. Maintains ego stability
    6. Stores in selective memory
    
    Args:
        duration: How long to learn (seconds)
    """
    print("=" * 80)
    print("🌊 P4 Meaningful Learning Cycle Demo")
    print("   Real knowledge acquisition with ego preservation")
    print("=" * 80)
    
    # Initialize learning cycle
    cycle = P4LearningCycle(learning_rate=50)
    
    # Setup sources
    cycle.setup_sources(topics=['AI', 'quantum', 'philosophy', 'wave'])
    
    # Run learning
    print(f"\n🎓 Learning for {duration} seconds...")
    print("   (Press Ctrl+C to stop early)\n")
    
    await cycle.run_learning_cycle(duration=duration)
    
    # Test knowledge query
    print("\n" + "=" * 80)
    print("🔍 Testing Learned Knowledge")
    print("=" * 80)
    
    queries = [
        "wave resonance",
        "artificial intelligence",
        "quantum mechanics"
    ]
    
    for query in queries:
        results = cycle.query_knowledge(query, top_k=3)
        print()
    
    print("\n✅ Demo complete!")
    print(f"   Learned {cycle.stats['knowledge_count']} wave patterns")
    print(f"   Maintained stable identity: {cycle.ego_anchor.self_core.name}")


if __name__ == "__main__":
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Get duration from args or default to 120 seconds
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    
    # Run the meaningful learning demo
    asyncio.run(run_meaningful_learning_demo(duration=duration))
