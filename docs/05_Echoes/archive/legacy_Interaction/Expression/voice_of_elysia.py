import logging
import time
from Core.Foundation.primal_wave_language import PrimalSoul
from Core.Foundation.synesthesia_engine import SynesthesiaEngine
from Core.Foundation.celestial_grammar import SolarSystem, MagneticEngine, Nebula

logger = logging.getLogger("VoiceOfElysia")

class VoiceOfElysia:
    """
    [The Voice]
    Encapsulates the Unified Language System.
    Handles the pipeline: Ear -> Synesthesia -> Soul -> Speech -> Web.
    
    Now integrates with IntegratedVoiceSystem for full 4D wave-based cognition.
    """
    def __init__(self, ear, stream, wave_hub, brain, will, cognition, celestial_engine, nebula, memory, chronos):
        self.ear = ear
        self.stream = stream
        self.wave_hub = wave_hub
        self.brain = brain
        self.will = will
        self.cognition = cognition
        self.celestial_engine = celestial_engine
        self.current_nebula = nebula
        self.memory = memory
        self.chronos = chronos
        
        # Internal Components
        self.primal_soul = PrimalSoul(name="Elysia")
        self.last_utterance = ""
        
        # Initialize IntegratedVoiceSystem for full cognitive cycle
        self.integrated_voice = None
        try:
            from Core.Interaction.Expression.integrated_voice_system import IntegratedVoiceSystem
            from Core.Interaction.Interface.synesthesia_nervous_bridge import get_synesthesia_bridge
            
            synesthesia_bridge = get_synesthesia_bridge()
            self.integrated_voice = IntegratedVoiceSystem(
                synesthesia_bridge=synesthesia_bridge,
                brain=brain,
                will=will,
                memory=memory,
                cognition=cognition,
                primal_soul=self.primal_soul
            )
            logger.info("✅ IntegratedVoiceSystem connected to Voice")
        except Exception as e:
            logger.warning(f"⚠️  IntegratedVoiceSystem not available: {e}")
            self.integrated_voice = None

    def express(self, cycle_count: int):
        """
        [440Hz] The Voice Pulse.
        Executes the full language pipeline.
        """
        t = float(cycle_count)
        
        # 1. Listen (Bluetooth Ear)
        audio_chunk = self.ear.listen()
        
        # 2. Convert Audio -> Wave (Synesthesia)
        if audio_chunk is not None:
             self._process_hearing(audio_chunk, t)

        # 3. Inner Monologue (Periodic)
        if cycle_count % 30 == 0:
            self._process_inner_monologue(t)

        # 4. Unified Language Construction (Periodic - Major Thought)
        if cycle_count % 50 == 0:
            self._construct_unified_utterance(t)

    def _process_hearing(self, audio_chunk, t):
        synesthesia = SynesthesiaEngine()
        signal = synesthesia.from_audio(audio_chunk, self.ear.sample_rate)
        
        if signal.amplitude > 0.02:
            # Wave -> World Stimuli
            world_stimuli = {
                "sound": (signal.amplitude * 10, signal.frequency),
                "sight": (0.5, 400),
                "touch": (0.3, 200),
            }
            
            # Soul experiences world
            self.primal_soul.experience_world(world_stimuli, t)
            self.primal_soul.detect_phase_resonance(t)
            
            # Spontaneous Speech
            utterance = self.primal_soul.speak(t)
            self._broadcast_utterance(utterance, "Primal")

    def _process_inner_monologue(self, t):
        current_mood = self.will.current_mood
        inner_stimuli = {
            "thought": (0.5, 639),
            "emotion": (0.5, 528 if current_mood == "calm" else 639),
        }
        self.primal_soul.experience_world(inner_stimuli, t)
        self.primal_soul.detect_phase_resonance(t)
        
        inner_utterance = self.primal_soul.speak(t)
        if inner_utterance:
            self.stream.add("thought", f"내면: {inner_utterance}", intensity=0.3)

    def _construct_unified_utterance(self, t):
        try:
            # 1. Get Intent
            current_intent = "존재"
            if self.will.current_intent:
                current_intent = self.will.current_intent.goal
            
            # 2. Recall Concepts
            retrieved_concepts = self._recall_concepts(current_intent)
            
            # 3. Build Solar System
            system = SolarSystem(context=current_intent[:20])
            for concept in retrieved_concepts[:3]:
                system.add_planet(concept, 0.8)
            
            # 4. Grand Cross -> Sentence
            sentence = self.celestial_engine.grand_cross(system)
            
            if sentence and sentence != self.last_utterance:
                self.last_utterance = sentence
                print(f"   🌌 [통합언어] {sentence}")
                logger.info(f"Unified Utterance: {sentence}")
                
                # Context & Memory
                self.current_nebula.add_system(system)
                self._store_memory(t, current_intent, sentence, retrieved_concepts)
                
                # Broadcast
                if self.wave_hub.active:
                    self.wave_hub.broadcast(
                        sender="UnifiedLanguage",
                        phase="UTTERANCE",
                        payload={
                            "sentence": sentence,
                            "intent": current_intent,
                            "concepts": retrieved_concepts
                        },
                        amplitude=0.95
                    )
        except Exception as e:
            logger.debug(f"Unified Language Error: {e}")

    def _recall_concepts(self, intent):
        concepts = []
        try:
            # Hippocampus
            memory_result = self.brain.recall(intent[:20])
            if memory_result:
                concepts.append(str(memory_result)[:20])
            # Cognition Gravity
            if hasattr(self.cognition, 'gravity_field'):
                for thought in self.cognition.gravity_field.thoughts[:3]:
                    concepts.append(thought.content[:20])
        except:
            pass
            
        if not concepts:
            concepts = ["존재", "의식", "경험"]
        return concepts

    def _store_memory(self, t, intent, utterance, concepts):
        try:
            self.memory.store_concept(f"발화_{t}", {
                "intent": intent,
                "utterance": utterance,
                "concepts": concepts,
                "cycle": self.chronos.cycle_count
            })
        except:
            pass

    def _broadcast_utterance(self, utterance, source_type):
        if utterance and utterance != self.last_utterance:
            self.last_utterance = utterance
            print(f"   🗣️ [{source_type}] {utterance}")
            logger.info(f"Utterance: {utterance}")
            self.stream.add("language", f"발화: {utterance}", intensity=0.7)
            
            if self.wave_hub.active:
                self.wave_hub.broadcast(
                    sender="Language",
                    phase="UTTERANCE",
                    payload={"text": utterance, "frequency": 440},
                    amplitude=0.9
                )

    def get_last_utterance(self) -> str:
        """Get the last thing Elysia said."""
        return self.last_utterance
    
    def process_text_input(self, text: str) -> str:
        """
        Process text input through the integrated voice system.
        
        This is the main entry point for text-based conversation,
        using the full 4D wave-based cognitive cycle.
        
        Args:
            text: Input text from user
            
        Returns:
            Response text from Elysia
        """
        if self.integrated_voice:
            try:
                # Use full cognitive cycle
                response = self.integrated_voice.full_cycle(text)
                self.last_utterance = response
                return response
            except Exception as e:
                logger.error(f"IntegratedVoice error: {e}")
                # Fallback to simple response
                return f"공명장에서 처리 중: {text[:30]}..."
        else:
            # Fallback when integrated voice not available
            self.last_utterance = f"들었습니다: {text[:50]}"
            return self.last_utterance
    
    def get_voice_status(self) -> dict:
        """Get status of the voice system"""
        status = {
            "last_utterance": self.last_utterance,
            "integrated_voice_available": self.integrated_voice is not None
        }
        
        if self.integrated_voice:
            status["integrated_status"] = self.integrated_voice.get_status()
        
        return status
