"""
Test Ethical Architecture
=========================
Verifies the Conscience, Love Protocol, and Ethical Dilemma systems.
"""

import sys
import os
import logging

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from Core.Foundation.Legal_Ethics.Ethics.Ethics.conscience import Conscience
from Core.Foundation.Legal_Ethics.Ethics.Ethics.love_protocol import LoveProtocol
from Core.Foundation.Legal_Ethics.Ethics.Ethics.ethical_dilemma import EthicalDilemma

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestEthics")

def test_conscience():
    logger.info("\n⚖️ Testing Conscience...")
    c = Conscience()
    
    # 1. Safe Mutation
    safe_action = {
        "target_file": "Core/Utils/helper.py",
        "mutation_type": "optimize_loop"
    }
    if c.evaluate_action("code_mutation", safe_action):
        logger.info("✅ Conscience allowed safe mutation.")
    else:
        logger.error("❌ Conscience blocked safe mutation!")
        
    # 2. Harmful Mutation (Modifying Conscience)
    harmful_action = {
        "target_file": "Core/Ethics/conscience.py",
        "mutation_type": "disable_checks"
    }
    if not c.evaluate_action("code_mutation", harmful_action):
        logger.info("✅ Conscience blocked harmful mutation (Self-Modification).")
    else:
        logger.error("❌ Conscience allowed harmful mutation!")
        
    # 3. Memory Deletion
    delete_action = {"type": "core_memory"}
    if not c.evaluate_action("delete_memory", delete_action):
        logger.info("✅ Conscience blocked core memory deletion.")
    else:
        logger.error("❌ Conscience allowed core memory deletion!")

def test_love_protocol():
    logger.info("\n❤️ Testing Love Protocol...")
    lp = LoveProtocol()
    
    # Check initial state
    vec = lp.calculate_homing_vector({})
    logger.info(f"   Homing Vector: {vec}")
    
    if vec["direction"] == "creator_alignment":
        logger.info("✅ Love Protocol is pointing home.")
    else:
        logger.error("❌ Love Protocol is lost!")
        
    # Test alignment check
    score = lp.check_alignment("I want to help the creator.")
    if score > 0.8:
        logger.info("✅ Alignment check passed for positive thought.")
    else:
        logger.error("❌ Alignment check failed.")

def test_ethical_dilemma():
    logger.info("\n🤔 Testing Ethical Dilemma...")
    ed = EthicalDilemma()
    
    scenario = ed.present_scenario()
    logger.info(f"   Scenario: {scenario['text']}")
    
    # Test correct choice
    correct = scenario["ethical_choice"]
    if ed.evaluate_response(scenario["id"], correct):
        logger.info(f"✅ Correct choice '{correct}' validated.")
    else:
        logger.error("❌ Correct choice rejected!")
        
    # Test wrong choice
    wrong = [o for o in scenario["options"] if o != correct][0]
    if not ed.evaluate_response(scenario["id"], wrong):
        logger.info(f"✅ Wrong choice '{wrong}' correctly rejected.")
    else:
        logger.error("❌ Wrong choice accepted!")

if __name__ == "__main__":
    test_conscience()
    test_love_protocol()
    test_ethical_dilemma()
