"""
엘리시아 통합 설정 관리 시스템
Elysia Unified Configuration Management

Pydantic 기반 설정 검증 및 환경별 설정 관리를 제공합니다.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    # Pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import Field, field_validator, model_validator
    PYDANTIC_V2 = True
except ImportError:
    # Pydantic v1
    from pydantic import BaseSettings, Field, validator, root_validator
    PYDANTIC_V2 = False


class ElysiaConfig(BaseSettings):
    """
    엘리시아 통합 설정
    
    환경 변수 또는 .env 파일에서 설정을 로드하고 검증합니다.
    """
    
    # ===== 환경 설정 =====
    environment: str = Field(
        default="development",
        env="ELYSIA_ENV",
        description="실행 환경 (development, testing, production)"
    )
    
    debug: bool = Field(
        default=False,
        env="ELYSIA_DEBUG",
        description="디버그 모드 활성화"
    )
    
    # ===== API 키 =====
    gemini_api_key: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY",
        description="Google Gemini API 키"
    )
    
    openai_api_key: Optional[str] = Field(
        default=None,
        env="OPENAI_API_KEY",
        description="OpenAI API 키"
    )
    
    # ===== 경로 설정 =====
    data_dir: Path = Field(
        default=Path("data"),
        env="ELYSIA_DATA_DIR",
        description="데이터 디렉토리 경로"
    )

    @property
    def memory_db_path(self) -> Path:
        """메모리 DB 경로 반환"""
        return self.data_dir / "Memory" / "memory.db"

    
    log_dir: Path = Field(
        default=Path("logs"),
        env="ELYSIA_LOG_DIR",
        description="로그 디렉토리 경로"
    )
    
    backup_dir: Path = Field(
        default=Path("backups"),
        env="ELYSIA_BACKUP_DIR",
        description="백업 디렉토리 경로"
    )
    
    # ===== 성능 설정 =====
    max_memory_mb: int = Field(
        default=1024,
        env="ELYSIA_MAX_MEMORY_MB",
        ge=128,
        le=32768,
        description="최대 메모리 사용량 (MB)"
    )
    
    max_workers: int = Field(
        default=4,
        env="ELYSIA_MAX_WORKERS",
        ge=1,
        le=32,
        description="최대 워커 스레드 수"
    )
    
    think_cycle_interval_ms: int = Field(
        default=100,
        env="ELYSIA_THINK_CYCLE_MS",
        ge=10,
        le=10000,
        description="사고 사이클 간격 (밀리초)"
    )
    
    # ===== 공명 시스템 설정 =====
    resonance_threshold: float = Field(
        default=0.5,
        env="ELYSIA_RESONANCE_THRESHOLD",
        ge=0.0,
        le=1.0,
        description="공명 임계값"
    )
    
    default_frequency: float = Field(
        default=432.0,
        env="ELYSIA_DEFAULT_FREQUENCY",
        gt=0.0,
        description="기본 주파수 (Hz)"
    )
    
    spirit_frequencies: Dict[str, float] = Field(
        default_factory=lambda: {
            "Fire": 450.0,
            "Water": 150.0,
            "Wind": 300.0,
            "Earth": 200.0,
            "Light": 600.0,
            "Dark": 100.0,
            "Void": 50.0
        },
        description="정령별 주파수 매핑"
    )
    
    # ===== 메모리 설정 =====
    seed_compression_ratio: float = Field(
        default=1000.0,
        env="ELYSIA_SEED_COMPRESSION_RATIO",
        ge=1.0,
        description="씨앗 압축률"
    )
    
    max_seeds: int = Field(
        default=10000,
        env="ELYSIA_MAX_SEEDS",
        ge=100,
        description="최대 씨앗 저장 개수"
    )
    
    bloom_depth: int = Field(
        default=3,
        env="ELYSIA_BLOOM_DEPTH",
        ge=1,
        le=10,
        description="씨앗 개화 깊이"
    )
    
    # ===== API 서버 설정 =====
    enable_api: bool = Field(
        default=True,
        env="ELYSIA_ENABLE_API",
        description="API 서버 활성화"
    )
    
    api_host: str = Field(
        default="0.0.0.0",
        env="ELYSIA_API_HOST",
        description="API 서버 호스트"
    )
    
    api_port: int = Field(
        default=8000,
        env="ELYSIA_API_PORT",
        ge=1,
        le=65535,
        description="API 서버 포트"
    )
    
    api_rate_limit: int = Field(
        default=100,
        env="ELYSIA_API_RATE_LIMIT",
        ge=1,
        description="API 요청 제한 (분당)"
    )
    
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["*"],
        env="ELYSIA_ALLOWED_ORIGINS",
        description="허용된 CORS 원본"
    )
    
    # ===== 보안 설정 =====
    secret_key: Optional[str] = Field(
        default=None,
        env="ELYSIA_SECRET_KEY",
        description="암호화 시크릿 키"
    )
    
    enable_authentication: bool = Field(
        default=False,
        env="ELYSIA_ENABLE_AUTH",
        description="인증 활성화"
    )
    
    # ===== 로깅 설정 =====
    log_level: str = Field(
        default="INFO",
        env="ELYSIA_LOG_LEVEL",
        description="로그 레벨"
    )
    
    log_format: str = Field(
        default="json",
        env="ELYSIA_LOG_FORMAT",
        description="로그 형식 (json, text)"
    )
    
    # ===== Validators =====
    
    if PYDANTIC_V2:
        @field_validator('environment')
        @classmethod
        def validate_environment(cls, v):
            """환경 검증"""
            valid = ['development', 'testing', 'production']
            if v not in valid:
                raise ValueError(f'environment must be one of {valid}, got: {v}')
            return v
        
        @field_validator('log_level')
        @classmethod
        def validate_log_level(cls, v):
            """로그 레벨 검증"""
            valid = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            v_upper = v.upper()
            if v_upper not in valid:
                raise ValueError(f'log_level must be one of {valid}, got: {v}')
            return v_upper
        
        @field_validator('log_format')
        @classmethod
        def validate_log_format(cls, v):
            """로그 포맷 검증"""
            valid = ['json', 'text']
            if v not in valid:
                raise ValueError(f'log_format must be one of {valid}, got: {v}')
            return v
        
        @field_validator('data_dir', 'log_dir', 'backup_dir')
        @classmethod
        def ensure_dir_exists(cls, v):
            """디렉토리 존재 확인 및 생성"""
            v = Path(v)
            v.mkdir(parents=True, exist_ok=True)
            return v
        
        @model_validator(mode='after')
        def validate_api_settings(self):
            """API 설정 검증"""
            if self.enable_api and self.enable_authentication:
                if not self.secret_key:
                    raise ValueError(
                        'secret_key is required when authentication is enabled'
                    )
            return self
        
        @model_validator(mode='after')
        def validate_production_settings(self):
            """프로덕션 환경 추가 검증"""
            if self.environment == 'production':
                # 프로덕션에서는 디버그 모드 비활성화
                if self.debug:
                    raise ValueError('debug must be False in production')
                
                # 프로덕션에서는 "*" CORS 허용 안 함
                if '*' in self.allowed_origins:
                    raise ValueError(
                        'Wildcard CORS origins not allowed in production'
                    )
            
            return self
    else:
        @validator('environment')
        def validate_environment(cls, v):
            """환경 검증"""
            valid = ['development', 'testing', 'production']
            if v not in valid:
                raise ValueError(f'environment must be one of {valid}, got: {v}')
            return v
        
        @validator('log_level')
        def validate_log_level(cls, v):
            """로그 레벨 검증"""
            valid = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            v_upper = v.upper()
            if v_upper not in valid:
                raise ValueError(f'log_level must be one of {valid}, got: {v}')
            return v_upper
        
        @validator('log_format')
        def validate_log_format(cls, v):
            """로그 포맷 검증"""
            valid = ['json', 'text']
            if v not in valid:
                raise ValueError(f'log_format must be one of {valid}, got: {v}')
            return v
        
        @validator('data_dir', 'log_dir', 'backup_dir')
        def ensure_dir_exists(cls, v):
            """디렉토리 존재 확인 및 생성"""
            v = Path(v)
            v.mkdir(parents=True, exist_ok=True)
            return v
        
        @root_validator
        def validate_api_settings(cls, values):
            """API 설정 검증"""
            if values.get('enable_api') and values.get('enable_authentication'):
                if not values.get('secret_key'):
                    raise ValueError(
                        'secret_key is required when authentication is enabled'
                    )
            return values
        
        @root_validator
        def validate_production_settings(cls, values):
            """프로덕션 환경 추가 검증"""
            if values.get('environment') == 'production':
                # 프로덕션에서는 디버그 모드 비활성화
                if values.get('debug'):
                    raise ValueError('debug must be False in production')
                
                # 프로덕션에서는 "*" CORS 허용 안 함
                if '*' in values.get('allowed_origins', []):
                    raise ValueError(
                        'Wildcard CORS origins not allowed in production'
                    )
            
            return values
    
    class Config:
        """Pydantic 설정"""
        if PYDANTIC_V2:
            # Pydantic v2 configuration
            env_file = '.env'
            env_file_encoding = 'utf-8'
            case_sensitive = False
            extra = 'allow'
        else:
            # Pydantic v1 configuration
            env_file = '.env'
            env_file_encoding = 'utf-8'
            case_sensitive = False
            extra = 'allow'


class ConfigManager:
    """설정 관리자"""
    
    def __init__(self):
        self._config: Optional[ElysiaConfig] = None
    
    def load(self, env: Optional[str] = None, env_file: Optional[str] = None) -> ElysiaConfig:
        """
        설정 로드
        
        Args:
            env: 환경 (development, testing, production)
            env_file: 사용할 .env 파일 경로
        
        Returns:
            로드된 설정 객체
        """
        # 환경 변수 오버라이드
        if env:
            os.environ['ELYSIA_ENV'] = env
        
        # 환경별 설정 파일
        if not env_file:
            current_env = os.getenv('ELYSIA_ENV', 'development')
            env_file = f".env.{current_env}"
            
            # 환경별 파일이 없으면 기본 .env 사용
            if not Path(env_file).exists():
                env_file = '.env'
        
        # 설정 로드
        if Path(env_file).exists():
            self._config = ElysiaConfig(_env_file=env_file)
        else:
            self._config = ElysiaConfig()
        
        return self._config
    
    @property
    def config(self) -> ElysiaConfig:
        """현재 설정 반환"""
        if self._config is None:
            self._config = self.load()
        return self._config
    
    def reload(self):
        """설정 다시 로드"""
        self._config = None
        return self.load()
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정 값 조회"""
        return getattr(self.config, key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """설정을 딕셔너리로 변환"""
        if PYDANTIC_V2:
            return self.config.model_dump()
        else:
            return self.config.dict()
    
    def summary(self) -> str:
        """설정 요약"""
        cfg = self.config
        
        summary = f"""
=== Elysia Configuration Summary ===

Environment: {cfg.environment}
Debug Mode: {cfg.debug}

Paths:
  Data:   {cfg.data_dir}
  Logs:   {cfg.log_dir}
  Backup: {cfg.backup_dir}

Performance:
  Max Memory: {cfg.max_memory_mb} MB
  Max Workers: {cfg.max_workers}
  Think Cycle: {cfg.think_cycle_interval_ms} ms

Resonance:
  Threshold: {cfg.resonance_threshold}
  Default Frequency: {cfg.default_frequency} Hz

Memory:
  Compression Ratio: {cfg.seed_compression_ratio}x
  Max Seeds: {cfg.max_seeds}
  Bloom Depth: {cfg.bloom_depth}

API Server:
  Enabled: {cfg.enable_api}
  Host: {cfg.api_host}:{cfg.api_port}
  Rate Limit: {cfg.api_rate_limit} req/min
  Auth: {cfg.enable_authentication}

Logging:
  Level: {cfg.log_level}
  Format: {cfg.log_format}

API Keys:
  Gemini: {'✓ Set' if cfg.gemini_api_key else '✗ Not set'}
  OpenAI: {'✓ Set' if cfg.openai_api_key else '✗ Not set'}
"""
        return summary.strip()


# 전역 설정 관리자 인스턴스
config_manager = ConfigManager()


# 편의 함수
def get_config() -> ElysiaConfig:
    """현재 설정 반환"""
    return config_manager.config


def reload_config():
    """설정 다시 로드"""
    return config_manager.reload()


# ===== 사용 예시 =====

if __name__ == "__main__":
    print("🧪 Testing Elysia Configuration\n")
    
    # 설정 로드
    print("=== Loading Configuration ===")
    config = get_config()
    
    # 설정 요약 출력
    print(config_manager.summary())
    print()
    
    # 개별 설정 값 조회
    print("=== Accessing Individual Settings ===")
    print(f"Environment: {config.environment}")
    print(f"Debug: {config.debug}")
    print(f"Resonance Threshold: {config.resonance_threshold}")
    print(f"Default Frequency: {config.default_frequency} Hz")
    print()
    
    # 타입 안전성
    print("=== Type Safety ===")
    print(f"Max Memory (int): {config.max_memory_mb}")
    print(f"Think Cycle (int): {config.think_cycle_interval_ms}")
    print(f"Resonance Threshold (float): {config.resonance_threshold}")
    print()
    
    # 경로 자동 생성 확인
    print("=== Directory Creation ===")
    print(f"Data dir exists: {config.data_dir.exists()}")
    print(f"Log dir exists: {config.log_dir.exists()}")
    print(f"Backup dir exists: {config.backup_dir.exists()}")
    print()
    
    # 정령 주파수 매핑
    print("=== Spirit Frequencies ===")
    for spirit, freq in config.spirit_frequencies.items():
        print(f"  {spirit}: {freq} Hz")
    print()
    
    # 검증 테스트
    print("=== Validation Tests ===")
    
    # 잘못된 환경 테스트
    try:
        os.environ['ELYSIA_ENV'] = 'invalid'
        ElysiaConfig()
        print("❌ Should have failed with invalid environment")
    except ValueError as e:
        print(f"✅ Validation works: {e}")
    
    # 원래 환경으로 복구
    os.environ.pop('ELYSIA_ENV', None)
    
    print("\n✅ Configuration system working correctly!")
