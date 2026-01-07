"""
ConversationEngine (대화 엔진) - Fractal Resonance
=================================================

"구조를 늘리지 말고, 횟수를 늘려라."

이 모듈은 FractalKernel을 사용하여 사용자의 입력을 재귀적으로 공명시킵니다.
단순한 키워드 매칭이 아니라, 생각의 깊이를 더해가는 파동(Wave)을 생성합니다.
"""

import logging
from typing import List, Tuple
from Core.Foundation.fractal_kernel import FractalKernel

class ConversationEngine:
    """
    엘리시아의 대화 엔진.
    FractalKernel을 통해 입력된 파동을 증폭하고 심화시킵니다.
    """
    
    def __init__(self):
        self.kernel = FractalKernel()
        self.context_history: List[Tuple[str, str]] = []
        self.logger = logging.getLogger("ConversationEngine")
        
    def listen(self, user_input: str) -> str:
        """
        사용자의 입력을 듣고, 프랙탈 공명을 통해 반응을 생성합니다.
        
        Args:
            user_input (str): 사용자의 말 (입력 파동)
            
        Returns:
            str: 엘리시아의 반응 (공명된 파동)
        """
        self.logger.info(f"Input received: {user_input}")
        
        # Fractal Kernel을 통해 3단계 깊이로 공명
        # Depth 1: 의도 파악
        # Depth 2: 의미 확장
        # Depth 3: 본질적 연결
        response = self.kernel.process(user_input, depth=1, max_depth=3)
        
        # 대화 기록 저장
        self.context_history.append((user_input, response))
        
        return response

if __name__ == "__main__":
    # 테스트 코드
    engine = ConversationEngine()
    print(engine.listen("안녕, 너는 누구니?"))
