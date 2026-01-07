"""
엘리시아 자율 계획 및 실행 능력 테스트
====================================

엘리시아가 고차원적 계획을 수립하고 실행할 수 있는지 확인합니다.

발견된 시스템:
1. PlanningCortex - 계획 생성 (의도 → 단계별 행동)
2. FreeWillEngine - 자유 의지 (욕망 → 학습 → 탐구 → 실행 → 반성)
3. RecursivePlanner - 재귀적 목표 분해
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AutonomyTest")


def test_planning_cortex():
    """계획 수립 시스템 테스트"""
    print("\n" + "=" * 70)
    print("📋 TEST 1: 계획 수립 (Planning Cortex)")
    print("=" * 70)
    print()
    
    try:
        from Core.Intelligence.Intelligence.Planning.planning_cortex import PlanningCortex
        
        cortex = PlanningCortex()
        
        # 테스트 1: 의도 합성
        print("🌊 공명 패턴 → 의도 합성")
        resonance = {"사랑": 0.9, "빛": 0.7, "기쁨": 0.6}
        intent = cortex.synthesize_intent(resonance)
        print(f"   입력: {resonance}")
        print(f"   합성된 의도: {intent}")
        
        # 테스트 2: 계획 생성
        print(f"\n📝 '{intent}' 계획 생성 중...")
        plan = cortex.generate_plan(intent)
        
        print(f"\n계획 세부사항:")
        print(f"   의도: {plan.intent}")
        print(f"   생성 시각: {plan.created_at.strftime('%H:%M:%S')}")
        print(f"   단계 수: {len(plan.steps)}")
        print(f"\n단계별 행동:")
        for step in plan.steps:
            print(f"   {step.step_id}. {step.description}")
            print(f"      액션: {step.action}")
            print(f"      필요 도구: {', '.join(step.required_tools)}")
            print(f"      예상 소요: {step.estimated_duration}초")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_free_will():
    """자유 의지 시스템 테스트"""
    print("\n" + "=" * 70)
    print("💫 TEST 2: 자유 의지 (Free Will Engine)")
    print("=" * 70)
    print()
    
    try:
        from Core.Intelligence.Intelligence.Will.free_will_engine import FreeWillEngine, MissionType
        
        engine = FreeWillEngine()
        
        print("욕망 생성 테스트...")
        desire = engine.desire(
            "아버지를 행복하게 하고 싶다",
            "I want to make Father happy",
            MissionType.MAKE_HAPPY,
            intensity=0.9
        )
        
        print(f"\n✨ 생성된 욕망:")
        print(f"   내용: {desire.content_kr}")
        print(f"   강도: {desire.intensity}")
        print(f"   미션: {desire.mission.name}")
        print(f"   원천: {desire.source}")
        
        print("\n🔮 상상력 테스트...")
        simulation = engine.imagine("빛과 소리로 메시지 전달하기")
        print(f"   시뮬레이션 결과:")
        print(f"   - 예측 응답: {simulation['predicted_response']}")
        print(f"   - 신뢰도: {simulation['confidence']:.1%}")
        print(f"   - 성공 확률: {simulation['success_probability']:.1%}")
        
        print("\n🎯 행동 테스트...")
        action = engine.act("따뜻한 메시지 작성하기", desire)
        print(f"   실행된 행동: {action.description_kr}")
        print(f"   시뮬레이션 결과: {action.simulated_outcome}")
        
        print("\n🤔 반성 테스트...")
        reflection = engine.reflect(
            action,
            actual_outcome="아버지가 미소를 지으셨다",
            success=True
        )
        print(f"   반성 내용:")
        print(f"   - 성공: {reflection.success}")
        print(f"   - 배운 것: {reflection.lessons_learned}")
        print(f"   - 다음 행동: {reflection.next_actions}")
        
        print(f"\n📈 성장 상태:")
        print(f"   현재 단계: {engine.current_phase.name}")
        print(f"   활성 욕망: {engine.active_desire.content_kr if engine.active_desire else 'None'}")
        print(f"   총 행동 수: {len(engine.actions)}")
        print(f"   총 반성 수: {len(engine.reflections)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_recursive_planning():
    """재귀적 계획 시스템 테스트"""
    print("\n" + "=" * 70)
    print("🔄 TEST 3: 재귀적 계획 (Recursive Planner)")
    print("=" * 70)
    print()
    
    try:
        from Core.Intelligence.Intelligence.executive_function import RecursivePlanner
        
        planner = RecursivePlanner()
        
        print("고차원 목표 분해 테스트...")
        goal = "과거 대화 기록을 분석하고 Yggdrasil에 통합하기"
        print(f"   목표: {goal}")
        
        print("\n📋 계획 수립 중...")
        plan = planner.formulate_plan(goal)
        
        print(f"\n✨ 생성된 계획:")
        for i, step in enumerate(plan, 1):
            print(f"   {i}. {step}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 70)
    print("🌌 엘리시아 자율 계획 및 실행 능력 평가")
    print("=" * 70)
    print()
    print("엘리시아의 고차원 계획 수립 및 실행 능력을 테스트합니다.")
    print()
    
    results = []
    
    # Test 1: Planning Cortex
    results.append(("계획 수립", test_planning_cortex()))
    
    # Test 2: Free Will Engine
    results.append(("자유 의지", test_free_will()))
    
    # Test 3: Recursive Planning
    results.append(("재귀적 계획", test_recursive_planning()))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 테스트 결과 요약")
    print("=" * 70)
    print()
    
    for name, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{status} - {name}")
    
    success_count = sum(1 for _, s in results if s)
    total = len(results)
    
    print()
    print(f"통과율: {success_count}/{total} ({success_count/total*100:.1f}%)")
    print()
    
    if success_count == total:
        print("🎉 모든 테스트 통과!")
        print("엘리시아는 고차원적 계획 수립 및 실행이 가능합니다.")
    else:
        print("⚠️ 일부 시스템에 문제가 있습니다.")
    
    print()


if __name__ == "__main__":
    main()
