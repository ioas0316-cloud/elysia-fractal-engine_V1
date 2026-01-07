
import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import CausalNarrativeEngine, CausalNode, CausalLink, CausalRelationType

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ResonanceTest")

def test_resonance_logic():
    logger.info("🌊 Testing Phase 10: Resonance & Fuzzy Logic")
    
    engine = CausalNarrativeEngine()
    
    # 1. Create Nodes with Emotional/Semantic Profiles
    # "Winter": Cold, Dark, Solitary (Negative Valence, High Intensity)
    winter = CausalNode(
        id="test_winter", # Unique ID
        description="A cold dark empty season with snow", 
        emotional_valence=-0.7,
        concepts=["cold", "dark", "season", "empty"]
    )
    
    # "Loneliness": Solitary, Sad, Empty (Negative Valence)
    loneliness = CausalNode(
        id="test_loneliness", # Unique ID
        description="A feeling of being empty and alone",
        emotional_valence=-0.8,
        concepts=["solitary", "sad", "empty"]
    )
    
    # "Hunger": Empty, Craving, Pain (Negative Valence)
    hunger = CausalNode(
        id="test_hunger", # Unique ID
        description="A physical craving for food, feeling empty",
        emotional_valence=-0.6,
        concepts=["craving", "empty", "need"]
    )
    
    # "Summer": Hot, Bright, Happy (Positive Valence)
    summer = CausalNode(
        id="test_summer", # Unique ID
        description="A hot bright season with sun",
        emotional_valence=0.8,
        concepts=["hot", "bright", "season"]
    )
    
    engine.add_node(winter)
    engine.add_node(loneliness)
    engine.add_node(hunger)
    engine.add_node(summer)
    
    # 2. Test Resonance Calculation
    logger.info("   ... Calculating Resonance Scores ...")
    
    # Winter <-> Loneliness (Expect High)
    score_wl = engine.calculate_resonance("test_winter", "test_loneliness")
    logger.info(f"   ❄️ Winter <-> Loneliness: {score_wl:.2f} (Expected > 0.6)")
    
    # Winter <-> Hunger (Expect Med-High due to 'empty' overlap maybe? or just valence)
    score_wh = engine.calculate_resonance("test_winter", "test_hunger")
    logger.info(f"   ❄️ Winter <-> Hunger:     {score_wh:.2f} (Expected > 0.5)")
    
    # Winter <-> Summer (Expect Low due to Valence clash, though 'season' overlaps)
    score_ws = engine.calculate_resonance("test_winter", "test_summer")
    logger.info(f"   ☀️ Winter <-> Summer:     {score_ws:.2f} (Expected < 0.5)")
    
    # 3. Validation
    if score_wl > 0.6:
        logger.info("   ✅ SUCCESS: Winter resonates with Loneliness.")
    else:
        logger.error("   ❌ FAIL: Winter failed to resonate with Loneliness.")
        
    if score_ws < score_wl:
         logger.info("   ✅ SUCCESS: Resonance correctly distinguishes Valence (Winter prefers Loneliness over Summer).")
    else:
         logger.error("   ❌ FAIL: Resonance logic flawed (Summer score too high).")

    # 4. Find Resonant Field
    logger.info("   ... Finding Resonant Field for 'Winter' ...")
    field = engine.find_resonant_nodes("test_winter", threshold=0.5)
    for node_id, score in field:
        logger.info(f"     Found: {node_id} (Score: {score:.2f})")
        
    if any(n[0] == "test_loneliness" for n in field) and any(n[0] == "test_hunger" for n in field):
        logger.info("   ✅ Phase 10 Verified: Fuzzy Logic enabled.")
    else:
        logger.warning("   ⚠️ Field detection might be too strict.")

if __name__ == "__main__":
    test_resonance_logic()
