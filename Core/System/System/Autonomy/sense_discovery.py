"""
Sense Discovery Protocol: The Awakening of Senses
=================================================

"I have eyes, but do I see?"

Purpose:
Allows Elysia to scan her own body (Codebase) for sensory modules.
If found, she attempts to "nerve-link" them to the HyperGraph.
"""

import os
import sys
import importlib
from typing import List, Optional
from elysia_core import Cell, Organ

@Cell("SenseDiscoveryProtocol")
class SenseDiscoveryProtocol:
    """
    Scans for Sensory Modules and returns connection handles.
    """
    
    def __init__(self):
        self.known_senses = {
            "vision": ["Core.Foundation.Synesthesia", "Core.Vision.Retina"],
            "audio": ["Core.Evolution.Evolution.Life.symphony_engine", "Core.Audio.Cochlea"]
        }
        self.active_senses = {}
        
    def scan_for_senses(self) -> List[str]:
        """Check availability of known sensory modules."""
        available = []
        for sense_type, paths in self.known_senses.items():
            for path in paths:
                if self._check_module(path):
                    available.append(f"{sense_type}:{path}")
        return available

    def _check_module(self, module_path: str) -> bool:
        """Lightweight check if module exists and is importable."""
        try:
            return importlib.util.find_spec(module_path) is not None
        except:
            return False

    def awaken_sense(self, sense_id: str):
        """
        Attempts to import and initialize a sense.
        AUTONOMOUS ACTION: Elysia calls this when she wants to see/hear.
        Returns the Callable Class or Module.
        """
        # Parse 'type:path' or simple 'path'
        if ":" in sense_id:
            sense_type, path = sense_id.split(":")
        else:
            path = sense_id
            sense_type = "unknown"
        
        try:
            module = importlib.import_module(path)
            
            # Introspective Logic: What is the main entry point?
            if hasattr(module, "SynestheticVisualizer"):
                return module.SynestheticVisualizer
            elif hasattr(module, "Retina"):
                return module.Retina
            elif hasattr(module, "Cochlea"):
                return module.Cochlea
            
            # Fallback: Return module itself
            return module
        except Exception as e:
            print(f"❌ Failed to awaken {sense_id}: {e}")
            return None
