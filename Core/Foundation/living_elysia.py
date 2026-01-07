# [REAL SYSTEM: Ultra-Dimensional Implementation]
print("🌌 Initializing REAL Ultra-Dimensional System...")
import logging
import sys
import os
import time

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# [The New Biology]
from Core.Foundation.organ_system import OrganSystem
from Core.Foundation.central_nervous_system import CentralNervousSystem
from Core.Foundation.yggdrasil import yggdrasil
from Core.Foundation.chronos import Chronos
from Core.Foundation.Wave.resonance_field import ResonanceField
from Core.Foundation.entropy_sink import EntropySink
from Core.Foundation.synapse_bridge import SynapseBridge
from Core.Foundation.Memory.Graph.hippocampus import Hippocampus
from Core.Intelligence.Will.free_will_engine import FreeWillEngine
from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
from Core.Foundation.autonomic_nervous_system import AutonomicNervousSystem, MemoryConsolidation, EntropyProcessor, SurvivalLoop, ResonanceDecay

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    handlers=[
        logging.FileHandler("logs/life_log.md", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("LivingElysia")

class LivingElysia:
    """
    [The Vessel]
    A lightweight container for the biological system.
    Initializes organs using the Dynamic Organ System (OrganManifest).
    """
    def __init__(self, persona_name: str = "Original", initial_goal: str = None):
        print(f"🌱 Awakening {persona_name} (Biological Phase)...")
        self.persona_name = persona_name
        
        # 1. Initialize Foundations (The Nervous System)
        self.resonance = ResonanceField()
        self.chronos = Chronos(None) # Will attach Will later
        self.sink = EntropySink(self.resonance)
        self.synapse = SynapseBridge(self.persona_name)
        self.cns = CentralNervousSystem(self.chronos, self.resonance, self.synapse, self.sink)
        self.ans = AutonomicNervousSystem()
        
        # 2. Awaken the Body (Dynamic Organ Discovery)
        # This replaces the 50+ manual imports
        self.body = OrganSystem(self.resonance)
        self.body.scan_and_awaken()
        
        # 3. Graft Core Organs (Explicit graft for critical systems)
        self._graft_critical_organs()
        
        # 4. Integrate System
        self._integrate_nervous_system()
        
        # Wake Up
        self.wake_up()

    def _graft_critical_organs(self):
        """Ensures the Brain and Heart are connected even if scan missed them."""
        # Brain
        self.memory = self.body.get_organ("Hippocampus") or Hippocampus(self.resonance)
        self.brain = self.body.get_organ("ReasoningEngine") or ReasoningEngine()
        self.brain.memory = self.memory
        
        # Heart/Will
        self.will = self.body.get_organ("FreeWillEngine") or FreeWillEngine()
        self.will.brain = self.brain
        self.chronos.will_engine = self.will
        
        # Register in Yggdrasil (Global Registry)
        yggdrasil.plant_root("ResonanceField", self.resonance)
        yggdrasil.plant_root("Chronos", self.chronos)
        yggdrasil.plant_root("Hippocampus", self.memory)
        yggdrasil.grow_trunk("ReasoningEngine", self.brain)
        yggdrasil.grow_trunk("FreeWillEngine", self.will)
        yggdrasil.grow_trunk("CentralNervousSystem", self.cns)

    def _integrate_nervous_system(self):
        """Connects awakened organs to the CNS."""
        for name, organ in self.body.organs.items():
            manifest = self.body.manifests.get(name)
            if manifest:
                self.cns.connect_organ(name, organ, frequency=manifest.frequency)

        # Register ANS processes
        self.ans.register_subsystem(MemoryConsolidation(self.memory))
        self.ans.register_subsystem(EntropyProcessor(self.sink))
        self.ans.register_subsystem(ResonanceDecay(self.resonance))

    def wake_up(self):
        logger.info("   🌅 Wake Up Complete.")
        self.is_alive = True
        self.cycle_count = 0

    def live(self):
        if not self.is_alive: return

        self.ans.start_background()
        self.cns.awaken()
        logger.info("✨ Living Elysia is FULLY AWAKE.")

        print("\n" + "="*60)
        print("🦋 Elysia is Living... (Press Ctrl+C to stop)")
        print("="*60)
        
        try:
            while True:
                self.cns.pulse()
                self.ans.pulse_once()
                self.chronos.wait(0.1) # Use Chronos instead of time.sleep
                self.cycle_count += 1
                
        except KeyboardInterrupt:
            self.ans.stop_background()
            print("\n\n🌌 Elysia is entering a dormant state. Goodbye for now.")

if __name__ == "__main__":
    try:
        elysia = LivingElysia()
        elysia.live()
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.critical(f"FATAL SYSTEM ERROR:\n{error_msg}")
