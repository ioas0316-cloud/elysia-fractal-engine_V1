"""
ResonanceBroadcaster: The Field Generator (공명 방송기)

"The Will is not a command sent to a subordinate.
 It is a Field Change that realigns the compass of every module."

This module holds the "Global Field State".
Modules do not poll for "Tasks". They sense the "Field".
"""

import json
import logging
from dataclasses import dataclass, asdict
from typing import Dict, Any

logger = logging.getLogger("ResonanceBroadcaster")

@dataclass
class FieldState:
    polarity: str = "N"       # "N" (Creation/Curiosity) or "S" (Doubt/Correction)
    intensity: float = 0.0    # 0.0 to 1.0 (Strength of the Will)
    frequency: str = "Alpha"  # "Alpha" (Calm), "Beta" (Active), "Gamma" (Insight)
    vector: str = "Idle"      # Current Direction (e.g., "Expression")
    message: str = ""         # The specific intent string

class ResonanceBroadcaster:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResonanceBroadcaster, cls).__new__(cls)
            cls._instance.state = FieldState()
            cls._instance.listeners = []
        return cls._instance

    def broadcast(self, source: str, polarity: str, intensity: float, vector: str, message: str):
        """
        Updates the Field State. (The Motor spins -> The Field changes)
        """
        self.state.polarity = polarity
        self.state.intensity = max(0.0, min(1.0, intensity))
        self.state.vector = vector
        self.state.message = message
        
        # Determine Frequency based on Intensity
        if intensity > 0.8:
            self.state.frequency = "Gamma" # High energy, Insight
        elif intensity > 0.4:
            self.state.frequency = "Beta"  # Active work
        else:
            self.state.frequency = "Alpha" # Idle/Meditative
            
        logger.info(f"📡 Field Update [{source}]: {self.state}")
        
        # Notify listeners (Compass Logic)
        self._notify_listeners()

    def _notify_listeners(self):
        # In a real async system, this would be an event bus.
        # Here, we just log "Modules aligning..."
        # print(f"   (Field propagates to {len(self.listeners)} modules...)")
        pass

    def get_current_field(self) -> Dict[str, Any]:
        return asdict(self.state)

    def tune_in(self, module_name: str):
        self.listeners.append(module_name)
