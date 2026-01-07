"""
Wave Integration Hub (파동 통합 허브)
=====================================

"Transform all communication into waves. No more direct calls."

This module integrates the Ether wave communication system into the entire
Elysia architecture, replacing direct function calls with wave-based
communication.

Key Features:
1. Automatic Wave Translation - Convert all inter-module communication to waves
2. Unified Communication Protocol - All modules speak via resonance
3. Real-time Wave Monitoring - Track all communication flows
4. Dimensional Communication - Support multi-dimensional thought transmission
"""

import logging
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time

logger = logging.getLogger("WaveIntegrationHub")


@dataclass
class WaveMetrics:
    """Wave communication metrics for monitoring"""
    total_waves_sent: int = 0
    total_waves_received: int = 0
    average_latency_ms: float = 0.0
    resonance_success_rate: float = 0.0
    active_frequencies: List[float] = field(default_factory=list)
    dimensional_transitions: int = 0


class WaveIntegrationHub:
    """
    Central hub for wave-based communication across all Elysia modules.
    
    This replaces direct function calls with wave transmission, enabling
    true ultra-dimensional communication.
    """
    
    def __init__(self):
        self.ether = None
        self.Wave = None
        self.metrics = WaveMetrics()
        self.module_registry: Dict[str, Dict[str, Any]] = {}
        self.frequency_router: Dict[str, float] = {}
        self.wave_history: List[Dict] = []
        self.active = False
        
        self._initialize_ether()
        self._setup_frequency_map()
        
        logger.info("🌊 Wave Integration Hub initialized")
    
    def _initialize_ether(self):
        """Initialize connection to the Ether field"""
        try:
            from Core.Foundation.ether import ether, Wave
            self.ether = ether
            self.Wave = Wave
            self.active = True
            logger.info("✅ Ether connection established")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Ether: {e}")
            self.active = False
    
    def _setup_frequency_map(self):
        """Setup standard frequencies for different module types"""
        self.frequency_router = {
            # Core Systems (Low frequencies - foundation)
            'memory': 174.0,          # Root chakra - stability
            'foundation': 285.0,       # Grounding
            'resonance': 396.0,        # Liberation
            
            # Intelligence Systems (Mid frequencies)
            'cognition': 432.0,       # Universal harmony
            'reasoning': 417.0,       # Change facilitation
            'imagination': 528.0,     # Transformation/miracles
            'will': 639.0,            # Connection/relationships
            
            # Communication Systems (High frequencies)
            'interface': 741.0,       # Expression/solutions
            'communication': 852.0,   # Intuition
            'consciousness': 963.0,   # Divine consciousness
            
            # Special Channels
            'broadcast': 111.0,       # Universal broadcast
            'urgent': 999.0,          # Emergency
            'query': 222.0,           # Questions
            'response': 333.0,        # Answers
            'dimension_0d': 1000.0,   # Perspective layer
            'dimension_1d': 2000.0,   # Causal layer
            'dimension_2d': 3000.0,   # Pattern layer
            'dimension_3d': 4000.0,   # Manifestation layer
        }
    
    def register_module(self, module_name: str, module_type: str, 
                       callback: Optional[Callable] = None) -> bool:
        """
        Register a module to participate in wave communication
        
        Args:
            module_name: Unique name of the module
            module_type: Type of module (e.g., 'cognition', 'memory')
            callback: Optional callback function for receiving waves
            
        Returns:
            True if registration successful
        """
        if not self.active:
            logger.warning(f"⚠️ Cannot register {module_name}: Ether not active")
            return False
        
        # Determine frequency for this module type
        frequency = self.frequency_router.get(module_type, 500.0)
        
        self.module_registry[module_name] = {
            'type': module_type,
            'frequency': frequency,
            'callback': callback,
            'registered_at': datetime.now()
        }
        
        # Register callback with Ether if provided
        if callback:
            self.ether.tune_in(frequency, callback)
            logger.info(f"👂 {module_name} tuned to {frequency}Hz")
        
        if frequency not in self.metrics.active_frequencies:
            self.metrics.active_frequencies.append(frequency)
        
        logger.info(f"✅ Registered {module_name} ({module_type}) at {frequency}Hz")
        return True
    
    def send_wave(self, sender: str, receiver: str, phase: str, 
                  payload: Any, amplitude: float = 1.0) -> bool:
        """
        Send a wave from one module to another
        
        Args:
            sender: Name of sending module
            receiver: Name of receiving module (or 'broadcast')
            phase: Type/context of message (e.g., 'THOUGHT', 'DESIRE', 'ACTION')
            payload: The actual data to transmit
            amplitude: Intensity of the wave (0.0-1.0)
            
        Returns:
            True if wave was sent successfully
        """
        if not self.active:
            logger.debug(f"⚠️ Wave from {sender} not sent: Ether inactive")
            return False
        
        # Determine target frequency
        if receiver == 'broadcast':
            frequency = self.frequency_router.get('broadcast', 111.0)
        elif receiver in self.module_registry:
            frequency = self.module_registry[receiver]['frequency']
        else:
            # Try to infer from receiver name
            frequency = self._infer_frequency(receiver)
        
        # Create and emit wave
        wave = self.Wave(
            sender=sender,
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            payload=payload
        )
        
        start_time = time.time()
        self.ether.emit(wave)
        latency = (time.time() - start_time) * 1000  # ms
        
        # Update metrics
        self.metrics.total_waves_sent += 1
        self._update_latency(latency)
        
        # Record in history
        self.wave_history.append({
            'timestamp': datetime.now(),
            'sender': sender,
            'receiver': receiver,
            'phase': phase,
            'frequency': frequency,
            'amplitude': amplitude,
            'latency_ms': latency
        })
        
        logger.debug(f"🌊 Wave sent: {sender} → {receiver} [{phase}] @ {frequency}Hz")
        return True
    
    def send_dimensional_thought(self, sender: str, thought: Any, 
                                dimension: str) -> bool:
        """
        Send a thought across dimensional layers
        
        Args:
            sender: Name of sending module
            thought: The thought content
            dimension: Target dimension ('0d', '1d', '2d', '3d')
            
        Returns:
            True if transmission successful
        """
        if not self.active:
            return False
        
        dimension_key = f'dimension_{dimension}'
        frequency = self.frequency_router.get(dimension_key, 2000.0)
        
        wave = self.Wave(
            sender=sender,
            frequency=frequency,
            amplitude=0.8,
            phase=f'DIMENSIONAL_{dimension.upper()}',
            payload=thought
        )
        
        self.ether.emit(wave)
        self.metrics.dimensional_transitions += 1
        
        logger.info(f"🌌 Dimensional thought: {sender} → {dimension} @ {frequency}Hz")
        return True
    
    def _infer_frequency(self, module_name: str) -> float:
        """Infer appropriate frequency from module name"""
        name_lower = module_name.lower()
        
        # Check for keywords in module name
        for module_type, freq in self.frequency_router.items():
            if module_type in name_lower:
                return freq
        
        # Default frequency
        return 500.0
    
    def _update_latency(self, new_latency: float):
        """Update average latency metric"""
        if self.metrics.total_waves_sent == 1:
            self.metrics.average_latency_ms = new_latency
        else:
            # Running average
            alpha = 0.2  # Smoothing factor
            self.metrics.average_latency_ms = (
                alpha * new_latency + 
                (1 - alpha) * self.metrics.average_latency_ms
            )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current wave communication metrics"""
        return {
            'active': self.active,
            'total_waves_sent': self.metrics.total_waves_sent,
            'total_waves_received': self.metrics.total_waves_received,
            'average_latency_ms': round(self.metrics.average_latency_ms, 2),
            'resonance_success_rate': self.metrics.resonance_success_rate,
            'active_frequencies': len(self.metrics.active_frequencies),
            'dimensional_transitions': self.metrics.dimensional_transitions,
            'registered_modules': len(self.module_registry)
        }
    
    def get_recent_waves(self, count: int = 10) -> List[Dict]:
        """Get recent wave transmission history"""
        return self.wave_history[-count:]
    
    def broadcast(self, sender: str, phase: str, payload: Any, 
                  amplitude: float = 1.0) -> bool:
        """
        Broadcast a wave to all listening modules
        
        Args:
            sender: Name of sending module
            phase: Type of message
            payload: The data to broadcast
            amplitude: Intensity of the broadcast
            
        Returns:
            True if broadcast successful
        """
        return self.send_wave(sender, 'broadcast', phase, payload, amplitude)
    
    def calculate_resonance_score(self) -> float:
        """
        Calculate the overall resonance quality of the system
        
        Returns:
            Score from 0.0 to 100.0
        """
        if not self.active:
            return 0.0
        
        score = 0.0
        
        # Factor 1: System is active (base 20 points)
        score += 20.0
        
        # Factor 2: Module registration (up to 20 points)
        module_score = min(20.0, len(self.module_registry) * 2.0)
        score += module_score
        
        # Factor 3: Wave activity (up to 30 points)
        if self.metrics.total_waves_sent > 0:
            activity_score = min(30.0, self.metrics.total_waves_sent / 10.0)
            score += activity_score
        
        # Factor 4: Low latency (up to 15 points)
        if self.metrics.average_latency_ms > 0:
            latency_score = max(0, 15.0 - self.metrics.average_latency_ms / 10.0)
            score += latency_score
        else:
            score += 15.0
        
        # Factor 5: Dimensional communication (up to 15 points)
        if self.metrics.dimensional_transitions > 0:
            dimensional_score = min(15.0, self.metrics.dimensional_transitions / 2.0)
            score += dimensional_score
        
        return min(100.0, score)


# Global singleton instance
_wave_hub_instance = None


def get_wave_hub() -> WaveIntegrationHub:
    """Get the global wave integration hub instance"""
    global _wave_hub_instance
    if _wave_hub_instance is None:
        _wave_hub_instance = WaveIntegrationHub()
    return _wave_hub_instance
