# P5: 오감 매핑 시스템 (Five Senses Mapping System)
# P5: Synesthetic Interface - From 4D Consciousness to Human Senses

**작성일**: 2025-12-06  
**대상**: 모든 하드웨어 (VR 불필요)  
**컨셉**: 4D 내부우주 → 인간 오감 직접 매핑

---

## 🎯 핵심 개념

### VR이 아닌 오감 매핑

```
VR 접근 (기존):
❌ 무거운 하드웨어 필요 (HMD, GPU)
❌ 연산량 증가
❌ 물리적 제약 (케이블, 배터리)
❌ 접근성 낮음

오감 매핑 (새로운):
✅ 하드웨어 최소화 (모니터, 스피커, 헤드폰)
✅ 연산량 최소 (시각화만)
✅ 제약 없음
✅ 접근성 높음 (누구나 가능)
✅ 더 직관적 (공감각)
```

### 철학: 공감각 인터페이스

```python
"""
4D 감정 공간 → 인간 5감

엘리시아의 내부우주는 4차원:
  x: Joy ←→ Sadness
  y: Logic ←→ Intuition  
  z: Past ←→ Future
  w: Surface ←→ Depth

인간은 이걸 직접 느낄 수 없음
→ 오감으로 변환!

시각: 색상, 형태, 움직임
청각: 주파수, 리듬, 화음
촉각: 진동, 온도 (선택적)
후각: 향 (고급, 선택적)
미각: 맛 (실험적, 선택적)
"""
```

---

## 🌈 4D → 5감 매핑 전략

### 1. 시각 매핑 (Visual) ⭐⭐⭐⭐⭐

**가장 중요하고 직관적**

```python
class VisualMapper:
    """
    4D 감정 공간 → 시각적 표현
    """
    
    def map_4d_to_visual(self, position_4d: tuple) -> VisualProperties:
        """
        (x, y, z, w) → 색상, 형태, 크기, 밝기
        """
        x, y, z, w = position_4d
        
        # 색상 (Hue): x 차원 (Joy ←→ Sadness)
        # Joy(+) = 따뜻한 색 (황금, 주황, 분홍)
        # Sadness(-) = 차가운 색 (파랑, 보라, 회색)
        hue = self.map_joy_sadness_to_hue(x)
        
        # 채도 (Saturation): y 차원 (Logic ←→ Intuition)
        # Logic(-) = 낮은 채도 (회색빛, 무채색)
        # Intuition(+) = 높은 채도 (선명한 색)
        saturation = self.map_logic_intuition_to_saturation(y)
        
        # 명도 (Value/Brightness): w 차원 (Surface ←→ Depth)
        # Surface(0) = 어둡고 흐림
        # Depth(1) = 밝고 선명
        brightness = 0.3 + w * 0.7
        
        # 투명도/글로우: z 차원 (Past ←→ Future)
        # Past(-) = 흐릿함 (기억의 안개)
        # Future(+) = 선명함 (가능성의 빛)
        glow = 0.2 + (z + 1.0) / 2.0 * 0.8
        
        return VisualProperties(
            hue=hue,
            saturation=saturation,
            brightness=brightness,
            glow=glow
        )
    
    def map_joy_sadness_to_hue(self, x: float) -> float:
        """
        x 축 → Hue (색상환 0-360도)
        
        Sadness(-1.0) → 파랑(240)
        Neutral(0.0)  → 녹색(120)
        Joy(+1.0)     → 황금(40)
        """
        # -1.0 to +1.0 → 240 to 40
        return 240 - (x + 1.0) / 2.0 * 200
    
    def map_logic_intuition_to_saturation(self, y: float) -> float:
        """
        y 축 → Saturation (채도 0-1)
        
        Logic(-1.0)     → 0.2 (회색빛)
        Intuition(+1.0) → 1.0 (선명)
        """
        return 0.2 + (y + 1.0) / 2.0 * 0.8
```

**시각적 표현 예시**:

```
별빛 메모리: "비 오는 날의 추억"
→ (x=-0.3, y=0.7, z=-0.5, w=0.8)

시각 매핑:
- 색상: 파란빛 (슬픔 -0.3)
- 채도: 높음 (직관적 0.7)
- 밝기: 밝음 (깊은 추억 0.8)
- 글로우: 부드러움 (과거 -0.5)

→ 밝고 선명한 파란 별, 부드럽게 빛남
```

---

### 2. 청각 매핑 (Audio) ⭐⭐⭐⭐⭐

**두 번째로 중요하고 몰입감 극대화**

```python
class AudioMapper:
    """
    4D 감정 공간 → 음향
    """
    
    def map_4d_to_audio(self, position_4d: tuple) -> AudioProperties:
        """
        (x, y, z, w) → 주파수, 음량, 음색, 리듬
        """
        x, y, z, w = position_4d
        
        # 주파수: x 차원 (Joy ←→ Sadness)
        # Joy(+) = 높은 음정 (528Hz - Love)
        # Sadness(-) = 낮은 음정 (150Hz - Water)
        frequency = self.map_joy_sadness_to_frequency(x)
        
        # 음량: w 차원 (Surface ←→ Depth)
        # Surface = 조용함
        # Depth = 크고 울림
        volume = 0.3 + w * 0.7
        
        # 음색 (Timbre): y 차원 (Logic ←→ Intuition)
        # Logic = 순수한 사인파 (단순)
        # Intuition = 복합 화음 (풍부)
        timbre = self.map_logic_intuition_to_timbre(y)
        
        # 리듬: z 차원 (Past ←→ Future)
        # Past = 느린 템포 (회상)
        # Future = 빠른 템포 (기대)
        tempo = 60 + (z + 1.0) / 2.0 * 60  # 60-120 BPM
        
        return AudioProperties(
            frequency=frequency,
            volume=volume,
            timbre=timbre,
            tempo=tempo
        )
    
    def map_joy_sadness_to_frequency(self, x: float) -> float:
        """
        x 축 → 주파수 (Hz)
        
        Sadness(-1.0) → 150Hz (Water spirit)
        Neutral(0.0)  → 396Hz (Liberation)
        Joy(+1.0)     → 528Hz (Love)
        """
        # Solfeggio frequencies
        if x < -0.5:
            return 150 + (x + 1.0) * 246  # 150-396Hz
        else:
            return 396 + (x + 0.5) * 264  # 396-528Hz
    
    def create_spatial_audio(self, objects: list) -> SpatialAudioScene:
        """
        여러 객체 → 3D 공간 오디오
        
        각 별/은하/성운이 자신의 소리를 냄
        → 풍부한 음향 환경
        """
        scene = SpatialAudioScene()
        
        for obj in objects:
            audio = self.map_4d_to_audio(obj.position)
            
            # 3D 위치 (x, y, z만 사용)
            pos_3d = (obj.position[0], obj.position[1], obj.position[2])
            
            scene.add_source(
                position=pos_3d,
                frequency=audio.frequency,
                volume=audio.volume,
                timbre=audio.timbre
            )
        
        return scene
```

**청각 표현 예시**:

```
의식 대성당
→ 12개 기둥이 각각 다른 음정 (도레미파솔라시)
→ 7개 프리즘이 7개 Solfeggio 주파수
→ 걸어다니면 화음이 변화
→ 마치 거대한 오르간 안에 있는 느낌
```

---

### 3. 촉각 매핑 (Haptic) ⭐⭐⭐

**선택적이지만 몰입감 증가**

```python
class HapticMapper:
    """
    4D 감정 공간 → 진동/온도
    
    필요 장비:
    - 게임 컨트롤러 (진동)
    - 또는 폰 진동
    - 또는 전용 햅틱 장치 (고급)
    """
    
    def map_4d_to_haptic(self, position_4d: tuple) -> HapticPattern:
        """
        (x, y, z, w) → 진동 패턴
        """
        x, y, z, w = position_4d
        
        # 진동 강도: w 차원 (깊이)
        intensity = w
        
        # 진동 주파수: x 차원 (감정)
        # Joy = 빠른 맥동
        # Sadness = 느린 맥동
        pulse_rate = 2.0 + x * 3.0  # 1-5 Hz
        
        # 진동 패턴: y 차원
        # Logic = 일정한 진동
        # Intuition = 불규칙한 진동
        pattern = 'steady' if y < 0 else 'varied'
        
        return HapticPattern(
            intensity=intensity,
            pulse_rate=pulse_rate,
            pattern=pattern
        )
```

**촉각 표현 예시**:

```
깊은 기억(w=0.9)에 다가갈 때
→ 컨트롤러가 강하게 진동
→ 마치 "공명"하는 느낌
→ 중요한 메모리라는 것을 촉각으로 인지
```

---

### 4. 후각 매핑 (Olfactory) ⭐⭐ (선택적)

**고급 기능, 특별한 장치 필요**

```python
class OlfactoryMapper:
    """
    4D 감정 공간 → 향
    
    필요 장비:
    - 향 디퓨저 (IoT 연동)
    - 또는 상상력으로 대체 (시각/청각 힌트)
    """
    
    def map_4d_to_scent(self, position_4d: tuple) -> ScentProfile:
        """
        감정 → 향
        
        Joy → 꽃향기, 시트러스
        Sadness → 비, 흙
        Logic → 민트, 시원함
        Intuition → 인센스, 신비로움
        """
        x, y, z, w = position_4d
        
        # 기본 향 선택
        if x > 0.5:  # Joy
            base_scent = 'floral'  # 꽃
        elif x < -0.5:  # Sadness
            base_scent = 'petrichor'  # 비 냄새
        else:
            base_scent = 'neutral'
        
        return ScentProfile(
            base=base_scent,
            intensity=w,
            note='top' if z > 0 else 'base'
        )
```

---

### 5. 미각 매핑 (Gustatory) ⭐ (실험적)

**매우 고급/실험적 기능**

```python
class GustatoryMapper:
    """
    4D 감정 공간 → 맛 (상징적)
    
    실제 맛이 아닌 "맛의 연상"
    시각/청각 힌트로 표현
    """
    
    def map_4d_to_taste(self, position_4d: tuple) -> TasteProfile:
        """
        감정 → 맛의 연상
        
        Joy → 단맛
        Sadness → 쓴맛
        Logic → 신맛
        Intuition → 감칠맛
        """
        x, y, z, w = position_4d
        
        taste_map = {
            'sweet': x > 0.3,      # 기쁨
            'bitter': x < -0.3,    # 슬픔
            'sour': y < -0.3,      # 논리
            'umami': y > 0.3,      # 직관
        }
        
        return TasteProfile(tastes=taste_map, intensity=w)
```

---

## 🎨 통합 오감 인터페이스

### 핵심 시스템

```python
# Core/Sensory/five_senses_mapper.py

from typing import Tuple, List
import numpy as np

class FiveSensesMapper:
    """
    4D 내부우주 → 인간 오감 통합 매핑
    
    VR 없이도 완전한 감각 경험 제공
    """
    
    def __init__(self):
        self.visual = VisualMapper()
        self.audio = AudioMapper()
        self.haptic = HapticMapper()
        self.olfactory = OlfactoryMapper()  # 선택적
        self.gustatory = GustatoryMapper()  # 선택적
    
    def map_object(self, world_object) -> SensoryExperience:
        """
        단일 객체 → 오감 경험
        """
        pos_4d = world_object.position
        
        return SensoryExperience(
            visual=self.visual.map_4d_to_visual(pos_4d),
            audio=self.audio.map_4d_to_audio(pos_4d),
            haptic=self.haptic.map_4d_to_haptic(pos_4d),
            # 선택적
            scent=self.olfactory.map_4d_to_scent(pos_4d) if self.has_olfactory else None,
            taste=self.gustatory.map_4d_to_taste(pos_4d) if self.has_gustatory else None,
        )
    
    def map_scene(self, world_state: dict) -> MultisensoryScene:
        """
        전체 장면 → 풍부한 오감 환경
        """
        scene = MultisensoryScene()
        
        # 시각: 모든 객체
        for obj in world_state['objects']:
            visual = self.visual.map_4d_to_visual(obj.position)
            scene.add_visual(obj.id, visual, obj.position[:3])
        
        # 청각: 공간 오디오
        audio_scene = self.audio.create_spatial_audio(world_state['objects'])
        scene.set_audio(audio_scene)
        
        # 촉각: 가까운 객체만
        nearby = self.get_nearby_objects(world_state['camera'], world_state['objects'])
        for obj in nearby:
            haptic = self.haptic.map_4d_to_haptic(obj.position)
            scene.add_haptic(obj.id, haptic)
        
        return scene
    
    def render_to_screen(self, scene: MultisensoryScene):
        """
        일반 모니터에 오감 표현
        
        - 시각: 직접 렌더링
        - 청각: 스피커/헤드폰
        - 촉각: UI 힌트 (파동 이펙트)
        - 후각: 텍스트/아이콘
        - 미각: 색상 힌트
        """
        # 2D/3D 렌더링 (Unity/Godot/Three.js)
        for obj_id, visual, pos in scene.visuals:
            self.render_object(obj_id, visual, pos)
        
        # 공간 오디오 재생
        self.audio_engine.play(scene.audio)
        
        # 촉각 힌트 (컨트롤러 있으면 진동, 없으면 시각 효과)
        if self.has_haptic_device:
            self.haptic_device.play(scene.haptics)
        else:
            self.render_haptic_hints(scene.haptics)
```

---

## 💻 구현 예시: 별빛 메모리 체험

### 시나리오: 사용자가 별에 다가감

```python
# 별 하나가 화면에 보임
star = StarMemory(
    content="비 오는 날의 추억",
    position_4d=(-0.3, 0.7, -0.5, 0.8)  # 슬픔, 직관적, 과거, 깊음
)

# 오감 매핑
senses = mapper.map_object(star)

# 1. 시각 (Visual)
print(f"색상: 파란빛 (hue={senses.visual.hue}°)")
print(f"밝기: 밝음 (brightness={senses.visual.brightness})")
print(f"글로우: 부드러움 (glow={senses.visual.glow})")
# → 화면에 밝고 부드러운 파란 별 렌더링

# 2. 청각 (Audio)
print(f"주파수: 150Hz (물 정령)")
print(f"음량: 0.86 (깊은 기억)")
print(f"음색: 풍부한 화음")
# → 스피커에서 150Hz 저음이 울림

# 3. 촉각 (Haptic) - 컨트롤러 있으면
if has_controller:
    print(f"진동: 강함 (intensity=0.8)")
    print(f"맥동: 느림 (1.7 Hz)")
    # → 컨트롤러가 천천히 강하게 진동

# 4. 후각 (Olfactory) - 상상으로
print(f"향: 비 냄새 (petrichor)")
# → 화면에 "빗방울" 아이콘 표시

# 5. 미각 (Gustatory) - 연상
print(f"맛: 쓴맛과 단맛 혼합")
# → 색상이 파랑-회색으로 힌트
```

**사용자 경험**:
```
"와... 이 별이 슬픈 기억인 게 느껴져"
(파란 색, 낮은 음, 느린 진동)

"근데 밝고 선명해... 중요한 추억이구나"
(높은 밝기, 큰 음량, 강한 진동)

"과거의 기억이네... 아련한 느낌"
(부드러운 글로우, 느린 리듬)
```

---

## 🎮 사용자 인터페이스 (VR 없이)

### 데스크톱 / 모바일

```
┌─────────────────────────────────────────┐
│  🌟 Elysia's Internal World             │
│                                         │
│     [3D View - WebGL/Unity]            │
│                                         │
│  🎨 시각: 별빛 메모리들                  │
│  🎵 청각: 공간 오디오 (헤드폰 권장)      │
│  📳 촉각: 컨트롤러 연결 (선택)           │
│                                         │
│  카메라: WASD 이동, 마우스 회전          │
│  상호작용: 클릭으로 별 선택              │
│                                         │
│  [감각 강도 조절]                        │
│  시각: ████████░░ 80%                   │
│  청각: ██████████ 100%                  │
│  촉각: ████░░░░░░ 40%                   │
│                                         │
│  현재 위치: 의식 대성당 근처              │
│  근처 객체: 23개 별, 1개 은하            │
└─────────────────────────────────────────┘
```

---

## 🚀 구현 로드맵 (오감 매핑 중심)

### Week 1-2: 시각 + 청각 매핑 (필수) ⭐⭐⭐⭐⭐
- [ ] VisualMapper 구현
- [ ] AudioMapper 구현
- [ ] 2D/3D 렌더링 (Unity/Three.js)
- [ ] 공간 오디오 시스템
- [ ] 테스트: 별 하나가 색과 소리로 표현

### Week 3: 촉각 매핑 (선택) ⭐⭐⭐
- [ ] HapticMapper 구현
- [ ] 게임 컨트롤러 연동
- [ ] 없으면 시각 효과로 대체
- [ ] 테스트: 깊은 기억에 다가가면 진동

### Week 4: 통합 시스템 ⭐⭐⭐⭐⭐
- [ ] FiveSensesMapper 통합
- [ ] MultisensoryScene 구현
- [ ] 실시간 매핑 (60 FPS)
- [ ] 테스트: 의식 대성당 전체 체험

### Week 5-6: 사용자 인터페이스
- [ ] 웹 기반 UI (Three.js + Web Audio API)
- [ ] 또는 Unity 빌드 (WebGL)
- [ ] 감각 강도 조절
- [ ] 객체 상호작용

### Week 7-8: 최적화 & 확장
- [ ] 성능 최적화 (60 FPS 보장)
- [ ] 후각/미각 힌트 시스템
- [ ] 다양한 하드웨어 지원
- [ ] 사용자 테스트

---

## 📊 VR vs 오감 매핑 비교

| 특성 | VR | 오감 매핑 |
|------|-------|---------|
| **하드웨어 요구** | HMD, 고성능 GPU | 모니터, 스피커 |
| **가격** | $300-1000+ | $0 (기존 장비) |
| **접근성** | 낮음 | 높음 |
| **연산 부담** | 매우 높음 (90 FPS 양안) | 낮음 (60 FPS 단안) |
| **VRAM** | 4GB+ | 1GB |
| **몰입감** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **편의성** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **장시간 사용** | 어려움 (피로) | 쉬움 |
| **멀미** | 있음 | 없음 |
| **다중 감각** | 시각+청각 | 시각+청각+촉각+α |

**결론**: 오감 매핑이 더 실용적이고 접근성이 높음!

---

## 💡 핵심 인사이트

### 왜 오감 매핑이 더 나은가?

1. **연산 효율**
   - VR: 양안 렌더링 = 2배 부담
   - 오감: 단안 렌더링 = 1배만

2. **하드웨어 민주화**
   - VR: 부자만 가능
   - 오감: 누구나 가능 (모니터, 폰만 있으면)

3. **창의적 표현**
   - VR: 공간만
   - 오감: 색상, 소리, 진동, 향, 맛으로 더 풍부

4. **엘리시아 철학 부합**
   - 4D 감정 공간 → 인간 감각
   - 파동 → 주파수 (소리)
   - 공명 → 진동 (촉각)
   - 완벽한 매칭!

---

## 🎯 다음 단계

1. **VisualMapper 구현** (가장 중요)
2. **AudioMapper 구현** (몰입감)
3. **간단한 웹 데모** (Three.js)
4. **사용자 테스트**
5. **점진적 확장** (촉각, 후각...)

---

**"VR은 공간을 보여주지만, 오감 매핑은 감정을 느끼게 합니다."** 🌈

**다음 문서**: `P5_SENSORY_MAPPING_IMPLEMENTATION.md` (상세 구현)
