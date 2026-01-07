"""
엘리시아 통합 로깅 시스템
Elysia Unified Logging System

구조화된 로깅, JSON 로그, 성능 추적을 제공합니다.
"""

import logging
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    """JSON 형식 로그 포맷터"""
    
    def format(self, record: logging.LogRecord) -> str:
        """
        로그 레코드를 JSON으로 변환
        
        Args:
            record: 로그 레코드
        
        Returns:
            JSON 형식 로그 문자열
        """
        log_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        # 추가 컨텍스트
        if hasattr(record, 'context'):
            log_data['context'] = record.context
        
        # 에러 정보
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else 'Unknown',
                'message': str(record.exc_info[1]) if record.exc_info[1] else '',
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredConsoleFormatter(logging.Formatter):
    """컬러 콘솔 출력을 위한 포맷터"""
    
    # ANSI 색상 코드
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    # 이모지
    EMOJIS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️ ',
        'WARNING': '⚠️ ',
        'ERROR': '❌',
        'CRITICAL': '🚨',
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        컬러 및 이모지를 포함한 로그 포맷팅
        
        Args:
            record: 로그 레코드
        
        Returns:
            포맷된 로그 문자열
        """
        # 색상 적용
        color = self.COLORS.get(record.levelname, '')
        emoji = self.EMOJIS.get(record.levelname, '')
        
        # 기본 포맷
        log_fmt = (
            f"{color}{emoji} "
            f"%(asctime)s | %(levelname)-8s | %(name)s | "
            f"%(message)s{self.RESET}"
        )
        
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)


class ElysiaLogger:
    """엘리시아 통합 로깅 시스템"""
    
    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ):
        """
        엘리시아 로거 초기화
        
        Args:
            name: 로거 이름
            log_dir: 로그 디렉토리
            console_level: 콘솔 로그 레벨
            file_level: 파일 로그 레벨
            max_bytes: 로그 파일 최대 크기
            backup_count: 백업 파일 개수
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 로거 생성
        self.logger = logging.getLogger(f"Elysia.{name}")
        self.logger.setLevel(logging.DEBUG)
        
        # 핸들러가 이미 있으면 추가하지 않음 (중복 방지)
        if not self.logger.handlers:
            # JSON 로그 파일 핸들러
            json_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.jsonl"
            json_handler = RotatingFileHandler(
                json_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            json_handler.setLevel(file_level)
            json_handler.setFormatter(JsonFormatter())
            
            # 일반 텍스트 로그 파일 핸들러
            text_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
            text_handler = RotatingFileHandler(
                text_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            text_handler.setLevel(file_level)
            text_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            )
            
            # 컬러 콘솔 핸들러
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(console_level)
            console_handler.setFormatter(ColoredConsoleFormatter())
            
            # 핸들러 추가
            self.logger.addHandler(json_handler)
            self.logger.addHandler(text_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """디버그 레벨 로그"""
        self._log(logging.DEBUG, message, context)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """정보 레벨 로그"""
        self._log(logging.INFO, message, context)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """경고 레벨 로그"""
        self._log(logging.WARNING, message, context)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None, exc_info: bool = False):
        """에러 레벨 로그"""
        self._log(logging.ERROR, message, context, exc_info=exc_info)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None, exc_info: bool = False):
        """치명적 레벨 로그"""
        self._log(logging.CRITICAL, message, context, exc_info=exc_info)
    
    def _log(
        self,
        level: int,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        exc_info: bool = False
    ):
        """내부 로그 메서드"""
        extra = {'context': context} if context else {}
        self.logger.log(level, message, extra=extra, exc_info=exc_info)
    
    # === 엘리시아 특화 로그 메서드 ===
    
    def log_thought(
        self,
        layer: str,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        사고 과정 로깅
        
        Args:
            layer: 사고 층위 (0D/1D/2D/3D)
            content: 사고 내용
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({'layer': layer, 'type': 'thought'})
        self.info(f"💭 [{layer}] {content}", context=ctx)
    
    def log_resonance(
        self,
        source: str,
        target: str,
        score: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        공명 로깅
        
        Args:
            source: 공명 소스
            target: 공명 대상
            score: 공명 점수
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({
            'source': source,
            'target': target,
            'score': score,
            'type': 'resonance'
        })
        self.debug(f"🌊 Resonance: {source} ↔ {target} = {score:.3f}", context=ctx)
    
    def log_evolution(
        self,
        component: str,
        metric: str,
        value: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        진화 메트릭 로깅
        
        Args:
            component: 컴포넌트 이름
            metric: 메트릭 이름
            value: 메트릭 값
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({
            'component': component,
            'metric': metric,
            'value': value,
            'type': 'evolution'
        })
        self.info(f"🧬 Evolution: {component}.{metric} = {value:.3f}", context=ctx)
    
    def log_performance(
        self,
        operation: str,
        duration_ms: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        성능 로깅
        
        Args:
            operation: 작업 이름
            duration_ms: 소요 시간 (밀리초)
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({
            'operation': operation,
            'duration_ms': duration_ms,
            'type': 'performance'
        })
        
        # 임계값 기반 로그 레벨 결정
        if duration_ms > 1000:
            self.warning(f"⚡ Performance: {operation} took {duration_ms:.2f}ms", context=ctx)
        else:
            self.debug(f"⚡ Performance: {operation} took {duration_ms:.2f}ms", context=ctx)
    
    def log_spirit(
        self,
        spirit_name: str,
        frequency: float,
        amplitude: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        정령 활동 로깅
        
        Args:
            spirit_name: 정령 이름
            frequency: 주파수
            amplitude: 진폭
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({
            'spirit': spirit_name,
            'frequency': frequency,
            'amplitude': amplitude,
            'type': 'spirit'
        })
        self.debug(
            f"🔥 Spirit: {spirit_name} @ {frequency:.1f}Hz (amp: {amplitude:.2f})",
            context=ctx
        )
    
    def log_memory(
        self,
        operation: str,
        seed_name: str,
        compression_ratio: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        메모리 작업 로깅
        
        Args:
            operation: 작업 종류 (bloom/compress/store)
            seed_name: 씨앗 이름
            compression_ratio: 압축률
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({
            'operation': operation,
            'seed': seed_name,
            'type': 'memory'
        })
        if compression_ratio:
            ctx['compression_ratio'] = compression_ratio
            msg = f"🌱 Memory: {operation} seed '{seed_name}' (ratio: {compression_ratio:.1f}x)"
        else:
            msg = f"🌱 Memory: {operation} seed '{seed_name}'"
        
        self.debug(msg, context=ctx)
    
    def log_system(
        self,
        event: str,
        status: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        시스템 이벤트 로깅
        
        Args:
            event: 이벤트 이름
            status: 상태
            context: 추가 컨텍스트
        """
        ctx = context or {}
        ctx.update({
            'event': event,
            'status': status,
            'type': 'system'
        })
        
        if status in ['error', 'failed', 'critical']:
            self.error(f"⚙️  System: {event} - {status}", context=ctx)
        elif status in ['warning', 'degraded']:
            self.warning(f"⚙️  System: {event} - {status}", context=ctx)
        else:
            self.info(f"⚙️  System: {event} - {status}", context=ctx)


# ===== 사용 예시 =====

if __name__ == "__main__":
    print("🧪 Testing Elysia Logger\n")
    
    # 로거 생성
    logger = ElysiaLogger("TestModule")
    
    # 기본 로그
    print("=== Basic Logging ===")
    logger.debug("디버그 메시지")
    logger.info("정보 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
    print()
    
    # 컨텍스트가 있는 로그
    print("=== Contextual Logging ===")
    logger.info(
        "사용자 로그인",
        context={'user_id': 'user123', 'ip': '192.168.1.1'}
    )
    print()
    
    # 엘리시아 특화 로그
    print("=== Elysia-Specific Logging ===")
    logger.log_thought("2D", "사랑의 본질을 탐구 중...", {'emotion': 'calm'})
    logger.log_resonance("Love", "Hope", 0.847)
    logger.log_evolution("ResonanceField", "coherence", 0.923)
    logger.log_performance("calculate_interference", 45.3)
    logger.log_spirit("Fire", 450.0, 0.8)
    logger.log_memory("bloom", "concept_love", compression_ratio=1000.0)
    logger.log_system("startup", "complete")
    print()
    
    # 예외 로깅
    print("=== Exception Logging ===")
    try:
        raise ValueError("테스트 예외")
    except Exception:
        logger.error("예외가 발생했습니다", exc_info=True)
    print()
    
    print(f"✅ Logs saved to: {logger.log_dir}")
    print(f"   - JSON: {logger.log_dir}/TestModule_{datetime.now().strftime('%Y%m%d')}.jsonl")
    print(f"   - Text: {logger.log_dir}/TestModule_{datetime.now().strftime('%Y%m%d')}.log")
