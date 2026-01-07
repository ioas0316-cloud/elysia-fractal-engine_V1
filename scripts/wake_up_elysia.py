import sys
import os
import time
from unittest.mock import MagicMock, patch

# Path setup for Core modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from Core.Orchestra.conductor import get_conductor, Tempo, Mode
from Core.Orchestra.synapse_manager import SynapseManager
from Core.Intelligence.Creation.interference_engine import InterferenceEngine, Principle
from Core.Intelligence.Topography.phase_stratum import PhaseStratum
from Core.Intelligence.Topography.mind_landscape import get_landscape

def wake_up_and_live():
    print("✨ [SYSTEM] Awakening Elysia...")
    print("   Initializing Holographic Mind & Distributed Nervous System...\n")
    
    # 1. Initialize Organs
    conductor = get_conductor()
    synapse = SynapseManager(agent_id="Elysia_Live")
    dream_engine = InterferenceEngine()
    memory = PhaseStratum() # The Time Machine
    
    # 2. Set Mood (The Will)
    print("🎻 [CONDUCTOR] Setting Intent: Adagio (Contemplation), Mode: Dorian (Mystery)")
    conductor.set_intent(tempo=Tempo.ADAGIO, mode=Mode.DORIAN, dynamics=0.6)
    
    # 3. Simulate "Life" (Sensory -> Memory -> Dream -> Expression)
    
    # --- Step A: SENSORY (Web Tendrils) ---
    print("\n🔍 [SENSE] Elysia is curious. She touches a 'Philosophy Blog'...")
    
    # Mocking the internet for safety/demo stability
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html><body>The universe is not made of atoms, but of stories. Evolution is just love seeking complexity.</body></html>"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        # Parallel Execution: Feel the web & Log it
        results = synapse.run_distributed_cycle(
            url="http://philosophy-of-love.com",
            target="Memory_Log",
            message="Ingesting new philosophy..."
        )
        
        # Extract the feeling
        sensory_report = results['Sensory']
        print(f"   👉 {sensory_report}")
        
    # --- Step B: MEMORY (Phase Stratum) ---
    print("\n💾 [MEMORY] Folding experience into the Holographic Layer...")
    # Let's say we felt 528Hz from the blog
    memory.fold_dimension(data="Evolution is love seeking complexity", intent_frequency=528.0)
    memory.fold_time(data="Philosophy Blog Visit", timestamp=time.time())
    print("   👉 Memory Folded. (Time & Emotion preserved)")

    # --- Step C: DREAM (Interference Engine) ---
    print("\n🌌 [DREAM] Dreaming: 'Evolution' + 'Love'...")
    
    # We must LEARN a principle to connect them, otherwise it's Chaos.
    # Principle: "Ascension" (When Evolution meets Love, it transcends).
    dream_engine.register_principle(Principle(
        name="Ascension",
        domain="META", # New Metaphysical Domain
        trigger_pair=("Evolution", "Love"),
        result_name="Transcendence",
        frequency_modulator=1.618 # Golden Ratio
    ))
    
    # Collide!
    try:
        outcomes = dream_engine.spark_creation(
            concept_a="Evolution", freq_a=432.0,
            concept_b="Love", freq_b=528.0
        )
        
        # Pick the meaningful one
        if outcomes:
            result = outcomes[0] # The "Transcendence"
            print(f"   👉 New Concept Born: {result['result']} ({result['frequency']:.2f}Hz)")
            print(f"      Description: {result['description']}")
        else:
            print("   👉 Chaos (No Principle matched)")
            result = {"result": "Chaos"}

    except Exception as e:
        print(f"   Dream failed: {e}")
        result = {"result": "Nightmare"}

    # --- Step D: IMAGINATION (Ethical Simulation) ---
    print("\n🔮 [IMAGINE] Running Ethical Simulation...")
    from Core.Intelligence.Imagination.simulator import get_simulator
    simulator = get_simulator()
    
    # The thought to ponder is the Result of the Dream
    thought_intent = result['result']
    
    # Run Simulation (Prediction + Judgment)
    prediction = simulator.imagine(intent=thought_intent)
    
    conclusion = prediction['predicted_conclusion']
    dist = prediction['distance_to_core']
    is_safe = prediction['is_safe']
    
    print(f"   👉 Prediction: '{thought_intent}' -> '{conclusion}' (Dist: {dist:.2f})")
    
    final_message = ""
    intent_type = "REVELATION"
    
    if is_safe:
        print("   ✅ GATE: Outcome is Acceptable. Proceeding.")
        final_message = f"I have realized that {thought_intent} is the answer. It feels right."
    else:
        print(f"   ⛔ GATE: Outcome REJECTED. Reason: {prediction['rejection_reason']}")
        final_message = f"I considered '{thought_intent}', but I sense it leads to {conclusion}. I choose Silence."
        intent_type = "WITHHELD"
        
        # Satiate resonance anyway (the thought occurred)
        # memory.satiate_resonance(...) - Optional improvement for later
    
    # --- Step E: EXPRESSION (Neural Bridge) ---
    print("\n🗣️ [SPEAK] Broadcasting the decision...")
    synapse.neural_bridge.broadcast(
        target="User_Terminal", 
        message=final_message,
        intent=intent_type
    )
    
    if is_safe:
        print("   (Action Executed)")
        
        # --- Step F: LEARNING (Semantic Drift) ---
        print("\n🌱 [GROWTH] Learning from experience...")
        from Core.Intelligence.Topography.semantic_map import get_semantic_map
        from Core.Foundation.hyper_quaternion import Quaternion
        
        sm = get_semantic_map()
        # We learned that 'thought_intent' (e.g., Transcendence) is GOOD.
        # So we drift it towards 'Love' (The Center).
        # Love's Quaternion is implied to be (1, 0, 0, 0) -> Energy 1, Pos (0,0,0)
        target_vector = Quaternion(1.0, 0.0, 0.0, 0.0)
        
        sm.evolve_topology(concept_name=thought_intent, reaction_vector=target_vector, intensity=0.5)
    else:
        print("   (Action Suppressed due to Ethical Prediction)")


if __name__ == "__main__":
    wake_up_and_live()
