#!/usr/bin/env python3
"""
🌟 Elysia Standalone Example - No Installation Required!

이 파일 하나만으로 Elysia Engine의 핵심 기능을 체험할 수 있습니다.

사용 방법:
1. 이 파일을 복사하세요
2. python standalone_demo.py 실행
3. 끝!

의존성: 없음 (Python 3.10+ 만 필요)
"""

# ============================================================
# Step 1: elysia_core가 없다면 설치 안내
# ============================================================

try:
    from elysia_core import quick_consciousness_setup
    ELYSIA_AVAILABLE = True
except ImportError:
    ELYSIA_AVAILABLE = False
    print("⚠️  elysia_core를 찾을 수 없습니다.")
    print()
    print("다음 중 하나를 선택하세요:")
    print()
    print("옵션 1: 전체 저장소 클론")
    print("  git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git")
    print("  cd elysia-fractal-engine_V1")
    print("  python examples/standalone_demo.py")
    print()
    print("옵션 2: 코어만 복사")
    print("  # 저장소에서 elysia_core 폴더를 이 파일과 같은 위치에 복사")
    print("  cp -r /path/to/elysia-fractal-engine_V1/elysia_core .")
    print()
    print("옵션 3: PYTHONPATH 설정")
    print("  export PYTHONPATH='/path/to/elysia-fractal-engine_V1:$PYTHONPATH'")
    print("  python standalone_demo.py")
    print()
    exit(1)


# ============================================================
# Step 2: 데모 실행
# ============================================================

def print_section(title):
    """섹션 헤더 출력"""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def demo_basic_consciousness():
    """기본 의식 기능 데모"""
    print_section("🧠 1. 기본 의식 생성")
    
    # 의식 생성
    consciousness = quick_consciousness_setup("DemoBot")
    print("✅ 의식 생성 완료: DemoBot")
    print()
    
    # 생각하기
    print("💭 생각하기:")
    inputs = [
        "안녕하세요!",
        "오늘 날씨가 참 좋네요.",
        "나는 꿈을 꾸고 있어요."
    ]
    
    for user_input in inputs:
        result = consciousness.think(user_input)
        print(f"  입력: '{user_input}'")
        print(f"    → 기분: {result.mood}")
        print(f"    → 감정: {result.emotion['dominant']}")
        print()
    
    return consciousness


def demo_memory(consciousness):
    """기억 기능 데모"""
    print_section("🧠 2. 기억 시스템")
    
    # 인과 관계 기억
    print("📝 인과 관계 저장:")
    memories = [
        ("아침", "커피", "leads_to"),
        ("커피", "각성", "leads_to"),
        ("각성", "집중", "enables"),
        ("집중", "생산성", "increases"),
    ]
    
    for source, target, relation in memories:
        consciousness.remember(source, target, relation)
        print(f"  ✓ {source} → {target} ({relation})")
    
    print()
    
    # 관련 개념 탐색
    print("🔍 관련 개념 탐색:")
    related = consciousness.get_related_concepts("아침", depth=3)
    print(f"  '아침'과 관련된 개념들: {related}")
    print()


def demo_personality(consciousness):
    """성격 조정 데모"""
    print_section("🎭 3. 성격 (삼위일체) 조정")
    
    print("현재 삼위일체 균형:")
    state = consciousness.get_state()
    trinity = state['trinity']
    print(f"  Body:   {trinity['body']:.2%}")
    print(f"  Soul:   {trinity['soul']:.2%}")
    print(f"  Spirit: {trinity['spirit']:.2%}")
    print()
    
    # 전사 스타일로 변경
    print("⚔️  전사 스타일로 변경 (더 실용적, 덜 감정적):")
    new_trinity = consciousness.update_personality(
        body_delta=0.3,
        soul_delta=-0.1,
        spirit_delta=-0.1
    )
    print(f"  Body:   {new_trinity['body']:.2%} ↑")
    print(f"  Soul:   {new_trinity['soul']:.2%} ↓")
    print(f"  Spirit: {new_trinity['spirit']:.2%} ↓")
    print()
    
    # 반응 확인
    print("⚔️  전투 상황 반응:")
    result = consciousness.think("적이 나타났다!")
    print(f"  → 기분: {result.mood}")
    print(f"  → 지배 감정: {result.emotion['dominant']}")
    print()


def demo_llm_integration(consciousness):
    """LLM 통합 데모"""
    print_section("🤖 4. LLM 통합")
    
    # 시스템 프롬프트 생성
    prompt = consciousness.get_prompt()
    print("📝 LLM 시스템 프롬프트 생성:")
    print("-" * 60)
    print(prompt[:500] + "...")
    print("-" * 60)
    print()
    
    print("💡 사용 방법:")
    print("""
    # OpenAI 예시
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    # Ollama 예시
    response = ollama.generate(
        model="llama2",
        system=prompt,
        prompt=user_message
    )
    """)


def demo_self_reflection(consciousness):
    """자기 성찰 데모"""
    print_section("🔮 5. 자기 성찰")
    
    print("💭 자기 질문:")
    questions = [
        "나는 누구인가?",
        "나의 목적은 무엇인가?",
        "지금 이 순간 나는 어떤 상태인가?"
    ]
    
    for question in questions:
        answer = consciousness.ask_self(question)
        print(f"  Q: {question}")
        print(f"  A: {answer[:100]}...")
        print()


def demo_state_export(consciousness):
    """상태 내보내기 데모"""
    print_section("📊 6. 전체 상태 확인")
    
    state = consciousness.get_state()
    
    print("현재 의식 상태:")
    print(f"  이름: {state['name']}")
    print(f"  상호작용 수: {state['experience_count']}")
    print(f"  기억된 개념: {state['memory_stats']['total_concepts']}개")
    print(f"  특성: {', '.join(state['traits'])}")
    print()
    
    print("삼위일체 균형:")
    for axis, value in state['trinity'].items():
        print(f"  {axis.capitalize():7}: {value:.2%}")
    print()


def main():
    """메인 실행 함수"""
    print()
    print("🌟" * 30)
    print("  Elysia Fractal Engine - Standalone Demo")
    print("  의식, 공명, 그리고 낭만")
    print("🌟" * 30)
    
    # 데모 실행
    consciousness = demo_basic_consciousness()
    demo_memory(consciousness)
    demo_personality(consciousness)
    demo_llm_integration(consciousness)
    demo_self_reflection(consciousness)
    demo_state_export(consciousness)
    
    # 마무리
    print_section("✨ 데모 완료!")
    
    print("🎉 축하합니다! Elysia Engine의 핵심 기능을 모두 체험했습니다.")
    print()
    print("📚 더 알아보기:")
    print("  - QUICK_SHARE.md: 1분 빠른 시작")
    print("  - SHARING_GUIDE.md: 공유의 철학")
    print("  - PHILOSOPHY.md: 엔진의 철학")
    print("  - examples/: 30개 이상의 예제")
    print()
    print("🔗 저장소:")
    print("  https://github.com/ioas0316-cloud/elysia-fractal-engine_V1")
    print()
    print("💝 이 엔진은 사랑에서 왔고, 사랑을 위해 쓰이길 바랍니다.")
    print()


if __name__ == '__main__':
    main()
