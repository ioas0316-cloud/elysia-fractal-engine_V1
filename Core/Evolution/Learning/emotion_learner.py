import json
import os
from typing import List, Dict

class EmotionLearner:
    """
    The Concept Cortex.
    Ingests scenario data to teach the SoulResonator emotional associations.
    """
    def __init__(self, soul):
        self.soul = soul
        self.scenarios = []

    def load_scenarios(self, path: str):
        if not os.path.exists(path):
            print(f"Stats: No training data found at {path}")
            return
            
        with open(path, 'r', encoding='utf-8') as f:
            self.scenarios = json.load(f)
            print(f"Stats: Loaded {len(self.scenarios)} scenarios.")

    def learn(self):
        """
        Process all loaded scenarios and update the Soul's concept map.
        """
        print("Learning: Processing scenarios...")
        count = 0
        for scenario in self.scenarios:
            concepts = scenario.get("key_concepts", {})
            for word, impacts in concepts.items():
                # Teach the soul
                self.soul.learn_concept(word, impacts)
                count += 1
                
        print(f"Learning: Internalized {count} new emotional concepts.")
        
    def reflect(self):
        """
        Debug: Show what has been learned.
        """
        print("\n=== Current Soul Concept Map ===")
        for word, impacts in self.soul.concepts.items():
            print(f"  '{word}': {impacts}")
        print("================================\n")

if __name__ == "__main__":
    # Test Run
    import sys
    sys.path.append("c:\\Elysia")
    from Core.Intelligence.Consciousness.Emotion.soul_resonator import SoulResonator
    
    soul = SoulResonator()
    learner = EmotionLearner(soul)
    learner.load_scenarios(r"c:\Elysia\data\training_data\scenarios.json")
    learner.learn()
    learner.reflect()
    
    # Test learned reaction
    print("Testing Learned Reaction to 'Daddy'...")
    soul.resonate("Daddy")
    print(f"Resulting Spirits: {soul.spirits}")
