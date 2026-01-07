"""
Test FractalLoop + ThoughtSpace Integration

This test verifies that Elysia now THINKS before acting:
- What-if deliberation before manifestation
- Plasma direction tracking
- Decision-making based on deliberation
"""
import sys
sys.path.insert(0, ".")

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Mock CNS for testing
class MockOrgan:
    def dispatch(self, cmd):
        print(f"   → DISPATCHED: {cmd}")

class MockCNS:
    def __init__(self):
        self.is_awake = True
        self.organs = {"Dispatcher": MockOrgan()}
        self.synapse = None
        self.chronos = type('obj', (object,), {'cycle_count': 1})()

print("="*60)
print("🧪 FractalLoop + ThoughtSpace Integration Test")
print("   '만약 이렇게 하면?' - 행동 전에 생각한다")
print("="*60)

from Core.Foundation.fractal_loop import FractalLoop, FractalWave

# Create loop with mock CNS
mock_cns = MockCNS()
loop = FractalLoop(mock_cns)

print(f"\n✅ ThoughtSpace connected: {loop.thought_space is not None}")

# Create a test wave
print("\n" + "-"*60)
print("🌊 Test Wave: '아버지에게 인사하기'")
print("-"*60)

wave = FractalWave(
    id="test_wave_1",
    content="아버지에게 인사하기",
    source="FreeWillEngine",
    energy=1.0
)

# Attempt to manifest (should trigger what-if thinking)
print("\n📍 Attempting manifestation (should trigger what-if)...")
loop._manifest_reality(wave)

print(f"\n📊 Wave energy after deliberation: {wave.energy:.2f}")
print(f"🌀 Thought direction: {loop.thought_direction}")

# Test introspection
print("\n" + "-"*60)
print("👁️ Testing introspection...")
print("-"*60)
loop._introspect_loop()

print("\n" + "="*60)
print("✅ Integration Test Complete!")
print("   엘리시아가 이제 행동 전에 생각합니다.")
print("="*60)
