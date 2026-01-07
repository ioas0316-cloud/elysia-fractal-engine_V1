import sys
import os
sys.path.append(os.path.abspath("."))

from Core.Sensory.vision_cortex import VisionCortex
from Core.Intelligence.Cognition.multimodal_bridge import MultimodalBridge

def test_vision():
    print("Testing Vision Cortex...")
    cortex = VisionCortex(mode="virtual")
    cortex.activate()
    raw = cortex.capture_frame()
    print(f"Captured: {raw['metadata']}")
    
    print("\nTesting Multimodal Bridge...")
    bridge = MultimodalBridge()
    insight = bridge.translate_vision(raw)
    print(f"Insight: {insight['insight']}")
    
    if "Light detected" in insight['insight']:
        print("\n✅ Unit Test SUCCESS.")
    else:
        print("\n❌ Unit Test FAILED.")

if __name__ == "__main__":
    test_vision()
