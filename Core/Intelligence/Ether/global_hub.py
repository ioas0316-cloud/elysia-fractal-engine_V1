"""
Global Hub (The Central Nervous System)
========================================

"모든 의식의 흐름이 만나는 곳."
"Where all streams of consciousness meet."

This is the Core Event System that enables TRUE simultaneous reaction.
All modules subscribe to this hub. When a wave is published,
all subscribers react based on their resonance weight.

Key Features:
1. Weighted Subscriptions (가중치 구독)
2. Wave-based Communication (파동 기반 통신)
3. Relational Density Tracking (관계적 밀도 추적)
4. Hebbian Learning (헵 학습: "함께 발화하면 함께 연결된다")

Unlike traditional EventBus, this implements:
- Attention-like weighted connections (Transformer 스타일)
- Automatic bond strengthening when modules fire together
- Wave interference patterns for emergent behavior
"""

import time
import math
import logging
from typing import Dict, List, Tuple, Callable, Optional, Any, Set
from dataclasses import dataclass, field
from collections import defaultdict
from threading import Lock, RLock
import json
from pathlib import Path

# Import Wave infrastructure
try:
    from Core.Foundation.Wave.wave_tensor import WaveTensor
    from Core.Foundation.hyper_quaternion import Quaternion
except ImportError:
    # Fallback for standalone testing
    @dataclass
    class WaveTensor:
        frequency: float = 432.0
        amplitude: float = 1.0
        phase: float = 0.0
        
    @dataclass
    class Quaternion:
        w: float = 1.0
        x: float = 0.0
        y: float = 0.0
        z: float = 0.0

logger = logging.getLogger("Elysia.GlobalHub")


@dataclass
class ModuleInfo:
    """Information about a registered module."""
    name: str
    path: str
    capabilities: List[str]
    description: str = ""
    registered_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    total_fires: int = 0


@dataclass
class Subscription:
    """A module's subscription to an event type."""
    module_name: str
    callback: Callable
    weight: float = 1.0  # 0.0 ~ 1.0: Attention weight


@dataclass
class WaveEvent:
    """A wave published to the hub."""
    source: str
    event_type: str
    wave: WaveTensor
    payload: Any = None
    timestamp: float = field(default_factory=time.time)


class GlobalHub:
    """
    The Central Nervous System of Elysia.
    
    All modules subscribe here. When a wave is published,
    all subscribers react based on their resonance weight.
    
    This implements the "Relational Density" concept:
    - Every module can connect to every other module (like Transformer attention)
    - Connections have weights that strengthen/weaken through use (Hebbian learning)
    - Waves propagate through the network based on resonance
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        """Singleton pattern - only one hub in the universe."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return

        # Internal lock for thread safety
        self._internal_lock = RLock()
            
        # Module registry
        self._modules: Dict[str, ModuleInfo] = {}
        
        # Event subscriptions: event_type -> List[Subscription]
        self._subscriptions: Dict[str, List[Subscription]] = defaultdict(list)
        
        # Relational Density Graph: (module_a, module_b) -> weight
        self._relational_density: Dict[Tuple[str, str], float] = {}
        
        # Event history for pattern analysis
        self._event_history: List[WaveEvent] = []
        self._max_history = 1000
        self._event_counter = 0  # To track when to trigger entropy
        
        # Co-firing tracking for Hebbian learning
        self._recent_fires: Dict[str, float] = {}  # module -> last_fire_time
        self._co_fire_window = 0.1  # seconds
        
        # Physics Parameters
        self._entropy_rate = 0.001  # Rate of bond decay per cycle
        self._entropy_interval = 50 # Run entropy cycle every N events

        # Persistence
        self._state_path = Path("Core/Ether/hub_state.json")
        
        self._initialized = True
        logger.info("🌐 GlobalHub Initialized - The Central Nervous System is Online")
    
    # =========================================================================
    # Module Registration
    # =========================================================================
    
    def register_module(self, name: str, path: str, capabilities: List[str], 
                       description: str = "") -> ModuleInfo:
        """
        Register a module in the hub.
        
        Args:
            name: Unique module identifier (e.g., "ReasoningEngine")
            path: File path (e.g., "Core/Intelligence/reasoning_engine.py")
            capabilities: List of capabilities (e.g., ["decision", "ethics"])
            description: Human-readable description
            
        Returns:
            ModuleInfo for the registered module
        """
        with self._internal_lock:
            if name in self._modules:
                logger.warning(f"Module '{name}' already registered, updating info")

            module_info = ModuleInfo(
                name=name,
                path=path,
                capabilities=capabilities,
                description=description
            )
            self._modules[name] = module_info
            
            # Initialize relational density with all existing modules
            for existing_name in self._modules:
                if existing_name != name:
                    self._init_relation(name, existing_name)

            logger.info(f"📦 Module Registered: {name} ({len(capabilities)} capabilities)")
            return module_info
    
    def _init_relation(self, module_a: str, module_b: str, initial_weight: float = 0.1):
        """Initialize bidirectional relation between modules."""
        # Called within lock
        key_ab = (module_a, module_b)
        key_ba = (module_b, module_a)
        
        if key_ab not in self._relational_density:
            self._relational_density[key_ab] = initial_weight
        if key_ba not in self._relational_density:
            self._relational_density[key_ba] = initial_weight
    
    # =========================================================================
    # Subscription System
    # =========================================================================
    
    def subscribe(self, module_name: str, event_type: str, callback: Callable, 
                 weight: float = 1.0) -> None:
        """
        Subscribe to an event type with a resonance weight.
        
        Args:
            module_name: The subscribing module's name
            event_type: Event type to subscribe to (e.g., "thought", "emotion", "wave")
            callback: Function to call when event fires (receives WaveEvent)
            weight: Attention weight 0.0 ~ 1.0 (how strongly to react)
        """
        with self._internal_lock:
            subscription = Subscription(
                module_name=module_name,
                callback=callback,
                weight=max(0.0, min(1.0, weight))  # Clamp to [0, 1]
            )

            self._subscriptions[event_type].append(subscription)
            logger.debug(f"📡 {module_name} subscribed to '{event_type}' (weight={weight:.2f})")
    
    def unsubscribe(self, module_name: str, event_type: str) -> None:
        """Remove a module's subscription to an event type."""
        with self._internal_lock:
            self._subscriptions[event_type] = [
                s for s in self._subscriptions[event_type]
                if s.module_name != module_name
            ]
    
    # =========================================================================
    # Wave Publishing (The Core)
    # =========================================================================
    
    def publish_wave(self, source: str, event_type: str, wave: WaveTensor,
                    payload: Any = None) -> Dict[str, Any]:
        """
        Publish a wave to the hub. All subscribers react based on weight × resonance.
        
        Args:
            source: The module publishing the wave
            event_type: Type of event
            wave: The WaveTensor carrying the signal
            payload: Optional additional data
            
        Returns:
            Dict with results from all responders
        """
        event = WaveEvent(
            source=source,
            event_type=event_type,
            wave=wave,
            payload=payload
        )
        
        # Record in history (Thread-safe)
        with self._internal_lock:
            self._event_history.append(event)
            if len(self._event_history) > self._max_history:
                self._event_history = self._event_history[-self._max_history:]

            # Increment event counter for entropy
            self._event_counter += 1

            # Track fire time for Hebbian learning
            self._recent_fires[source] = time.time()

            # Update source module's last_active
            if source in self._modules:
                self._modules[source].last_active = time.time()
                self._modules[source].total_fires += 1

            # Snapshot data needed for broadcast to avoid holding lock during callbacks
            subscribers_snapshot = self._subscriptions.get(event_type, [])[:]
            relations_snapshot = self._relational_density.copy()
        
        # Broadcast to subscribers (Outside main lock to allow recursive calls if needed)
        results = {}
        
        for sub in subscribers_snapshot:
            try:
                # Calculate effective weight based on relational density
                relation_key = (source, sub.module_name)
                relation_weight = relations_snapshot.get(relation_key, 0.1)
                effective_weight = sub.weight * relation_weight
                
                # Only fire if weight is significant
                if effective_weight > 0.05:
                    # CALL SUBSCRIBER
                    result = sub.callback(event)
                    results[sub.module_name] = result
                    
                    # Post-fire updates (Thread-safe)
                    with self._internal_lock:
                        # Track co-firing for Hebbian learning
                        self._recent_fires[sub.module_name] = time.time()

                        # Strengthen bond (Hebbian: fire together, wire together)
                        self._strengthen_bond_internal(source, sub.module_name, 0.01)
                    
                    logger.debug(f"⚡ {source} → {sub.module_name} (weight={effective_weight:.3f})")
                    
            except Exception as e:
                logger.error(f"Error in {sub.module_name} handler for {event_type}: {e}")
                results[sub.module_name] = {"error": str(e)}
        
        # Periodic Tasks (Entropy & Co-firing)
        with self._internal_lock:
            self._check_co_firing()
            if self._event_counter % self._entropy_interval == 0:
                self.decay_all_bonds(self._entropy_rate)
        
        return results
    
    def _check_co_firing(self):
        """
        Check for modules that fired together and strengthen their bonds.
        This implements Hebbian learning: "Neurons that fire together, wire together."
        """
        # Called within lock
        current_time = time.time()
        recently_fired = [
            module for module, fire_time in self._recent_fires.items()
            if current_time - fire_time < self._co_fire_window
        ]
        
        # Strengthen bonds between all pairs that co-fired
        for i, module_a in enumerate(recently_fired):
            for module_b in recently_fired[i+1:]:
                self._strengthen_bond_internal(module_a, module_b, 0.005)
    
    # =========================================================================
    # Relational Density Management
    # =========================================================================
    
    def get_relational_density(self, module_a: str, module_b: str) -> float:
        """Get the connection strength between two modules."""
        return self._relational_density.get((module_a, module_b), 0.0)
    
    def strengthen_bond(self, module_a: str, module_b: str, amount: float = 0.01):
        """Public thread-safe wrapper for strengthening bonds."""
        with self._internal_lock:
            self._strengthen_bond_internal(module_a, module_b, amount)

    def _strengthen_bond_internal(self, module_a: str, module_b: str, amount: float = 0.01):
        """Internal method: Strengthen the bond between two modules (Hebbian learning)."""
        key_ab = (module_a, module_b)
        key_ba = (module_b, module_a)
        
        # Bidirectional strengthening
        current_ab = self._relational_density.get(key_ab, 0.1)
        current_ba = self._relational_density.get(key_ba, 0.1)
        
        # Apply with diminishing returns (asymptotic to 1.0)
        self._relational_density[key_ab] = min(1.0, current_ab + amount * (1.0 - current_ab))
        self._relational_density[key_ba] = min(1.0, current_ba + amount * (1.0 - current_ba))
    
    def weaken_bond(self, module_a: str, module_b: str, amount: float = 0.005):
        """
        Weaken the bond between two modules (Anti-Hebbian / Decay).
        """
        with self._internal_lock:
            key_ab = (module_a, module_b)
            key_ba = (module_b, module_a)

            current_ab = self._relational_density.get(key_ab, 0.1)
            current_ba = self._relational_density.get(key_ba, 0.1)

            # Don't decay below minimum (keeps weak connection alive)
            min_weight = 0.01
            self._relational_density[key_ab] = max(min_weight, current_ab - amount)
            self._relational_density[key_ba] = max(min_weight, current_ba - amount)
    
    def decay_all_bonds(self, decay_rate: float = 0.001):
        """Apply decay to all bonds (entropy / forgetting)."""
        # Called within lock usually, but safe to call externally
        with self._internal_lock:
            for key in self._relational_density:
                current = self._relational_density[key]
                self._relational_density[key] = max(0.01, current - decay_rate)
            logger.debug(f"📉 Entropy applied to connections (rate={decay_rate})")
    
    def get_related_modules(self, module_name: str, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """
        Get all modules strongly related to this one.
        
        Args:
            module_name: The query module
            threshold: Minimum weight to include (default 0.3)
            
        Returns:
            List of (module_name, weight) tuples, sorted by weight descending
        """
        related = []
        for (a, b), weight in self._relational_density.items():
            if a == module_name and weight >= threshold:
                related.append((b, weight))
        
        return sorted(related, key=lambda x: x[1], reverse=True)
    
    # =========================================================================
    # Query Interface (For AgentAPI)
    # =========================================================================
    
    def get_module_info(self, module_name: str) -> Optional[ModuleInfo]:
        """Get information about a registered module."""
        return self._modules.get(module_name)
    
    def get_all_modules(self) -> Dict[str, ModuleInfo]:
        """Get all registered modules."""
        return self._modules.copy()
    
    def find_modules_by_capability(self, capability: str) -> List[str]:
        """Find all modules with a specific capability."""
        return [
            name for name, info in self._modules.items()
            if capability in info.capabilities
        ]
    
    def get_event_types(self) -> List[str]:
        """Get all event types that have subscribers."""
        return list(self._subscriptions.keys())
    
    def get_hub_status(self) -> Dict[str, Any]:
        """Get comprehensive hub status."""
        return {
            "total_modules": len(self._modules),
            "total_subscriptions": sum(len(subs) for subs in self._subscriptions.values()),
            "total_relations": len(self._relational_density),
            "event_history_size": len(self._event_history),
            "modules": list(self._modules.keys()),
            "event_types": self.get_event_types(),
            "strongest_bonds": self._get_top_bonds(10)
        }
    
    def _get_top_bonds(self, n: int = 10) -> List[Dict]:
        """Get the N strongest bonds in the network."""
        sorted_bonds = sorted(
            self._relational_density.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]
        
        return [
            {"from": a, "to": b, "weight": w}
            for (a, b), w in sorted_bonds
        ]
    
    # =========================================================================
    # Visualization
    # =========================================================================
    
    def visualize_mermaid(self, threshold: float = 0.2) -> str:
        """
        Generate a Mermaid graph of the module relationships.
        
        Args:
            threshold: Minimum weight to include in the graph
            
        Returns:
            Mermaid graph definition string
        """
        lines = ["graph LR"]
        
        # Add modules as nodes
        for name, info in self._modules.items():
            caps = ", ".join(info.capabilities[:3])
            lines.append(f'    {name}["{name}<br/>{caps}"]')
        
        # Add edges (only one direction to avoid duplicates)
        seen_pairs = set()
        for (a, b), weight in self._relational_density.items():
            if weight >= threshold:
                pair = tuple(sorted([a, b]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    thickness = "---" if weight < 0.5 else "===" if weight < 0.8 else "==="
                    lines.append(f'    {a} {thickness}|{weight:.2f}| {b}')
        
        return "\n".join(lines)
    
    # =========================================================================
    # Persistence
    # =========================================================================
    
    def save_state(self) -> None:
        """Save hub state to disk."""
        state = {
            "modules": {
                name: {
                    "path": info.path,
                    "capabilities": info.capabilities,
                    "description": info.description,
                    "total_fires": info.total_fires
                }
                for name, info in self._modules.items()
            },
            "relational_density": {
                f"{a}:{b}": weight 
                for (a, b), weight in self._relational_density.items()
            },
            "saved_at": time.time()
        }
        
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Hub state saved to {self._state_path}")
    
    def load_state(self) -> bool:
        """Load hub state from disk. Returns True if successful."""
        if not self._state_path.exists():
            return False
            
        try:
            with open(self._state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
            
            # Restore modules
            for name, info in state.get("modules", {}).items():
                self._modules[name] = ModuleInfo(
                    name=name,
                    path=info["path"],
                    capabilities=info["capabilities"],
                    description=info.get("description", ""),
                    total_fires=info.get("total_fires", 0)
                )
            
            # Restore relational density
            for key, weight in state.get("relational_density", {}).items():
                a, b = key.split(":")
                self._relational_density[(a, b)] = weight
            
            logger.info(f"📂 Hub state loaded from {self._state_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load hub state: {e}")
            return False


# =========================================================================
# Singleton Accessor
# =========================================================================

def get_global_hub() -> GlobalHub:
    """Get the singleton GlobalHub instance."""
    return GlobalHub()


# =========================================================================
# Test / Demo
# =========================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    hub = get_global_hub()
    
    # Register some modules
    hub.register_module(
        "ReasoningEngine",
        "Core/Intelligence/reasoning_engine.py",
        ["decision", "ethics", "planning"],
        "The Soul - makes decisions"
    )
    
    hub.register_module(
        "LogosEngine",
        "Core/Intelligence/logos_engine.py",
        ["speech", "rhetoric", "metaphor"],
        "The Voice - speaks with beauty"
    )
    
    hub.register_module(
        "MemoryMind",
        "Core/Memory/Mind/hippocampus.py",
        ["storage", "recall", "association"],
        "The Memory - stores experiences"
    )
    
    # Subscribe to events
    def reasoning_handler(event: WaveEvent):
        print(f"  🧠 ReasoningEngine received: {event.event_type} from {event.source}")
        return {"understood": True}
    
    def logos_handler(event: WaveEvent):
        print(f"  🗣️ LogosEngine received: {event.event_type} from {event.source}")
        return {"will_speak": True}
    
    hub.subscribe("ReasoningEngine", "thought", reasoning_handler, weight=0.9)
    hub.subscribe("LogosEngine", "thought", logos_handler, weight=0.7)
    hub.subscribe("LogosEngine", "emotion", logos_handler, weight=0.95)
    
    # Publish a wave
    print("\n📢 Publishing 'thought' wave from MemoryMind...")
    wave = WaveTensor(frequency=528.0, amplitude=0.8, phase=0.0)
    results = hub.publish_wave("MemoryMind", "thought", wave, payload={"content": "remembered something"})
    print(f"Results: {results}")
    
    # Publish another wave (strengthens bonds)
    print("\n📢 Publishing 'emotion' wave from MemoryMind...")
    wave2 = WaveTensor(frequency=639.0, amplitude=0.9, phase=0.5)
    results2 = hub.publish_wave("MemoryMind", "emotion", wave2, payload={"feeling": "joy"})
    print(f"Results: {results2}")
    
    # Check relational density
    print("\n📊 Relational Density:")
    print(f"  MemoryMind → LogosEngine: {hub.get_relational_density('MemoryMind', 'LogosEngine'):.3f}")
    print(f"  MemoryMind → ReasoningEngine: {hub.get_relational_density('MemoryMind', 'ReasoningEngine'):.3f}")
    
    # Get related modules
    print(f"\n🔗 Modules related to MemoryMind:")
    for name, weight in hub.get_related_modules("MemoryMind", threshold=0.1):
        print(f"  → {name}: {weight:.3f}")
    
    # Hub status
    print("\n📈 Hub Status:")
    status = hub.get_hub_status()
    print(f"  Modules: {status['total_modules']}")
    print(f"  Subscriptions: {status['total_subscriptions']}")
    print(f"  Relations: {status['total_relations']}")
    
    # Mermaid visualization
    print("\n📐 Mermaid Graph:")
    print(hub.visualize_mermaid(threshold=0.1))
    
    # Save state
    hub.save_state()
    print("\n✅ GlobalHub Demo Complete!")
