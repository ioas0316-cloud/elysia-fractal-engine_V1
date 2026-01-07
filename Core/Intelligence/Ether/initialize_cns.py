"""
Central Nervous System Initializer
===================================

"모든 신경이 깨어난다."
"All nerves awaken."

This module initializes all core systems and registers them with GlobalHub.
Run this at startup to ensure all modules are connected.
"""

import logging

logger = logging.getLogger("Elysia.Initializer")

def initialize_central_nervous_system():
    """
    Initialize all core systems and connect them to GlobalHub.
    
    This should be called at Elysia's awakening.
    """
    logger.info("🌅 Awakening Central Nervous System...")
    
    # 1. Initialize GlobalHub (the central nervous system itself)
    from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
    hub = get_global_hub()
    logger.info("   ✅ GlobalHub initialized")
    
    # 2. Initialize core reasoning systems
    try:
        from Core.Intelligence.Intelligence.reasoning_engine import ReasoningEngine
        reasoning = ReasoningEngine()
        logger.info("   ✅ ReasoningEngine connected")
    except Exception as e:
        logger.warning(f"   ⚠️ ReasoningEngine: {e}")
    
    # 3. Initialize the Why-Engine (Axiom/Causality system)
    try:
        from Core.Foundation.fractal_concept import ConceptDecomposer
        decomposer = ConceptDecomposer()
        logger.info("   ✅ ConceptDecomposer (Why-Engine) connected")
    except Exception as e:
        logger.warning(f"   ⚠️ ConceptDecomposer: {e}")
    
    # 4. Initialize the Logical Core (Truth Tree)
    try:
        from Core.Intelligence.Intelligence.Logos.philosophical_core import get_logos_engine
        logos = get_logos_engine()
        logger.info("   ✅ LogosEngine (Truth Tree) connected")
    except Exception as e:
        logger.warning(f"   ⚠️ LogosEngine: {e}")
    
    # 5. Initialize the Ether Dynamics (Field Physics)
    try:
        from Core.Intelligence.Consciousness.Ether.field_operators import DynamicsEngine
        dynamics = DynamicsEngine()
        logger.info("   ✅ DynamicsEngine (Field Physics) connected")
    except Exception as e:
        logger.warning(f"   ⚠️ DynamicsEngine: {e}")
    
    # 6. Report status
    status = hub.get_hub_status()
    logger.info(f"🌐 Central Nervous System Online")
    logger.info(f"   Connected Modules: {status['total_modules']}")
    logger.info(f"   Modules: {status['modules']}")
    logger.info(f"   Event Types: {status['event_types']}")
    
    return hub


def demonstrate_wave_communication():
    """
    Demonstrate how modules communicate via waves.
    """
    from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
    from Core.Foundation.Wave.wave_tensor import WaveTensor
    
    hub = get_global_hub()
    
    print("\n" + "=" * 60)
    print("🌊 Wave Communication Demo")
    print("=" * 60)
    
    # Create wave using correct API
    wave = WaveTensor("ThoughtWave")
    wave.add_component(528.0, amplitude=0.9, phase=0.0)
    
    # Publish a thought wave
    results = hub.publish_wave(
        "Demo",
        "thought",
        wave,
        payload={"content": "What is the meaning of existence?"}
    )
    
    print(f"\n📢 Published 'thought' wave (528Hz)")
    print(f"   Responders: {list(results.keys())}")
    
    # Check relational density
    print(f"\n🔗 Strongest Bonds:")
    for bond in hub.get_hub_status()["strongest_bonds"][:5]:
        print(f"   {bond['from']} <-> {bond['to']}: {bond['weight']:.3f}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    hub = initialize_central_nervous_system()
    print("\n" + "=" * 60)
    print(hub.visualize_mermaid(threshold=0.05))
    print("=" * 60)
    
    demonstrate_wave_communication()
