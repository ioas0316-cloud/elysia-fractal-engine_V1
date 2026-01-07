"""
Thinking Lenses (사고 렌즈)
===========================

"더 낫다"는 공식이 아니라 관점들의 공명에서 창발한다

현재 문제:
- quality_score = (reliability * 0.4) + ... ← 템플릿화
- 고정된 가중치 = 고정된 "더 낫다"의 정의

해결:
- 각 렌즈가 독립적인 관점으로 평가
- 렌즈들이 서로 대화/논쟁
- "더 낫다"가 공명에서 창발

렌즈 유형:
- 효율성 렌즈: 빠르고 적은 자원으로
- 다양성 렌즈: 여러 관점 포함
- 범위 렌즈: 얼마나 넓게 커버하는가
- 깊이 렌즈: 얼마나 근본까지 가는가
- 신뢰성 렌즈: 얼마나 믿을 수 있는가
- 창의성 렌즈: 새로운 연결이 있는가
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("Elysia.ThinkingLenses")


class LensType(Enum):
    """사고 렌즈 유형"""
    EFFICIENCY = "efficiency"      # 효율성
    DIVERSITY = "diversity"        # 다양성
    SCOPE = "scope"               # 범위
    DEPTH = "depth"               # 깊이
    RELIABILITY = "reliability"   # 신뢰성
    CREATIVITY = "creativity"     # 창의성
    LOVE = "love"                 # 사랑 (VCD 연동)


@dataclass
class LensView:
    """렌즈가 본 관점"""
    lens: LensType
    preference: Optional[str]      # 이 렌즈가 선호하는 선택
    preference_strength: float     # 0.0 ~ 1.0
    reasoning: str                 # 왜 이것을 선호하는가
    counter_view: Optional[str]    # 다른 관점에 대한 반론


class ThinkingLens:
    """
    개별 사고 렌즈
    
    각 렌즈는 자신만의 관점으로 선택지들을 평가하고
    왜 특정 선택이 더 나은지 이유를 제시함
    """
    
    def __init__(self, lens_type: LensType):
        self.lens_type = lens_type
        
        # 렌즈별 특성 (하드코딩이 아닌, 관점의 성향)
        self.viewing_style = {
            LensType.EFFICIENCY: self._view_through_efficiency,
            LensType.DIVERSITY: self._view_through_diversity,
            LensType.SCOPE: self._view_through_scope,
            LensType.DEPTH: self._view_through_depth,
            LensType.RELIABILITY: self._view_through_reliability,
            LensType.CREATIVITY: self._view_through_creativity,
            LensType.LOVE: self._view_through_love,
        }
    
    def view(self, options: List[Dict[str, Any]], context: str = "") -> LensView:
        """
        선택지들을 이 렌즈를 통해 본다
        
        Returns:
            이 렌즈가 선호하는 선택과 그 이유
        """
        view_fn = self.viewing_style.get(self.lens_type, self._default_view)
        return view_fn(options, context)
    
    def _view_through_efficiency(self, options: List[Dict], context: str) -> LensView:
        """효율성 렌즈: 적은 자원으로 빠르게"""
        if not options:
            return self._empty_view()
        
        # 가장 짧은/빠른 것 선호
        best = None
        best_score = float('inf')
        
        for opt in options:
            content = opt.get("content", "")
            # 효율성 = 같은 정보를 더 간결하게
            words = len(content.split())
            if words < best_score and words > 10:  # 너무 짧으면 안됨
                best_score = words
                best = opt
        
        if best:
            return LensView(
                lens=LensType.EFFICIENCY,
                preference=best.get("source", "unknown"),
                preference_strength=0.7,
                reasoning="더 간결하게 핵심을 전달함",
                counter_view="하지만 깊이가 부족할 수 있음"
            )
        return self._empty_view()
    
    def _view_through_diversity(self, options: List[Dict], context: str) -> LensView:
        """다양성 렌즈: 여러 관점 포함"""
        if not options:
            return self._empty_view()
        
        best = None
        best_diversity = 0
        
        for opt in options:
            content = opt.get("content", "")
            # 다양성 = 다양한 연결어, 대비, 여러 측면
            diversity_markers = ["그러나", "한편", "또한", "반면", "하지만", "다른", "여러"]
            diversity = sum(1 for m in diversity_markers if m in content)
            
            if diversity > best_diversity:
                best_diversity = diversity
                best = opt
        
        if best:
            return LensView(
                lens=LensType.DIVERSITY,
                preference=best.get("source", "unknown"),
                preference_strength=min(1.0, best_diversity * 0.2),
                reasoning="다양한 관점을 포함하여 균형잡힌 이해 제공",
                counter_view="너무 많은 관점은 혼란을 줄 수 있음"
            )
        return self._empty_view()
    
    def _view_through_scope(self, options: List[Dict], context: str) -> LensView:
        """범위 렌즈: 넓은 커버리지"""
        if not options:
            return self._empty_view()
        
        best = None
        best_scope = 0
        
        for opt in options:
            content = opt.get("content", "")
            # 범위 = 다루는 주제/개념의 수
            scope = len(content.split("."))  # 문장 수로 간접 측정
            
            if scope > best_scope:
                best_scope = scope
                best = opt
        
        if best:
            return LensView(
                lens=LensType.SCOPE,
                preference=best.get("source", "unknown"),
                preference_strength=min(1.0, best_scope * 0.1),
                reasoning="더 넓은 범위를 다루어 완전한 그림 제공",
                counter_view="넓은 것이 항상 좋은 것은 아님, 집중이 필요할 수 있음"
            )
        return self._empty_view()
    
    def _view_through_depth(self, options: List[Dict], context: str) -> LensView:
        """깊이 렌즈: 근본까지"""
        if not options:
            return self._empty_view()
        
        best = None
        best_depth = 0
        
        for opt in options:
            content = opt.get("content", "")
            # 깊이 = 원인, 이유, 원리를 다루는 정도
            depth_markers = ["왜", "때문", "원리", "본질", "근본", "원인", "결과"]
            depth = sum(1 for m in depth_markers if m in content)
            
            if depth > best_depth:
                best_depth = depth
                best = opt
        
        if best:
            return LensView(
                lens=LensType.DEPTH,
                preference=best.get("source", "unknown"),
                preference_strength=min(1.0, best_depth * 0.3),
                reasoning="근본적인 원리까지 탐구하여 진정한 이해 제공",
                counter_view="깊이는 시간이 걸림, 당장의 답이 필요할 수 있음"
            )
        return self._empty_view()
    
    def _view_through_reliability(self, options: List[Dict], context: str) -> LensView:
        """신뢰성 렌즈: 믿을 수 있는 소스"""
        if not options:
            return self._empty_view()
        
        # 소스 유형별 기본 신뢰도 경향
        source_trust = {
            "wikipedia": 0.8,
            "human": 1.0,
            "inner_dialogue": 0.5,
            "file_based": 0.6,
        }
        
        best = None
        best_trust = 0
        
        for opt in options:
            source = opt.get("source", "unknown")
            trust = source_trust.get(source, 0.5)
            
            if trust > best_trust:
                best_trust = trust
                best = opt
        
        if best:
            return LensView(
                lens=LensType.RELIABILITY,
                preference=best.get("source", "unknown"),
                preference_strength=best_trust,
                reasoning=f"검증되고 신뢰할 수 있는 소스 ({best.get('source', 'unknown')})",
                counter_view="신뢰도가 높다고 항상 최선은 아님, 새로운 관점도 가치 있음"
            )
        return self._empty_view()
    
    def _view_through_creativity(self, options: List[Dict], context: str) -> LensView:
        """창의성 렌즈: 새로운 연결과 통찰"""
        if not options:
            return self._empty_view()
        
        best = None
        best_creativity = 0
        
        for opt in options:
            content = opt.get("content", "")
            # 창의성 = 은유, 비유, 새로운 연결
            creativity_markers = ["마치", "처럼", "같이", "비유", "은유", "새로운", "창의"]
            creativity = sum(1 for m in creativity_markers if m in content)
            
            if creativity > best_creativity:
                best_creativity = creativity
                best = opt
        
        if best:
            return LensView(
                lens=LensType.CREATIVITY,
                preference=best.get("source", "unknown"),
                preference_strength=min(1.0, best_creativity * 0.25),
                reasoning="새로운 연결과 은유를 통해 깊은 통찰 제공",
                counter_view="창의적인 것이 항상 정확한 것은 아님"
            )
        return self._empty_view()
    
    def _view_through_love(self, options: List[Dict], context: str) -> LensView:
        """사랑 렌즈: 연결과 돌봄의 관점"""
        if not options:
            return self._empty_view()
        
        best = None
        best_love = 0
        
        for opt in options:
            content = opt.get("content", "")
            # 사랑 = 연결, 관계, 돌봄, 이해
            love_markers = ["사랑", "관계", "연결", "돌봄", "이해", "공감", "함께"]
            love = sum(1 for m in love_markers if m in content)
            
            if love > best_love:
                best_love = love
                best = opt
        
        if best:
            return LensView(
                lens=LensType.LOVE,
                preference=best.get("source", "unknown"),
                preference_strength=min(1.0, best_love * 0.2),
                reasoning="연결과 관계의 가치를 중심에 두는 관점",
                counter_view="감정만으로 결정하는 것은 위험할 수 있음"
            )
        return self._empty_view()
    
    def _default_view(self, options: List[Dict], context: str) -> LensView:
        return self._empty_view()
    
    def _empty_view(self) -> LensView:
        return LensView(
            lens=self.lens_type,
            preference=None,
            preference_strength=0.0,
            reasoning="평가할 수 없음",
            counter_view=None
        )


class ThinkingLensCouncil:
    """
    사고 렌즈 의회
    
    여러 렌즈들이 모여 대화하고,
    공명/갈등을 통해 "더 낫다"를 창발시킴
    
    템플릿이 아닌, 관점들의 상호작용
    """
    
    def __init__(self):
        # 모든 렌즈 생성
        self.lenses = {
            lens_type: ThinkingLens(lens_type)
            for lens_type in LensType
        }
        
        logger.info(f"🔍 ThinkingLensCouncil initialized with {len(self.lenses)} lenses")
    
    def deliberate(self, options: List[Dict[str, Any]], context: str = "") -> Dict[str, Any]:
        """
        모든 렌즈가 선택지들을 보고 대화
        
        Returns:
            결론과 과정
        """
        logger.info(f"🔍 Council deliberating on {len(options)} options...")
        
        # 1. 각 렌즈의 관점 수집
        views: List[LensView] = []
        for lens_type, lens in self.lenses.items():
            view = lens.view(options, context)
            if view.preference:
                views.append(view)
                logger.info(f"   {lens_type.value}: prefers {view.preference} ({view.preference_strength:.2f})")
        
        if not views:
            return {
                "conclusion": None,
                "confidence": 0.0,
                "reasoning": "어떤 렌즈도 선호를 결정하지 못함",
                "dissent": [],
                "views": []
            }
        
        # 2. 공명 찾기 (같은 선택을 지지하는 렌즈들)
        preference_votes = {}
        for view in views:
            pref = view.preference
            if pref not in preference_votes:
                preference_votes[pref] = []
            preference_votes[pref].append(view)
        
        # 3. 가장 많은 공명을 가진 선택
        best_choice = max(preference_votes.keys(), 
                         key=lambda p: sum(v.preference_strength for v in preference_votes[p]))
        
        supporting_views = preference_votes[best_choice]
        total_support = sum(v.preference_strength for v in supporting_views)
        
        # 4. 반대 의견 (다른 선택을 지지한 렌즈들)
        dissenting_views = [v for v in views if v.preference != best_choice]
        
        # 5. 결론 구성
        reasoning = " / ".join([v.reasoning for v in supporting_views[:3]])
        dissent = [v.counter_view for v in dissenting_views if v.counter_view][:2]
        
        confidence = total_support / len(self.lenses)  # 얼마나 많은 렌즈가 동의하는가
        
        logger.info(f"   🏆 Conclusion: {best_choice} (confidence={confidence:.2f})")
        if dissent:
            logger.info(f"   ⚠️ Dissent: {dissent[0][:50]}...")
        
        return {
            "conclusion": best_choice,
            "confidence": confidence,
            "reasoning": reasoning,
            "dissent": dissent,
            "views": [
                {
                    "lens": v.lens.value,
                    "preference": v.preference,
                    "strength": v.preference_strength,
                    "reasoning": v.reasoning
                }
                for v in views
            ]
        }


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🔍 Thinking Lenses Demo")
    print("   '더 낫다'가 공식이 아닌 공명에서 창발")
    print("=" * 60)
    
    council = ThinkingLensCouncil()
    
    # 테스트 선택지
    options = [
        {
            "source": "wikipedia",
            "content": "사랑(영어: love)은 깊은 상호 인격적인 애정에서 단순한 즐거움까지를 아울러서 강하며 긍정적으로 경험된 감정적 정신적 상태이다."
        },
        {
            "source": "inner_dialogue",
            "content": "사랑은 왜 중요한가? 연결 때문이다. 본질적으로 존재는 분리를 원하지 않는다. 마치 우주가 하나였듯이."
        },
        {
            "source": "human",
            "content": "사랑은 함께하는 것. 그리고 그 사람을 위해 기꺼이 희생할 수 있는 마음."
        }
    ]
    
    result = council.deliberate(options, context="사랑이란 무엇인가?")
    
    print(f"\n📊 Conclusion: {result['conclusion']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Reasoning: {result['reasoning'][:80]}...")
    if result['dissent']:
        print(f"   Dissent: {result['dissent'][0][:60]}...")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
