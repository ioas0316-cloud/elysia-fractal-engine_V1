"""
Verify Weaving Mechanism (The Hot Pan Prototype)
================================================

Purpose:
To demonstrate the 'Causal Loom' architecture where independent Intelligence Lines
emit Propositions (Facts) that are woven into a Causal Chain to deduce a conclusion.

Scenario:
User Input: "I put the metal pan on the fire."
Lines: Physics, Chemistry, Biology.
Goal: Deduce "Burn Hazard".
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
logger = logging.getLogger("CausalLoom")

# --- 1. Data Structures (The Threads) ---

@dataclass(frozen=True) # Frozen to be hashable
class Concept:
    name: str
    category: str

    def __repr__(self):
        return f"{self.name}({self.category})"

@dataclass(frozen=True)
class Proposition:
    subject: Concept
    predicate: str
    object: Concept

    def __repr__(self):
        return f"[{self.subject} --{self.predicate}--> {self.object}]"

@dataclass
class KnowledgeThread:
    source: str
    facts: List[Proposition]

# --- 2. The Lines (The Sources) ---

class IntelligenceLine:
    def __init__(self, name):
        self.name = name

    def perceive(self, context_text: str) -> KnowledgeThread:
        return KnowledgeThread(self.name, [])

# Mocking Specific Domain Logic
class PhysicsLine(IntelligenceLine):
    def perceive(self, text: str) -> KnowledgeThread:
        facts = []
        if "pan" in text and "fire" in text:
            # Fact: Fire heats Pan
            facts.append(Proposition(
                Concept("Fire", "Energy"), "heats", Concept("Pan", "Object")
            ))
        if "pan" in text:
             # Fact: Pan has Temperature
            facts.append(Proposition(
                Concept("Pan", "Object"), "has_property", Concept("Temperature", "Property")
            ))
        return KnowledgeThread(self.name, facts)

class MaterialLine(IntelligenceLine):
    def perceive(self, text: str) -> KnowledgeThread:
        facts = []
        if "metal" in text or "pan" in text: # Assuming pan is metal for this context
            # Fact: Pan is made of Metal
            facts.append(Proposition(
                Concept("Pan", "Object"), "is_made_of", Concept("Metal", "Material")
            ))
            # Principle: Metal conducts Heat
            facts.append(Proposition(
                Concept("Metal", "Material"), "conducts", Concept("Heat", "Energy")
            ))
        return KnowledgeThread(self.name, facts)

class BiologyLine(IntelligenceLine):
    def perceive(self, text: str) -> KnowledgeThread:
        facts = []
        # General knowledge always available
        # Fact: High Temperature causes Burn
        facts.append(Proposition(
            Concept("Temperature", "Property"), "affects", Concept("Skin", "Organ")
        ))
        facts.append(Proposition(
            Concept("HighHeat", "Condition"), "causes", Concept("Burn", "Injury")
        ))
        return KnowledgeThread(self.name, facts)

# --- 3. The Weaver (The Loom) ---

class CausalWeaver:
    def __init__(self):
        self.lines = [PhysicsLine("Physics"), MaterialLine("Material"), BiologyLine("Biology")]

    def weave(self, text: str):
        logger.info(f"🧵 Weaving context for: '{text}'")

        # 1. Gather Threads
        all_facts: List[Proposition] = []
        for line in self.lines:
            thread = line.perceive(text)
            if thread.facts:
                logger.info(f"  - {line.name} reported: {len(thread.facts)} facts")
                for f in thread.facts:
                    logger.info(f"    * {f}")
                all_facts.extend(thread.facts)

        # 2. Find Knots (Shared Concepts)
        # We look for simple transitive links: A->B and B->C
        logger.info("🪢 Knotting threads...")

        inferences = []

        # Simple Rule Engine for the PoC
        # Rule 1: Transfer of Property (If A heats B, B gains Heat/Temp)
        has_heat = False
        hot_object = None

        for f in all_facts:
            if f.predicate == "heats":
                inferences.append(f"INFERENCE: {f.subject.name} is increasing energy of {f.object.name}")
                has_heat = True
                hot_object = f.object

        # Rule 2: Material Conduction (If Object is Material M, and M conducts Heat, Object becomes Hot)
        is_conductive = False
        for f in all_facts:
            if f.predicate == "is_made_of" and f.subject == hot_object:
                material = f.object
                # Check if material conducts
                for f2 in all_facts:
                    if f2.subject == material and f2.predicate == "conducts":
                        is_conductive = True
                        inferences.append(f"INFERENCE: {hot_object.name} is conductive ({material.name}). It will get HOT.")

        # Rule 3: Danger Check (If Object is Hot -> Danger to Skin)
        if is_conductive and has_heat:
             # Find Biological Consequence
             inferences.append(f"⚠️ CRITICAL: {hot_object.name} exceeds biological safety threshold.")
             inferences.append(f"ACTION: Remove {hot_object.name} from Fire immediately.")

        # 3. Output Result
        print("\n--- Final Weave ---")
        if not inferences:
            print("No Causal Chain formed.")
        else:
            for inf in inferences:
                print(inf)

# --- 4. Execution ---

if __name__ == "__main__":
    weaver = CausalWeaver()
    user_input = "I put the metal pan on the fire."
    weaver.weave(user_input)
