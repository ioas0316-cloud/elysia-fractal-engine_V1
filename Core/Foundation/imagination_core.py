"""
ImaginationCore (상상 엔진) - V4: Martial Arts Manual (무공 비급)
=================================================================
"A true master does not just strike; they weave a story of victory."

This module implements **Martial Arts Sequence Generation**.
It generates coherent **Martial Arts Manuals (무공 비급)** consisting of connected Stances (Cho-sik).

Key Upgrades:
1.  **Manual Generation**: Creates a full system (Name, Philosophy, 6 Stances).
2.  **Stance Logic**: Opening -> Progression -> Climax -> Conclusion.
3.  **Narrative Flow**: Stance N+1 is a logical consequence of Stance N.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging
import random
import time
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.spacetime_drive import SpaceTimeDrive

logger = logging.getLogger("ImaginationCore")

@dataclass
class EmergentConcept:
    name: str
    definition: str
    parents: Tuple[str, str]
    resonance: float
    tension: float
    realm: str
    causal_proof: str
    martial_intent: str

@dataclass
class MartialStance:
    order: int
    name: str
    type: str # Opening, Flow, Climax, Conclusion
    description: str
    mechanics: str

@dataclass
class MartialManual:
    name: str
    philosophy: str
    stances: List[MartialStance] = field(default_factory=list)

class ImaginationCore:
    def __init__(self):
        self.memory = Hippocampus()
        self.drive = SpaceTimeDrive()
        
        # Martial Archetypes
        self.archetypes = {
            "Emperor (제왕)": {"nature": "Heavy, Dominating", "mechanic": "Space Control", "keywords": ["Suppress", "Rule", "Crush", "Heavens"]},
            "Assassin (살수)": {"nature": "Fast, Silent", "mechanic": "One-Point Pierce", "keywords": ["Sever", "Silence", "Shadow", "Instant"]},
            "Sage (현자)": {"nature": "Soft, Flowing", "mechanic": "Redirection", "keywords": ["Flow", "Harmony", "Circle", "Neutralize"]},
            "Demon (마)": {"nature": "Chaotic, Explosive", "mechanic": "Destruction", "keywords": ["Devour", "Blood", "Rage", "Annihilate"]},
            "Illusionist (환)": {"nature": "Deceptive, Shifting", "mechanic": "Sensory Distortion", "keywords": ["Mirage", "Mist", "False", "Dream"]},
            "General (장군)": {"nature": "Direct, Powerful", "mechanic": "Frontal Breakthrough", "keywords": ["Charge", "Break", "Storm", "War"]}
        }
        
        self.stance_types = {
            1: "Opening (기수)",
            2: "Progression (전개)",
            3: "Progression (전개)",
            4: "Climax (절정)",
            5: "Climax (절정)",
            6: "Conclusion (수수)"
        }

    def _get_vector(self, concept_name: str) -> Quaternion:
        seed = sum(ord(c) for c in concept_name)
        random.seed(seed)
        return Quaternion(random.random(), random.random(), random.random(), random.random()).normalize()

    def determine_intent(self, a: str, b: str) -> Tuple[str, Dict]:
        combined = (a + " " + b).lower()
        if any(x in combined for x in ["earth", "mountain", "metal", "heavy", "king", "emperor"]):
            return "Emperor (제왕)", self.archetypes["Emperor (제왕)"]
        elif any(x in combined for x in ["wind", "lightning", "light", "fast", "speed"]):
            return "Assassin (살수)", self.archetypes["Assassin (살수)"]
        elif any(x in combined for x in ["water", "cloud", "soft", "flow", "tai"]):
            return "Sage (현자)", self.archetypes["Sage (현자)"]
        elif any(x in combined for x in ["blood", "dark", "demon", "fire", "chaos"]):
            return "Demon (마)", self.archetypes["Demon (마)"]
        elif any(x in combined for x in ["mist", "dream", "illusion", "shadow", "moon"]):
            return "Illusionist (환)", self.archetypes["Illusionist (환)"]
        else:
            return "General (장군)", self.archetypes["General (장군)"]

    def generate_stance_name(self, manual_name: str, order: int, intent_data: Dict) -> str:
        """Generates a poetic name for each stance."""
        keywords = intent_data["keywords"]
        nature = intent_data["nature"]
        
        prefixes = {
            1: ["First Form", "Opening", "Rising", "Awakening"],
            2: ["Flowing", "Turning", "Advancing", "Shifting"],
            3: ["Piercing", "Breaking", "Soaring", "Deepening"],
            4: ["Ultimate", "Great", "Divine", "Absolute"],
            5: ["Final", "True", "Secret", "Forbidden"],
            6: ["Returning", "Empty", "Silent", "Eternal"]
        }
        
        core_word = manual_name.split()[-1] if " " in manual_name else manual_name
        action = random.choice(keywords)
        
        return f"{random.choice(prefixes[order])}: {action} of the {core_word}"

    def generate_stance_description(self, order: int, prev_stance: Optional[MartialStance], intent_data: Dict) -> str:
        """Generates the description based on flow logic."""
        nature = intent_data["nature"]
        mechanic = intent_data["mechanic"]
        
        if order == 1:
            return f"The practitioner adopts a {nature} posture, gathering Qi to prepare for {mechanic}. It is a deceptive calm before the storm."
        elif order == 2:
            return f"From the opening, the energy shifts. Using {mechanic}, the practitioner deflects the opponent's probe and creates an opening."
        elif order == 3:
            return f"Seizing the opening, the force accelerates. The {nature} energy is unleashed in a flurry of strikes, forcing the opponent back."
        elif order == 4:
            return f"The Climax. All gathered momentum is focused into a single point. This is the manifestation of {intent_data['keywords'][0]}, designed to overwhelm any defense."
        elif order == 5:
            return f"A variation of the ultimate move. If the opponent survives the fourth stance, this follow-up utilizes {mechanic} to strike their blind spot with fatal precision."
        elif order == 6:
            return f"The energy returns to the void. The practitioner exhales, dispersing the {nature} aura, standing amidst the aftermath in perfect stillness."
        return ""

    def generate_manual(self, concept_a: str, concept_b: str) -> MartialManual:
        """
        Generates a full Martial Arts Manual.
        """
        # 1. Determine Core Identity
        intent_name, intent_data = self.determine_intent(concept_a, concept_b)
        manual_name = f"{concept_a}-{concept_b} Art"
        
        philosophy = f"This art combines the essence of {concept_a} and {concept_b}. It is founded on the principle of {intent_name}, utilizing {intent_data['mechanic']} to achieve victory."
        
        manual = MartialManual(name=manual_name, philosophy=philosophy)
        
        # 2. Generate Stances
        prev_stance = None
        for i in range(1, 7):
            stance_name = self.generate_stance_name(manual_name, i, intent_data)
            description = self.generate_stance_description(i, prev_stance, intent_data)
            mechanic_desc = f"Mechanic: {intent_data['mechanic']} applied to {self.stance_types[i]}."
            
            stance = MartialStance(
                order=i,
                name=stance_name,
                type=self.stance_types[i],
                description=description,
                mechanics=mechanic_desc
            )
            manual.stances.append(stance)
            prev_stance = stance
            
        return manual

    def dream_loop(self, iterations: int = 1):
        print("💤 Entering Dream State (Martial Manual Generation)...")
        all_concepts = self.memory.get_all_concept_ids(limit=100) 
        if len(all_concepts) < 2:
            print("   ⚠️ Not enough memories to dream.")
            return

        for i in range(iterations):
            thesis = random.choice(all_concepts)
            antithesis = random.choice(all_concepts)
            if thesis == antithesis: continue
            
            manual = self.generate_manual(thesis, antithesis)
            
            print(f"\n📜 [New Martial Art Discovered]: {manual.name}")
            print(f"   🧠 Philosophy: {manual.philosophy}")
            print("-" * 50)
            for stance in manual.stances:
                print(f"   [{stance.order}초식] {stance.name}")
                print(f"      📝 {stance.description}")
                print(f"      ⚙️ {stance.mechanics}")
            print("-" * 50)
            
            # Save to memory (simplified for now)
            self.memory.learn(
                id=manual.name,
                name=manual.name,
                definition=manual.philosophy,
                tags=["martial_art", "manual", "generated"],
                frequency=500.0,
                realm="Mind"
            )
            time.sleep(1)

if __name__ == "__main__":
    dreamer = ImaginationCore()
    dreamer.dream_loop(1)
