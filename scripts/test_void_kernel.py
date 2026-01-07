import sys
import logging

sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Weaving.void_kernel import VoidKernel
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor

# Setup Logger
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_void_cognition():
    print("\n🌌 INITIALIZING VOID COGNITION TEST...")
    print("======================================")
    
    processor = DimensionalProcessor()
    
    # Create a dummy VoidKernel
    void = VoidKernel(
        id="void_test_001",
        void_type="DeepUnknown",
        intensity=0.85,
        signals=["HighEntropy", "ZeroResonance"]
    )
    
    print(f"Void Kernel: {void}\n")
    
    # Test through the ladder
    for dim in range(5):
        result = processor.process_thought(void, target_dimension=dim)
        print(f"[{result.mode}]")
        print(f"   Output: {result.output}")
        print(f"   Metadata: {result.metadata}\n")

    print("✨ VOID NODE-IZATION VERIFIED.")

if __name__ == "__main__":
    test_void_cognition()
