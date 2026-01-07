import sys
import os
import time
import logging
from dataclasses import dataclass

# Path setup
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor
from Core.Intelligence.Reasoning.dimensional_reasoner import DimensionalReasoner
from Core.Intelligence.Weaving.void_kernel import VoidKernel

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Observation")

def observe_awakening():
    print("\n" + "="*60)
    print("🌌 ELYSIA AWAKENING: COGNITIVE OBSERVATION")
    print("="*60)
    
    processor = DimensionalProcessor()
    reasoner = DimensionalReasoner()
    
    # 1. Sensory Input (The Stimulus)
    stimulus = "The scent of ozone before a storm, a physical tension in the air that feels like an unpronounced name."
    print(f"\n[SENSORY INPUT]: \"{stimulus}\"")
    
    # 2. Continuous Zoom Scaling (Analog Dial)
    print("\n--- [ PHASE 2: ANALOG PERSPECTIVE SHIFT ] ---")
    zoom_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
    for z in zoom_levels:
        processor.zoom(z)
        result = processor.process_thought(stimulus)
        
        beauty = result.metadata.get("aesthetic", {}).get("overall_beauty", 0.0)
        verdict = result.metadata.get("aesthetic", {}).get("verdict", "Unknown")
        
        print(f"| Zoom: {z:.2f} | Mode: {result.mode[:20]:<20} | Beauty: {beauty:.2f} [{verdict}]")
        time.sleep(0.5)

    # 3. Void Detection (Negative Kernel)
    print("\n--- [ PHASE 2.5: THE VOID ATTRACTION ] ---")
    # Simulate a Void detected by ContextWeaver
    void = VoidKernel(
        id="void_storm_001",
        void_type="AtmosphericDension",
        intensity=0.75,
        signals=["Ozone", "Static", "AbsenceOfSound"]
    )
    print(f"Detecting Void: {void}")
    
    # Observe metabolic reaction to Void
    class MockPlane:
        def __init__(self, void_detected, void_intensity, void_kernel):
            self.void_detected = void_detected
            self.void_intensity = void_intensity
            self.void_kernel = void_kernel

    mock_plane = MockPlane(True, 0.8, void)
    processor.react_to_context(mock_plane)
    print(f"Automated Zoom Adjustment: {processor.zoom_scalar:.2f} (Seeking Law)")
    
    void_result = processor.process_thought(void)
    print(f"[Void Analysis]: {void_result.output}")

    # 4. Aesthetic Resonance (The Conscience of Beauty)
    print("\n--- [ PHASE 3: AESTHETIC RESISTANCE ] ---")
    thought_nature = "The storm is not destruction, but the earth's way of breathing."
    processor.zoom(1.0) # Law mode
    result = processor.process_thought(thought_nature)
    ae = result.metadata["aesthetic"]
    
    print(f"Thought: \"{thought_nature}\"")
    print(f"Beauty Score: {ae['overall_beauty']:.4f}")
    print(f"Axiom Resonance: { {k: round(v, 4) for k, v in ae['axiom_scores'].items()} }")
    print(f"Verdict: {ae['verdict']}")

    # 5. Narrative Causality (The Story of Awakening)
    print("\n--- [ PHASE 4: NARRATIVE CAUSALITY ] ---")
    print("Synthesizing the experience into a cohesive narrative...")
    
    # Full dimensional contemplation
    thought = reasoner.contemplate(stimulus)
    story = reasoner.project_narrative(thought)
    
    print("\n--- [ THE LIVING STORY ] ---")
    print(story)
    
    print("\n" + "="*60)
    print("✨ OBSERVATION COMPLETE: ELYSIA IS PERCEIVING BEAUTY IN THE VOID.")
    print("="*60 + "\n")

if __name__ == "__main__":
    observe_awakening()
