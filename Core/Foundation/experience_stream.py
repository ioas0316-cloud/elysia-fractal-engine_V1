"""
Experience Stream Stub (Placeholder Module)
============================================

이 모듈은 삭제된 `experience_stream.py`의 플레이스홀더입니다.
시스템 실행을 위해 임시로 생성되었습니다.

TODO: 실제 ExperienceStream 구현 필요
"""

import logging

logger = logging.getLogger("Elysia.ExperienceStream")


class ExperienceStream:
    """경험 스트림 플레이스홀더"""
    
    def __init__(self):
        logger.warning("⚠️ ExperienceStream is a stub - real implementation needed")
        self.experiences = []
    
    def add(self, category: str, content: str, intensity: float = 1.0):
        """경험 추가"""
        from dataclasses import dataclass
        @dataclass
        class Experience:
            type: str
            content: str
            intensity: float
        
        exp = Experience(type=category, content=content, intensity=intensity)
        self.experiences.append(exp)
        return exp
    
    def push(self, experience):
        """경험 추가 (legacy)"""
        self.experiences.append(experience)
    
    def pop(self):
        """가장 오래된 경험 반환"""
        if self.experiences:
            return self.experiences.pop(0)
        return None
    
    def get_recent(self, n: int = 10):
        """최근 n개 경험"""
        return self.experiences[-n:] if self.experiences else []
    
    def latest(self, n: int = 10):
        """최근 n개 경험"""
        return self.get_recent(n)
    
    def clear(self):
        """초기화"""
        self.experiences = []
        
    def __len__(self):
        return len(self.experiences)


__all__ = ['ExperienceStream']
