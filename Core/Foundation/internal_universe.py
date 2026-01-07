"""
Internal Universe Facade (Redirect Module)
==========================================

이 모듈은 레거시 호환성을 위한 리다이렉트 파사드입니다.

실제 구현: Core/Memory/Vector/internal_universe.py

35개 이상의 파일이 이 경로에서 InternalUniverse를 찾고 있어서,
모든 파일을 수정하는 대신 이 파사드를 제공합니다.

사용법:
    # 레거시 (이 파사드를 통해 작동)
    from Core.Foundation.internal_universe import InternalUniverse
    
    # 권장 (직접 import)
    from Core.Intelligence.Memory_Linguistics.Memory.Vector.internal_universe import InternalUniverse
"""

import warnings

# 경고 표시 (하지만 작동은 함)
warnings.warn(
    "Core.Foundation.internal_universe is deprecated. "
    "Use Core.Foundation.Memory.Vector.internal_universe instead.",
    DeprecationWarning,
    stacklevel=2
)

# 실제 모듈에서 모든 것을 가져옴
from Core.Intelligence.Memory.Vector.internal_universe import *
from Core.Intelligence.Memory.Vector.internal_universe import InternalUniverse, WorldCoordinate

# 명시적 export
__all__ = ['InternalUniverse', 'WorldCoordinate']
