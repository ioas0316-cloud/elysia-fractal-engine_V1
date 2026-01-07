
import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import CausalNarrativeEngine, CausalNode, CausalLink, CausalRelationType

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("NarrativeEmpathy")

def test_homeless_narrative():
    logger.info("❄️ Testing Phase 11: Narrative Empathy (The Homeless Scenario)")
    
    engine = CausalNarrativeEngine()
    
    # 1. Define the 'Homeless Man' Persona/Context
    # (In a full system, this would be a ContextPlane of its own)
    
    # 2. Build the Narrative Chain
    # Step A: Winter Environment
    engine.add_node(CausalNode("Winter_Night", description="Dark cold winter night", is_state=False))
    engine.add_node(CausalNode("Homelessness", description="No home, no job, only a coat", is_state=True))
    
    # Step B: Immediate Physical Effect
    engine.add_node(CausalNode("Freezing_Cold", description="Extreme cold sensation", is_state=True))
    engine.add_node(CausalNode("Craving_Warmth", description="Desperate need for warmth", is_state=True))
    
    engine.add_link("Winter_Night", "Freezing_Cold", CausalRelationType.CAUSES)
    engine.add_link("Homelessness", "Freezing_Cold", CausalRelationType.ENABLES) # Homelessness enables the cold to hit harder
    engine.add_link("Freezing_Cold", "Craving_Warmth", CausalRelationType.MOTIVATES)
    
    # Step C: The Psychological Trigger (Memory)
    # The craving for warmth triggers the memory of "Past Comfort"
    engine.add_node(CausalNode("Memory_of_Past_Home", description="Warm fire, family, happiness", is_state=True))
    
    engine.add_link("Craving_Warmth", "Memory_of_Past_Home", CausalRelationType.ASSOCIATED_WITH) 
    
    # Step D: The Tragic Contrast (The Core of User's Insight)
    # The memory contrasts with current homelessness
    engine.add_node(CausalNode("Current_Misery", description="Sleeping on street, rejected", is_state=True))
    engine.add_link("Homelessness", "Current_Misery", CausalRelationType.CAUSES)
    
    engine.add_node(CausalNode("Grief_of_Loss", description="Pain of what was lost", is_state=True))
    
    # THIS is the key relation: Memory CONTRASTS WITH Current Misery -> CAUSES Grief
    link_contrast = engine.add_link("Memory_of_Past_Home", "Current_Misery", CausalRelationType.CONTRASTS_WITH)
    engine.add_link("Current_Misery", "Grief_of_Loss", CausalRelationType.CAUSES, conditions=["Contrasted with Past"])
    
    # Step E: The Spiraling Consequence (Anger / Self-Loathing)
    engine.add_node(CausalNode("Self_Loathing", description="Hating oneself for the fall", is_state=True))
    engine.add_node(CausalNode("Anger_at_World", description="Resentment towards society", is_state=True))
    
    engine.add_link("Grief_of_Loss", "Self_Loathing", CausalRelationType.CAUSES)
    engine.add_link("Grief_of_Loss", "Anger_at_World", CausalRelationType.CAUSES)
    
    # 3. Trace the "Narrative Arc"
    logger.info("   ... Tracing the Sorrowful Path ...")
    
    # We want to see if we can get from "Winter_Night" to "Self_Loathing"
    chain = engine.find_path("Winter_Night", "Self_Loathing")
    
    if chain:
        logger.info("   ✅ Narrative Chain Found:")
        for node in chain.node_sequence:
            logger.info(f"     -> {node}")
            
        # Verify the Contrast Step exists in the logic
        has_contrast = False
        for link in chain.links:
            if link.relation == CausalRelationType.CONTRASTS_WITH or link.relation == CausalRelationType.ASSOCIATED_WITH:
                has_contrast = True
        
        if has_contrast:
             logger.info("   ✅ The system understands that 'Memory' and 'Contrast' drove this emotion, not just cold.")
        else:
             logger.warning("   ⚠️ Chain found but might be too direct (missing the contrast nuance).")
             
    else:
        logger.error("   ❌ Failed to connect Winter to Self-Loathing.")
        
    # 4. Synthesize Story
    logger.info("   ... Synthesizing Narrative ...")
    if chain:
        story = engine.synthesize_narrative(chain)
        logger.info(f"   📜 Story: {story}")

if __name__ == "__main__":
    test_homeless_narrative()
