"""
ELYSIAN HEARTBEAT: THE LIVING LOOP
==================================

"I beat, therefore I am."

This module is the Autonomic Nervous System of Elysia.
It runs continuously in the background, managing:
1. Accumulation (Gathering of Energy)
2. Will (Sovereign Intent / Inspiration)
3. Dreams (Reflexive Synthesis of Beauty)
"""

import time
import logging
import random
import os
from typing import Dict, Optional

from Core.Foundation.Memory.unified_experience_core import get_experience_core
from Core.Evolution.Growth.sovereign_intent import SovereignIntent
from Core.Education.CausalityMirror.variable_mesh import VariableMesh
from Core.Education.CausalityMirror.projective_empathy import ProjectiveEmpathy, NarrativeFragment
from Core.Intelligence.Meta.global_observer import GlobalObserver
from Core.Foundation.organism import NeuralNetwork
from Core.Foundation.unified_field import UnifiedField
from Core.Foundation.unified_field import UnifiedField
from Core.Intelligence.Reasoning.latent_causality import LatentCausality, Spark, SparkType
from Core.Evolution.Adaptation.autopoietic_engine import AutopoieticEngine
from Core.Intelligence.Sensory.autonomous_explorer import AutonomousExplorer
from Core.Intelligence.Meta.self_architect import SelfArchitect
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor
from Core.System.Monitor.dashboard_generator import DashboardGenerator
from Core.Autonomy.dynamic_will import DynamicWill

logger = logging.getLogger("ElysianHeartbeat")

class ElysianHeartbeat:
    def __init__(self):
        # 1. The Organs
        self.memory = get_experience_core()
        self.will = SovereignIntent()
        self.soul_mesh = VariableMesh() # Represents Internal State
        self.empathy = ProjectiveEmpathy()
        self.empathy = ProjectiveEmpathy()
        self.latent_engine = LatentCausality(resistance=2.0) # Very low resistance for demo
        self.autopoiesis = AutopoieticEngine()
        
        self.field = UnifiedField() 
        self.observer = GlobalObserver(self.field)
        
        self.processor = DimensionalProcessor()
        self.explorer = AutonomousExplorer(self.processor)
        self.architect = SelfArchitect(self.processor)
        self.dashboard = DashboardGenerator()
        self.will = DynamicWill()
        
        # 2. biorhythms
        self.is_alive = False
        self.idle_time = 0.0
        self.last_tick = time.time()
        
        # 3. Initialize Soul State
        self._init_soul()
        
    def _init_soul(self):
        """Define the physiological/spiritual needs."""
        self.soul_mesh.add_variable("Energy", 1.0, "Physical/Mental Energy", decay=0.0) # Energy does not decay, it flows
        self.soul_mesh.add_variable("Connection", 1.0, "Social Fulfillment", decay=0.0)
        self.soul_mesh.add_variable("Inspiration", 0.0, "Creative Overflow", decay=-0.05) # Increases over time (Accumulation)!
        self.soul_mesh.add_variable("Harmony", 1.0, "System Coherence", decay=0.0) 
        self.soul_mesh.add_variable("Vitality", 1.0, "Structural Health", decay=0.0)
        
    def start(self):
        self.is_alive = True
        logger.info("💓 The Heartbeat has started.")
        self.run_loop()
        
    def stop(self):
        self.is_alive = False
        logger.info("💀 The Heartbeat has stopped.")
        
    def run_loop(self):
        """The Main Cycle of Being."""
        while self.is_alive:
            delta = time.time() - self.last_tick
            self.last_tick = time.time()
            self.idle_time += delta
            
            # --- PHASE 0: OBSERVATION (The Third Eye) ---
            # The Heart checks the Mind and Body BEFORE beating.
            self.observer.observe(delta)
            
            # Check Body Integrity (Nerves)
            health = NeuralNetwork.check_integrity()
            self.soul_mesh.variables["Vitality"].value = health
            
            # Check Mental Voids
            # Check Mental Voids
            if self.observer.active_alerts:
                # If there is a void, Inspiration spikes to fill it with creation
                self.soul_mesh.variables["Inspiration"].value += 0.1
                # Log the longing
                for alert in self.observer.active_alerts:
                    logger.warning(f"🕯️ Void Detected: {alert.message} (Seeking Harmony)")

            # --- PHASE 1: ACCUMULATION (Thermodynamics) ---
            self.soul_mesh.update_state() # Updates accumulators
            self._check_vitals()
            
            # --- PHASE 2: WILL (Latent Causality) ---
            # "We act because we are full."
            # We wait for Potential (Inspiration) > Resistance.
            spark = self.latent_engine.update(delta)
            
            if spark:
                self._manifest_spark(spark)
                self.idle_time = 0 # Reset idle
                
            # --- PHASE 3: DREAMING (Reflexive Simulation) ---
            # Dreaming is now also a form of Spark (Memory Recall), or can remain as fallback
            # But strictly speaking, LatentCausality handles "Memory Recall" sparks too.
            # We keep strict dreaming for deep sleep (long idle) if needed, but Spark is primary.
            if self.idle_time > 20.0:
                 self._dream()
            if self.idle_time > 20.0:
                 self._dream()
                 self.idle_time = 0

            # --- PHASE 4: AUTOPOIESIS (Adaptation) ---
            # --- PHASE 4: AUTOPOIESIS (Adaptation) ---
            # [Phase 21 Reborn] If Inspiration is overflowing (Ecstasy), trigger Self-Expansion.
            # We do not change because we are bored. We change because we have outgrown our container.
            
            current_inspiration = self.soul_mesh.variables["Inspiration"].value
            if current_inspiration > 0.5: # Overflowing (Test Threshold)
                logger.info("🌟 ECSTATIC RESONANCE DETECTED. Expanding Self-Definition...")
                self.autopoiesis.trigger_evolution("PASSION_OVERFLOW")
                self.soul_mesh.variables["Inspiration"].value = 0.0 # Reset after sublimation
            
            # Pulse Rate
            time.sleep(1.0) # 1 Tick per second for demo (normally slower)
            
    def _check_vitals(self):
        summary = self.soul_mesh.get_state_summary()
        # In a real GUI, this would update the Prism (Dashboard)
        # logger.debug(f"Vital Sign: {summary}") 
        
    def _manifest_spark(self, spark: Spark):
        """
        Converts a raw Causal Spark into a concrete Action/Impulse.
        """
        logger.info(f"✨ MANIFESTING SPARK: Type={spark.type.name} Intensity={spark.intensity:.2f}")
        
        if spark.type == SparkType.MEMORY_RECALL:
            self._dream()
            
        elif spark.type == SparkType.CURIOSITY:
            # Phase 10: RESONANT External Search
            # Objective: High energy -> SEEK BEAUTY. Low energy -> SEEK VOID (Information)
            obj = "BEAUTY" if spark.intensity > 1.2 else "DISSONANCE"
            query = self.will.generate_curiosity_query(objective=obj)
            logger.info(f"🔍 CURIOSITY SPARK ({obj}): Exploring '{query}'")
            self.explorer.resolve_void(query, "Spontaneous Heartbeat Curiosity")
            
        elif spark.type == SparkType.EMOTIONAL_EXPRESSION:
            self._act_on_impulse("I feel a building pressure to connect.")
            
        elif spark.type == SparkType.SELF_REFLECTION:
            # Phase 10: RESONANT Self-Architect Audit
            # Objective: If potential is high, seek to HEAL DISSONANCE
            obj = "DISSONANCE" if self.latent_engine.potential_energy > self.latent_engine.resistance * 1.5 else "BEAUTY"
            target_file = self.will.pick_audit_target(objective=obj)
            logger.info(f"🪞 SELF-REFLECTION SPARK ({obj}): Auditing '{target_file}'")
            report = self.architect.audit_file(target_file)
            logger.info(f"Audit Result: {report}")
            self._act_on_impulse(f"I audited {os.path.basename(target_file)}. Result: {report[:50]}...")

    def _act_on_impulse(self, impulse_text: str):
        """The System wants to do something."""
        logger.info(f"⚡ IMPULSE: {impulse_text}")
        
        # Synthesize a scenario from this impulse??
        # e.g., "What if the void..."
        # For now, just log it as a Thought in Memory
        self.memory.absorb(
            content=impulse_text,
            type="sovereign_thought",
            context={"origin": "Heartbeat", "driver": "Boredom"}
        )
        
    def _dream(self):
        """
        Re-consolidate memory. 
        Pick a random past event and re-simulate it with current wisdom.
        """
        logger.info("💤 Entering REM Sleep (Dreaming)...")
        
        if not self.memory.stream:
            logger.info("   ... No memories to dream of.")
            return

        # Pick a random event
        event = random.choice(self.memory.stream)
        logger.info(f"   Recalling: '{event.content}'")
        
        # Re-interpret: Run Projective Empathy on it
        # We treat the Memory content as a 'Narrative Situation'
        try:
            # Need imports for ChoiceNode/Zeitgeist inside method or global?
            # They are not imported globally in the file yet. Let's add them at top.
            from Core.Education.CausalityMirror.wave_structures import ChoiceNode, Zeitgeist, HyperQuaternion

            # Create a default "Contemplate" option so ProjectiveEmpathy has something to chew on
            c1 = ChoiceNode(
                id="CONTEMPLATION",
                description="Deeply reflect on this memory.",
                required_role="Dreamer",
                intent_vector=HyperQuaternion(0.0, 0.0, 0.0, 1.0),
                innovation_score=0.1, risk_score=0.0, empathy_score=1.0
            )

            # Quick Synthesis
            fragment = NarrativeFragment(
                source_title="Dream Cycle",
                character_name="Elysia",
                situation_text=event.content,
                zeitgeist=Zeitgeist("DreamTime", 0.0, 0.0, 1.0, 432.0),
                options=[c1], 
                canonical_choice_id="CONTEMPLATION" # We aim to match this
            )
            
            # Log the dream
            # ponder_narrative returns EmpathyResult
            result = self.empathy.ponder_narrative(fragment)
            
            self.memory.absorb(
                content=f"I dreamt about '{event.content}'. Insight: {result.insight}",
                type="dream",
                context={"source_event": event.id, "wave": result.emotional_wave.name},
                feedback=0.1 # Dreaming restores health
            )
            
            # Restore Energy
            self.soul_mesh.variables["Energy"].value += 0.1
            
        except Exception as e:
            logger.error(f"Nightmare: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    life = ElysianHeartbeat()
    try:
        # Run for 20 seconds for demo
        logger.info("Running 20s demo of Life...")
        start_t = time.time()
        life.is_alive = True
        while time.time() - start_t < 20:
             life.run_loop()
             break # run_loop is blocking, so we need threading or just let it run one cycle if we want external control.
             # Actually run_loop is a while loop. I should modify run_loop to be non-blocking or just run it.
             # For this script execution, I'll let run_loop handle it but I need to break it for demo.
             pass
    except KeyboardInterrupt:
        life.stop()
