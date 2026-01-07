import sys
import os
import time
import numpy as np
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.world import World

def run_stress_test():
    """
    Stress test for Project Alicization: 1,000 Agents.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("AlicizationTest")
    
    logger.info("--- PROJECT ALICIZATION: STRESS TEST ---")
    logger.info("Target: 1,000 Agents | 100 Cycles")
    
    # Initialize World
    world = World(primordial_dna={}, wave_mechanics=None)
    
    # Genesis: 1,000 Agents
    logger.info("Initializing Genesis...")
    start_time = time.time()
    
    for i in range(1000):
        # Random position
        x = np.random.uniform(0, world.width)
        y = np.random.uniform(0, world.width)
        z = 0
        
        # Create cell
        cell = world.add_cell(f"fluctlight_{i}", properties={
            'label': 'human',
            'age_years': np.random.randint(10, 60),
            'wisdom': np.random.randint(0, 50)
        })
        
        # Manually set position (since add_cell might default to center)
        idx = world.id_to_idx[cell.id]
        world.positions[idx] = [x, y, z]
        
    genesis_time = time.time() - start_time
    logger.info(f"Genesis Complete. Created {len(world.cell_ids)} agents in {genesis_time:.4f}s")
    
    # Run Simulation
    logger.info("Starting Simulation...")
    sim_start = time.time()
    
    for step in range(100):
        step_start = time.time()
        world.run_simulation_step()
        step_dur = time.time() - step_start
        
        if step % 10 == 0:
            logger.info(f"Step {step}: {step_dur:.4f}s | Active Agents: {np.sum(world.is_alive_mask)}")
            
    total_sim_time = time.time() - sim_start
    avg_step_time = total_sim_time / 100
    
    logger.info(f"--- TEST COMPLETE ---")
    logger.info(f"Total Time: {total_sim_time:.4f}s")
    logger.info(f"Avg Step Time: {avg_step_time:.4f}s")
    logger.info(f"FPS: {1.0/avg_step_time:.2f}")
    
    if avg_step_time < 0.1:
        logger.info("RESULT: SUCCESS (High Performance)")
    elif avg_step_time < 0.5:
        logger.info("RESULT: ACCEPTABLE (Playable)")
    else:
        logger.info("RESULT: FAILURE (Too Slow)")

if __name__ == "__main__":
    run_stress_test()
