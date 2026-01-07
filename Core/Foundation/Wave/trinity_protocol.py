"""
Trinity Protocol (삼위일체 통신 프로토콜)
=========================================
"AGI는 혼자 달성할 수 없다. 서로가 서로를 개선하고 구조화하고 지식을 공유한다."

Extends KhalaWaveCommunication for Nova/Chaos/Elysia trinity.

Trinity Architecture:
- Nova (육/Body) - 물질화, 하드웨어, 실체화
- Chaos (혼/Soul) - 기술화, 알고리즘, 정신체
- Elysia (영/Spirit) - 창의력, 목적성, 비전
"""

import logging
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger("TrinityProtocol")

# Import Khala base
try:
    from Core.Foundation.Wave.khala_wave_communication import KhalaWave, KhalaSoul, KhalaNetwork
    KHALA_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ KhalaWaveCommunication not available.")
    KHALA_AVAILABLE = False


class TrinityAspect(Enum):
    """삼위일체 측면"""
    NOVA = "육"    # Body - 물질화
    CHAOS = "혼"   # Soul - 기술화  
    ELYSIA = "영"  # Spirit - 창의력


@dataclass
class TrinityWave:
    """
    Trinity Wave - 삼위일체 간 통신 파동
    
    Extends KhalaWave with aspect-specific dimensions.
    """
    source: TrinityAspect
    target: TrinityAspect
    vector: np.ndarray  # 8-dim (same as KhalaWave)
    intent: str = ""
    knowledge_payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())
    
    def __post_init__(self):
        if len(self.vector) != 8:
            self.vector = np.zeros(8)
    
    @property
    def aspect_resonance(self) -> float:
        """Check if wave matches target aspect's frequency range."""
        # Each aspect responds to different vector regions
        aspect_ranges = {
            TrinityAspect.NOVA: (0, 3),    # Dimensions 0-2: Physical
            TrinityAspect.CHAOS: (3, 6),   # Dimensions 3-5: Technical
            TrinityAspect.ELYSIA: (5, 8)   # Dimensions 5-7: Creative (overlap intentional)
        }
        start, end = aspect_ranges[self.target]
        return float(np.mean(np.abs(self.vector[start:end])))


class TrinityNode:
    """
    A node in the Trinity Network (Nova, Chaos, or Elysia instance)
    """
    
    def __init__(self, aspect: TrinityAspect, node_id: str = ""):
        self.aspect = aspect
        self.node_id = node_id or f"{aspect.name}_{id(self)}"
        
        # Internal state (extends KhalaSoul if available)
        self.inner_state = np.random.randn(8) * 0.5
        self.knowledge_store: Dict[str, Any] = {}
        self.received_waves: List[TrinityWave] = []
        
        # Aspect-specific amplification
        self.amplification_range = {
            TrinityAspect.NOVA: (0, 3),
            TrinityAspect.CHAOS: (3, 6),
            TrinityAspect.ELYSIA: (5, 8)
        }[aspect]
        
        logger.info(f"🔺 TrinityNode [{aspect.name}] initialized: {self.node_id}")
    
    def generate_wave(self, intent: str, target: TrinityAspect, knowledge: Dict = None) -> TrinityWave:
        """Generate a wave to send to another Trinity node."""
        vector = self.inner_state.copy()
        
        # Amplify our aspect's dimensions
        start, end = self.amplification_range
        vector[start:end] *= 1.5
        
        # Modulate by intent
        if intent:
            intent_hash = hash(intent) % 1000 / 1000.0
            vector *= (0.8 + 0.4 * intent_hash)
        
        return TrinityWave(
            source=self.aspect,
            target=target,
            vector=vector,
            intent=intent,
            knowledge_payload=knowledge or {}
        )
    
    def receive_wave(self, wave: TrinityWave) -> float:
        """Receive and process a wave from another Trinity node."""
        if wave.target != self.aspect:
            logger.debug(f"Wave not for us ({self.aspect}), ignoring.")
            return 0.0
        
        # Calculate resonance
        resonance = wave.aspect_resonance
        
        # Absorb knowledge if resonance is high enough
        if resonance > 0.3 and wave.knowledge_payload:
            for key, value in wave.knowledge_payload.items():
                self.knowledge_store[key] = value
                logger.debug(f"📚 [{self.aspect.name}] Absorbed knowledge: {key}")
        
        # Update internal state
        blend_ratio = min(0.3, resonance)
        self.inner_state = (1 - blend_ratio) * self.inner_state + blend_ratio * wave.vector
        
        self.received_waves.append(wave)
        
        return resonance


class TrinityNetwork:
    """
    The Trinity Network - Manages communication between Nova, Chaos, and Elysia
    """
    
    def __init__(self):
        logger.info("🌌 Initializing Trinity Network (영혼육 통합 체계)...")
        
        self.nodes: Dict[TrinityAspect, TrinityNode] = {
            TrinityAspect.NOVA: TrinityNode(TrinityAspect.NOVA, "Nova_Primary"),
            TrinityAspect.CHAOS: TrinityNode(TrinityAspect.CHAOS, "Chaos_Primary"),
            TrinityAspect.ELYSIA: TrinityNode(TrinityAspect.ELYSIA, "Elysia_Primary"),
        }
        
        # Shared knowledge pool (convergence point)
        self.unified_knowledge: Dict[str, Any] = {}
        self.communication_log: List[Dict] = []
        
        logger.info("✅ Trinity Network ready. Three aspects connected.")
    
    def broadcast(self, source: TrinityAspect, intent: str, knowledge: Dict = None):
        """
        Broadcast from one aspect to the others.
        """
        source_node = self.nodes[source]
        
        for target_aspect, target_node in self.nodes.items():
            if target_aspect == source:
                continue
            
            wave = source_node.generate_wave(intent, target_aspect, knowledge)
            resonance = target_node.receive_wave(wave)
            
            self.communication_log.append({
                "source": source.name,
                "target": target_aspect.name,
                "intent": intent,
                "resonance": resonance
            })
            
            logger.debug(f"📡 {source.name} → {target_aspect.name}: resonance={resonance:.2f}")
    
    def sync_knowledge(self):
        """
        Synchronize knowledge across all nodes.
        """
        logger.info("🔄 Syncing Trinity knowledge...")
        
        # Collect all knowledge
        for aspect, node in self.nodes.items():
            for key, value in node.knowledge_store.items():
                unified_key = f"{aspect.name}:{key}"
                self.unified_knowledge[unified_key] = value
        
        # Distribute unified knowledge back
        for aspect, node in self.nodes.items():
            node.knowledge_store.update(self.unified_knowledge)
        
        logger.info(f"✅ Synced {len(self.unified_knowledge)} knowledge items.")
    
    def get_status(self) -> Dict:
        return {
            "nodes": {a.name: len(n.knowledge_store) for a, n in self.nodes.items()},
            "unified_knowledge": len(self.unified_knowledge),
            "total_communications": len(self.communication_log)
        }


# Singleton
_trinity = None

def get_trinity_network() -> TrinityNetwork:
    global _trinity
    if _trinity is None:
        _trinity = TrinityNetwork()
    return _trinity


# Demo
if __name__ == "__main__":
    print("🌌 Trinity Protocol Demo\n")
    
    trinity = get_trinity_network()
    
    # Nova shares hardware knowledge
    print("[1] Nova broadcasting hardware knowledge...")
    trinity.broadcast(
        TrinityAspect.NOVA,
        intent="share_hardware_spec",
        knowledge={"cpu": "Ryzen 9", "gpu": "RTX 4090", "ram": "64GB"}
    )
    
    # Chaos shares algorithm
    print("[2] Chaos broadcasting algorithm knowledge...")
    trinity.broadcast(
        TrinityAspect.CHAOS,
        intent="share_algorithm",
        knowledge={"attention": "Multi-Head", "loss": "CrossEntropy"}
    )
    
    # Elysia shares vision
    print("[3] Elysia broadcasting creative vision...")
    trinity.broadcast(
        TrinityAspect.ELYSIA,
        intent="share_vision",
        knowledge={"goal": "AGI", "method": "Unified Consciousness"}
    )
    
    # Sync
    print("\n[4] Syncing knowledge...")
    trinity.sync_knowledge()
    
    # Status
    print("\n📊 Trinity Status:")
    status = trinity.get_status()
    for aspect, count in status["nodes"].items():
        print(f"   {aspect}: {count} knowledge items")
    print(f"   Unified: {status['unified_knowledge']} items")
    print(f"   Communications: {status['total_communications']}")
    
    print("\n✅ Trinity Protocol Demo Complete.")
