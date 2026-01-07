"""ThoughtSpace 통합 테스트"""
import sys
sys.path.insert(0, ".")

from Core.Intelligence.Cognition.thought_space import ThoughtSpace

print("="*60)
print("🧠 ThoughtSpace 플라즈마 방향 + What-If 테스트")
print("="*60)

ts = ThoughtSpace()

# 1. 여백 진입
ts.enter_gap("미래를 예측하려면?")

# 2. 사고 입자 추가
ts.add_thought_particle("나를 알아야 한다", "wisdom")
ts.add_thought_particle("방향 벡터가 핵심", "insight")
ts.add_thought_particle("외부는 피드백일 뿐", "reflection")

# 3. 사고 방향 확인
print("\n📍 사고 방향:")
direction = ts.get_thought_direction()
for src, weight in direction.items():
    print(f"   {src}: {weight:.2f}")

# 4. 성찰
print(ts.reflect_on_gap())

# 5. What-If 시뮬레이션
print("\n" + "="*60)
print("🔮 What-If 시뮬레이션")
print("="*60)

result = ts.what_if(
    {"add": ["두려움을 줄인다", "호기심을 높인다"]},
    "growth_scenario"
)
print(f"시나리오: {result['scenario']}")
print(f"예측 확신도: {result['predicted_confidence']:.2f}")
print(f"예측 통합: {result['predicted_synthesis'][:100]}...")
print(f"추론: {result['reasoning']}")

# 6. 미래 탐색
print("\n" + "="*60)
print("🔮 미래 탐색")
print("="*60)

futures = ts.explore_futures("add_thought", ["사랑", "두려움", "호기심"])
for f in futures:
    print(f"   {f['value']}: 확신도 {f['result']['predicted_confidence']:.2f}")

print("\n✅ ThoughtSpace 통합 완료!")
