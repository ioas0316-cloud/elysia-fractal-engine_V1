"""
Knowledge Hunter (지식 사냥꾼)
==============================

"The Wolf does not wait for the sheep."
"늑대는 양을 기다리지 않는다."

High-level module orchestrating Active Exploration.
Combines SearchTendril and KnowledgeIngestor.
"""

import logging
import random
from typing import List
from Core.Sensory.Network.search_tendril import SearchTendril
from Core.Evolution.Learning.external_digester import ExternalDigester

logger = logging.getLogger("KnowledgeHunter")

class KnowledgeHunter:
    def __init__(self):
        self.scout = SearchTendril()
        self.stomach = ExternalDigester()
        
    def hunt(self, topic: str) -> str:
        """
        Actively hunts for knowledge on a topic.
        1. Search.
        2. Select.
        3. Eat.
        """
        logger.info(f"🏹 Hunting for: {topic}")
        
        # 1. Scout
        urls = self.scout.search(topic, limit=3)
        
        if not urls:
            return f"❌ Hunt failed. No trails found for '{topic}'."
            
        # 2. Select (For now, random or first, later Tone-based choice)
        target = urls[0] # The alpha prey
        logger.info(f"   🎯 Locked on target: {target}")
        
        # 3. Eat
        result = self.stomach.digest_url(target)
        
        # 4. Feel Joy (Dopamine Reward)
        from Core.Intelligence.Cognitive.curiosity_core import get_curiosity_core
        joy_engine = get_curiosity_core()
        joy_engine.satisfy_curiosity(topic, novelty_score=0.9) # High novelty for active hunt
        
        return f"🍖 Hunt Successful. {result} (Dopamine Released)"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    hunter = KnowledgeHunter()
    print(hunter.hunt("Consciousness"))
