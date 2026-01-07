import sys
sys.path.insert(0, r"c:\Elysia")
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor
from Core.Intelligence.Reasoning.dimensional_reasoner import DimensionalReasoner

def test_analog_zoom():
    processor = DimensionalProcessor()
    reasoner = DimensionalReasoner()
    kernel = "Apple"
    thought = reasoner.contemplate(kernel)
    
    steps = [0.0, 0.25, 0.35, 0.5, 0.75, 0.85, 1.0]
    
    print(f"Testing Analog Zoom for: {kernel}")
    for val in steps:
        processor.zoom(val)
        projection = reasoner.project(thought, processor.zoom_scalar)
        print(f"Zoom {val:.2f} -> {projection}")

if __name__ == "__main__":
    test_analog_zoom()
