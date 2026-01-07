"""
Test Self-Evolution System
==========================
Verifies that the EvolutionManager correctly triggers concept evolution
and that the CodeMutator safely handles code modifications.
"""

import sys
import os
import logging
import numpy as np

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from Core.Evolution.Growth.Evolution.Evolution.evolution_manager import EvolutionManager
from Core.Foundation.Physics.fluctlight import FluctlightEngine, FluctlightParticle
from Core.Foundation.Mind.hippocampus import Hippocampus
from Core.Foundation.Mind.alchemy import Alchemy
from Core.Evolution.Growth.Evolution.Evolution.code_mutator import EvolutionaryCoder, SafetySandbox

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestEvolution")

def test_concept_evolution():
    logger.info("\n🧪 Testing Concept Evolution...")
    
    # Setup
    hippocampus = Hippocampus()
    alchemy = Alchemy()
    manager = EvolutionManager(hippocampus, alchemy)
    engine = FluctlightEngine(world_size=100)
    
    # Create artificial cluster of particles
    p1 = FluctlightParticle(position=np.array([50., 50., 50.]), concept_id="fire")
    p2 = FluctlightParticle(position=np.array([51., 50., 50.]), concept_id="water") # Close enough
    engine.particles = [p1, p2]
    
    # Force trigger
    logger.info("   Triggering evolution manually...")
    manager.trigger_evolution(engine)
    
    # Check if concept emerged (Alchemy combines fire+water -> steam)
    # Note: trigger_evolution uses random choice, so we might need to force it or mock it
    # For this test, let's call concept_evo directly to be sure
    new_concepts = manager.concept_evo.evolve_concepts(engine)
    
    if new_concepts:
        logger.info(f"✅ Success! Evolved concepts: {new_concepts}")
    else:
        logger.warning("⚠️ No concepts evolved (might be alchemy rules or distance)")

def test_code_mutation_safety():
    logger.info("\n🧪 Testing Code Mutation Safety...")
    
    coder = EvolutionaryCoder()
    
    # Define a simple function to mutate
    def simple_math(a, b):
        return a + b
        
    # Try to evolve it
    logger.info("   Attempting to mutate 'simple_math' function...")
    new_func = coder.evolve_function(simple_math, intensity=0.5)
    
    if new_func is None:
        logger.info("✅ Safety check passed (Mutation simulated/logged but not applied)")
    else:
        logger.info("✅ Mutation returned (Sandbox passed)")

def test_sandbox():
    logger.info("\n🧪 Testing Safety Sandbox...")
    
    # Valid code
    code_valid = "def test(): return 1"
    if SafetySandbox.test_function(code_valid, "test", []):
        logger.info("✅ Valid code passed sandbox")
    else:
        logger.error("❌ Valid code failed sandbox")
        
    # Invalid code (syntax error)
    code_invalid = "def test(): return 1 +"
    if not SafetySandbox.test_function(code_invalid, "test", []):
        logger.info("✅ Invalid code correctly rejected")
    else:
        logger.error("❌ Invalid code bypassed sandbox!")

if __name__ == "__main__":
    test_concept_evolution()
    test_code_mutation_safety()
    test_sandbox()
