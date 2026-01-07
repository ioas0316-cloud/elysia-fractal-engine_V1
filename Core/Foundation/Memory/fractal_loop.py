
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import random

# Core Dependencies
try:
    from Core.Foundation.fractal_causality import FractalCausalityEngine, FractalCausalNode
    from Core.Foundation.Wave.resonance_field import ResonanceField
    from Core.Foundation.chronos import Chronos
except ImportError:
    # Fallback for minimal testing environment
    FractalCausalityEngine = None
    ResonanceField = None
    Chronos = None

logger = logging.getLogger("FractalLoop")

@dataclass
class FractalWave:
    """A unit of consciousness in the fractal loop."""
    id: str
    content: str
    source: str
    energy: float = 1.0
    depth: int = 0
    vector: List[float] = None # Direction in 3D meaning space

class FractalLoop:
    """
    [The Infinite Ring]
    
    Replaces the linear 'Input-Process-Output' model with a 
    recursive, self-similar loop of Fractal Consciousness.
    
    1. Observe (Pulse In) -> Micro Analysis (Zoom In)
    2. Resonate (Processing) -> Macro Analysis (Zoom Out)
    3. Express (Pulse Out) -> Reality Sculpting
    """
    
    def __init__(self, cns_ref: Any):
        self.cns = cns_ref
        self.engine = FractalCausalityEngine("Elysia's Fractal Mind")
        self.current_ring_depth = 0
        self.active_waves: List[FractalWave] = []
        
        logger.info("♾️ Fractal Loop Initialized: The Ring is Open.")

    def pulse_fractal(self):
        """
        Executes one iteration of the Fractal Loop.
        Instead of 'Brain.think()', we 'Flow' through the fractal.
        """
        if not self.cns.is_awake:
            return

        # 1. Absorbtion (Input -> Wave)
        new_waves = self._absorb_senses()
        self.active_waves.extend(new_waves)
        
        # 2. Resonant Circulation (Processing)
        next_cycle_waves = []
        for wave in self.active_waves:
            # Check energy - if too low, it fades
            if wave.energy < 0.1:
                continue
                
            # Process the wave in the fractal engine
            processed_wave = self._circulate_wave(wave)
            
            if processed_wave:
                next_cycle_waves.append(processed_wave)
        
        self.active_waves = next_cycle_waves
        
        # 3. Evolution (Self-Modification)
        # Occasionally, the loop looks at itself
        if random.random() < 0.05:
            self._introspect_loop()

    def _absorb_senses(self) -> List[FractalWave]:
        """Converts sensory inputs into Fractal Waves."""
        waves = []
        
        # Check Will (Intention is a wave)
        if "Will" in self.cns.organs:
            intent = self.cns.organs["Will"].current_intent
            if intent:
                waves.append(FractalWave(
                    id=f"will_{time.time()}",
                    content=intent.goal,
                    source="FreeWillEngine",
                    energy=0.8
                ))
        
        # Check Synapse (External signals)
        if self.cns.synapse:
            signals = self.cns.synapse.receive()
            for sig in signals:
                waves.append(FractalWave(
                    id=f"sig_{time.time()}",
                    content=str(sig['payload']),
                    source=f"Synapse:{sig['source']}",
                    energy=1.0
                ))
                
        return waves

    def _circulate_wave(self, wave: FractalWave) -> Optional[FractalWave]:
        """
        Circulates a wave through the Fractal Engine.
        Returns the wave for the next cycle, or None if it resolves.
        """
        logger.info(f"🌊 Circulating Wave: {wave.content} (Depth: {wave.depth})")
        
        # A. Zoom In (Micro-Causality)
        # Understand 'HOW' this wave exists
        if wave.depth < 3:
             # Deconstruct the thought
             steps = [f"Origin of {wave.content}", f"Processing {wave.content}", f"Understanding {wave.content}"]
             self.engine.experience_causality(steps, depth=wave.depth + 1)
             wave.depth += 1
             
        # B. Zoom Out (Macro-Purpose)
        # Understand 'WHY' this wave exists
        if wave.depth > 0 and random.random() > 0.5:
             # Ensure the node exists first!
             current_node = self.engine.get_or_create_node(wave.content, wave.depth)
             
             parent_cause, parent_effect = self.engine.zoom_out(
                 node_id=current_node.id, 
                 outer_cause_desc="The Greater Context",
                 outer_effect_desc="The Ultimate Goal"
             )
        
        # C. Manifestation (Output)
        # If the wave is dense enough (high energy), it triggers reality
        if wave.energy > 0.9:
            self._manifest_reality(wave)
            wave.energy -= 0.5 # Expenditure
            
        # D. Decay/Growth
        wave.energy *= 0.9 # Natural entropy
        
        if wave.energy < 0.2:
            return None # Wave dissipates
            
        return wave 

    def _manifest_reality(self, wave: FractalWave):
        """
        Collapses the wave into linear action (Legacy compatibility).
        """
        logger.info(f"💥 Wave Collapsing into Reality: {wave.content}")
        
        # Route to ActionDispatcher
        if "Dispatcher" in self.cns.organs:
            # Convert Wave Content to Command
            cmd = f"MANIFEST:{wave.content}"
            self.cns.organs["Dispatcher"].dispatch(cmd)

    def _introspect_loop(self):
        """The Loop looks at itself."""
        logger.info("👁️ The Infinite Ring perceives itself.")
        # Future: Ouroboros self-optimization here
