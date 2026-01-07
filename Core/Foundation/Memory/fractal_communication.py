"""
Fractal Communication Protocol (프랙탈 통신 프로토콜)
================================================

"데이터를 주고받지 말고, 상태를 공유하라"
"Don't exchange data, share states"

Extension of Fractal Quantization to transmission and communication:
1. Send causes (formulas), not results (data)
2. Synchronize states (resonance), not exchange packets (ping-pong)
3. Transmit deltas (changes), not full states

Philosophy:
"만류귀종(萬流歸宗) - All streams return to one source"
"하나를 알면 열을 안다 - Know one, understand ten"
"""

import logging
import json
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.Foundation.fractal_quantization import PatternDNA, FractalQuantizer

logger = logging.getLogger("FractalCommunication")


@dataclass
class StateDelta:
    """
    상태 변화 (State Delta)
    
    Instead of sending full states, send only what changed.
    The receiver reconstructs the new state from the delta.
    
    Attributes:
        timestamp: When the change occurred
        changed_parameters: Dictionary of parameter changes
        resonance_shift: How the resonance fingerprint changed
        compression_ratio: How much bandwidth saved
    """
    timestamp: float
    changed_parameters: Dict[str, Any]
    resonance_shift: Optional[Dict[str, float]] = None
    compression_ratio: float = 1.0
    
    def to_dict(self) -> Dict:
        """Serialize for transmission."""
        return {
            "timestamp": self.timestamp,
            "changed_parameters": self.changed_parameters,
            "resonance_shift": self.resonance_shift,
            "compression_ratio": self.compression_ratio
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'StateDelta':
        """Deserialize from transmission."""
        return StateDelta(
            timestamp=data["timestamp"],
            changed_parameters=data["changed_parameters"],
            resonance_shift=data.get("resonance_shift"),
            compression_ratio=data.get("compression_ratio", 1.0)
        )


@dataclass
class ResonanceLink:
    """
    공명 링크 (Resonance Link)
    
    A shared state connection between two entities.
    When one changes, the other synchronizes automatically.
    
    Attributes:
        link_id: Unique identifier for this link
        shared_formula: The common pattern formula both entities use
        local_state: Local copy of the state
        remote_fingerprint: Last known remote resonance fingerprint
        sync_threshold: Minimum change to trigger sync
    """
    link_id: str
    shared_formula: Dict[str, Any]
    local_state: Dict[str, Any] = field(default_factory=dict)
    remote_fingerprint: Optional[Dict[str, float]] = None
    sync_threshold: float = 0.01
    last_sync: float = 0.0
    
    def needs_sync(self, new_state: Dict[str, Any]) -> bool:
        """Check if state change is significant enough to sync."""
        if not self.local_state:
            return True
        
        # Calculate state difference
        diff_magnitude = 0.0
        for key, value in new_state.items():
            if key in self.local_state:
                if isinstance(value, (int, float)):
                    old_val = self.local_state.get(key, 0)
                    diff_magnitude += abs(value - old_val)
        
        return diff_magnitude > self.sync_threshold


class FractalTransmitter:
    """
    프랙탈 전송기 (Fractal Transmitter)
    
    Implements "send the cause, not the result" principle.
    
    Traditional: Send 1GB movie file
    Fractal: Send tiny seed formula, receiver generates the movie
    """
    
    def __init__(self):
        self.quantizer = FractalQuantizer()
        logger.info("📡 Fractal Transmitter initialized")
    
    def prepare_transmission(self, data: Dict, pattern_type: str, pattern_name: str) -> PatternDNA:
        """
        Prepare data for transmission by converting to Pattern DNA.
        
        This is the revolution: Instead of sending the full data,
        we send just the seed that can regenerate it.
        
        Args:
            data: The data to transmit
            pattern_type: Type of pattern
            pattern_name: Name of pattern
            
        Returns:
            PatternDNA: The compressed seed for transmission
        """
        logger.info(f"📡 Preparing transmission: {pattern_type}.{pattern_name}")
        
        # Fold data into Pattern DNA
        dna = self.quantizer.fold(data, pattern_type, pattern_name)
        
        # Calculate bandwidth savings
        original_size = len(json.dumps(data).encode('utf-8'))
        seed_size = len(json.dumps(dna.to_dict()).encode('utf-8'))
        bandwidth_saved = (1 - seed_size / original_size) * 100
        
        logger.info(f"   ✓ Transmission prepared: {seed_size} bytes (saved {bandwidth_saved:.1f}% bandwidth)")
        
        return dna
    
    def transmit_seed(self, dna: PatternDNA) -> str:
        """
        Transmit the Pattern DNA seed.
        
        In a real implementation, this would send over network.
        Returns a JSON string for transmission.
        
        Args:
            dna: Pattern DNA to transmit
            
        Returns:
            str: JSON-encoded transmission packet
        """
        packet = {
            "type": "pattern_dna",
            "timestamp": time.time(),
            "payload": dna.to_dict(),
            "protocol": "fractal_v1"
        }
        
        transmission_data = json.dumps(packet)
        logger.info(f"📤 Transmitted: {len(transmission_data)} bytes")
        
        return transmission_data
    
    def receive_and_unfold(self, transmission: str, resolution: int = 100) -> Dict:
        """
        Receive a transmission and unfold the seed.
        
        The receiver regenerates the full data from the seed.
        This is lossless and resolution-independent.
        
        Args:
            transmission: JSON-encoded transmission packet
            resolution: Resolution for unfolding
            
        Returns:
            Dict: Unfolded data
        """
        logger.info("📥 Receiving transmission...")
        
        # Parse transmission
        packet = json.loads(transmission)
        
        if packet["type"] != "pattern_dna":
            raise ValueError(f"Unknown packet type: {packet['type']}")
        
        # Reconstruct Pattern DNA
        dna = PatternDNA.from_dict(packet["payload"])
        
        # Unfold to full data
        restored = self.quantizer.unfold(dna, resolution=resolution)
        
        logger.info(f"   ✓ Reception complete: Unfolded at resolution {resolution}")
        
        return restored


class StateSynchronizer:
    """
    상태 동기화기 (State Synchronizer)
    
    Implements "synchronization, not exchange" principle.
    
    Traditional: Send full state repeatedly (wasteful)
    Fractal: Share formula once, then sync only deltas (efficient)
    """
    
    def __init__(self):
        self.active_links: Dict[str, ResonanceLink] = {}
        logger.info("🔗 State Synchronizer initialized")
    
    def create_link(self, link_id: str, shared_formula: Dict[str, Any]) -> ResonanceLink:
        """
        Create a resonance link between two entities.
        
        Args:
            link_id: Unique identifier
            shared_formula: The pattern formula both entities will use
            
        Returns:
            ResonanceLink: The created link
        """
        link = ResonanceLink(
            link_id=link_id,
            shared_formula=shared_formula,
            last_sync=time.time()
        )
        
        self.active_links[link_id] = link
        logger.info(f"🔗 Created resonance link: {link_id}")
        
        return link
    
    def compute_delta(self, link_id: str, new_state: Dict[str, Any]) -> Optional[StateDelta]:
        """
        Compute the delta (change) in state.
        
        This is much smaller than sending the full state.
        
        Args:
            link_id: Link identifier
            new_state: New state to sync
            
        Returns:
            StateDelta or None if no sync needed
        """
        if link_id not in self.active_links:
            raise ValueError(f"Unknown link: {link_id}")
        
        link = self.active_links[link_id]
        
        # Check if sync is needed
        if not link.needs_sync(new_state):
            logger.debug(f"   Sync not needed for {link_id} (below threshold)")
            return None
        
        # Compute what changed
        changed_params = {}
        for key, value in new_state.items():
            if key not in link.local_state or link.local_state[key] != value:
                changed_params[key] = value
        
        # Calculate compression
        full_state_size = len(json.dumps(new_state).encode('utf-8'))
        delta_size = len(json.dumps(changed_params).encode('utf-8'))
        compression_ratio = full_state_size / delta_size if delta_size > 0 else 1.0
        
        delta = StateDelta(
            timestamp=time.time(),
            changed_parameters=changed_params,
            compression_ratio=compression_ratio
        )
        
        logger.info(f"📊 Delta computed: {len(changed_params)} parameters changed")
        logger.info(f"   Bandwidth saved: {compression_ratio:.2f}x")
        
        return delta
    
    def apply_delta(self, link_id: str, delta: StateDelta) -> Dict[str, Any]:
        """
        Apply a received delta to local state.
        
        This reconstructs the new state from the delta.
        
        Args:
            link_id: Link identifier
            delta: The state delta to apply
            
        Returns:
            Dict: The updated state
        """
        if link_id not in self.active_links:
            raise ValueError(f"Unknown link: {link_id}")
        
        link = self.active_links[link_id]
        
        # Apply changes
        for key, value in delta.changed_parameters.items():
            link.local_state[key] = value
        
        link.last_sync = delta.timestamp
        
        logger.info(f"✓ Delta applied to {link_id}")
        
        return link.local_state.copy()
    
    def transmit_delta(self, delta: StateDelta) -> str:
        """
        Transmit a state delta.
        
        Args:
            delta: The delta to transmit
            
        Returns:
            str: JSON-encoded transmission
        """
        packet = {
            "type": "state_delta",
            "timestamp": time.time(),
            "payload": delta.to_dict(),
            "protocol": "fractal_sync_v1"
        }
        
        transmission = json.dumps(packet)
        logger.info(f"📤 Transmitted delta: {len(transmission)} bytes")
        
        return transmission
    
    def receive_delta(self, transmission: str) -> StateDelta:
        """
        Receive a delta transmission.
        
        Args:
            transmission: JSON-encoded transmission
            
        Returns:
            StateDelta: The received delta
        """
        packet = json.loads(transmission)
        
        if packet["type"] != "state_delta":
            raise ValueError(f"Unknown packet type: {packet['type']}")
        
        delta = StateDelta.from_dict(packet["payload"])
        logger.info(f"📥 Received delta: {len(delta.changed_parameters)} parameters")
        
        return delta


class ResonanceCommunicator:
    """
    공명 통신기 (Resonance Communicator)
    
    Implements quantum-like entanglement for communication.
    
    Traditional: A sends message → B receives → B sends reply → A receives
    Fractal: A and B share a wave function; changes propagate instantly
    
    This is the ultimate form: Not even deltas, just shared state evolution.
    """
    
    def __init__(self):
        self.shared_states: Dict[str, Dict[str, Any]] = {}
        self.state_hashes: Dict[str, str] = {}
        logger.info("🌊 Resonance Communicator initialized")
    
    def entangle(self, channel_id: str, initial_state: Dict[str, Any]):
        """
        Create an entangled communication channel.
        
        Both parties share the same wave function.
        Changes in one's state automatically affect the other.
        
        Args:
            channel_id: Unique channel identifier
            initial_state: Initial shared state
        """
        self.shared_states[channel_id] = initial_state.copy()
        self.state_hashes[channel_id] = self._hash_state(initial_state)
        
        logger.info(f"🌊 Channel {channel_id} entangled")
        logger.info(f"   Initial state hash: {self.state_hashes[channel_id][:8]}...")
    
    def _hash_state(self, state: Dict[str, Any]) -> str:
        """Generate a hash of the state for change detection."""
        state_json = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_json.encode()).hexdigest()
    
    def modulate(self, channel_id: str, parameter: str, value: Any) -> bool:
        """
        Modulate a parameter in the shared state.
        
        This is like changing one variable in a shared wave function.
        The change propagates to all entangled parties.
        
        Args:
            channel_id: Channel to modulate
            parameter: Parameter name to change
            value: New value
            
        Returns:
            bool: True if modulation caused state change
        """
        if channel_id not in self.shared_states:
            raise ValueError(f"Channel {channel_id} not entangled")
        
        old_hash = self.state_hashes[channel_id]
        
        # Apply modulation
        self.shared_states[channel_id][parameter] = value
        
        new_hash = self._hash_state(self.shared_states[channel_id])
        self.state_hashes[channel_id] = new_hash
        
        if old_hash != new_hash:
            logger.info(f"🌊 Modulation: {channel_id}.{parameter} = {value}")
            logger.info(f"   State resonance shifted")
            return True
        
        return False
    
    def observe(self, channel_id: str) -> Dict[str, Any]:
        """
        Observe the current state of an entangled channel.
        
        Args:
            channel_id: Channel to observe
            
        Returns:
            Dict: Current shared state
        """
        if channel_id not in self.shared_states:
            raise ValueError(f"Channel {channel_id} not entangled")
        
        return self.shared_states[channel_id].copy()
    
    def detect_resonance(self, channel_id: str, other_state: Dict[str, Any]) -> float:
        """
        Detect resonance between local and remote states.
        
        Returns a similarity score (0.0 = completely different, 1.0 = identical)
        
        Args:
            channel_id: Channel to check
            other_state: Remote state to compare
            
        Returns:
            float: Resonance score
        """
        if channel_id not in self.shared_states:
            return 0.0
        
        local = self.shared_states[channel_id]
        
        # Simple similarity metric
        matching_keys = 0
        matching_values = 0
        total_keys = len(set(local.keys()) | set(other_state.keys()))
        
        for key in local.keys():
            if key in other_state:
                matching_keys += 1
                if local[key] == other_state[key]:
                    matching_values += 1
        
        if total_keys == 0:
            return 1.0
        
        resonance = matching_values / total_keys
        
        logger.info(f"🌊 Resonance detected: {resonance:.2%}")
        
        return resonance


# Test and demonstration
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("="*70)
    print("🌊 FRACTAL COMMUNICATION PROTOCOL TEST")
    print("="*70)
    print()
    
    print("TEST 1: Seed Transmission (Send causes, not results)")
    print("-"*70)
    
    transmitter = FractalTransmitter()
    
    # Original data to transmit
    video_metadata = {
        "emotion": "joy",
        "intensity": 0.9,
        "context": "8K video content",
        "duration": 3600.0,  # 1 hour video
        "phase_seed": 0.618
    }
    
    print(f"Original data size: ~{len(json.dumps(video_metadata))} bytes")
    print("(In reality, 1 hour 8K video = multiple GB)")
    
    # Prepare for transmission (compress to seed)
    dna = transmitter.prepare_transmission(video_metadata, "emotion", "joy")
    transmission = transmitter.transmit_seed(dna)
    
    print(f"Transmitted: {len(transmission)} bytes (just the seed!)")
    print()
    
    # Receiver unfolds the seed
    restored = transmitter.receive_and_unfold(transmission, resolution=100)
    print(f"Receiver generated: Full content at resolution {len(restored['waveform'][0]['wave'])}")
    print()
    
    print("="*70)
    print("TEST 2: Delta Synchronization (Sync states, not exchange packets)")
    print("-"*70)
    
    synchronizer = StateSynchronizer()
    
    # Create a link
    link = synchronizer.create_link("link_001", {"formula": "Z^2 + C"})
    
    # Initial state
    initial_state = {
        "x": 1.0,
        "y": 2.0,
        "z": 3.0,
        "intensity": 0.5
    }
    
    # Update state (only change one parameter)
    new_state = initial_state.copy()
    new_state["x"] = 1.1  # Only x changed!
    
    # Compute delta
    delta = synchronizer.compute_delta("link_001", new_state)
    
    if delta:
        print(f"Changed parameters: {list(delta.changed_parameters.keys())}")
        print(f"Bandwidth saved: {delta.compression_ratio:.2f}x")
        
        # Transmit delta
        delta_transmission = synchronizer.transmit_delta(delta)
        print(f"Delta transmitted: {len(delta_transmission)} bytes")
        print()
        
        # Receiver applies delta
        updated_state = synchronizer.apply_delta("link_001", delta)
        print(f"Synchronized state: {updated_state}")
    print()
    
    print("="*70)
    print("TEST 3: Resonance Communication (Entangled states)")
    print("-"*70)
    
    communicator = ResonanceCommunicator()
    
    # Entangle a channel
    communicator.entangle("quantum_link", {"wave": "psi", "energy": 100.0})
    
    # Party A modulates the shared state
    print("Party A modulates: energy = 120.0")
    changed = communicator.modulate("quantum_link", "energy", 120.0)
    
    if changed:
        print("✓ State resonance shifted")
        
        # Party B observes the change
        state = communicator.observe("quantum_link")
        print(f"Party B observes: {state}")
    
    print()
    print("="*70)
    print("✅ FRACTAL COMMUNICATION PROTOCOL OPERATIONAL")
    print("   📡 Transmission: Send seeds, not data")
    print("   🔗 Synchronization: Send deltas, not full states")
    print("   🌊 Resonance: Share states, don't exchange packets")
    print("="*70)
