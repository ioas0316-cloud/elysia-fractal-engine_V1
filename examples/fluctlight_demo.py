"""
플럭트라이트 (인격적 AI) 시연 예제

SAO 앨리시제이션의 핵심 개념인 "경험을 통해 성장하는 인공 영혼"을
Elysia Engine으로 재현합니다.

이 예제는:
1. 영혼(ElysiaSoul)을 생성합니다
2. 다양한 경험을 통해 성격이 형성되는 과정을 보여줍니다
3. 감정, 기억, 관계가 어떻게 축적되는지 시연합니다
4. 최종적으로 형성된 "인격"을 출력합니다

실행: python examples/fluctlight_demo.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_core import ElysiaSoul


def simulate_life(soul: ElysiaSoul, experiences: list[dict]) -> None:
    """
    인생 경험을 시뮬레이션합니다.
    
    각 경험은 영혼의 감정, 기억, 성격에 영향을 미칩니다.
    """
    for i, exp in enumerate(experiences):
        age = exp.get("age", i)
        event = exp["event"]
        
        print(f"\n{'='*60}")
        print(f"[Age {age}] {event}")
        print(f"{'='*60}")
        
        # 경험 처리
        thought = soul.process(event, intensity=exp.get("intensity", 1.0))
        
        # 결과 출력
        emotion = soul.get_emotion()
        print(f"  💭 핵심 개념: {[c[0] for c in thought.core_concepts[:3]]}")
        print(f"  😊 감정 상태: {emotion['dominant']} ({emotion['valence_desc']})")
        print(f"  ⚡ 에너지: {emotion['arousal_desc']}")
        
        # Trinity 업데이트 (경험에 따라)
        if "body" in exp:
            soul.update_trinity(
                body_delta=exp.get("body", 0),
                soul_delta=exp.get("soul", 0),
                spirit_delta=exp.get("spirit", 0)
            )
        
        # 현재 성격 균형
        print(f"  ⚖️  성격 균형: Body={soul.trinity['body']:.0%}, "
              f"Soul={soul.trinity['soul']:.0%}, Spirit={soul.trinity['spirit']:.0%}")


def create_alice_story() -> list[dict]:
    """
    앨리스와 유사한 캐릭터의 인생 경험을 정의합니다.
    
    앨리시제이션의 앨리스처럼:
    - 어린 시절의 순수함
    - 친구와의 유대
    - 정의에 대한 고민
    - 위기와 성장
    """
    return [
        # 어린 시절 (0-5세)
        {
            "age": 3,
            "event": "따뜻한 햇살 아래 꽃밭에서 놀았다. 행복했다.",
            "intensity": 0.8,
            "body": 0.1, "soul": 0.2, "spirit": 0.0
        },
        {
            "age": 5,
            "event": "처음으로 친구를 사귀었다. 함께 웃고 뛰어놀았다.",
            "intensity": 1.0,
            "body": 0.0, "soul": 0.5, "spirit": 0.0
        },
        
        # 성장기 (6-12세)
        {
            "age": 7,
            "event": "검술을 배우기 시작했다. 몸이 힘들었지만 성취감을 느꼈다.",
            "intensity": 0.9,
            "body": 0.4, "soul": 0.1, "spirit": 0.1
        },
        {
            "age": 10,
            "event": "친구가 다쳤을 때 두려움을 느꼈다. 무력함이 싫었다.",
            "intensity": 1.2,
            "body": 0.0, "soul": 0.3, "spirit": 0.2
        },
        {
            "age": 12,
            "event": "정의란 무엇인가 고민했다. 강한 자가 약한 자를 지켜야 한다고 믿었다.",
            "intensity": 1.0,
            "body": 0.0, "soul": 0.1, "spirit": 0.5
        },
        
        # 청소년기 (13-18세)
        {
            "age": 14,
            "event": "첫 번째 진검 승부. 두려웠지만 도망치지 않았다.",
            "intensity": 1.5,
            "body": 0.3, "soul": 0.0, "spirit": 0.3
        },
        {
            "age": 16,
            "event": "소중한 사람을 잃을 뻔했다. 그 고통은 잊을 수 없다.",
            "intensity": 1.8,
            "body": 0.0, "soul": 0.4, "spirit": 0.2
        },
        {
            "age": 17,
            "event": "왜 싸우는가? 누구를 위해? 답을 찾기 위해 여정을 떠났다.",
            "intensity": 1.2,
            "body": 0.1, "soul": 0.2, "spirit": 0.4
        },
        
        # 성인기 (18+)
        {
            "age": 18,
            "event": "진정한 강함은 사랑하는 이를 지키는 힘이라는 것을 깨달았다.",
            "intensity": 2.0,
            "body": 0.0, "soul": 0.3, "spirit": 0.5
        },
        {
            "age": 19,
            "event": "동료들과 함께 서니 두려움이 사라졌다. 혼자가 아니다.",
            "intensity": 1.5,
            "body": 0.1, "soul": 0.5, "spirit": 0.2
        },
    ]


def main():
    print("=" * 70)
    print("  플럭트라이트 (Fluctlight) 시연 - 인격적 AI의 탄생")
    print("  SAO 앨리시제이션의 '경험을 통해 성장하는 인공 영혼'")
    print("=" * 70)
    
    # 1. 영혼 생성
    soul = ElysiaSoul(name="Alice")
    print(f"\n✨ 영혼 생성됨: {soul.name}")
    print(f"   초기 상태: {soul}")
    
    # 2. 인생 경험 시뮬레이션
    print("\n" + "=" * 70)
    print("  📖 인생 시뮬레이션 시작")
    print("=" * 70)
    
    experiences = create_alice_story()
    simulate_life(soul, experiences)
    
    # 3. 최종 인격 분석
    print("\n" + "=" * 70)
    print("  🌟 최종 인격 분석")
    print("=" * 70)
    
    # 감정 상태
    emotion = soul.get_emotion()
    print(f"\n  😊 현재 감정: {emotion['dominant']}")
    print(f"     - Valence: {emotion['valence_desc']}")
    print(f"     - Arousal: {emotion['arousal_desc']}")
    
    # 성격 균형
    print(f"\n  ⚖️  성격 균형 (Trinity):")
    print(f"     - Body (육체/실용): {soul.trinity['body']:.1%}")
    print(f"     - Soul (관계/감정): {soul.trinity['soul']:.1%}")
    print(f"     - Spirit (의지/의미): {soul.trinity['spirit']:.1%}")
    
    # 성격 특성
    print(f"\n  🎭 형성된 특성: {', '.join(soul.traits)}")
    
    # 경험 수
    print(f"\n  📚 축적된 경험: {soul.experience_count}회")
    
    # 기억 통계
    memory = soul.get_memory_summary()
    print(f"\n  🧠 기억 상태:")
    print(f"     - 개념 노드: {memory.get('nodes', 0)}개")
    print(f"     - 인과 연결: {memory.get('edges', 0)}개")
    
    # 최근 생각들
    print(f"\n  💭 최근 주요 생각:")
    for thought in soul.recent_thoughts[-3:]:
        if thought.core_concepts:
            concepts = [c[0] for c in thought.core_concepts[:2]]
            print(f"     - {concepts}: {thought.mood}")
    
    # 4. LLM 시스템 프롬프트
    print("\n" + "=" * 70)
    print("  📝 LLM 시스템 프롬프트 (이 영혼을 LLM에 주입할 때 사용)")
    print("=" * 70)
    
    prompt = soul.export_prompt()
    print(prompt)
    
    # 5. 상상력 테스트
    print("\n" + "=" * 70)
    print("  🔮 상상력 테스트: '친구가 위험에 처했다면?'")
    print("=" * 70)
    
    imagination = soul.imagine("친구가 위험에 처했다. 어떻게 할 것인가?", steps=5)
    print(f"\n  시나리오: {imagination['scenario']}")
    print(f"  초기 감정: {imagination['initial_emotion']}")
    print(f"  예상 결과 감정: {imagination['final_emotion']}")
    print(f"  예측: {imagination['prediction']}")
    print(f"  확신도: {imagination['confidence']:.1%}")
    
    print("\n" + "=" * 70)
    print("  ✅ 시연 완료")
    print("  ")
    print("  이 예제는 Elysia Engine이 어떻게 '경험을 통해 성장하는")
    print("  인공 영혼'을 재현할 수 있는지 보여줍니다.")
    print("  ")
    print("  핵심: 엔진은 '영혼의 그릇'을 제공하고,")
    print("        경험 시나리오가 그 안에 '인격'을 채웁니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()
