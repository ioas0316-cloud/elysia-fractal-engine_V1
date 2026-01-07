
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import (
    ThoughtUniverse, DimensionLevel, UniversalLaw, EpistemicSpace
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("SelfEvolutionTest")

def test_self_evolution():
    logger.info("🌌 Testing Phase 14: Metacognitive Architecture (Self-Evolution)")
    
    # Initialize Universe
    universe = ThoughtUniverse("Elysia_Developing_Mind")
    
    # 1. Initialize "Child Elysia" State
    # A simple, 1-dimensional concept of "Justice"
    justice_node = universe.add_point(
        id="Justice",
        description="Punishing bad people."
    )
    # Simple link (Low differentiation, low integration)
    universe.add_line("BadAction", "Justice", "causes")
    
    logger.info(f"   Created Concept: {justice_node.id} ({justice_node.description})")
    
    
    # 2. Self-Diagnosis: Evaluate Maturity
    logger.info("   ... Elysia analyzing her own understanding of 'Justice' ...")
    
    gap_report = universe.evaluate_maturity("Justice")
    
    logger.info(f"   📊 Maturity Report: {gap_report['status']}")
    logger.info(f"      - Current Metrics: Diff={gap_report['current_metrics'].differentiation:.2f}, Int={gap_report['current_metrics'].integration:.2f}")
    
    # Verify Detection
    if gap_report['status'] == "IMMATURE":
         logger.info("   ✅ Correctly self-diagnosed as IMMATURE.")
    else:
         logger.error("   ❌ Failed to diagnose immaturity.")
         return

    # 3. Autonomous Drive: Formulate Growth Plan
    logger.info("   ... Elysia formulating growth intentions ...")
    
    intentions = universe.formulate_growth_plan(gap_report)
    
    if intentions:
        logger.info("   ✅ Generated Growth Intentions:")
        for intent in intentions:
            logger.info(f"      > {intent}")
    else:
        logger.error("   ❌ Failed to generate intentions.")
        return

    logger.info("✅ Phase 14 Verified: Elysia can self-diagnose and plan her own cognitive evolution.")

if __name__ == "__main__":
    test_self_evolution()
