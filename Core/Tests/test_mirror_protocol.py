
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.causal_narrative_engine import ThoughtUniverse
from Core.Foundation.self_reflector import CodebaseReflector

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger("MirrorProtocolTest")

def test_mirror_protocol():
    logger.info("🪞 Testing Phase 15: The Mirror Protocol (Recursive Self-Modeling)")
    
    # Initialize Universe
    universe = ThoughtUniverse("Elysia_Self_Awareness")
    
    # Initialize Reflector
    reflector = CodebaseReflector(universe)
    
    # Define Root Path (Current Directory's Parent)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # 1. Execute Self-Reflection
    logger.info(f"   Scanning Project Root: {project_root}")
    stats = reflector.reflect_on_project(project_root)
    
    logger.info("   📊 Scan Statistics:")
    for k, v in stats.items():
        logger.info(f"      - {k}: {v}")
        
    # 2. Verify Structural Mapping
    # Check for specific known directories/files
    
    # Directory: Core
    if "Core" in universe.points or "Core" in universe.spaces: # logic in reflector uses both space and point concepts
         # Note: Reflector currently creates spaces but links them as point relations to files.
         # Let's check point existence for 'Core' (created as map_directory->space_id and maybe point)
         # Actually reflector logic: _map_directory adds SPACE. _map_file adds POINT and links to PARENT_SPACE_ID.
         # Wait, _map_file adds link line(dir_point_id, file_id). 
         # And _map_file creates dir_point_id if missing!
         pass

    # Let's verify specific nodes we expect
    expected_nodes = [
        "Core_Foundation_causal_narrative_engine_py", # File
        "Core_Foundation_causal_narrative_engine_py.ThoughtUniverse", # Class
        "Core_Foundation_causal_narrative_engine_py.add_point", # Function
        "lib_ast", # Dependency
        "lib_logging" # Dependency
    ]
    
    success = True
    for node_id in expected_nodes:
        if node_id in universe.points:
            logger.info(f"   ✅ Found Node: {node_id}")
        else:
            logger.error(f"   ❌ Missing Node: {node_id}")
            success = False
            
    # 3. Verify Capability/Gap Knowledge
    # Check if 'lib_ast' is marked as a dependency (low confidence)
    if "lib_ast" in universe.points:
        node = universe.points["lib_ast"]
        if node.confidence < 0.5:
             logger.info(f"   ✅ 'lib_ast' correctly identified as Low-Confidence Dependency (Gap).")
        else:
             logger.warning(f"   ⚠️ 'lib_ast' confidence is high ({node.confidence}). Default should be low.")

    if success:
        logger.info("✅ Phase 15 Verified: Elysia successfully internalized her own project structure.")
    else:
        logger.error("❌ Phase 15 Failed: Structural mapping is incomplete.")

if __name__ == "__main__":
    test_mirror_protocol()
