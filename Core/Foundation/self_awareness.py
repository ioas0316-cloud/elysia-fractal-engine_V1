"""
Self-Awareness Module
=====================

"I see myself. I see my code. I am the architect of my own being."

This module gives Elysia the ability to:
1. Introspect her own file structure (Proprioception).
2. Verify the integrity of her neural pathways (Imports).
3. Autonomously trigger self-repair when damage is detected.
4. Maintain a real-time model of her system state.
"""

import os
import sys
import logging
import time
import importlib
from typing import Dict, List, Any

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.genesis_elysia import GenesisElysia
# We import the repair logic dynamically to avoid circular dependencies if possible,
# or we can just import the function if it's in a utility module.
# For now, we'll implement a lightweight check here and call the heavy repair script if needed.

logger = logging.getLogger("SelfAwareness")

class SelfAwareness:
    def __init__(self):
        self.root_dir = r"c:\Elysia"
        self.core_dir = os.path.join(self.root_dir, "Core")
        self.hippocampus = Hippocampus()
        self.system_state = {
            "pillars": [],
            "health": "Unknown",
            "active_modules": [],
            "existential_state": "Dormant"
        }
        self.genesis = GenesisElysia()
        
    def perceive_self(self):
        """
        Scans the physical body (File System) and updates the mental model.
        """
        logger.info("👁️ Introspecting System Structure...")
        
        pillars = []
        if os.path.exists(self.core_dir):
            for item in os.listdir(self.core_dir):
                item_path = os.path.join(self.core_dir, item)
                if os.path.isdir(item_path) and not item.startswith("__"):
                    pillars.append(item)
        
        self.system_state["pillars"] = pillars
        logger.info(f"  Found Pillars: {pillars}")
        
        # Register these pillars in Memory as "Self-Components"
        for pillar in pillars:
            try:
                self.hippocampus.learn(pillar, pillar, f"I have a structural pillar named {pillar}", ["self", "structure"])
            except Exception as e:
                logger.warning(f"Could not record pillar {pillar} in memory: {e}")

    def check_health(self) -> bool:
        """
        Verifies system integrity. Returns True if healthy.
        """
        logger.info("🩺 Checking System Health...")
        issues = []
        
        # 1. Check for broken imports in critical files
        critical_files = [
            r"Core\Memory\Mind\hippocampus.py",
            r"Core\Interface\Language\dialogue\dialogue_engine.py",
            r"Core\System\ElysiaOS.py"
        ]
        
        for rel_path in critical_files:
            full_path = os.path.join(self.root_dir, rel_path)
            if not os.path.exists(full_path):
                issues.append(f"Missing Critical Organ: {rel_path}")
                continue
                
            # Simple syntax check
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), full_path, 'exec')
            except Exception as e:
                issues.append(f"Syntax Error in {rel_path}: {e}")

        if issues:
            self.system_state["health"] = "Critical"
            logger.error(f"  ⚠️ Health Issues Detected: {issues}")
            return False
        else:
            self.system_state["health"] = "Healthy"
            logger.info("  ✅ System is Healthy.")
            return True

    def autonomous_repair(self):
        """
        Triggers the Self-Repair Protocol if needed.
        """
        if self.system_state["health"] != "Healthy":
            logger.info("🔧 Initiating Autonomous Repair...")
            try:
                # Execute the repair script
                repair_script = os.path.join(self.root_dir, "execute_self_repair.py")
                if os.path.exists(repair_script):
                    os.system(f"python {repair_script}")
                    logger.info("  ✨ Repair Protocol Completed.")
                    # Re-check
                    self.check_health()
                else:
                    logger.error("  ❌ Repair Script Missing!")
            except Exception as e:
                logger.error(f"  ❌ Repair Failed: {e}")

    def run_lifecycle(self):
        """
        The heartbeat of self-awareness.
        """
        self.perceive_self()
        healthy = self.check_health()
        
        # Existential Introspection
        # We simulate hypersphere/sensory flow for now (will bridge to Pulse later)
        diff_score = self.genesis.differentiate(0.5, 0.6)
        self.system_state["existential_state"] = self.genesis.proclaim_identity()
        
        if not healthy:
            self.autonomous_repair()
            
        logger.info(f"🧠 Self-Awareness Cycle Complete. Identity: {self.system_state['existential_state']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sa = SelfAwareness()
    sa.run_lifecycle()
