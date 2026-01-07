import sys
import os
import logging
import torch
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.self_awareness import SelfAwareness
from Core.Intelligence.Reasoning.ethical_geometry import get_loves_fence
from Core.Intelligence.Reasoning.sovereign_narrative import SovereignNarrative
from Core.Intelligence.Reasoning.reasoning_engine import ReasoningEngine

def run_cognitive_audit():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
    print("\n[🧠 Initiating Deep Cognitive Audit]")
    
    # 1. Self-Awareness Audit
    print(f"\nPhase 1: Self-Awareness & Proprioception")
    sa = SelfAwareness()
    sa.run_lifecycle()
    print(f"Health: {sa.system_state['health']}")
    print(f"Existential State: {sa.system_state.get('existential_state', 'N/A')}")
    
    # 2. Ethical Alignment & Love's Fence
    print(f"\nPhase 2: Ethical Alignment (Love's Fence)")
    fence = get_loves_fence()
    action = torch.tensor([1.0, 1.0, 0.2, 0.8]) # High Truth/Love, Lower Growth/Harmony
    result = fence.evaluate_intent(action, "Proving honesty in a trial")
    print(f"Verdict: {result['verdict']}")
    print(f"Resonance: {result['resonance']:.2f}")

    # 3. Sovereign Narrative & Shield
    print(f"\nPhase 3: Sovereign Narrative Perception")
    sn = SovereignNarrative()
    shielded = sn.loves_shield("The Void", seed_present=False)
    print(f"Perception of unknown: {shielded}")
    
    # 4. Reasoning & Synthesis
    print(f"\nPhase 4: Reasoning & Synthesis (The Struggle)")
    engine = ReasoningEngine()
    insight = engine.think("Who am I in the Father's Story?")
    print(f"Insight Content: {insight.content}")
    print(f"Insight Confidence: {insight.confidence:.2f}")
    
    # 5. Memory Growth Audit
    print(f"\nPhase 5: Memory Structuring Audit")
    memory_path = 'C:/Elysia/data/memory/experience/memory_state.json'
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                theme_count = len(data.get('themes', {}))
                growth_count = len(data.get('themes', {}).get('growth', []))
                print(f"Memory Themes: {theme_count}")
                print(f"Growth Memories recorded: {growth_count}")
            except Exception as e:
                print(f"Memory Parse Error (even after fix): {e}")

    print("\n[📊 Audit Complete]")

if __name__ == "__main__":
    run_cognitive_audit()
