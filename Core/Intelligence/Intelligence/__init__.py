"""
Core.Intelligence - 지성 모듈
=============================

Elysia의 지성을 구성하는 모듈들.

- InnerVoice: 로컬 LLM 기반 내면의 목소리
- SelfAwareness: 자기 인식
- FreeWillEngine: 자유 의지 엔진
- CausalitySeed: 인과 추론 (Logos)
- UnifiedIntelligence: 통합 지성
"""

from .inner_voice import InnerVoice, SelfAwareness

__all__ = [
    'InnerVoice',
    'SelfAwareness',
]