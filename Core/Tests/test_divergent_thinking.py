"""
발산적 사고 + 중력 어텐션 테스트

Divergent Expansion + Gravity Attention Test
- 생각이 결론으로 수렴하지 않고 확장
- 의도에 따라 중요한 것만 빛남
- 주권적 선택
"""
import sys
sys.path.insert(0, ".")
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

from Core.Intelligence.Cognition.thought_space import ThoughtSpace, ThoughtShape

print("="*60)
print("🌳 발산적 사고 + 중력 어텐션 테스트")
print("   '수렴하지 않고 확장, 의도에 맞는 것만 빛남'")
print("="*60)

ts = ThoughtSpace()

# 1. 여백 진입
ts.enter_gap("사랑에 대한 생각")

# 2. 형태를 가진 입자 추가
print("\n📍 사고 입자 추가 (형태 포함):")

from Core.Intelligence.Cognition.thought_space import ThoughtParticle
import hashlib

# 수동으로 형태 정의
p1 = ThoughtParticle(
    id="love_1",
    content="사랑은 주는 것",
    source="wisdom",
    shape=ThoughtShape(
        protrusions=["사랑", "주는"],  # 제공하는 것
        recesses=["받는", "감정"]       # 필요한 것
    )
)
p2 = ThoughtParticle(
    id="love_2",
    content="받는 것이 감정의 교류",
    source="insight",
    shape=ThoughtShape(
        protrusions=["받는", "감정"],   # 제공
        recesses=["사랑", "연결"]        # 필요
    )
)
p3 = ThoughtParticle(
    id="love_3", 
    content="연결은 사랑의 본질",
    source="reflection",
    shape=ThoughtShape(
        protrusions=["연결", "본질"],
        recesses=["사랑", "관계"]
    )
)

ts.active_particles.extend([p1, p2, p3])
print(f"   추가된 입자: {len(ts.active_particles)}")

# 3. 퍼즐 연결 찾기
print("\n" + "-"*60)
print("🧩 퍼즐 연결 (형태 맞물림):")
print("-"*60)

connections = ts.find_puzzle_connections(threshold=0.3)
for pa, pb, score in connections:
    print(f"   {pa.content[:15]}... ↔ {pb.content[:15]}... (fit: {score:.2f})")

# 4. 발산적 확장
print("\n" + "-"*60)
print("🌿 발산적 확장 (수렴하지 않음):")
print("-"*60)

before_count = len(ts.active_particles)
ts.diverge_all()
after_count = len(ts.active_particles)
print(f"   확장: {before_count} → {after_count} 입자")

# 5. 중력 어텐션
print("\n" + "-"*60)
print("☀️ 중력 어텐션 (의도에 맞는 것만 빛남):")
print("-"*60)

ts.apply_gravity_attention("사랑을 주는 방법")

illuminated = ts.get_illuminated_thoughts(threshold=0.4)
dark = ts.get_dark_thoughts(threshold=0.3)

print(f"   빛나는 입자: {len(illuminated)}")
for p in illuminated[:3]:
    print(f"      ☀️ {p.content[:30]}... (light: {p.illumination:.2f})")

print(f"   어두운 입자: {len(dark)}")
for p in dark[:3]:
    print(f"      🌑 {p.content[:30]}... (light: {p.illumination:.2f})")

# 6. 주권적 선택
print("\n" + "-"*60)
print("👑 주권적 선택:")
print("-"*60)

chosen = ts.sovereign_select("사랑을 주는 방법")
if chosen:
    print(f"   선택됨: {chosen.content}")
    print(f"   이유: 의도와 가장 공명함 (빛: {chosen.illumination:.2f})")

print("\n" + "="*60)
print("✅ 테스트 완료!")
print("   발산: 결론 없이 계속 확장")
print("   어텐션: 의도에 맞는 것만 빛남")
print("   선택: 로직이 아닌 끌림으로")
print("="*60)
