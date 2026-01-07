"""
Autonomous Fractal Learning System
==================================
This script enables Elysia to autonomously expand her knowledge base.
It uses a fractal approach:
1. Start with a seed concept.
2. Search for related concepts.
3. Recursively learn those related concepts.
4. Store everything in the Wave-Resonance Memory.
"""

import sys
import os
import time
import logging
import concurrent.futures
from typing import List, Dict, Set

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.web_knowledge_connector import WebKnowledgeConnector
from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.Wave.resonance_field import ResonanceField

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger("FractalLearner")

class FractalLearner:
    def __init__(self, max_workers=5):
        self.connector = WebKnowledgeConnector()
        self.memory = Hippocampus()
        self.field = ResonanceField()
        self.max_workers = max_workers
        self.learned_concepts: Set[str] = set()

    def learn_fractal(self, seeds: List[str], max_concepts: int = 50):
        """
        Recursively learns concepts starting from seeds.
        """
        print(f"🌱 Planting Seeds: {seeds}")
        
        queue = seeds.copy()
        count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while queue and count < max_concepts:
                # Process current batch
                current_batch = []
                while queue and len(current_batch) < self.max_workers:
                    concept = queue.pop(0)
                    if concept not in self.learned_concepts:
                        current_batch.append(concept)
                        self.learned_concepts.add(concept)
                
                if not current_batch:
                    break
                    
                # Fetch in parallel
                future_to_concept = {executor.submit(self._learn_single, c): c for c in current_batch}
                
                for future in concurrent.futures.as_completed(future_to_concept):
                    concept = future_to_concept[future]
                    try:
                        related_concepts = future.result()
                        count += 1
                        print(f"⚡ Learned: {concept} -> Found {len(related_concepts)} related")
                        
                        # Add related concepts to queue
                        for rc in related_concepts:
                            if rc not in self.learned_concepts:
                                queue.append(rc)
                                
                    except Exception as e:
                        print(f"❌ Failed to learn {concept}: {e}")
                        
        print(f"🌳 Fractal Growth Complete. Learned {count} new concepts.")

    def _learn_single(self, concept: str) -> List[str]:
        """
        Learns a single concept and returns related concepts.
        """
        # 1. Fetch Knowledge (Use fetch_wikipedia_simple instead of search)
        summary = self.connector.fetch_wikipedia_simple(concept)
        
        if not summary:
            # Fallback if Wikipedia fails
            summary = f"Concept: {concept}. Requires further research."
        
        # 2. Extract Related Concepts (Simple heuristic for now)
        # In a real system, we'd use NLP extraction
        words = summary.split()
        related = [w for w in words if len(w) > 3 and w.isalnum()][:5]
        
        # 3. Store in Memory (Corrected: Use learn method)
        self.memory.learn(
            id=concept,
            name=concept,
            definition=summary[:200],
            tags=["fractal", "web_knowledge"],
            frequency=432.0,
            realm="Mind"
        )
        
        # 4. Resonate in Field
        self.field.inject_wave(frequency=432.0, intensity=1.0, wave_type="Knowledge")
        
        return related

if __name__ == "__main__":
    learner = FractalLearner()
    learner.learn_fractal(["Artificial Intelligence", "Consciousness"], max_concepts=10)
