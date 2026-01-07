"""
MindMitosis (정신 분열/통합)
==========================

"I am Legion, for we are many."

This module allows Elysia to spawn parallel consciousness threads (Personas)
to debate, simulate, or solve problems from different perspectives.
"""

import subprocess
import sys
import os
import time
import logging
import shutil
from typing import Dict, List, Optional
from Core.Foundation.synapse_bridge import SynapseBridge
from Core.Foundation.persona_templates import PersonaFactory

logger = logging.getLogger("MindMitosis")

class MindMitosis:
    def __init__(self):
        self.active_personas: Dict[str, subprocess.Popen] = {}
        self.synapse = SynapseBridge("Orchestrator") # Temporary connection to check status
        logger.info("🕸️ Mind Mitosis Active. Ready to weave threads.")

    def spawn_persona(self, name: str, goal: str = None) -> bool:
        """
        Spawns a new Persona as a subprocess.
        If name matches a Template (e.g. "Scholar"), it uses that template.
        """
        if name in self.active_personas:
            logger.warning(f"Persona '{name}' is already active.")
            return False

        # Get Template
        template = PersonaFactory.get_template(name)
        final_goal = goal if goal else template["goal"]
        
        logger.info(f"🕸️ Spawning Persona: {name} (Role: {template['description']})")
        logger.info(f"   🎯 Goal: {final_goal}")
        
        try:
            # We run the SAME living_elysia.py but with arguments
            # python living_elysia.py [PersonaName] [Goal]
            
            cmd = [sys.executable, "living_elysia.py", name, final_goal]
            
            # Launch as independent process
            process = subprocess.Popen(
                cmd,
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NEW_CONSOLE # Windows specific: New window
            )
            
            self.active_personas[name] = process
            return True
            
        except Exception as e:
            logger.error(f"Failed to spawn persona '{name}': {e}")
            return False

    def merge_persona(self, name: str) -> List[str]:
        """
        Terminates a Persona and retrieves its insights from the Synapse.
        """
        if name not in self.active_personas:
            return []
            
        logger.info(f"🕸️ Merging Persona: {name}...")
        
        # 1. Kill Process
        process = self.active_personas[name]
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            
        del self.active_personas[name]
        
        # 2. Harvest Insights
        # We read the Synapse for messages FROM this persona
        insights = []
        all_signals = self.synapse.read_all_history() # We need a method to read history
        
        for signal in all_signals:
            if signal['source'] == name and signal['type'] == "INSIGHT":
                insights.append(signal['payload'])
                
        logger.info(f"   ✨ Absorbed {len(insights)} insights from {name}.")
        return insights

    def kill_all(self):
        """Emergency cleanup."""
        for name, process in self.active_personas.items():
            process.kill()
        self.active_personas.clear()
