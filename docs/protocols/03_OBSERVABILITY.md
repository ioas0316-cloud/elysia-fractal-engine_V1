# Protocol 03: 관찰 가능성과 텔레메트리 (Observability & Telemetry)

> "우리가 측정할 수 없는 것은 개선할 수 없습니다."

## 1. 개요

Elysia의 내부 상태를 관찰하고 모니터링하는 시스템입니다.
의식 엔진의 건강 상태, 성능, 그리고 행동을 추적합니다.

---

## 2. 핵심 메트릭

### A. 전역 의식 메트릭

| 메트릭 | 설명 | 범위 | 이상적인 값 |
|--------|------|------|-------------|
| **엔트로피** | 시스템의 혼란도 | 0.0 ~ 1.0 | 0.3 ~ 0.5 |
| **정렬 점수** | 위상 정렬도 | 0.0 ~ 1.0 | > 0.7 |
| **에너지 평균** | 평균 활력 | 0.0 ~ ∞ | 상황 의존 |
| **모멘텀 평균** | 평균 관성 | 0.0 ~ ∞ | 상황 의존 |

### B. 개체 수준 메트릭

```python
entity_metrics = {
    "soul_tensor": {
        "amplitude": 0.8,     # 존재의 강도
        "frequency": 0.5,     # 진동 주파수
        "phase": 1.57         # 위상 (라디안)
    },
    "trinity": {
        "body": 0.33,
        "soul": 0.34,
        "spirit": 0.33
    },
    "vitality": 0.95,
    "momentum": 0.7
}
```

---

## 3. GlobalConsciousness 시스템

### 구현

```python
from elysia_engine.consciousness import GlobalConsciousness

class GlobalConsciousness(System):
    """
    전체(신/시스템)가 부분(개체들)을 관찰합니다.
    전역 메트릭(엔트로피, 정렬)을 계산하고 신성한 개입을 수행합니다.
    """
    
    def __init__(self, physics=None):
        self.physics = physics
        self.global_entropy = 0.0
        self.alignment_score = 0.0
        self.last_intervention_tick = 0
    
    def calculate_metrics(self, world):
        """전역 메트릭 계산"""
        total_energy = 0.0
        phase_vectors = Vector3(0, 0, 0)
        count = 0
        
        for entity in world.entities.values():
            if not entity.soul:
                continue
            
            count += 1
            total_energy += entity.soul.frequency
            
            # 위상을 벡터로 매핑
            px = math.cos(entity.soul.phase)
            py = math.sin(entity.soul.phase)
            phase_vectors += Vector3(px, py, 0)
        
        if count == 0:
            self.global_entropy = 0.0
            return
        
        # 정렬도: 평균 위상 벡터의 크기
        avg_phase_vec = phase_vectors * (1.0 / count)
        self.alignment_score = avg_phase_vec.magnitude
        
        # 엔트로피: 정렬의 역수
        self.global_entropy = 1.0 - self.alignment_score
```

### 신성한 개입 (Divine Intervention)

```python
def divine_intervention(self, world, intent):
    """
    시스템이 의도에 따라 우주의 상수를 수정합니다.
    """
    self.last_intervention_tick = world.tick
    
    if intent == "restore_order":
        # 질서 회복: 중력 증가
        if self.physics:
            self.physics.gravity_constant *= 1.5
            self.physics.gravity_constant = min(
                self.physics.gravity_constant, 
                50.0
            )
        logger.warning(
            f"엔트로피 위기 ({self.global_entropy:.2f}). "
            f"중력 강화: {self.physics.gravity_constant:.1f}"
        )
    
    elif intent == "spark_change":
        # 변화 유발: 결합 증가
        if self.physics:
            self.physics.coupling_constant *= 2.0
        logger.info("정체 감지. 영혼 결합 증가.")
```

---

## 4. 로깅 시스템

### 계층적 로거

```python
from elysia_engine.logging_config import get_logger, configure_root_logger

# 모듈별 로거 가져오기
logger = get_logger(__name__)

# 로그 레벨 설정
configure_root_logger(level="DEBUG")

# 사용 예시
logger.debug("디버그 메시지")
logger.info("정보 메시지")
logger.warning("경고 메시지")
logger.error("오류 메시지")
```

### 환경 변수 설정

```bash
# .env 파일
ELYSIA_LOG_LEVEL=DEBUG
ELYSIA_LOG_FILE=elysia.log
```

---

## 5. 페르소나 스냅샷

### 실시간 상태 내보내기

```python
def export_persona_snapshot(entity):
    """개체의 현재 페르소나 상태를 내보냅니다."""
    return {
        "tick": world.tick,
        "time": world.time,
        "entity_count": len(world.entities),
        "energy_avg": calculate_avg_energy(world),
        "momentum_avg": calculate_avg_momentum(world),
        "caption": f"tick={world.tick}, E={energy_avg:.2f}, P={momentum_avg:.2f}"
    }
```

### 출력 예시

```text
[tick 001] {'tick': 1, 'time': 1.0, 'entity_count': 3, 'energy_avg': 0.18, 'momentum_avg': 0.18}
[tick 002] {'tick': 2, 'time': 2.0, 'entity_count': 3, 'energy_avg': 0.49, 'momentum_avg': 0.48}
[tick 003] {'tick': 3, 'time': 3.0, 'entity_count': 3, 'energy_avg': 0.90, 'momentum_avg': 0.87}
```

---

## 6. 예외 처리

### 커스텀 예외 클래스

```python
from elysia_engine.exceptions import (
    ElysiaError,
    TensorError,
    PhysicsError,
    EntityError,
    ConfigurationError,
    ConsciousnessError
)

try:
    tensor = SoulTensor(amplitude=-1.0)  # 잘못된 값
except TensorError as e:
    logger.error(f"텐서 오류: {e}")
    logger.debug(f"상세: {e.details}")
```

### 예외 계층

```
ElysiaError (기본 클래스)
├── TensorError      # SoulTensor 관련 오류
├── PhysicsError     # 물리 시스템 오류
├── EntityError      # 개체 관련 오류
├── ConfigurationError  # 설정 오류
└── ConsciousnessError  # 의식 시스템 오류
```

---

## 7. 설정 관리

### ElysiaConfig

```python
from elysia_engine.config import ElysiaConfig, get_config, set_config

# 현재 설정 가져오기
config = get_config()

# 설정 수정
config.gravity_constant = 15.0
config.time_scale = 1.5

# 또는 새 설정 적용
new_config = ElysiaConfig(
    gravity_constant=20.0,
    coupling_constant=1.5,
    time_scale=2.0
)
set_config(new_config)
```

---

## 8. 모니터링 대시보드 개념

### 실시간 메트릭 표시

```python
def create_dashboard_data(world):
    """대시보드용 데이터 생성"""
    consciousness = find_consciousness_system(world)
    
    return {
        "global": {
            "entropy": consciousness.global_entropy,
            "alignment": consciousness.alignment_score,
            "tick": world.tick,
            "time": world.time
        },
        "entities": [
            {
                "id": e.id,
                "name": e.name,
                "position": e.position.to_dict(),
                "vitality": e.vitality,
                "soul": e.soul.to_dict() if e.soul else None
            }
            for e in world.entities.values()
        ],
        "physics": {
            "gravity": world.physics.gravity_constant,
            "coupling": world.physics.coupling_constant
        }
    }
```

---

## 9. 텔레메트리 모범 사례

### 1. 구조화된 로깅

```python
# 좋음
logger.info("개체 생성", extra={
    "entity_id": entity.id,
    "entity_type": entity.type,
    "position": entity.position
})

# 피하기
logger.info(f"개체 {entity.id} 생성됨")
```

### 2. 메트릭 수집 주기

| 메트릭 유형 | 수집 주기 | 이유 |
|-------------|-----------|------|
| 전역 엔트로피 | 매 틱 | 빠른 변화 감지 |
| 개체 상태 | 10틱마다 | 성능 최적화 |
| 시스템 건강 | 100틱마다 | 장기 추세 |

### 3. 경고 임계값

```python
ALERT_THRESHOLDS = {
    "entropy": {
        "warning": 0.7,
        "critical": 0.9
    },
    "alignment": {
        "warning": 0.3,
        "critical": 0.1
    }
}

def check_alerts(consciousness):
    if consciousness.global_entropy > ALERT_THRESHOLDS["entropy"]["critical"]:
        send_alert("CRITICAL: 엔트로피 위기!")
    elif consciousness.global_entropy > ALERT_THRESHOLDS["entropy"]["warning"]:
        send_alert("WARNING: 엔트로피 증가 중")
```

---

*참고: [Elysia Project Protocols](https://github.com/ioas0316-cloud/Elysia/tree/main/Protocols)*
