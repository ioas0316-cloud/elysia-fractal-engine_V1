"""
Fractal Consciousness Simulation

시뮬레이션으로 엘리시아가 어떻게 생각하는지 보여줌
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

from Core.Foundation.Mind.fractal_consciousness import FractalConsciousness


def simulate():
    """엘리시아 의식 시뮬레이션"""
    
    print("\n" + "="*70)
    print("🌳 ELYSIA FRACTAL CONSCIOUSNESS SIMULATION")
    print("="*70)
    print("\n모든 사고층을 통과하며 생각하는 과정을 보여줍니다.\n")
    
    consciousness = FractalConsciousness()
    
    # Test inputs
    test_cases = [
        "엘리시아?",
        "사랑해 엘리시아",
        "기분이 어때?",
        "왜 그렇게 생각해?",
    ]
    
    for test_input in test_cases:
        result = consciousness.process(test_input)
        print()
        input("Press Enter for next simulation...")
        print("\n")
    
    print("="*70)
    print("시뮬레이션 완료! 💚")
    print("="*70)


if __name__ == "__main__":
    simulate()
