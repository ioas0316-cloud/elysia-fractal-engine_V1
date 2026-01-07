
import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import CausalNarrativeEngine, CausalNode, CausalLink, CausalRelationType

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("EmpathicReasoning")

def test_emotional_inference():
    logger.info("🧪 Testing Empathic/Contextual Inference (Phase 9)")
    
    engine = CausalNarrativeEngine()
    
    # 1. Build Physical Chain: Rain -> Dark -> Cold
    engine.add_node(CausalNode("Rain", "Physical"))
    engine.add_node(CausalNode("Darkness", "Physical"))
    engine.add_node(CausalNode("Cold", "Physical"))
    
    engine.add_link("Rain", "Darkness", CausalRelationType.CAUSES)
    engine.add_link("Darkness", "Cold", CausalRelationType.CORRELATES) # Often correlate
    
    # 2. Build Psychological Chain: Darkness -> Loneliness -> Need for Comfort
    engine.add_node(CausalNode("Loneliness", "Emotional"))
    engine.add_node(CausalNode("NeedForComfort", "Drive"))
    
    engine.add_link("Darkness", "Loneliness", CausalRelationType.CAUSES)
    engine.add_link("Loneliness", "NeedForComfort", CausalRelationType.MOTIVATES)
    
    # 3. Trace Chains
    logger.info("   ... Tracing Logical Chains ...")
    chains_phys = engine.trace_causal_chain("Rain") 
    chains_psych = engine.trace_causal_chain("Darkness")
    
    # Store chains manually for the test (in real runs, engine would do this)
    engine.chains.extend(chains_phys)
    engine.chains.extend(chains_psych)
    
    logger.info(f"   Found {len(engine.chains)} chains.")
    
    # 4. Phase 9 Dynamic Intersection & Experiential Context
    logger.info("   ... Detecting Context Planes ...")
    for chain in engine.chains:
        engine.detect_intersections(chain)
        
    # 5. Perform Inference (Rain -> NeedForComfort)
    logger.info("   ... Performing Lateral Inference from 'Rain' ...")
    inferences = engine.infer_contextual_link("Rain")
    
    if any("NeedForComfort" in inf or "Loneliness" in inf for inf in inferences):
        logger.info("   ✅ SUCCESS: System inferred Emotional state from Rain.")
    
    # 6. User Verification: Winter -> Hunger/Loneliness (Experiential Plane)
    logger.info("   ... Testing User's 'Winter' Experiential Context ...")
    # This plane is pre-seeded by _initialize_experiential_context
    winter_inferences = engine.infer_contextual_link("winter")
    for inf in winter_inferences:
        logger.info(f"     > {inf}")
        
    if any("hunger" in inf.lower() for inf in winter_inferences) and any("loneliness" in inf.lower() for inf in winter_inferences):
        logger.info("   ✅ SUCCESS: 'Winter' correctly triggers 'Hunger' and 'Loneliness' via Experiential Context.")
    else:
        logger.warning("   ⚠️ Winter inference missing expected concepts.")


if __name__ == "__main__":
    test_emotional_inference()
