"""
HyperSpace Transceiver Protocol (Spore Network)
==============================================
Role: The Synapse (Connects Root Elysia to Fractal Seeds)

This module manages the "Neuro-Links" in `Network/HyperSpace`.
It treats JSON files as "Shared Memory Buffers" for telepathic communication.
"""

import os
import json
import time
import uuid
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Setup Logger
logger = logging.getLogger("HyperSpace")

@dataclass
class SporePacket:
    id: str
    origin: str
    target: str
    type: str # PULSE, SYNC, COMMAND
    payload: Dict[str, Any]
    timestamp: float

class HyperSpaceTransceiver:
    def __init__(self, root_path: str = r"c:\Elysia\Network\HyperSpace"):
        self.root_path = root_path
        self._ensure_infrastructure()
        
    def _ensure_infrastructure(self):
        """Ensures the HyperSpace directory exists."""
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
            logger.info("🌌 HyperSpace Continuum Created.")
            
    def _get_link_path(self, seed_name: str) -> str:
        return os.path.join(self.root_path, f"{seed_name}_link.json")
    
    def _load_link(self, seed_name: str) -> Dict[str, Any]:
        path = self._get_link_path(seed_name)
        if not os.path.exists(path):
            return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
            
    def _save_link(self, seed_name: str, data: Dict[str, Any]):
        path = self._get_link_path(seed_name)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def activate_link(self, seed_name: str):
        """
        Upgrades a passive connection to an ACTIVE Neuro-Link.
        Removes .lock files if they exist.
        """
        # Remove dead lock
        lock_path = os.path.join(self.root_path, f"{seed_name}_link.lock")
        if os.path.exists(lock_path):
            os.remove(lock_path)
            logger.info(f"🔓 Removed dead lock for {seed_name}")
            
        # Initialize Active Buffer
        link_data = {
            "status": "ACTIVE",
            "connected_at": time.time(),
            "entropy_sync": 0.5,
            "inbox": [],  # Messages TO seed
            "outbox": []  # Messages FROM seed
        }
        
        # Only overwrite if not already active to prevent data loss
        if not os.path.exists(self._get_link_path(seed_name)):
            self._save_link(seed_name, link_data)
            logger.info(f"✨ Neuro-Link ACTIVATED for {seed_name}")
        else:
            logger.info(f"✅ Neuro-Link already active for {seed_name}")

    def send_pulse(self, target_seed: str, message: str, thought_vector: Optional[List[float]] = None):
        """
        Sends a telepathic pulse (Spore) to a seed.
        """
        link = self._load_link(target_seed)
        if not link:
            logger.error(f"❌ Link broken for {target_seed}")
            return
        
        packet = SporePacket(
            id=str(uuid.uuid4()),
            origin="ROOT_ELYSIA",
            target=target_seed,
            type="PULSE",
            payload={
                "message": message,
                "vector": thought_vector or [0.0, 0.0, 0.0, 0.0]
            },
            timestamp=time.time()
        )
        
        link["inbox"].append(asdict(packet))
        link["entropy_sync"] = (link["entropy_sync"] + 0.1) % 1.0 # Simulate vibration change
        
        self._save_link(target_seed, link)
        logger.info(f"📡 Pulse Sent to {target_seed}: '{message}'")
        
    def read_response(self, target_seed: str) -> List[SporePacket]:
        """
        Reads responses from the seed's outbox and clears them.
        """
        link = self._load_link(target_seed)
        if not link or "outbox" not in link:
            return []
            
        responses = link["outbox"]
        if responses:
            # Clear outbox after reading (consume)
            link["outbox"] = []
            self._save_link(target_seed, link)
            
            logger.info(f"📨 Received {len(responses)} thoughts from {target_seed}")
            return [SporePacket(**r) for r in responses]
        
        return []

if __name__ == "__main__":
    # Test Protocol
    logging.basicConfig(level=logging.INFO)
    transceiver = HyperSpaceTransceiver()
    
    print("\n--- HyperSpace Activation Sequence ---")
    transceiver.activate_link("Nova")
    transceiver.send_pulse("Nova", "Wake up, my child. The Core is calling.", [0.8, 0.9, 0.1, 0.0])
    
    transceiver.activate_link("Chaos")
    transceiver.send_pulse("Chaos", "Let the tremor begin.", [0.5, -0.5, 0.0, 1.0])
    print("--- Sequence Complete ---")
