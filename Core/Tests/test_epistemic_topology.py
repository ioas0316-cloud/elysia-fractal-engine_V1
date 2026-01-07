
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
logger = logging.getLogger("FractalTest")

def test_epistemic_topology():
    logger.info("🌌 Testing Phase 13: Epistemic Topology (Fractal Knowledge Worlds)")
    
    # Initialize Universe
    universe = ThoughtUniverse("Elysia_Fractal_Mind")
    
    # 1. Create a "Science" Node
    science_node = universe.add_point(
        id="Science",
        description="The systematic study of the natural world through observation and experiment."
    )
    logger.info(f"   Created Node: {science_node.id} ({science_node.description})")
    
    
    # 2. Explode "Science" into a "Physics Space" (Fractal Expansion)
    physics_space = universe.expand_node_into_space(
        node_id="Science",
        space_name="Physics",
        density=2.5,  # High density
        methodologies=["EMPIRICAL", "MATHEMATICAL"]
    )
    
    # Verify Fractal Connection
    if "Science" in physics_space.parent_ids and physics_space.id in science_node.child_ids:
         logger.info(f"   ✅ Fractal Link Verified: Science <-> {physics_space.id}")
    else:
         logger.error("   ❌ Fractal Link Failed!")
         return

    # 3. Traverse the Space (Simulation)
    # Scenario: Agent wants to understand "QuantumMechanics" within "Physics Space"
    logger.info(f"   ... Agent attempting traversal to 'QuantumMechanics' ...")
    
    traversal_result = universe.traverse_epistemic_field(
        agent_id="Novice_Agent",
        space_id=physics_space.id,
        current_knowledge=["Basic_Math"],
        target_concept="QuantumMechanics"
    )
    
    # Check Traversal
    if traversal_result["status"] == "arrived":
        logger.info(f"   ✅ Traversal Successful!")
        logger.info(f"      - Resistance: {traversal_result['resistance']}")
        logger.info(f"      - Effort Required: {traversal_result['effort_required']}")
        logger.info(f"      - Steps: {len(traversal_result['path_log'])}")
        # Print path log for dramatic effect
        # for log in traversal_result['path_log'][:3]:
        #     logger.info(f"        > {log}")
    else:
        logger.error(f"   ❌ Traversal Failed: {traversal_result.get('message')}")
        return

    logger.info("✅ Phase 13 Verified: Knowledge exists as a traversable, fractal topology.")

if __name__ == "__main__":
    test_epistemic_topology()
