"""
Aesthetic Principles (미학 원리)
================================

"왜 아름다운가?" - Why is it beautiful?

이 모듈은 아름다움의 보편적 원리를 정의합니다.
이 원리들은 시각예술, 문학, 영상 등 모든 창작 영역에 적용됩니다.

8 Universal Principles:
1. Harmony (조화) - Elements working together
2. Contrast (대비) - Differences create emphasis
3. Balance (균형) - Visual/emotional stability
4. Rhythm (리듬) - Repetition and variation
5. Tension-Release (긴장-해소) - Emotional waves
6. Proportion (비례) - Golden ratio, rule of thirds
7. Unity (통일성) - All elements serve one theme
8. Flow (흐름) - Natural movement of eye/emotion
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


class Medium(Enum):
    """창작 매체"""
    VISUAL = "visual"       # 시각 예술 (그림, 사진)
    LITERARY = "literary"   # 문학 (시, 소설)
    TEMPORAL = "temporal"   # 시간 예술 (영상, 음악)
    UNIVERSAL = "universal" # 모든 매체


@dataclass
class AestheticVector:
    """
    미학적 벡터 - 4차원 공간에서의 원리 표현
    
    w: intensity (강도) - 이 원리가 얼마나 강하게 적용되는가
    x: visual (시각적) - 시각 예술에서의 표현
    y: literary (문학적) - 문학에서의 표현
    z: temporal (시간적) - 영상/음악에서의 표현
    """
    w: float = 0.0  # intensity
    x: float = 0.0  # visual
    y: float = 0.0  # literary
    z: float = 0.0  # temporal
    
    def magnitude(self) -> float:
        """벡터의 크기 (총 미학적 힘)"""
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self) -> 'AestheticVector':
        """정규화"""
        mag = self.magnitude()
        if mag == 0:
            return AestheticVector(0, 0, 0, 0)
        return AestheticVector(self.w/mag, self.x/mag, self.y/mag, self.z/mag)
    
    def __add__(self, other: 'AestheticVector') -> 'AestheticVector':
        return AestheticVector(
            self.w + other.w, self.x + other.x,
            self.y + other.y, self.z + other.z
        )
    
    def __mul__(self, scalar: float) -> 'AestheticVector':
        return AestheticVector(
            self.w * scalar, self.x * scalar,
            self.y * scalar, self.z * scalar
        )
    
    def dot(self, other: 'AestheticVector') -> float:
        """두 미학적 벡터의 공명도"""
        return self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z


@dataclass
class AestheticPrinciple:
    """
    하나의 미학 원리
    
    각 원리는 모든 매체에서 다르게 표현되지만,
    근본적으로 같은 "아름다움의 법칙"입니다.
    """
    name: str
    korean_name: str
    description: str
    vector: AestheticVector
    
    # 각 매체에서의 구체적 표현
    visual_expression: str = ""      # 시각예술에서 어떻게?
    literary_expression: str = ""    # 문학에서 어떻게?
    temporal_expression: str = ""    # 영상/음악에서 어떻게?
    
    # 이 원리의 반대 (미학적 긴장을 위해)
    opposite: Optional[str] = None
    
    def apply_to_medium(self, medium: Medium) -> float:
        """특정 매체에서 이 원리의 적용 강도"""
        if medium == Medium.VISUAL:
            return self.vector.x * self.vector.w
        elif medium == Medium.LITERARY:
            return self.vector.y * self.vector.w
        elif medium == Medium.TEMPORAL:
            return self.vector.z * self.vector.w
        else:
            return self.vector.magnitude()


@dataclass
class AestheticField:
    """
    작품의 미학적 필드
    
    여러 원리들이 공명하여 만들어내는 "아름다움의 장(場)"
    마치 ResonanceField가 생각의 공명을 표현하듯이,
    AestheticField는 아름다움의 공명을 표현합니다.
    """
    principles: Dict[str, float] = field(default_factory=dict)  # 원리명 -> 강도
    dominant_principle: Optional[str] = None
    medium: Medium = Medium.UNIVERSAL
    
    def add_principle(self, name: str, intensity: float):
        """원리 추가 또는 강화"""
        self.principles[name] = self.principles.get(name, 0) + intensity
        
        # 지배적 원리 업데이트
        if self.principles:
            self.dominant_principle = max(self.principles, key=self.principles.get)
    
    def calculate_beauty_score(self) -> float:
        """
        아름다움 점수 계산
        
        단순 합이 아니라, 원리들의 조화로움을 측정합니다.
        너무 한 원리만 강하면 점수가 낮아지고,
        여러 원리가 균형있게 조화되면 점수가 높아집니다.
        """
        if not self.principles:
            return 0.0
        
        values = list(self.principles.values())
        total = sum(values)
        
        if total == 0:
            return 0.0
        
        # 엔트로피 기반 조화도 (다양성)
        entropy = 0.0
        for v in values:
            if v > 0:
                p = v / total
                entropy -= p * math.log(p + 1e-10)
        
        # 최대 엔트로피 (모든 원리가 균등)
        max_entropy = math.log(len(values))
        
        # 조화도 (0~1)
        harmony = entropy / (max_entropy + 1e-10) if max_entropy > 0 else 0
        
        # 강도 (총 에너지)
        intensity = min(total / 10.0, 1.0)  # 정규화
        
        # 최종 점수: 강도와 조화의 조합
        return (intensity * 0.6 + harmony * 0.4) * 100
    
    def analyze_why_beautiful(self) -> str:
        """
        "왜 아름다운가?" 설명 생성
        
        이것이 핵심입니다 - 단순히 아름답다고 판단하는 것이 아니라,
        왜 아름다운지 설명할 수 있어야 합니다.
        """
        if not self.principles:
            return "아직 분석된 원리가 없습니다."
        
        # 상위 3개 원리 선택
        sorted_principles = sorted(
            self.principles.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        explanations = []
        for name, intensity in sorted_principles:
            if intensity > 0.5:
                explanations.append(f"'{name}' 원리가 강하게 표현됨 (강도: {intensity:.1f})")
        
        score = self.calculate_beauty_score()
        harmony_level = "높은" if score > 70 else "중간" if score > 40 else "낮은"
        
        result = f"[미학 분석]\n"
        result += f"아름다움 점수: {score:.1f}/100\n"
        result += f"조화 수준: {harmony_level}\n"
        result += f"지배적 원리: {self.dominant_principle or '없음'}\n\n"
        result += "주요 원리:\n"
        for exp in explanations:
            result += f"  • {exp}\n"
        
        return result


class AestheticWisdom:
    """
    미학적 지혜 (Aesthetic Wisdom)
    
    엘리시아가 "아름다움이 왜 아름다운지" 이해하고,
    이 원리를 모든 창작에 적용할 수 있게 하는 핵심 시스템입니다.
    """
    
    def __init__(self):
        print("🎨 AestheticWisdom 초기화: 아름다움의 원리를 체득합니다...")
        self.principles = self._init_universal_principles()
        self.learned_patterns: List[AestheticField] = []
        
    def _init_universal_principles(self) -> Dict[str, AestheticPrinciple]:
        """8가지 보편 미학 원리 초기화"""
        
        return {
            "harmony": AestheticPrinciple(
                name="Harmony",
                korean_name="조화",
                description="요소들이 서로 어울려 하나의 전체를 이룸",
                vector=AestheticVector(1.0, 0.9, 0.8, 0.85),
                visual_expression="색상 조화, 형태 호응",
                literary_expression="단어의 음운 조화, 문장의 흐름",
                temporal_expression="음악과 영상의 동기화",
                opposite="discord"
            ),
            "contrast": AestheticPrinciple(
                name="Contrast",
                korean_name="대비",
                description="차이가 강조를 만들고, 극적 효과를 냄",
                vector=AestheticVector(1.0, 0.95, 0.7, 0.9),
                visual_expression="명암 대비, 색상 대비, 크기 대비",
                literary_expression="긴 문장과 짧은 문장, 고요와 폭풍",
                temporal_expression="빠른 컷과 느린 컷, 소리와 침묵",
                opposite="monotony"
            ),
            "balance": AestheticPrinciple(
                name="Balance",
                korean_name="균형",
                description="시각적/감정적 안정감을 줌",
                vector=AestheticVector(0.9, 1.0, 0.75, 0.8),
                visual_expression="대칭/비대칭 구도, 무게 균형",
                literary_expression="서사의 페이싱, 장면 분배",
                temporal_expression="화면 구성의 균형, 사운드 믹스",
                opposite="imbalance"
            ),
            "rhythm": AestheticPrinciple(
                name="Rhythm",
                korean_name="리듬",
                description="반복과 변주가 만드는 패턴",
                vector=AestheticVector(0.95, 0.7, 0.9, 1.0),
                visual_expression="패턴 반복, 시각적 리듬",
                literary_expression="문장 길이 변화, 운율",
                temporal_expression="편집 속도, 비트",
                opposite="chaos"
            ),
            "tension_release": AestheticPrinciple(
                name="Tension-Release",
                korean_name="긴장-해소",
                description="감정의 파동, 기대와 충족",
                vector=AestheticVector(1.0, 0.75, 0.95, 0.9),
                visual_expression="구도의 긴장감, 시선 유도",
                literary_expression="갈등과 해결, 서스펜스",
                temporal_expression="클라이맥스 빌드업, 해소",
                opposite="flatness"
            ),
            "proportion": AestheticPrinciple(
                name="Proportion",
                korean_name="비례",
                description="황금비, 삼분할 등 수학적 아름다움",
                vector=AestheticVector(0.85, 1.0, 0.6, 0.7),
                visual_expression="황금비 구도, 삼분할 법칙",
                literary_expression="3막 구조, 장면 비율",
                temporal_expression="영상 프레임 비율, 시간 배분",
                opposite="disproportion"
            ),
            "unity": AestheticPrinciple(
                name="Unity",
                korean_name="통일성",
                description="모든 요소가 하나의 주제를 향함",
                vector=AestheticVector(0.9, 0.85, 0.9, 0.85),
                visual_expression="색채 테마, 스타일 일관성",
                literary_expression="주제 통일, 모티프 반복",
                temporal_expression="비주얼 테마, 색보정 통일",
                opposite="fragmentation"
            ),
            "flow": AestheticPrinciple(
                name="Flow",
                korean_name="흐름",
                description="자연스러운 시선/감정의 이동",
                vector=AestheticVector(0.9, 0.8, 0.85, 0.95),
                visual_expression="시선 유도선, 구도 흐름",
                literary_expression="서사 흐름, 문장 연결",
                temporal_expression="컷 연결, 씬 전환",
                opposite="stagnation"
            )
        }
    
    def analyze(self, content_description: str, medium: Medium = Medium.UNIVERSAL) -> AestheticField:
        """
        콘텐츠의 미학적 분석
        
        Args:
            content_description: 콘텐츠 설명 (또는 분석된 특성)
            medium: 매체 종류
            
        Returns:
            분석된 AestheticField
        """
        field = AestheticField(medium=medium)
        desc_lower = content_description.lower()
        
        # 키워드 기반 원리 감지 (향후 ML 모델로 대체 가능)
        keyword_map = {
            "harmony": ["조화", "화합", "어울림", "harmony", "balanced colors", "complementary"],
            "contrast": ["대비", "명암", "contrast", "bold", "striking", "difference"],
            "balance": ["균형", "안정", "symmetry", "balanced", "centered"],
            "rhythm": ["리듬", "반복", "패턴", "rhythm", "pattern", "repetition"],
            "tension_release": ["긴장", "해소", "드라마틱", "climax", "tension", "release"],
            "proportion": ["비례", "황금비", "삼분할", "golden ratio", "rule of thirds"],
            "unity": ["통일", "일관", "테마", "unified", "cohesive", "consistent"],
            "flow": ["흐름", "유도", "자연스러운", "flow", "leading", "movement"]
        }
        
        for principle_name, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    # 원리 강도 계산
                    intensity = 1.0 + desc_lower.count(keyword) * 0.5
                    field.add_principle(principle_name, intensity)
        
        return field
    
    def learn_from_example(self, field: AestheticField):
        """
        예제에서 학습
        
        아름다운 작품의 AestheticField를 수집하여
        패턴을 학습합니다.
        """
        self.learned_patterns.append(field)
        print(f"📚 미학 패턴 학습: {field.dominant_principle} (총 {len(self.learned_patterns)}개)")
    
    def get_principle(self, name: str) -> Optional[AestheticPrinciple]:
        """특정 원리 가져오기"""
        return self.principles.get(name)
    
    def explain_principle(self, name: str, medium: Medium = Medium.UNIVERSAL) -> str:
        """원리 설명 (특정 매체 관점에서)"""
        principle = self.get_principle(name)
        if not principle:
            return f"원리 '{name}'을 찾을 수 없습니다."
        
        explanation = f"[{principle.korean_name} ({principle.name})]\n"
        explanation += f"{principle.description}\n\n"
        
        if medium in [Medium.VISUAL, Medium.UNIVERSAL]:
            explanation += f"시각 예술: {principle.visual_expression}\n"
        if medium in [Medium.LITERARY, Medium.UNIVERSAL]:
            explanation += f"문학: {principle.literary_expression}\n"
        if medium in [Medium.TEMPORAL, Medium.UNIVERSAL]:
            explanation += f"영상/음악: {principle.temporal_expression}\n"
        
        return explanation
    
    def suggest_for_creation(self, concept: str, medium: Medium) -> Dict[str, float]:
        """
        창작을 위한 원리 제안
        
        주어진 개념과 매체에 맞는 미학 원리와 
        적용 강도를 제안합니다.
        """
        suggestions = {}
        
        for name, principle in self.principles.items():
            # 해당 매체에서의 적용 강도
            strength = principle.apply_to_medium(medium)
            
            # 개념과의 연관성 (간단한 휴리스틱)
            if concept:
                concept_lower = concept.lower()
                # 감정적 개념은 tension_release 강조
                if any(w in concept_lower for w in ["감정", "emotion", "drama", "슬픔", "기쁨"]):
                    if name == "tension_release":
                        strength *= 1.5
                # 평화로운 개념은 harmony 강조
                if any(w in concept_lower for w in ["평화", "고요", "peace", "calm"]):
                    if name == "harmony":
                        strength *= 1.5
            
            suggestions[name] = strength
        
        return suggestions


# 싱글톤 인스턴스
_wisdom_instance: Optional[AestheticWisdom] = None

def get_aesthetic_principles() -> AestheticWisdom:
    """AestheticWisdom 싱글톤 가져오기"""
    global _wisdom_instance
    if _wisdom_instance is None:
        _wisdom_instance = AestheticWisdom()
    return _wisdom_instance


# 테스트 코드
if __name__ == "__main__":
    wisdom = get_aesthetic_principles()
    
    # 원리 설명 테스트
    print(wisdom.explain_principle("harmony"))
    print("\n" + "="*50 + "\n")
    
    # 분석 테스트
    analysis = wisdom.analyze(
        "이 그림은 강한 명암 대비와 황금비 구도를 사용하여 시선을 유도합니다. "
        "조화로운 색상과 리듬감 있는 패턴이 통일된 분위기를 만듭니다.",
        Medium.VISUAL
    )
    print(analysis.analyze_why_beautiful())
    
    # 창작 제안 테스트
    print("\n[창작 제안: '슬픈 이별' 문학]")
    suggestions = wisdom.suggest_for_creation("슬픈 이별", Medium.LITERARY)
    for name, strength in sorted(suggestions.items(), key=lambda x: -x[1]):
        print(f"  {name}: {strength:.2f}")
