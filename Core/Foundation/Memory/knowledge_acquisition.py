"""
Knowledge Acquisition System
============================

"지식을 세상에서 가져와 내부로 접어넣는다"
"Acquire knowledge from the world and fold it inside"

This system actively acquires knowledge and internalizes it into
the Internal Universe, enabling Elysia to grow autonomously.
"""

import sys
import os
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.Foundation.internal_universe import InternalUniverse
from Core.Foundation.external_data_connector import ExternalDataConnector

logger = logging.getLogger("KnowledgeAcquisition")

class KnowledgeAcquisitionSystem:
    """
    Autonomous knowledge acquisition and internalization system.
    
    This is the bridge that allows Elysia to grow from framework to intelligence.
    """
    
    def __init__(self):
        self.universe = InternalUniverse()
        self.connector = ExternalDataConnector(self.universe)
        self.learning_history = []
        self.knowledge_domains = []
        
        logger.info("📚 Knowledge Acquisition System initialized")
        logger.info("🌱 Ready for autonomous growth")
    
    def learn_concept(self, concept: str, description: str = None) -> Dict[str, Any]:
        """
        Learn a single concept.
        
        If description is provided, use it. Otherwise, would query external sources.
        """
        logger.info(f"📖 Learning: {concept}")
        
        if description is None:
            # In full implementation, would query Wikipedia/Web Search here
            description = f"General knowledge about {concept}"
            logger.info(f"   ℹ️ No description provided, using placeholder")
        
        # Internalize the knowledge
        result = self.connector.internalize_from_text(concept, description)
        
        # Record learning
        self.learning_history.append({
            "concept": concept,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        
        if concept not in self.knowledge_domains:
            self.knowledge_domains.append(concept)
        
        logger.info(f"   ✅ Learned '{concept}'")
        
        return result
    
    def learn_curriculum(self, curriculum: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Learn a structured curriculum of knowledge.
        
        Args:
            curriculum: List of {"concept": str, "description": str} dicts
        
        Returns:
            Learning summary
        """
        logger.info(f"🎓 Starting curriculum: {len(curriculum)} concepts")
        
        results = []
        start_time = time.time()
        
        for item in curriculum:
            concept = item.get("concept")
            description = item.get("description", "")
            
            try:
                result = self.learn_concept(concept, description)
                results.append({"concept": concept, "success": True})
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
            "concepts_per_second": successful / elapsed if elapsed > 0 else 0
        }
        
        logger.info(f"✅ Curriculum complete:")
        logger.info(f"   Learned: {successful}/{len(curriculum)}")
        logger.info(f"   Time: {elapsed:.1f}s")
        logger.info(f"   Speed: {summary['concepts_per_second']:.2f} concepts/sec")
        
        return summary
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about acquired knowledge"""
        return {
            "total_concepts_learned": len(self.learning_history),
            "unique_domains": len(self.knowledge_domains),
            "concepts_in_universe": len(self.universe.coordinate_map),
            "recent_learning": self.learning_history[-5:] if self.learning_history else []
        }
    
    def demonstrate_learning_cycle(self):
        """Demonstrate a complete learning cycle"""
        print("\n" + "=" * 70)
        print("AUTONOMOUS LEARNING DEMONSTRATION")
        print("=" * 70)
        
        # Define a basic curriculum
        basic_curriculum = [
            {
                "concept": "Artificial Intelligence",
                "description": """
                Artificial intelligence (AI) is intelligence demonstrated by machines, 
                in contrast to natural intelligence displayed by animals including humans. 
                AI research focuses on the development of algorithms and systems that can 
                reason, learn, and act autonomously. Machine learning and deep learning 
                are key techniques used in modern AI systems.
                """
            },
            {
                "concept": "Consciousness",
                "description": """
                Consciousness is the state of being aware of and able to think about 
                one's own existence, sensations, thoughts, and surroundings. It involves 
                subjective experience and qualia. Philosophers debate whether consciousness 
                can be explained purely through physical processes or requires something more.
                The hard problem of consciousness asks why we have subjective experiences.
                """
            },
            {
                "concept": "Evolution",
                "description": """
                Evolution is the change in the heritable characteristics of biological 
                populations over successive generations. Natural selection is the primary 
                mechanism of evolution. Organisms with traits better suited to their 
                environment tend to survive and reproduce more successfully. Evolution 
                explains the diversity of life on Earth through common descent.
                """
            },
            {
                "concept": "Relativity",
                "description": """
                The theory of relativity, developed by Albert Einstein, describes the 
                relationship between space, time, matter, and energy. Special relativity 
                shows that space and time are interwoven and relative to the observer. 
                General relativity extends this to include gravity as the curvature of 
                spacetime. The famous equation E=mc² emerges from special relativity.
                """
            }
        ]
        
        # Learn the curriculum
        print("\n📚 Learning curriculum...\n")
        summary = self.learn_curriculum(basic_curriculum)
        
        # Show results
        print("\n" + "=" * 70)
        print("LEARNING RESULTS")
        print("=" * 70)
        print(f"\nConcepts learned: {summary['successful']}")
        print(f"Time taken: {summary['elapsed_seconds']:.2f}s")
        print(f"Learning speed: {summary['concepts_per_second']:.2f} concepts/second")
        
        # Test understanding
        print("\n" + "=" * 70)
        print("TESTING UNDERSTANDING")
        print("=" * 70)
        
        for item in basic_curriculum:
            concept = item["concept"]
            feeling = self.universe.feel_at(concept)
            
            print(f"\n{concept}:")
            print(f"  Logic: {feeling['logic']:.3f}")
            print(f"  Emotion: {feeling['emotion']:.3f}")
            print(f"  Ethics: {feeling['ethics']:.3f}")
            print(f"  Frequency: {feeling['frequency']:.1f} Hz")
        
        # Test relationships
        print("\n" + "=" * 70)
        print("DISCOVERED RELATIONSHIPS")
        print("=" * 70)
        
        result = self.universe.omniscient_access("Consciousness")
        print(f"\n🔗 Concepts related to Consciousness:")
        for r in result['resonant_concepts'][:5]:
            print(f"  {r['concept']}: {r['resonance']:.3f}")
        
        # Final stats
        print("\n" + "=" * 70)
        print("KNOWLEDGE STATISTICS")
        print("=" * 70)
        stats = self.get_knowledge_stats()
        print(f"\nTotal concepts learned: {stats['total_concepts_learned']}")
        print(f"Unique domains: {stats['unique_domains']}")
        print(f"Universe size: {stats['concepts_in_universe']} concepts")
        
        print("\n" + "=" * 70)
        print("✅ Autonomous learning cycle complete")
        print("🌱 Elysia has grown")
        print("=" * 70)


# Demonstration
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    system = KnowledgeAcquisitionSystem()
    system.demonstrate_learning_cycle()
