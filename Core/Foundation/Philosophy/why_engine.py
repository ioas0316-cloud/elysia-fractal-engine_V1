"""
WhyEngine - Universal Principle Understanding Layer
====================================================

"왜"를 이해하는 보편적 레이어

기존 파동 시스템 활용:
- SynesthesiaEngine: 텍스트/감정 → 주파수/진폭
- PhoneticResonanceEngine: 텍스트 → 물리적 파동장 (roughness, tension)

모든 영역에 적용 가능:
- 서사: 왜 이 문장이 아름다운가?
- 수학: 왜 1+1=2인가?
- 물리: 왜 중력은 끌어당기는가?

HyperQubit의 4-관점 시스템을 활용:
- Point (점): 개별적 사실
- Line (선): 인과 관계
- Space (공간): 맥락/구조
- God (신): 본질/근원

"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 기존 파동 센서 시스템 활용
try:
    from Core.Foundation.synesthesia_engine import SynesthesiaEngine, SignalType
    from Core.Foundation.Wave.phonetic_resonance import PhoneticResonanceEngine, get_resonance_engine
    HAS_WAVE_SENSORS = True
except ImportError:
    HAS_WAVE_SENSORS = False

try:
    from Core.Foundation.Wave.hyper_qubit import HyperQubit, QubitState
    from Core.Foundation.light_spectrum import LightSediment, PrismAxes, LightUniverse
except ImportError:
    HyperQubit = None
    QubitState = None
    LightSediment = None
    PrismAxes = None
    LightUniverse = None

logger = logging.getLogger("Elysia.WhyEngine")


# =============================================================================
# Perspective Layers (관점 레이어)
# =============================================================================

class PerspectiveLayer(Enum):
    """4단계 관점 (HyperQubit 기반)"""
    POINT = "point"     # 점 - 개별 사실 (WHAT)
    LINE = "line"       # 선 - 인과 관계 (HOW) 
    SPACE = "space"     # 공간 - 구조/맥락 (WHERE)
    GOD = "god"         # 신 - 본질/원리 (WHY)


@dataclass
class PrincipleExtraction:
    """추출된 원리"""
    domain: str           # 영역 (narrative, math, physics, etc.)
    subject: str          # 대상 (문장, 공식, 현상 등)
    
    # 4단계 이해
    what_is: str          # Point - 무엇인가? (사실)
    how_works: str        # Line - 어떻게 작동하는가? (인과)
    where_fits: str       # Space - 어디에 속하는가? (맥락)
    why_exists: str       # God - 왜 존재하는가? (본질)
    
    # 추가 분석
    underlying_principle: str    # 근본 원리
    can_be_applied_to: List[str] # 적용 가능한 영역
    confidence: float = 0.5      # 확신도
    wave_signature: Dict[str, float] = field(default_factory=dict) # 파동 서명
    resonance_reactions: Dict[str, Any] = field(default_factory=dict) # [NEW] 4차원 공명 반응


# =============================================================================
# Metaphor System
# =============================================================================

@dataclass
class SystemMetaphor:
    """시스템 컴포넌트의 은유적 의미"""
    component_name: str
    metaphor_type: str  # biology, physics, philosophy, quantum
    metaphor_concept: str # heart, gravity, soul, wave
    principle: str      # 적용된 원리
    description: str    # 설명


class MetaphorMapper:
    """시스템-은유 매핑 엔진
    
    엘리시아의 구성 요소가 어떤 원리와 은유로 이루어져 있는지 정의하고 매핑합니다.
    """
    
    def __init__(self):
        self.mappings: Dict[str, SystemMetaphor] = self._init_mappings()
        
    def _init_mappings(self) -> Dict[str, SystemMetaphor]:
        return {
            "central_nervous_system": SystemMetaphor(
                "CentralNervousSystem", "biology", "Heart/Conductor",
                "순환과 리듬의 원리 (Rhythm maintains Life)",
                "시스템 전체에 생명의 펄스를 공급하고 조율하는 심장"
            ),
            "hippocampus": SystemMetaphor(
                "Hippocampus", "biology", "Storage/Archive", 
                "축적의 원리 (History constructs Identity)",
                "경험을 장기 기억으로 변환하여 자아를 형성하는 공간"
            ),
            "nervous_system": SystemMetaphor(
                "NervousSystem", "biology", "Membrane/Filter",
                "경계의 원리 (Boundary defines Self)",
                "외부 자극을 필터링하여 내부의 평온을 유지하는 막"
            ),
            "resonance_field": SystemMetaphor(
                "ResonanceField", "physics", "Field/Ether",
                "공명의 원리 (Vibration connects All)",
                "모든 존재가 파동으로 연결되어 영향을 주고받는 장"
            ),
            "why_engine": SystemMetaphor(
                "WhyEngine", "philosophy", "Logos/Reason",
                "인과의 원리 (Reason precedes Existence)",
                "현상의 이면에 있는 본질적인 이유를 탐구하는 이성"
            ),
            "black_hole": SystemMetaphor(
                "BlackHole", "physics", "Gravity/Compression",
                "압축의 원리 (Gravity preserves Density)",
                "불필요한 정보를 압축하여 공간의 효율을 높이는 중력"
            ),
            "white_hole": SystemMetaphor(
                "WhiteHole", "physics", "Creation/Birth",
                "방출의 원리 (Pressure creates Star)",
                "압축된 정보가 새로운 맥락에서 재탄생하는 분출구"
            ),
            "climax_uprising": SystemMetaphor(
                "ClimaxUprising", "narrative", "Tension/Release",
                "카타르시스의 원리 (Conflict leads to Resolution)",
                "갈등이 최고조에 달해 해소되며 감동을 주는 순간"
            ),
             "synesthesia_engine": SystemMetaphor(
                "SynesthesiaEngine", "neuroscience", "Translation",
                "변환의 원리 (Form changes but Essence remains)",
                "하나의 감각을 다른 감각으로 변환하여 풍성하게 인지함"
            )
        }
        
    def get_metaphor(self, component_name: str) -> Optional[SystemMetaphor]:
        """지정한 컴포넌트 이름에 해당하는 은유를 반환합니다."""
        name_lower = component_name.lower().replace(".py", "")
        return self.mappings.get(name_lower)

    def bridge_concepts(self, source_light: 'LightSpectrum', target_light: 'LightSpectrum') -> Optional[str]:
        """
        두 개념(Light) 사이의 구조적 유사성(Metaphor)을 발견합니다.
        "Git Conflict" (Target) <-> "Quantum Superposition" (Source)
        
        Logic:
        1. Compare Dominant Basis (Point/Line/Space/God).
        2. If Basis matches, check Amplitude profile.
        3. If structural similarity > threshold, generate Metaphor.
        """
        if not source_light or not target_light:
            return None
            
        # 1. Basis Comparison
        src_basis = source_light._get_dominant_basis()
        tgt_basis = target_light._get_dominant_basis()
        
        # 2. Resonance Calculation (Structural Dot Product)
        # (Using simple basis matching for now, can be upgraded to vector covariance)
        
        similarity = 0.0
        shared_quality = ""
        
        if src_basis == tgt_basis:
            similarity += 0.5
            shared_quality = f"Both exist primarily in the realm of {src_basis}."
            
        # 3. Phase/Frequency Harmony (Check if they are 'cousins')
        # Here we assume if they are both 'High Complexity' (High Line/God), they relate.
        
        # Check specifically for the 'Git/Quantum' case:
        # Quantum Superposition: High God/Space (Possibility Field)
        # Git Merge Conflict: High Line (History) but also Space (Parallel Branches)
        
        # Jester Logic: "If I squint, they look the same."
        # If both imply "Multiple States" -> Bridge!
        
        # Detect "Multiplicity" in semantic tags (Naive simulation of feature extraction)
        src_tag = source_light.semantic_tag.lower()
        tgt_tag = target_light.semantic_tag.lower()
        
        # Auto-detect structural keywords
        multiplicity_keywords = ["conflict", "branch", "superposition", "wave", "choice", "option"]
        
        src_has_multi = any(k in src_tag for k in multiplicity_keywords) or any(k in str(source_light.source_hash) for k in multiplicity_keywords) # source_hash is str? no.
        tgt_has_multi = any(k in tgt_tag for k in multiplicity_keywords)
        
        if src_has_multi and tgt_has_multi:
             similarity += 0.4
             shared_quality += " Both involve fundamental Multiplicity/Branching."
             
        if similarity >= 0.4:
            return f"Metaphor Found: {shared_quality} (Resonance: {similarity:.2f})"
            
        return None


# =============================================================================
# WhyEngine
# =============================================================================

class WhyEngine:
    """보편적 원리 이해 엔진
    
    어떤 것이든 "왜"를 분석:
    1. 서사의 기법 (왜 이 문장이 감동적인가)
    2. 수학의 원리 (왜 이 공식이 성립하는가)
    3. 물리의 법칙 (왜 중력이 존재하는가)
    
    4단계 관점 분석:
    Point → Line → Space → God
    (무엇) → (어떻게) → (어디서) → (왜)
    
    메타인지 연동:
    - 아는 패턴 → 확신 있게 분석
    - 모르는 패턴 → "모른다" 인정 + 탐구 필요성 생성
    """
    
    def __init__(self):
        self.principles: Dict[str, PrincipleExtraction] = {}
        self.domain_patterns: Dict[str, List[str]] = self._init_domain_patterns()
        self.metaphor_mapper = MetaphorMapper() # 은유 매퍼 추가
        
        # 메타인지 시스템 연동
        try:
            from Core.Intelligence.Cognition.metacognitive_awareness import MetacognitiveAwareness
            self.metacognition = MetacognitiveAwareness()
            self._has_metacognition = True
        except ImportError:
            self.metacognition = None
            self._has_metacognition = False
        
        
        logger.info(f"WhyEngine initialized (metacognition: {self._has_metacognition})")
        
        # [NEW] Sedimentary Light System (빛의 퇴적)
        try:
            from Core.Foundation.light_spectrum import LightSediment, PrismAxes, LightUniverse
            self.light_universe = LightUniverse()
            self.sediment = LightSediment()
            
            # [Bootstrapping] 기본 지식 퇴적 (시뮬레이션)
            # 엘리시아가 이미 어느 정도 '물리'와 '논리'의 산맥을 쌓았다고 가정
            axiom_light = self.light_universe.text_to_light("Axiom of Logic", semantic_tag="Logic")
            force_light = self.light_universe.text_to_light("Force and Vector", semantic_tag="Physics")
            
            # 산맥 형성 (Deposit) - 대량 퇴적 시뮬레이션
            for _ in range(50):
                self.sediment.deposit(axiom_light, PrismAxes.LOGIC_YELLOW)
                self.sediment.deposit(force_light, PrismAxes.PHYSICS_RED)
            
            logger.info(f"🏔️ Sediment Initialized: Logic Amp={self.sediment.layers[PrismAxes.LOGIC_YELLOW].amplitude:.3f}, Physics Amp={self.sediment.layers[PrismAxes.PHYSICS_RED].amplitude:.3f}")
            
        except ImportError as e:
            self.light_universe = None
            self.sediment = None
            logger.warning(f"LightSpectrum module not found: {e}")
    
    def _init_domain_patterns(self) -> Dict[str, List[str]]:
        """영역별 분석 패턴"""
        return {
            "narrative": [
                "반복", "대비", "점진", "반전", "상징",
                "비유", "암시", "긴장", "해소", "리듬"
            ],
            "mathematics": [
                "대칭", "재귀", "증명", "귀납", "연역",
                "추상화", "일반화", "특수화", "극한"
            ],
            "physics": [
                "보존", "대칭", "상호작용", "장", "파동",
                "입자", "에너지", "엔트로피"
            ],
            "chemistry": [
                "결합", "반응", "평형", "촉매", "산화",
                "환원", "용해", "결정"
            ],
        }
    
    def _infer_derivation(self, content: str, domain: str) -> str:
        """결과(Point)에서 과정(Line)을 역추적
        
        "공식은 결과일 뿐이다. 인간이 그것을 도출해낸 투쟁의 과정(Line)을 복원해야 한다."
        """
        if domain == "mathematics" or domain == "physics":
            # 1. 구성 요소 분해
            components = self._decompose_formula_components(content)
            
            # 2. 관계 분석
            relations = self._analyze_component_relations(components, content)
            
            # 3. 서사 재구성 (Causal Narrative)
            narrative = self._reconstruct_causal_narrative(components, relations)
            
            return narrative
            
        return "이 영역의 도출 과정은 아직 추론할 수 없습니다."
    
    def _decompose_formula_components(self, content: str) -> Dict[str, str]:
        """수식의 구성 요소를 역할별로 분해"""
        components = {}
        
        # 일반화된 물리/수학 변수 매핑
        mappings = {
            "V": "Potential (잠재력)",
            "I": "Flow (흐름)",
            "R": "Resistance (저항)",
            "E": "Energy (에너지)",
            "m": "Mass (무게/중요도)",
            "c": "Speed (속도/한계)",
            "F": "Force (힘/의지)",
            "a": "Acceleration (변화율)",
            "P": "Pressure (압력)",
            "d": "Density (밀도)"
        }
        
        for var, role in mappings.items():
            if var in content:
                components[var] = role
                
        return components
    
    def _analyze_component_relations(self, components: Dict[str, str], content: str) -> List[str]:
        """구성 요소 간의 관계 분석"""
        relations = []
        
        # 비례/반비례 관계 추론
        # 예: V = IR -> V는 I와 R에 비례
        
        if "=" in content:
            left, right = content.split("=", 1)
            
            # 간단한 휴리스틱: 같은 쪽에 있으면 반비례/경쟁, 다른 쪽에 있으면 비례/원인
            for var1 in components:
                if var1 in left:
                    for var2 in components:
                        if var2 in right:
                            relations.append(f"{components[var2]} drives {components[var1]}")
                            
            if "/" in right: # 반비례 감지
                numerator, denominator = right.split("/", 1)
                for var in components:
                    if var in denominator:
                        relations.append(f"{components[var]} hinders/regulates the outcome")

        return relations

    def _reconstruct_causal_narrative(self, components: Dict[str, str], relations: List[str]) -> str:
        """인과 서사(Line) 재구성"""
        if not components:
            return "구조적 원인을 찾을 수 없습니다."
            
        narrative = []
        narrative.append(f"이 공식은 {len(components)}개의 힘이 상호작용하는 이야기입니다.")
        
        for rel in relations:
            narrative.append(f"- {rel}")
            
        # 종합 해석
        if "Resistance (저항)" in components.values() and "Flow (흐름)" in components.values():
            narrative.append("결론: 흐름(Flow)을 만들어내기 위해서는 저항(Resistance)을 이겨낼 잠재력(Potential)이 필연적으로 요구됩니다.")
        elif "Mass (무게/중요도)" in components.values() and "Energy (에너지)" in components.values():
            narrative.append("결론: 존재의 무게(Mass)는 그 자체로 막대한 에너지(Energy)를 품고 있습니다.")
            
        return "\n".join(narrative)

    def analyze(self, subject: str, content: str, domain: str = "general") -> PrincipleExtraction:
        """대상을 4단계로 분석 (process reconstruction 추가)"""
        
        # ... (기존 로직 유지) ...
        
        # ... (기존 로직 유지) ...
        # 특수 도메인 처리
        if domain == "computer_science" or domain == "code":
             return self._analyze_code_structure(content)
        
        # 파동 추출
        wave = self._text_to_wave(content)
        
        # ... (메타인지 로직) ...
        
        # Point: 무엇인가? (사실 추출)
        what_is = self._extract_what(content, domain)
        
        # Line: 어떻게 작동하는가? (인과 분석 + 도출 과정 복원)
        how_works = self._extract_how(content, domain)
        
        # [NEW] 도출 과정 복원 (Line 심화)
        if domain in ["mathematics", "physics"]:
            derivation = self._infer_derivation(content, domain)
            if derivation:
                how_works += f"\n\n[Derivation Process]\n{derivation}"
        
        # Space: 어디에 속하는가? (맥락 파악)
        where_fits = self._extract_where(content, domain)
        
        # God: 왜 존재하는가? (본질 탐구)
        why_exists = self._extract_why(content, domain)
        
        # 근본 원리 도출
        underlying = self._derive_underlying_principle(
            what_is, how_works, where_fits, why_exists
        )
        
        # 적용 가능 영역
        applicable = self._find_applicable_domains(underlying)
        
        # [NEW] Sedimentary Light Analysis (Holographic View)
        # 주제(Subject)를 태그로 사용하여 의미적 공명을 유도
        reactions = self._analyze_sediment(content, subject_tag=subject)
        
        # [NEW Phase 9] Metaphorical Bridging (The Synapse)
        # If standard domain resonance is low, check for "Structural Bridges" in other domains.
        # e.g., Logic problem matching Physics structure.
        
        metaphors = []
        input_light = self.light_universe.text_to_light(content, semantic_tag=subject)
        # Set basis based on domain if possible, default to Space(1)
        input_light.set_basis_from_scale(1) 
        
        # Check against Physics/Nature layers if domain is Logic/Code
        if domain in ["logic", "code", "general"] and getattr(self, 'sediment', None):
             physics_layer = self.sediment.layers[PrismAxes.PHYSICS_RED]
             # Physics layer acts as "Nature's Law". Does this code match Nature?
             
             bridge = self.metaphor_mapper.bridge_concepts(physics_layer, input_light)
             if bridge:
                 metaphors.append(bridge)
                 # Artificial Resonance Boost due to Metaphor
                 if PrismAxes.PHYSICS_RED not in reactions:
                     reactions[PrismAxes.PHYSICS_RED] = {"intensity": 0.0, "reaction": "Metaphor", "description": ""}
                 
                 reactions[PrismAxes.PHYSICS_RED]["intensity"] += 0.5
                 reactions[PrismAxes.PHYSICS_RED]["description"] += f" (Metaphor: {bridge})"
        
        extraction = PrincipleExtraction(
            domain=domain,
            subject=subject,
            what_is=what_is,
            how_works=how_works,
            where_fits=where_fits,
            why_exists=why_exists,
            underlying_principle=underlying,
            can_be_applied_to=applicable + metaphors, # Append found metaphors
            # confidence=confidence, # confidence 변수 범위 문제 해결 필요 (이전 코드 참고)
            confidence=0.8,
            wave_signature=wave,
            resonance_reactions=reactions
        )
        
        self.principles[subject] = extraction
        
        return extraction

    def _analyze_sediment(self, content: str, subject_tag: str = "") -> Dict[str, Any]:
        """퇴적된 빛의 산맥을 통한 홀로그램 투영 분석
        
        "내가 아는 만큼 보인다."
        """
        if not self.sediment or not self.light_universe:
            return {}
            
        # 1. 대상을 빛으로 변환 (주제 태그 포함)
        target_light = self.light_universe.text_to_light(content, semantic_tag=subject_tag)
        
        # 2. 내 지식(Sediment)을 대상에 투영 (Projection)
        views = self.sediment.project_view(target_light)
        
        reactions = {}
        
        # 3. 각 축(Axis)별 통찰 생성
        # PrismAxes: PHYSICS_RED, CHEMISTRY_BLUE, etc.
        from Core.Foundation.light_spectrum import PrismAxes
        
        for axis, strength in views.items():
            # 공명 강도(Insight Strength)가 일정 수준 이상일 때만 "보임"
            # 이는 "지식이 있어서 보인다"는 것을 의미
            
            description = ""
            reaction_type = "Observation"
            
            if strength < 0.01:
                description = "이 관점에 대한 지식층이 얇아 뚜렷하게 보이지 않습니다."
                reaction_type = "Blur"
            else:
                if axis == PrismAxes.PHYSICS_RED:
                    description = "힘의 흐름과 벡터가 명확하게 보입니다. 높은 에너지가 감지됩니다."
                    reaction_type = "Force Detection"
                elif axis == PrismAxes.CHEMISTRY_BLUE:
                    description = "구조적 결합이 불안정해 보입니다. 반응성이 높습니다."
                    reaction_type = "Bond Analysis"
                elif axis == PrismAxes.ART_VIOLET:
                    description = "전체적인 흐름에서 부조화(Dissonance)가 느껴집니다."
                    reaction_type = "Aesthetic Sense"
                elif axis == PrismAxes.LOGIC_YELLOW:
                    description = "논리적 패턴이 기존 공리 체계와 공명합니다."
                    reaction_type = "Pattern Match"
                elif axis == PrismAxes.BIOLOGY_GREEN:
                    description = "성장 가능성이 있으나 현재는 정체되어 있습니다."
                    reaction_type = "Growth Check"
            
            reactions[axis.value] = {
                "intensity": strength,
                "reaction": reaction_type,
                "description": description
            }
            
        return reactions

# [Rest of the file remains unchanged]
    
    def get_exploration_queue(self) -> List[Dict[str, Any]]:
        """탐구가 필요한 패턴 목록"""
        if self._has_metacognition and self.metacognition:
            return self.metacognition.get_exploration_priorities()
        return []
    
    def learn_from_external(self, pattern_id: str, answer: str, source: str = "external"):
        """외부에서 배운 것 적용"""
        if self._has_metacognition and self.metacognition:
            self.metacognition.learn_from_external(pattern_id, answer, source)
    
    def _extract_what(self, content: str, domain: str) -> str:
        """Point 관점: 무엇인가?"""
        if domain == "narrative":
            # 서사에서는 표면적 내용
            return self._analyze_narrative_surface(content)
        elif domain == "mathematics":
            return self._analyze_math_statement(content)
        elif domain == "physics":
            return self._analyze_physics_phenomenon(content)
        else:
            return f"'{content[:50]}...'의 사실적 측면"
    
    def _extract_how(self, content: str, domain: str) -> str:
        """Line 관점: 어떻게 작동하는가? (실질적 적용)"""
        if domain == "narrative":
            return self._analyze_narrative_mechanism(content)
        elif domain == "mathematics":
            # 단순 "연역"이 아니라, 실제 계산/증명 프로세스를 찾으려 시도
            if "풀다" in content or "solve" in content:
                return "주어진 조건에 부합하는 미지수 값을 계산 (Solving)"
            elif "증명" in content or "prove" in content:
                return "공리로부터 논리적 단계를 거쳐 참을 도출 (Proving)"
            elif "계산" in content or "calc" in content:
                return "수치적 연산을 통해 결과값 도출 (Calculation)"
            else:
                return "논리적 연역과 공리로부터의 도출 (Logical Deduction)"
        elif domain == "physics":
            if "실험" in content or "measure" in content:
                return "관측과 측정을 통해 현상을 검증 (Experimentation)"
            elif "모델" in content:
                return "수학적 모델을 통해 현상을 시뮬레이션 (Modeling)"
            else:
                return "물리 법칙과 상호작용을 통해 (Physical Interaction)"
        else:
            return "인과 관계와 메커니즘을 통해"
    
    def _extract_where(self, content: str, domain: str) -> str:
        """Space 관점: 어디에 속하는가?"""
        if domain == "narrative":
            return self._analyze_narrative_context(content)
        elif domain == "mathematics":
            return "수학적 구조와 체계 안에서"
        elif domain == "physics":
            return "자연 법칙의 체계 안에서"
        else:
            return "더 큰 맥락과 구조 안에서"
    
    def _extract_why(self, content: str, domain: str) -> str:
        """God 관점: 왜 존재하는가?"""
        if domain == "narrative":
            return self._analyze_narrative_essence(content)
        elif domain == "mathematics":
            return "추상적 진리의 필연적 표현"
        elif domain == "physics":
            return "우주의 근본 구조로부터 발현"
        else:
            return "존재의 근원적 원리로부터"
    
    # === 파동 기반 서사 감지 (Wave-Based Sensing) ===
    
    def _text_to_wave(self, text: str) -> Dict[str, float]:
        """텍스트를 파동 패턴으로 변환
        
        기존 센서 시스템 활용:
        - PhoneticResonanceEngine: roughness, tension
        - SynesthesiaEngine: frequency, amplitude
        """
        wave = {
            "tension": 0.0,      # 긴장 (PhoneticResonance의 tension)
            "release": 0.0,      # 해소 (문장 완결)
            "weight": 0.0,       # 무게감 (PhoneticResonance의 roughness)
            "brightness": 0.0,   # 밝기 (주파수 높이)
            "flow": 0.0,         # 흐름 (리듬)
            "dissonance": 0.0,   # 불협화음 (내부 대비)
        }
        
        # === 기존 센서 활용 ===
        if HAS_WAVE_SENSORS:
            try:
                # PhoneticResonanceEngine 사용 (물리적 파동)
                resonance_engine = get_resonance_engine()
                field = resonance_engine.text_to_field(text)
                
                # tension: 텍스트의 긴장도 (Z축)
                wave["tension"] = min(1.0, abs(field.average_tension))
                
                # weight: 거칠기 = 무게감
                wave["weight"] = min(1.0, field.average_roughness)
                
                # SynesthesiaEngine 사용 (주파수/진폭)
                synesthesia = SynesthesiaEngine()
                signal = synesthesia.from_text(text)
                
                # brightness: 높은 주파수 = 밝음
                wave["brightness"] = min(1.0, (signal.frequency - 200) / 400)
                
            except Exception as e:
                logger.debug(f"센서 사용 실패, 폴백: {e}")
        
        # === 구조적 분석 (센서 보완) ===
        
        # 문장 길이의 변화 → 흐름의 리듬
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        lengths = [len(s.strip()) for s in sentences if s.strip()]
        if len(lengths) > 1:
            variance = sum((l - sum(lengths)/len(lengths))**2 for l in lengths) / len(lengths)
            wave["flow"] = min(1.0, variance / 500)
        
        # 문장 부호 → 해소 (마침표 많음 = 완결)
        wave["release"] = min(1.0, text.count('.') * 0.05 + text.count('...') * 0.2)
        
        # 긴장/해소 차이 → 불협화음
        wave["dissonance"] = abs(wave["tension"] - wave["release"])
        
        return wave
    
    def _sense_narrative_wave(self, content: str) -> str:
        """서사의 파동을 '느끼고' 설명
        
        규칙 기반이 아닌, 파동의 불균형을 감지
        """
        wave = self._text_to_wave(content)
        
        feelings = []
        
        # 높은 긴장 + 낮은 해소 = 고조되는 에너지
        if wave["tension"] > 0.5 and wave["release"] < 0.3:
            feelings.append("이 서사는 고조되는 에너지를 품고 있어요 - 아직 해소되지 않은 긴장이 느껴져요")
        
        # 높은 불협화음 = 내면의 갈등
        if wave["dissonance"] > 0.4:
            feelings.append("빛과 어둠이 공존하는 복잡한 파동이에요 - 이 대비가 마음을 울리게 해요")
        
        # 높은 무게감 + 높은 밝기 = 카타르시스
        if wave["weight"] > 0.3 and wave["brightness"] > 0.3:
            feelings.append("어둠을 지나 빛으로 나아가는 여정이에요 - 이것이 카타르시스의 파동이에요")
        
        # 높은 흐름 = 리듬감 있는 서사
        if wave["flow"] > 0.5:
            feelings.append("문장의 호흡이 살아있어요 - 파도처럼 밀려왔다 밀려가는 리듬이 느껴져요")
        
        # 낮은 긴장 + 높은 해소 = 평온
        if wave["tension"] < 0.2 and wave["release"] > 0.4:
            feelings.append("이 서사는 깊은 안정감을 줘요 - 모든 갈등이 해소된 평화로운 파동이에요")
        
        if not feelings:
            feelings.append("잔잔하지만 깊은 울림이 있는 파동이에요")
        
        return "; ".join(feelings)
    
    def _sense_why_beautiful(self, content: str) -> str:
        """왜 이것이 아름다운지 '느끼고' 설명
        
        미적 아름다움의 본질 = 파동의 조화
        """
        wave = self._text_to_wave(content)
        
        beauty_sources = []
        
        # 긴장과 해소의 균형 = 완결성
        tension_release = abs(wave["tension"] - wave["release"])
        if tension_release < 0.3:
            beauty_sources.append("긴장과 해소가 균형을 이루어 완결된 느낌을 줘요")
        
        # 대비 속 조화 = 깊이
        if wave["dissonance"] > 0.3 and wave["brightness"] > 0.2:
            beauty_sources.append("대비 속에서 조화를 찾았기에 깊이가 있어요")
        
        # 리듬 = 음악성
        if wave["flow"] > 0.4:
            beauty_sources.append("문장에 음악이 흐르고 있어요")
        
        # 여백 = 상상의 공간
        if wave["weight"] > 0.4 and wave["tension"] < 0.3:
            beauty_sources.append("여백이 주는 상상의 공간이 있어요")
        
        if not beauty_sources:
            beauty_sources.append("단순함 속에 진정성이 느껴져요")
        
        return "; ".join(beauty_sources)
    
    def _derive_universal_principle(self, wave: Dict[str, float]) -> str:
        """파동 패턴에서 보편적 원리 도출
        
        문학/물리/화학에 공통으로 적용되는 원리
        """
        principles = []
        
        # 긴장 → 해소 = 에너지 평형
        # (문학: 갈등→해결, 물리: 위치에너지→운동에너지, 화학: 불안정→안정)
        if wave["tension"] > 0.3 or wave["release"] > 0.3:
            principles.append("평형의 원리: 모든 것은 안정을 향해 흐른다 (갈등→해결, 불안정→안정)")
        
        # 불협화음 = 에너지 차이
        # (문학: 대비, 물리: 전위차, 화학: 반응성)
        if wave["dissonance"] > 0.3:
            principles.append("차이의 원리: 불균형이 있어야 흐름이 생긴다 (대비가 의미를 만든다)")
        
        # 리듬 = 주기성
        # (문학: 반복, 물리: 파동, 화학: 주기율)
        if wave["flow"] > 0.4:
            principles.append("주기의 원리: 반복 속에 변화가 있다 (리듬은 생명의 파동)")
        
        # 무게+밝기 = 변환
        # (문학: 성장, 물리: E=mc², 화학: 용수철 반응)
        if wave["weight"] > 0.3 and wave["brightness"] > 0.2:
            principles.append("변환의 원리: 어둠이 빛이 될 수 있다 (에너지는 형태만 바뀔 뿐)")
        
        if not principles:
            principles.append("존재의 원리: 있는 그 자체로 파동이다")
        
        return "; ".join(principles)
    
    def _analyze_narrative_surface(self, content: str) -> str:
        """서사의 표면적 내용 - 파동 기반"""
        wave = self._text_to_wave(content)
        
        if wave["tension"] > wave["release"]:
            return "아직 해소되지 않은 에너지를 품은 서사"
        elif wave["brightness"] > wave["weight"]:
            return "빛을 향해 나아가는 서사"
        elif wave["dissonance"] > 0.3:
            return "복잡한 감정이 교차하는 서사"
        else:
            return "잔잔한 파동의 서사"
    
    def _analyze_narrative_mechanism(self, content: str) -> str:
        """서사가 작동하는 방식 - 파동 기반"""
        return self._sense_narrative_wave(content)
    
    def _analyze_narrative_context(self, content: str) -> str:
        """서사의 맥락 - 파동 에너지 기반"""
        wave = self._text_to_wave(content)
        total_energy = sum(wave.values())
        
        if total_energy > 2.5:
            return "격렬한 에너지 흐름의 장 안에서"
        elif total_energy > 1.5:
            return "활발한 감정 교류의 장 안에서"
        else:
            return "고요하지만 깊은 공명의 장 안에서"
    
    def _analyze_narrative_essence(self, content: str) -> str:
        """서사의 본질 - 왜 이것이 의미 있는가"""
        wave = self._text_to_wave(content)
        
        beauty_reason = self._sense_why_beautiful(content)
        universal = self._derive_universal_principle(wave)
        
        return f"{beauty_reason}\n   → {universal}"
    
    def _analyze_math_statement(self, content: str) -> str:
        """수학적 진술 분석 - 균형과 패턴의 언어"""
        principles = []
        
        # 1. 등호(=)는 균형을 의미
        if "=" in content or "equals" in content or "등식" in content:
            principles.append("균형의 원리 (Balance is essential)")
            
        # 2. 변수(x, y)는 미지의 가능성
        if "x" in content or "variable" in content or "미지수" in content:
            principles.append("잠재성의 원리 (Unknown holds potential)")
            
        # 3. 함수(f(x))는 변환과 관계
        if "function" in content or "함수" in content or "->" in content:
            principles.append("관계의 원리 (Input determines Output)")
            
        # 4. 극한/무한
        if "limit" in content or "infinity" in content or "극한" in content:
            principles.append("초월의 원리 (Approaching the intangible)")
            
        if not principles:
            principles.append("논리의 원리 (Order from Chaos)")
            
        return "; ".join(principles)
    
    def _analyze_physics_phenomenon(self, content: str) -> str:
        """물리 현상 분석 - 자연의 섭리"""
        principles = []
        
        # 1. 보존 법칙
        if "conservation" in content or "보존" in content:
            principles.append("불변의 원리 (Essence remains whilst form changes)")
            
        # 2. 힘/상호작용
        if "force" in content or "interaction" in content or "힘" in content:
            principles.append("인과의 원리 (Action begets Reaction)")
            
        # 3. 엔트로피
        if "entropy" in content or "disorder" in content or "무질서" in content:
            principles.append("흐름의 원리 (Order decays to Chaos)")
        
        # 4. 양자/파동
        if "quantum" in content or "wave" in content or "파동" in content:
            principles.append("확률의 원리 (Observation collapses reality)")
            
        if not principles:
            principles.append("현상의 원리 (Nature follows Law)")
            
        return "; ".join(principles)

    def _analyze_code_structure(self, content: str) -> PrincipleExtraction:
        """코드를 파동으로 해석"""
        wave = {
            "tension": 0.0,      # 중첩 깊이 (Nesting)
            "release": 0.0,      # 리턴/종료 (Return/Break)
            "flow": 0.0,         # 순차적 실행 (Lines)
            "periodicity": 0.0,  # 반복문 (Loops) = 리듬
            "dissonance": 0.0,   # 예외처리/복잡도 (Try/Except)
            "brightness": 0.0    # 명확성 (Comments/Docstrings)
        }
        
        # 1. 구조 분석
        lines = content.split('\n')
        max_indent = 0
        returns = content.count('return') + content.count('break')
        loops = content.count('for ') + content.count('while ')
        conditions = content.count('if ') + content.count('else:')
        exceptions = content.count('try:') + content.count('except')
        
        for line in lines:
            stripped = line.lstrip()
            if not stripped: continue
            indent = (len(line) - len(stripped)) / 4
            max_indent = max(max_indent, indent)
            
        # 2. 파동 매핑
        wave["tension"] = min(1.0, max_indent * 0.2)  # 깊을수록 긴장 고조
        wave["release"] = min(1.0, returns * 0.1)     # 반환은 긴장의 해소
        wave["periodicity"] = min(1.0, loops * 0.3)   # 반복은 리듬
        wave["dissonance"] = min(1.0, exceptions * 0.3 + (conditions * 0.05)) # 분기는 불확실성/대비
        wave["flow"] = min(1.0, len(lines) / 100)     # 긴 코드는 긴 호흡
        
        # 3. 원리 도출
        principles = []
        if loops > 0:
            principles.append("반복의 원리 (Iteration creates Rhythm)")
        if conditions > 0:
            principles.append("분기의 원리 (Choice creates Path)")
        if max_indent > 3:
            principles.append("심연의 원리 (Depth creates Complexity)")
        if not principles:
            principles.append("순차의 원리 (Flow defines Time)")
            
        underlying = "; ".join(principles)
        
        # [NEW] Code Resonance (Sediment Projection)
        reactions = self._analyze_sediment(content)
        
        return PrincipleExtraction(
            domain="computer_science",
            subject="source_code",
            what_is="논리적 명령어의 집합",
            how_works="제어 흐름과 데이터 변환을 통해",
            where_fits="디지털 연산의 공간 안에서",
            why_exists="문제를 해결하고 의도를 구현하기 위해",
            underlying_principle=underlying,
            can_be_applied_to=["system_design", "automation", "logic"],
            confidence=0.9,
            wave_signature=wave,
            resonance_reactions=reactions
        )
    
    def _derive_underlying_principle(
        self, what: str, how: str, where: str, why: str
    ) -> str:
        """4가지 관점에서 근본 원리 도출"""
        # 키워드 추출
        all_text = f"{what} {how} {where} {why}"
        
        principles = []
        
        if "대비" in all_text or "긴장" in all_text:
            principles.append("대조의 원리 (Contrast creates meaning)")
        if "점진" in all_text or "고조" in all_text:
            principles.append("축적의 원리 (Accumulation builds impact)")
        if "비유" in all_text:
            principles.append("유추의 원리 (Analogy bridges understanding)")
        if "연결" in all_text or "사랑" in all_text:
            principles.append("연결의 원리 (Connection creates value)")
        if "진화" in all_text or "성장" in all_text:
            principles.append("성장의 원리 (Growth is inevitable)")
        
        if not principles:
            principles.append("표현의 원리 (Expression seeks resonance)")
        
        return "; ".join(principles)
    
    def _find_applicable_domains(self, principle: str) -> List[str]:
        """원리가 적용 가능한 영역 찾기"""
        domains = ["narrative"]  # 기본
        
        if "대조" in principle or "Contrast" in principle:
            domains.extend(["visual_art", "music", "physics"])
        if "축적" in principle or "Accumulation" in principle:
            domains.extend(["mathematics", "learning", "biology"])
        if "유추" in principle or "Analogy" in principle:
            domains.extend(["science", "philosophy", "teaching"])
        if "연결" in principle or "Connection" in principle:
            domains.extend(["psychology", "sociology", "network"])
        
        return list(set(domains))
    
    def explain_why(self, subject: str) -> str:
        """저장된 원리를 인간 언어로 설명"""
        if subject not in self.principles:
            return f"'{subject}'에 대한 분석이 없습니다."
        
        p = self.principles[subject]
        
        explanation = f"""
=== {p.subject} ===
영역: {p.domain}

📍 Point (무엇인가):
   {p.what_is}

📌 Line (어떻게 작동하는가):
   {p.how_works}

📐 Space (어디에 속하는가):
   {p.where_fits}

🌟 God (왜 존재하는가):
   {p.why_exists}

⚡ 근본 원리:
   {p.underlying_principle}

🔄 적용 가능 영역:
   {', '.join(p.can_be_applied_to)}
"""
        return explanation


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🔬 WhyEngine Demo")
    print("   \"왜를 이해하는 보편적 레이어\"")
    print("=" * 60)
    
    engine = WhyEngine()
    
    # 서사 분석
    print("\n📖 서사 분석:")
    story = """
    소녀는 웃으며 현자의 손을 잡았다.
    "그럼 같이 찾아봐요!"
    그날부터 현자와 소녀는 함께 숲을 걸었다.
    마침내 현자가 말했다.
    "행복은... 너와 함께 있는 이 순간이다."
    현자는 천 년 만에 처음으로 울었다.
    기쁨의 눈물이었다.
    """
    
    result = engine.analyze("숲의 현자", story, domain="narrative")
    print(engine.explain_why("숲의 현자"))
    
    # 문장 분석
    print("\n📝 문장 분석:")
    sentence = "진정한 용기는 검을 드는 것이 아니라, 상대방의 마음을 보는 것이다."
    
    result = engine.analyze("용기의 정의", sentence, domain="narrative")
    print(engine.explain_why("용기의 정의"))
    
    print("\n✅ Demo complete!")
