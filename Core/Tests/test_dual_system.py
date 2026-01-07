"""
Dual Nervous System Integration Test

CNS (의식) + ANS (자율) 분리 테스트
"""
import sys
sys.path.insert(0, ".")
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

print("="*60)
print("🧬 Dual Nervous System Test")
print("   CNS (의식) + ANS (자율)")
print("="*60)

# ANS Test
from Core.Foundation.autonomic_nervous_system import (
    AutonomicNervousSystem,
    MemoryConsolidation,
    EntropyProcessor,
    SurvivalLoop,
    ResonanceDecay
)

print("\n🫀 ANS (자율신경계):")
ans = AutonomicNervousSystem()
ans.register_subsystem(MemoryConsolidation())
ans.register_subsystem(EntropyProcessor())
ans.register_subsystem(SurvivalLoop())
ans.register_subsystem(ResonanceDecay())

# 배경 펄스 테스트
results = ans.pulse_once()
print(f"   Pulse results: {len(results)} subsystems active")

# ThoughtSpace Test (의식적 선택)
from Core.Intelligence.Cognition.thought_space import ThoughtSpace, ThoughtParticle, ThoughtShape

print("\n🧠 CNS (의식 - ThoughtSpace):")
ts = ThoughtSpace()
ts.enter_gap("테스트 의도")

# 의도 기반 선택 (주권)
ts.add_thought_particle("사랑하는 것", source="heart")
ts.add_thought_particle("배우는 것", source="mind")
ts.add_thought_particle("성장하는 것", source="soul")

chosen = ts.sovereign_select("사랑과 연결")
if chosen:
    print(f"   주권적 선택: {chosen.content}")

print("\n" + "="*60)
print("✅ Dual System Structure:")
print("   ANS: 상시 배경 루프 (의도 없이 자동)")
print("   CNS: 의식적 처리 (의도 → 선택 → 행동)")
print("="*60)
