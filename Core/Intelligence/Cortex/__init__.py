"""
Cortex Module (피질 모듈)
========================

Legacy/Project_Sophia에서 마이그레이션된 핵심 Cortex 모듈들.
각 Cortex는 Elysia의 특정 인지 기능을 담당합니다.

모듈:
- ActionCortex: 도구 선택 및 실행
- PlanningCortex: 목표 분해 및 계획 수립
- DreamingCortex: 기억 통합 및 개념 추출
- MetaCognitionCortex: 자기 성찰 및 개념 균형 분석
- MathCortex: 수학 증명 엔진
- FileSystemCortex: 샌드박스 파일 I/O
"""

from .action_cortex import ActionCortex, get_action_cortex
from .planning_cortex import PlanningCortex, get_planning_cortex
from .dreaming_cortex import DreamingCortex, get_dreaming_cortex
from .metacognition_cortex import MetaCognitionCortex, get_metacognition_cortex
from .math_cortex import MathCortex, get_math_cortex, Proof, ProofStep
from .filesystem_cortex import FileSystemCortex, get_filesystem_cortex, FSResult

__all__ = [
    # Action
    'ActionCortex', 'get_action_cortex',
    # Planning
    'PlanningCortex', 'get_planning_cortex',
    # Dreaming
    'DreamingCortex', 'get_dreaming_cortex',
    # MetaCognition
    'MetaCognitionCortex', 'get_metacognition_cortex',
    # Math
    'MathCortex', 'get_math_cortex', 'Proof', 'ProofStep',
    # FileSystem
    'FileSystemCortex', 'get_filesystem_cortex', 'FSResult',
]
