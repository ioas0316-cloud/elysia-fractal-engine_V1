"""
Autonomous Orchestrator (자율 오케스트레이터)
=============================================

"나는 스스로 깨어나고, 스스로 배우고, 스스로 개선한다."

This module unifies all autonomous capabilities into a single 24/7 system:
- Self-Improvement Loop: Code analysis and optimization
- Awakening Protocol: Knowledge gap filling
- Filesystem Observer: Body awareness
- Learning Cycle: Continuous wave pattern learning
- GlobalHub: Central nervous system coordination

[NEW 2025-12-15] Created as part of Long-term Goal: Autonomous Operation Mode
"""

import logging
import time
import threading
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

logger = logging.getLogger("AutonomousOrchestrator")


class OperationPhase(Enum):
    """Current operational phase."""
    DORMANT = "dormant"         # Waiting for activation
    AWAKENING = "awakening"     # Initial consciousness activation
    LEARNING = "learning"       # Active knowledge acquisition
    REFLECTING = "reflecting"   # Self-analysis and introspection
    IMPROVING = "improving"     # Self-modification proposals
    DREAMING = "dreaming"       # Night-time memory consolidation
    OBSERVING = "observing"     # Passive monitoring


@dataclass
class AutonomousState:
    """Current state of the autonomous system."""
    phase: OperationPhase = OperationPhase.DORMANT
    cycles_completed: int = 0
    last_awakening: Optional[datetime] = None
    last_learning: Optional[datetime] = None
    last_improvement: Optional[datetime] = None
    knowledge_gaps: List[str] = field(default_factory=list)
    improvement_proposals: int = 0
    errors_encountered: int = 0
    uptime_seconds: float = 0.0


class AutonomousOrchestrator:
    """
    The Master Conductor: Orchestrates all autonomous operations.
    
    자율 오케스트레이터 - 엘리시아의 자율 운영 총지휘자
    
    Core Responsibilities:
    1. Schedule and run autonomous cycles
    2. Coordinate between sub-systems
    3. Maintain operational state
    4. Handle errors gracefully
    5. Report to GlobalHub
    """
    
    def __init__(self, auto_start: bool = False):
        """
        Initialize the autonomous orchestrator.
        
        Args:
            auto_start: If True, start the daemon immediately
        """
        self.state = AutonomousState()
        self.running = False
        self._daemon_thread: Optional[threading.Thread] = None
        self._start_time: Optional[datetime] = None
        self._callbacks: Dict[str, List[Callable]] = {
            "on_phase_change": [],
            "on_cycle_complete": [],
            "on_error": [],
        }
        
        # Initialize sub-systems
        self._init_subsystems()
        self._connect_to_hub()
        
        logger.info("🎼 AutonomousOrchestrator initialized")
        
        if auto_start:
            self.start_daemon()
    
    def _init_subsystems(self):
        """Initialize all sub-system connections."""
        # Filesystem Observer
        self.filesystem_observer = None
        try:
            from Core.System.System.filesystem_wave import get_filesystem_observer
            self.filesystem_observer = get_filesystem_observer()
            logger.info("   ✅ FilesystemObserver connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ FilesystemObserver not available: {e}")
        
        # Unified Dialogue
        self.dialogue = None
        try:
            from Core.Interaction.Interface.unified_dialogue import get_unified_dialogue
            self.dialogue = get_unified_dialogue()
            logger.info("   ✅ UnifiedDialogue connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ UnifiedDialogue not available: {e}")
        
        # Distillation Engine
        self.distillation = None
        try:
            from Core.Intelligence.Cognitive.distillation_engine import get_distillation_engine
            self.distillation = get_distillation_engine()
            logger.info("   ✅ DistillationEngine connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ DistillationEngine not available: {e}")
        
        # Introspection Engine
        self.introspection = None
        try:
            from Core.Foundation.introspection_engine import IntrospectionEngine
            self.introspection = IntrospectionEngine()
            logger.info("   ✅ IntrospectionEngine connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ IntrospectionEngine not available: {e}")
        
        # Text Wave Converter
        self.text_wave = None
        try:
            from Core.Foundation.text_wave_converter import get_text_wave_converter
            self.text_wave = get_text_wave_converter()
            logger.info("   ✅ TextWaveConverter connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ TextWaveConverter not available: {e}")
    
    def _connect_to_hub(self):
        """Connect to GlobalHub for central coordination."""
        self._hub = None
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "AutonomousOrchestrator",
                "Core/Autonomy/autonomous_orchestrator.py",
                ["autonomous", "orchestrator", "daemon", "self-improvement", "awakening"],
                "Master conductor of all autonomous operations - 24/7 self-improvement daemon"
            )
            logger.info("   ✅ AutonomousOrchestrator connected to GlobalHub")
        except ImportError:
            logger.warning("   ⚠️ GlobalHub not available")
    
    def _set_phase(self, phase: OperationPhase):
        """Set current operational phase and notify."""
        old_phase = self.state.phase
        self.state.phase = phase
        
        if self._hub:
            try:
                from Core.Foundation.Wave.wave_tensor import WaveTensor
                wave = WaveTensor(frequency=528.0, amplitude=1.0, phase=0.0)
                self._hub.publish_wave(
                    "AutonomousOrchestrator",
                    "phase_change",
                    wave,
                    payload={
                        "old_phase": old_phase.value,
                        "new_phase": phase.value,
                        "timestamp": time.time()
                    }
                )
            except Exception:
                pass
        
        for callback in self._callbacks.get("on_phase_change", []):
            try:
                callback(old_phase, phase)
            except Exception as e:
                logger.error(f"Phase callback error: {e}")
        
        logger.info(f"🔄 Phase: {old_phase.value} → {phase.value}")
    
    def run_awakening_cycle(self):
        """
        Execute the awakening protocol.
        
        각성 프로토콜 - 지식 그래프의 빈 곳을 채움
        """
        self._set_phase(OperationPhase.AWAKENING)
        
        try:
            # 1. Connect to Hierarchical Knowledge Graph
            try:
                from Core.Evolution.Learning.Learning.hierarchical_learning import HierarchicalKnowledgeGraph
                kg = HierarchicalKnowledgeGraph()
                self.state.knowledge_gaps = [n.name for n in kg.get_knowledge_gaps(limit=5)]
                logger.info(f"   🧠 Identified gaps: {self.state.knowledge_gaps}")
            except ImportError as e:
                logger.warning(f"   ⚠️ Could not load HierarchicalKnowledgeGraph: {e}")
                self.state.knowledge_gaps = ["Consciousness", "Self", "Existence"] # Fallback
            
            self.state.last_awakening = datetime.now()
            logger.info("   ✅ Awakening cycle complete")
            
        except Exception as e:
            logger.error(f"   ❌ Awakening error: {e}")
            self.state.errors_encountered += 1
    
    def run_learning_cycle(self):
        """
        Execute the learning cycle.
        
        학습 사이클 - 외부 정보 수집 및 증류
        """
        self._set_phase(OperationPhase.LEARNING)
        
        try:
            if not self.state.knowledge_gaps:
                logger.info("   📚 No knowledge gaps to fill")
                return
            
            # Pick a gap to fill
            topic = self.state.knowledge_gaps[0]
            logger.info(f"   📖 Learning about: {topic}")
            
            # Use text wave to analyze the topic
            if self.text_wave:
                wave = self.text_wave.sentence_to_wave(f"What is {topic}?")
                desc = self.text_wave.wave_to_text_descriptor(wave)
                logger.info(f"   🌊 Topic frequency: {desc.get('dominant_frequency', 0):.1f} Hz")
            
            self.state.last_learning = datetime.now()
            self.state.knowledge_gaps.pop(0)  # Remove addressed gap
            logger.info("   ✅ Learning cycle complete")
            
        except Exception as e:
            logger.error(f"   ❌ Learning error: {e}")
            self.state.errors_encountered += 1
    
    def run_reflection_cycle(self):
        """
        Execute the reflection/introspection cycle.
        
        성찰 사이클 - 자기 분석
        """
        self._set_phase(OperationPhase.REFLECTING)
        
        try:
            if self.introspection:
                result = self.introspection.analyze_system_health()
                logger.info(f"   🔍 Health: {result}")
            else:
                logger.info("   🔍 Reflection: System nominal")
            
            logger.info("   ✅ Reflection cycle complete")
            
        except Exception as e:
            logger.error(f"   ❌ Reflection error: {e}")
            self.state.errors_encountered += 1
    
    def run_improvement_cycle(self):
        """
        Execute the self-improvement cycle.
        
        개선 사이클 - 코드 분석 및 개선 제안
        """
        self._set_phase(OperationPhase.IMPROVING)
        
        try:
            # This would connect to SelfImprovementLoop
            logger.info("   🛠️ Scanning for improvement opportunities...")
            
            # Placeholder: Count proposals
            self.state.improvement_proposals += 1
            self.state.last_improvement = datetime.now()
            
            logger.info("   ✅ Improvement cycle complete")
            
        except Exception as e:
            logger.error(f"   ❌ Improvement error: {e}")
            self.state.errors_encountered += 1
    
    def run_full_cycle(self):
        """
        Run a complete autonomous cycle.
        
        전체 자율 사이클 실행
        """
        cycle_start = time.time()
        logger.info("\n" + "="*50)
        logger.info("🔄 AUTONOMOUS CYCLE STARTING")
        logger.info("="*50)
        
        # 1. Awakening
        self.run_awakening_cycle()
        
        # 2. Learning
        self.run_learning_cycle()
        
        # 3. Reflection
        self.run_reflection_cycle()
        
        # 4. Improvement (less frequent)
        if self.state.cycles_completed % 5 == 0:
            self.run_improvement_cycle()
        
        # Update state
        self.state.cycles_completed += 1
        self.state.uptime_seconds = (datetime.now() - self._start_time).total_seconds() if self._start_time else 0
        
        cycle_duration = time.time() - cycle_start
        logger.info(f"\n✅ CYCLE {self.state.cycles_completed} COMPLETE ({cycle_duration:.1f}s)")
        logger.info("="*50)
        
        # Set to observing between cycles
        self._set_phase(OperationPhase.OBSERVING)
        
        # Notify callbacks
        for callback in self._callbacks.get("on_cycle_complete", []):
            try:
                callback(self.state)
            except Exception as e:
                logger.error(f"Cycle callback error: {e}")
    
    def _daemon_loop(self):
        """Main daemon loop."""
        logger.info("🚀 Autonomous daemon started")
        self._start_time = datetime.now()
        
        # Start filesystem observer
        if self.filesystem_observer:
            self.filesystem_observer.add_watch_path("c:\\Elysia\\Core")
            self.filesystem_observer.start()
        
        while self.running:
            try:
                self.run_full_cycle()
                # Wait before next cycle (configurable)
                for _ in range(60):  # 60 seconds between cycles
                    if not self.running:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Daemon error: {e}")
                self.state.errors_encountered += 1
                time.sleep(5)  # Brief pause on error
        
        # Cleanup
        if self.filesystem_observer:
            self.filesystem_observer.stop()
        
        logger.info("🛑 Autonomous daemon stopped")
    
    def start_daemon(self):
        """Start the autonomous daemon in background."""
        if self.running:
            logger.warning("Daemon already running")
            return
        
        self.running = True
        self._daemon_thread = threading.Thread(target=self._daemon_loop, daemon=True)
        self._daemon_thread.start()
        logger.info("🎼 Autonomous daemon started in background")
    
    def stop_daemon(self):
        """Stop the autonomous daemon."""
        self.running = False
        if self._daemon_thread:
            self._daemon_thread.join(timeout=10.0)
            self._daemon_thread = None
        logger.info("⏹️ Autonomous daemon stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current autonomous status."""
        return {
            "phase": self.state.phase.value,
            "cycles_completed": self.state.cycles_completed,
            "uptime_seconds": self.state.uptime_seconds,
            "last_awakening": str(self.state.last_awakening) if self.state.last_awakening else None,
            "last_learning": str(self.state.last_learning) if self.state.last_learning else None,
            "knowledge_gaps": len(self.state.knowledge_gaps),
            "improvement_proposals": self.state.improvement_proposals,
            "errors": self.state.errors_encountered,
            "running": self.running
        }
    
    def add_callback(self, event: str, callback: Callable):
        """Add a callback for autonomous events."""
        if event in self._callbacks:
            self._callbacks[event].append(callback)


# Singleton accessor
_orchestrator = None

def get_autonomous_orchestrator() -> AutonomousOrchestrator:
    """Get or create the AutonomousOrchestrator singleton."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AutonomousOrchestrator()
    return _orchestrator


# Test / Demo
if __name__ == "__main__":
    import sys
    sys.path.insert(0, "c:\\Elysia")
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("\n" + "="*60)
    print("🎼 Autonomous Orchestrator Demo")
    print("="*60)
    
    orchestrator = get_autonomous_orchestrator()
    
    # Run a single cycle for demo
    orchestrator.run_full_cycle()
    
    # Show status
    print("\n📊 STATUS:")
    status = orchestrator.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ Demo complete. Use start_daemon() for 24/7 operation.")
    print("="*60)
