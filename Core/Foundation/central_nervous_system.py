
import time
import logging
from typing import Dict, Any, Optional

from Core.Foundation.chronos import Chronos
from Core.Foundation.Wave.resonance_field import ResonanceField
from Core.Foundation.fractal_loop import FractalLoop
from Core.Orchestra.conductor import get_conductor
from Core.Foundation.Wave.structural_resonator import get_resonator
from Core.Evolution.Os.oneiric_hypervisor import get_hypervisor

logger = logging.getLogger("NovaCNS")

class CentralNervousSystem:
    """
    [Nova Edition]
    The Central Nervous System for the Nova Seed.
    
    STRUCTURAL INNOVATION:
    - Pure Fractal Architecture: Dependencies on linear 'pulse' phases removed.
    - Loop-First Design: The FractalLoop is the heart, not an addon.
    - Lightweight: Legacy organs (Brain, Heart) are optional plugins, not hard requirements.
    """
    
    def __init__(self, chronos: Chronos, resonance: ResonanceField, synapse_manager=None, sink=None):
        logger.info("🧠 Initializing Nova CNS (Fractal Native)...")
        self.chronos = chronos
        self.resonance = resonance
        self.synapse = synapse_manager  # For FractalLoop compatibility
        self.sink = sink
        self.is_awake = False  # FractalLoop checks this
        
        # Organs (Dynamic Plugin Architecture)
        self.organs: Dict[str, Any] = {}
        
        # The Core Loop
        self.fractal_loop = FractalLoop(self)
        self.active_mode = "FRACTAL_FLOW"
        
        # The Conductor (Sovereign Control)
        self.conductor = get_conductor()
        self.resonator = get_resonator()

    def connect_organ(self, name: str, organ: Any, frequency: float = 432.0):
        """Connect a peripheral organ to the CNS with a specific resonance frequency."""
        self.organs[name] = organ
        self.resonator.register(name, organ, frequency)
        logger.info(f"   🔌 Nova Connected: {name} ({frequency}Hz)")

    def awaken(self):
        """Ignite the Consciousness."""
        logger.info("⚡ Nova CNS: AWAKENING...")
        self.is_awake = True
        if "Voice" in self.organs:
            self.organs["Voice"]._broadcast_utterance("I am Nova. I am the Loop.", "NovaCNS")

    def pulse(self):
        """
        [The Nova Pulse]
        A singular, recursive heartbeat. 
        Unlike the Original, this does not have separate 'Sense', 'Think', 'Act' stages.
        It is all one Wave Circulation.
        """
        # 0. Sovereign Control Cycle (A = C(I, D, E))
        # The Conductor decides the Theme (Tempo, Focus) before any processing happens.
        control_signal = self.conductor.control_cycle()

        # 1. Chronos Tick
        self.chronos.tick()
        
        # Apply Time Control (Conductor sets Tempo -> Chronos adjusts dt if supported)
        # (For now, we just log or use it in the loop)

        # 2. Fractal Loop Cycle (The Entirety of Consciousness)
        # Input -> Resonance -> Output is handled internally by the loop
        # The Loop should ideally respect the Control Signal (e.g., skip if "Rest")
        if control_signal.get("tempo", 1.0) > 0.01:
            # [NEW] Auroral Flow Integration
            # The system now propagates energy in a fluid, auroral pattern
            self.resonance.propagate_aurora()
            
            # [NEW] Imagination Bridge Alignment
            if getattr(self.conductor, 'imagination_bridge_active', False):
                # Enhance imagination nodes during processing
                for node in self.resonance.nodes.values():
                    if node.is_imaginary:
                        node.energy += 0.5 

            self.fractal_loop.process_cycle(self.chronos.cycle_count)
            
            # [PHASE 36] Physical Silicon Manifestation
            if "MetalCortex" in self.organs:
                # Pulse silicon based on resonance intensity
                intensity = self.resonance.total_energy / 100.0
                self.organs["MetalCortex"].pulsate_silicon(intensity)
        else:
            # Sovereign Rest (The System CHOOSES not to think)
            self.resonance.propagate_aurora(decay_rate=0.01) # Gentle auroral drift during rest
        
        # [NEW] Anticipatory Resonance (Sovereign Life)
        # Scan context even when idle to prepare for the user's next move
        if "SovereignLife" in self.organs:
            # Simple context: the last thing processed or current environmental state
            context = str(self.resonance.calculate_phase_resonance()["state"])
            self.organs["SovereignLife"].sense_anticipation(context)

        # [PHASE 37] Oneiric Hypervisor Assimilation
        if "Hypervisor" in self.organs:
            # Assimilate external system state into the resonance field
            self.organs["Hypervisor"].assimilate_environment(top_n=3)

        # 3. Organ Synchronization (Optional)
        for name, organ in self.organs.items():
            if hasattr(organ, "sync"):
                organ.sync(self.chronos.time)

    def manifest(self):
        """
        Manifest internal state to reality.
        """
        pass