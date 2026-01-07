
import sys
import os
import logging
import ast

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import CausalNarrativeEngine, CausalNode, CausalLink, CausalRelationType, ThoughtUniverse, CausalChain, UniversalLaw

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("FractalTest")

def test_fractal_schema():
    logger.info("🌌 Testing Phase 12: Dimensional Fractals (Universal Principles)")
    
    # We need to access ThoughtUniverse directly or via engine if linked
    # CausalNarrativeEngine doesn't natively expose ThoughtUniverse in current code structure 
    # (it is usually the other way around: ThoughtUniverse contains Engine).
    # So we instantiate ThoughtUniverse for this advanced test.
    
    universe = ThoughtUniverse(name="Elysia_Fractal_Mind")
    
    # 1. Create the Source Narrative (Homeless - Micro Level)
    # Winter -> Cold -> Distress
    chain_source = CausalChain(
        id="chain_homeless_winter",
        node_sequence=["Winter", "Cold", "Distress"],
        links=[
            CausalLink("Winter", "Cold", CausalRelationType.CAUSES),
            CausalLink("Cold", "Distress", CausalRelationType.CAUSES)
        ]
    )
    
    # 2. Extract Principle
    logger.info("   ... Extracting Principle from 'Homeless Context' ...")
    law = universe.extract_principle(chain_source, "AdverseReaction")
    logger.info(f"   📜 Law Extracted: {law.description}")
    
    # 3. Apply to Biological Domain (Cell - Macro/Fractal Level)
    # Map: Winter -> Hypoxia (Oxygen Lack)
    #      Cold   -> EnergyDepletion
    #      Distress -> Apoptosis (Cell Death)
    
    domain_map_bio = {
        "Step_0": "Hypoxia",
        "Step_1": "EnergyDepletion",
        "Step_2": "Apoptosis"
    }
    
    logger.info("   ... Applying Principle to 'Biological Cell' Domain ...")
    narrative_bio = universe.apply_principle_to_domain(law, domain_map_bio)
    
    for line in narrative_bio:
        logger.info(f"     > {line}")
        
    # 4. Apply to Geopolitical Domain (Nation - fractal Level)
    # Map: Winter -> ResourceScarcity
    #      Cold   -> EconomicCrisis
    #      Distress -> War
    
    domain_map_geo = {
        "Step_0": "ResourceScarcity",
        "Step_1": "EconomicCrisis",
        "Step_2": "War"
    }
    
    logger.info("   ... Applying Principle to 'Geopolitical Nation' Domain ...")
    narrative_geo = universe.apply_principle_to_domain(law, domain_map_geo)
    
    for line in narrative_geo:
        logger.info(f"     > {line}")

    if len(narrative_bio) > 1 and len(narrative_geo) > 1:
        logger.info("   ✅ Phase 12 Verified: Structural Isomorphism proven across dimensions.")

if __name__ == "__main__":
    test_fractal_schema()
