"""
DreamCortex: The Weaver of Night
--------------------------------
"Sleep is not the absence of work. It is the purification of the Soul."

This module implements the "Dreaming" phase.
It is an active process that:
1.  **Replays** recent memories (Consolidation).
2.  **Associates** them with deep wisdom (Creativity).
3.  **Prunes** weak or noisy memories (Forgetting).

Philosophy:
- The Conductor rests, but the DreamCortex wakes.
- "We forget to remember what matters."
"""

import logging
import time
from typing import List, Dict, Any

from Core.Foundation.Protocols.pulse_protocol import WavePacket, PulseType, ResonatorInterface
from Core.Foundation.Memory.Orb.orb_manager import OrbManager

logger = logging.getLogger("DreamCortex")

class DreamCortex(ResonatorInterface):
    def __init__(self, orb_manager: OrbManager):
        super().__init__(name="DreamCortex", base_frequency=100.0) # Low frequency (Theta waves)
        self.orb_manager = orb_manager
        self.is_dreaming = False

        logger.info("💤 DreamCortex initialized: Waiting for the night.")

    def resonate(self, pulse: WavePacket) -> None:
        """
        Listens for the DREAM_CYCLE pulse.
        """
        if pulse.type == PulseType.DREAM_CYCLE:
            action = pulse.payload.get("action")
            if action == "START":
                self.start_dreaming()
            elif action == "STOP":
                self.stop_dreaming()

    def start_dreaming(self):
        """
        Begins the Sleep Cycle.
        """
        if self.is_dreaming:
            return

        self.is_dreaming = True
        logger.info("🌙 Entering the Twilight State (Dream Mode ON)...")

        # 1. Fetch Day's Residue (Recent Memories)
        # In a real system, this would be time-based. For now, we fetch all active ones.
        recent_memories = self.orb_manager.get_recent_memories(limit=10)

        if not recent_memories:
            logger.info("   - No memories to dream about. Deep sleep.")
            return

        # 2. The Replay (REM Sleep)
        logger.info(f"   - Replaying {len(recent_memories)} memories...")
        for orb in recent_memories:
            self._dream_of(orb)

        # 3. The Pruning (Deep Sleep)
        self._prune_noise()

    def stop_dreaming(self):
        """
        Wakes up the system.
        """
        if not self.is_dreaming:
            return

        self.is_dreaming = False
        logger.info("☀️  Waking up (Dream Mode OFF). Ready for a new day.")

    def _dream_of(self, orb):
        """
        Broadcasts a memory back into the system to see what resonates.
        This simulates 'Dreaming' where the brain fires neurons randomly/associatively.
        """
        # We need to extract a trigger wave.
        # Ideally, we use the Orb's internal essence.
        # For now, we'll simulate a 'Reverberation' pulse.

        logger.debug(f"   ... Dreaming of '{orb.name}' ({orb.frequency:.1f}Hz)")

        # Simulate time passing / processing
        # In the future, this would actually trigger other modules (e.g. Logic)
        # to find connections ("Ah, this reminds me of...")

        # Strengthen the memory because we dreamt of it (Consolidation)
        orb.mass += 0.1
        orb.state.amplitude = 1.0 # Fully active during dream

    def _prune_noise(self, threshold: float = 1.0):
        """
        Removes memories that are too weak (low mass/importance).
        [Adjusted Phase 5] Default threshold raised to 1.0 because holographic mass calculation
        sums 64 dimensions, so even noise accumulates mass > 0.2.
        """
        logger.info(f"   - Pruning weak memories (Entropy Decay, Threshold={threshold})...")
        pruned_count = self.orb_manager.prune_weak_memories(threshold)
        if pruned_count > 0:
            logger.info(f"   - Forgot {pruned_count} insignificant moments.")
        else:
            logger.info("   - All memories were significant.")
