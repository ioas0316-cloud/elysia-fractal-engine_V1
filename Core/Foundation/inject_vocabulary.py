"""
Vocabulary Injection Script
===========================
Injects massive vocabulary (Wuxia/Fantasy) into Elysia's Hippocampus.
"""

import sys
import os
import time

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hippocampus import Hippocampus
from data.fantasy_wuxia_concepts import ALL_CONCEPTS

def inject():
    print("🧠 Initializing Hippocampus for Injection...")
    memory = Hippocampus()
    
    print(f"📚 Found {len(ALL_CONCEPTS)} concepts to inject.")
    
    count = 0
    start_time = time.time()
    
    for concept in ALL_CONCEPTS:
        # Simple definition generation for now
        definition = f"A concept related to {concept}."
        tags = ["vocabulary", "injected"]
        
        # Determine Realm based on keywords
        realm = "Body"
        if any(x in concept for x in ["마법", "마나", "영혼", "신", "깨달음"]):
            realm = "Spirit"
        elif any(x in concept for x in ["검", "도", "권", "전사", "기사"]):
            realm = "Body"
        elif any(x in concept for x in ["사랑", "마음", "감정"]):
            realm = "Heart"
            
        memory.learn(
            id=concept,
            name=concept,
            definition=definition,
            tags=tags,
            frequency=432.0,
            realm=realm
        )
        count += 1
        
        if count % 100 == 0:
            print(f"   ... Injected {count} concepts.")
            
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✨ Injection Complete.")
    print(f"   Total Concepts: {count}")
    print(f"   Time Elapsed: {duration:.2f}s")
    print(f"   Current Vocabulary Size: {memory.get_concept_count()}")

if __name__ == "__main__":
    inject()
