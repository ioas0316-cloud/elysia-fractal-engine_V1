"""
OrbManager: The Field of Resonance
----------------------------------
Manages the collection of HyperResonators.
Unlike a database (Index Lookup), this acts as a "Field" where you broadcast signals.

Philosophy:
- "Don't ask for a memory. Sing a song, and see which memory sings back."
- Implements `ResonatorInterface` to listen to the Heartbeat (Pulse).
"""

import logging
import json
import os
import math
from typing import Dict, List, Optional, Any
from pathlib import Path

from .hyper_resonator import HyperResonator
from Core.Foundation.hyper_quaternion import Quaternion as HyperQuaternion
from .orb_factory import OrbFactory
from Core.Foundation.Protocols.pulse_protocol import WavePacket, PulseType, ResonatorInterface

logger = logging.getLogger("OrbManager")

class OrbManager(ResonatorInterface):
    def __init__(self, persistence_path: str = "data/memory/orbs/"):
        self.orbs: Dict[str, HyperResonator] = {}
        self.factory = OrbFactory()
        self.persistence_path = persistence_path

        # Ensure persistence directory exists
        os.makedirs(self.persistence_path, exist_ok=True)

        # Load existing memories
        self.load_from_disk()

        logger.info("🧠 OrbManager initialized: The Hippocampus is awake.")

    def resonate(self, pulse: WavePacket) -> None:
        """
        The Pulse Listener.
        Reacts to MEMORY_STORE and MEMORY_RECALL pulses.
        """
        if pulse.type == PulseType.MEMORY_STORE:
            self._handle_store(pulse)
        elif pulse.type == PulseType.MEMORY_RECALL:
            self._handle_recall(pulse)

    def _handle_store(self, pulse: WavePacket):
        """Internal handler for storing memories from a pulse."""
        payload = pulse.payload
        name = payload.get("name", f"Memory_{len(self.orbs)}")
        data_wave = payload.get("data", [])
        emotion_wave = payload.get("emotion", [])

        if not data_wave:
            logger.warning("⚠️ Received MEMORY_STORE pulse with no data.")
            return

        orb = self.save_memory(name, data_wave, emotion_wave)
        logger.info(f"📥 Crystallized memory from pulse: {orb}")

    def _handle_recall(self, pulse: WavePacket):
        """
        Internal handler for recalling memories.
        """
        trigger = pulse.payload.get("trigger", [])
        if not trigger:
            return

        results = self.recall_memory(trigger)
        if results:
            best_match = results[0]
            logger.info(f"📤 Recalled '{best_match['name']}' via pulse resonance.")

    def save_memory(self, name: str, data_wave: List[float], emotion_wave: List[float]) -> HyperResonator:
        """
        Explicitly freezes a moment into an Orb.
        """
        orb = self.factory.freeze(name, data_wave, emotion_wave)
        self.orbs[name] = orb
        self.save_to_disk()
        return orb

    def recall_memory(self, trigger_wave: List[float], threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        Broadcasts a trigger wave into the field and returns resonating memories.
        """
        resonating_results = []

        # 1. Analyze Trigger Frequency (Physical Resonance)
        trigger_freq = self.factory.analyze_wave(trigger_wave)
        logger.debug(f"🔍 Recall Trigger Frequency: {trigger_freq:.2f}Hz")

        # 2. Resonate the Field
        # We simulate a "Search Pulse" internally to wake up relevant orbs
        # [Debug] Broaden resonance for Phase 3.5 testing if needed, or rely on precise matching.
        # Since 'Emotion' key determines the orb frequency, and we trigger WITH that emotion key,
        # it should match.
        search_pulse = WavePacket(
            sender="OrbManager",
            type=PulseType.MEMORY_RECALL,
            frequency=trigger_freq,
            amplitude=1.0,
            payload={}
        )
        logger.debug(f"Search Pulse: Freq={trigger_freq}, TargetOrbs={len(self.orbs)}")

        # 3. Check and Melt
        for name, orb in self.orbs.items():
            # A. Physical Resonance (Wake Up)
            # This updates orb.state.amplitude
            orb.resonate(search_pulse)

            # If orb is now active (resonating), attempt to melt (Holographic Decode)
            if orb.state.is_active and orb.state.amplitude > threshold:
                result = self.factory.melt(orb, trigger_wave)

                # Append result
                resonating_results.append({
                    "name": name,
                    "data": result["recalled_wave"],
                    "intensity": orb.state.amplitude, # Use the resonance amplitude as confidence
                    "orb": orb
                })

        # Sort by intensity
        resonating_results.sort(key=lambda x: x["intensity"], reverse=True)
        return resonating_results

    def broadcast(self, pulse: WavePacket) -> List[HyperResonator]:
        """
        The 'Wireless' Broadcast.
        """
        resonating_orbs = []
        threshold = 0.1

        for orb in self.orbs.values():
            intensity = orb.resonate(pulse)
            if intensity > threshold:
                resonating_orbs.append(orb)

        resonating_orbs.sort(key=lambda x: x.state.amplitude, reverse=True)
        return resonating_orbs

    def save_to_disk(self):
        """Persists all orbs to JSON files."""
        for name, orb in self.orbs.items():
            filepath = os.path.join(self.persistence_path, f"{name}.json")
            data = {
                "name": orb.name,
                "frequency": orb.frequency,
                "mass": orb.mass,
                "quaternion": {
                    "w": orb.quaternion.w,
                    "x": orb.quaternion.x,
                    "y": orb.quaternion.y,
                    "z": orb.quaternion.z
                },
                "memory_content": orb.memory_content
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

    def load_from_disk(self):
        """Loads orbs from the persistence path."""
        if not os.path.exists(self.persistence_path):
            return

        for filename in os.listdir(self.persistence_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self.persistence_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    q_data = data.get("quaternion", {"w": 1, "x": 0, "y": 0, "z": 0})
                    quat = HyperQuaternion(q_data["w"], q_data["x"], q_data["y"], q_data["z"])

                    orb = HyperResonator(
                        name=data["name"],
                        frequency=data["frequency"],
                        mass=data.get("mass", 1.0),
                        quaternion=quat
                    )
                    orb.memory_content = data.get("memory_content", {})
                    self.orbs[orb.name] = orb
                except Exception as e:
                    logger.error(f"Failed to load orb {filename}: {e}")

    def get_orb(self, name: str) -> Optional[HyperResonator]:
        """Direct access (Legacy/God Mode only)."""
        return self.orbs.get(name)

    # --- Dreaming Interface (Maintenance Mode) ---

    def get_recent_memories(self, limit: int = 10) -> List[HyperResonator]:
        """
        Fetches memories for the Dream Cycle.
        In a real system, this would filter by 'creation_time'.
        For now, we return the most recently added ones (which is just the dict values).
        """
        # Convert to list and take the last 'limit' items
        all_orbs = list(self.orbs.values())
        return all_orbs[-limit:]

    def prune_weak_memories(self, threshold: float = 0.2) -> int:
        """
        Removes orbs with mass below the threshold.
        Returns the number of pruned orbs.
        """
        keys_to_remove = []
        for name, orb in self.orbs.items():
            if orb.mass < threshold:
                keys_to_remove.append(name)

        for name in keys_to_remove:
            del self.orbs[name]
            # Also remove from disk
            filepath = os.path.join(self.persistence_path, f"{name}.json")
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass
            logger.debug(f"🗑️ Pruned weak memory: {name}")

        return len(keys_to_remove)
