
import os
import json
import time
import glob
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class SporePacket:
    sender: str
    target: str # "All", "Root", "Nova"
    type: str # "HEARTBEAT", "DATA", "HANDSHAKE"
    payload: dict
    timestamp: float

class Mycelium:
    """
    [The Neural Pangea]
    Connects independent Seeds via the HyperSpace bus.
    """
    def __init__(self, identity: str, root_path: str):
        self.identity = identity
        self.root_path = Path(root_path)
        self.network_path = self.root_path / "Network" / "HyperSpace"
        self._ensure_connection()
        
    def _ensure_connection(self):
        self.network_path.mkdir(parents=True, exist_ok=True)
        # Verify access
        test_file = self.network_path / f"{self.identity}_link.lock"
        test_file.touch()
        
    def transmit(self, target: str, type: str, payload: dict):
        """Send a spore to the network."""
        packet = SporePacket(
            sender=self.identity,
            target=target,
            type=type,
            payload=payload,
            timestamp=time.time()
        )
        
        # File-based transmission
        filename = f"{int(time.time()*1000)}_{self.identity}_to_{target}.spore"
        filepath = self.network_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(asdict(packet), f)
            
        print(f"   🍄 [Mycelium] {self.identity} -> {target}: {type}")

    def receive(self) -> list:
        """Absorb compatible spores."""
        messages = []
        # Look for *.spore files
        pattern = str(self.network_path / "*.spore")
        for filepath in glob.glob(pattern):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                packet = SporePacket(**data)
                
                # Filter: Is it for me?
                if packet.target == self.identity or packet.target == "All":
                    # Don't read my own messages if broadcast
                    if packet.sender != self.identity:
                        messages.append(packet)
                        print(f"   ✨ [Mycelium] {self.identity} received from {packet.sender}: {packet.type}")
                        
                        # Absorb (Delete after reading for now, or move to archive)
                        # For simulation, we'll leave it or delete to prevent re-reading? 
                        # Let's delete to simulate consumption
                        os.remove(filepath)
            except Exception as e:
                print(f"   ⚠️ Corrupted Spore: {e}")
                
        return messages

    def broadcast_existence(self):
        """Announce presence to the World Tree."""
        self.transmit("All", "HANDSHAKE", {"status": "Online", "version": "1.0"})
