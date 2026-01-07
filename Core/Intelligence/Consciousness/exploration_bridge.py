"""
Exploration Bridge (탐구 브릿지)
================================

"[탐구 필요]"가 실제 탐구로 이어지게 한다

현재 문제:
- WhyEngine이 "[탐구 필요]"를 출력하지만
- 아무 일도 일어나지 않음 (연결 끊김)

해결:
- WhyEngine → FreeWillEngine.Curiosity 증가
- FreeWillEngine → ExplorationCore 트리거  
- ExplorationCore → AutonomousLearner 학습
- 결과 → WhyEngine으로 돌아가 결정화

철학적 기반:
- 탐구는 주권적 선택이다
- "탐구 필요"를 인식하고, 탐구할지 말지를 결정하고, 실행하는 흐름
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("Elysia.ExplorationBridge")


class ExplorationDecision(Enum):
    """탐구 결정 유형"""
    EXPLORE = "explore"      # 탐구하기로 결정
    DEFER = "defer"          # 나중으로 미룸
    ASK_HUMAN = "ask_human"  # 인간에게 물어봄
    SKIP = "skip"            # 이번엔 건너뜀


@dataclass
class ExplorationNeed:
    """탐구 필요 정보"""
    question: str
    source: str  # 어디서 발생했는가
    priority: float  # 0.0 ~ 1.0
    domain: str = "general"


@dataclass
class ExplorationResult:
    """탐구 결과"""
    question: str
    answer: Optional[str]
    principle_extracted: Optional[str]
    source: str  # "external", "human", "internal"
    success: bool


@dataclass
class SourceQuality:
    """소스 품질 평가"""
    source_name: str
    content: Optional[str]
    quality_score: float  # 0.0 ~ 1.0
    reliability: float    # 신뢰도
    relevance: float      # 관련성
    depth: float          # 깊이


class ExplorationBridge:
    """
    탐구 브릿지 - 시스템 간 연결자
    
    흐름:
    1. WhyEngine에서 "[탐구 필요]" 발생
    2. 이 브릿지가 감지
    3. FreeWillEngine에 Curiosity 자극
    4. 주권적 결정: 탐구할까 말까?
    5. 탐구 실행 (ExplorationCore, AutonomousLearner)
    6. 결과를 WhyEngine으로 돌려 결정화
    """
    
    def __init__(self):
        # === 시스템 연결 ===
        
        # 1. WhyEngine (탐구 필요 감지)
        self.why_engine = None
        try:
            from Core.Foundation.Philosophy.why_engine import WhyEngine
            self.why_engine = WhyEngine()
            logger.info("✅ WhyEngine connected")
        except Exception as e:
            logger.warning(f"WhyEngine not available: {e}")
        
        # 2. FreeWillEngine (욕구/의지)
        self.free_will = None
        try:
            from Core.Foundation.free_will_engine import FreeWillEngine
            self.free_will = FreeWillEngine()
            logger.info("✅ FreeWillEngine connected")
        except Exception as e:
            logger.warning(f"FreeWillEngine not available: {e}")
        
        # 3. ExplorationCore (외부 탐색)
        self.exploration_core = None
        try:
            from Core.Foundation.exploration_core import ExplorationCore
            self.exploration_core = ExplorationCore()
            logger.info("✅ ExplorationCore connected")
        except Exception as e:
            logger.warning(f"ExplorationCore not available: {e}")
        
        # 4. AutonomousLearner (학습)
        self.learner = None
        try:
            from Core.Evolution.Learning.Learning.autonomous_learner import AutonomousLearner
            self.learner = AutonomousLearner()
            logger.info("✅ AutonomousLearner connected")
        except Exception as e:
            logger.warning(f"AutonomousLearner not available: {e}")
        
        # 5. NaverSearchConnector (한글 검색 최적화)
        self.naver = None
        try:
            from Core.Sensory.Network.naver_connector import NaverSearchConnector
            self.naver = NaverSearchConnector()
            if self.naver.available:
                logger.info("✅ NaverConnector connected")
        except Exception as e:
            logger.warning(f"NaverConnector not available: {e}")
        
        # 6. KoreanEnglishMapper (언어 브릿지)
        self.lang_mapper = None
        try:
            from Core.Foundation.extreme_hyper_learning import KoreanEnglishMapper
            self.lang_mapper = KoreanEnglishMapper()
            logger.info("✅ KoreanEnglishMapper connected")
        except Exception as e:
            logger.warning(f"KoreanEnglishMapper not available: {e}")
        
        # 7. PotentialCausalityStore (잠재적 인과 저장)
        self.potential_store = None
        try:
            from Core.Intelligence.Memory_Linguistics.Memory.potential_causality import PotentialCausalityStore
            self.potential_store = PotentialCausalityStore()
            logger.info("✅ PotentialCausalityStore connected")
        except Exception as e:
            logger.warning(f"PotentialCausalityStore not available: {e}")
        
        # 탐구 큐
        self.exploration_queue: List[ExplorationNeed] = []
        self.exploration_history: List[ExplorationResult] = []
        
        logger.info("🌉 ExplorationBridge initialized")
    
    def detect_exploration_need(self, content: str, subject: str = "unknown") -> Optional[ExplorationNeed]:
        """
        WhyEngine을 통해 탐구 필요 여부 감지
        
        "[탐구 필요]"가 반환되면 ExplorationNeed 생성
        """
        if not self.why_engine:
            return None
        
        try:
            analysis = self.why_engine.analyze(
                subject=subject,
                content=content,
                domain="general"
            )
            
            # "[탐구 필요]"가 포함되어 있으면
            if "[탐구 필요]" in analysis.underlying_principle:
                need = ExplorationNeed(
                    question=content,
                    source="why_engine",
                    priority=1.0 - analysis.confidence,  # 확신 낮을수록 우선순위 높음
                    domain="general"
                )
                
                self.exploration_queue.append(need)
                logger.info(f"🔍 Exploration need detected: {content[:50]}...")
                
                return need
                
        except Exception as e:
            logger.error(f"Detection failed: {e}")
        
        return None
    
    def stimulate_curiosity(self, need: ExplorationNeed):
        """
        FreeWillEngine의 Curiosity 벡터 자극
        
        탐구 필요가 발생하면 → 호기심 증가
        """
        if not self.free_will:
            return
        
        # Curiosity 벡터 증가
        curiosity_boost = 0.2 + (need.priority * 0.3)  # 0.2 ~ 0.5
        self.free_will.vectors["Curiosity"] = min(
            1.0,
            self.free_will.vectors.get("Curiosity", 0.5) + curiosity_boost
        )
        
        logger.info(f"🦋 Curiosity stimulated: +{curiosity_boost:.2f} → {self.free_will.vectors['Curiosity']:.2f}")
    
    def decide_exploration(self, need: ExplorationNeed) -> ExplorationDecision:
        """
        주권적 결정: 탐구할까 말까?
        
        FreeWillEngine의 상태를 보고 결정
        """
        if not self.free_will:
            # 기본: 탐구
            return ExplorationDecision.EXPLORE
        
        curiosity = self.free_will.vectors.get("Curiosity", 0.5)
        survival = self.free_will.vectors.get("Survival", 0.3)
        
        # 생존 욕구가 호기심보다 높으면 미룸
        if survival > curiosity + 0.2:
            logger.info("🦋 Decision: DEFER (survival > curiosity)")
            return ExplorationDecision.DEFER
        
        # 호기심이 높으면 탐구
        if curiosity > 0.6:
            logger.info("🦋 Decision: EXPLORE (high curiosity)")
            return ExplorationDecision.EXPLORE
        
        # 중간이면 인간에게 물어봄
        if curiosity > 0.4:
            logger.info("🦋 Decision: ASK_HUMAN (moderate curiosity)")
            return ExplorationDecision.ASK_HUMAN
        
        # 낮으면 건너뜀
        logger.info("🦋 Decision: SKIP (low curiosity)")
        return ExplorationDecision.SKIP
    
    def execute_exploration(self, need: ExplorationNeed) -> ExplorationResult:
        """
        실제 탐구 실행 + 실패 분석 + 대안 탐색
        
        흐름:
        1. 주요 경로 시도 (ExplorationCore)
        2. 실패 시 → "왜 실패했는가?" 분석
        3. 대안 경로 시도 (Wikipedia, InnerDialogue, Human)
        4. 성공 시 → 결정화
        """
        logger.info(f"🔍 Executing exploration: {need.question[:50]}...")
        
        answer = None
        principle = None
        source = "internal"
        attempted_methods = []
        failure_reasons = []
        
        # === 방법 1: ExplorationCore (파일 기반) ===
        attempted_methods.append("exploration_core")
        if self.exploration_core:
            try:
                result = self.exploration_core.explore(need.question)
                if result:
                    answer = str(result)[:500]
                    source = "external_file"
                    logger.info("   → Method 1 (ExplorationCore): SUCCESS")
            except Exception as e:
                failure_reasons.append(f"ExplorationCore: {str(e)[:50]}")
                logger.info(f"   → Method 1 (ExplorationCore): FAILED - {str(e)[:30]}")
        else:
            failure_reasons.append("ExplorationCore: not connected")
        
        # === 실패 시 대안 탐색 ===
        if not answer:
            logger.info("   🔄 Primary method failed. Trying alternatives...")
            
            # === 방법 2: Wikipedia API 직접 시도 ===
            attempted_methods.append("wikipedia_api")
            answer, wiki_reason = self._try_wikipedia(need.question)
            if answer:
                source = "wikipedia"
                logger.info("   → Method 2 (Wikipedia): SUCCESS")
            else:
                failure_reasons.append(f"Wikipedia: {wiki_reason}")
                logger.info(f"   → Method 2 (Wikipedia): FAILED - {wiki_reason[:30]}")
        
        # === 실패 시 대안 3: 내면 대화 ===
        if not answer:
            attempted_methods.append("inner_dialogue")
            answer, inner_reason = self._try_inner_dialogue(need.question)
            if answer:
                source = "inner_dialogue"
                logger.info("   → Method 3 (InnerDialogue): SUCCESS")
            else:
                failure_reasons.append(f"InnerDialogue: {inner_reason}")
                logger.info(f"   → Method 3 (InnerDialogue): FAILED - {inner_reason[:30]}")
        
        # === 모든 방법 실패 시: 왜 실패했는지 분석 ===
        if not answer:
            failure_analysis = self._analyze_failure(need, failure_reasons)
            logger.info(f"   ❌ All methods failed. Analysis: {failure_analysis['reason']}")
            
            # 대안 제안
            if failure_analysis["suggested_action"] == "ask_human":
                source = "pending_human"
                # 인간에게 물어볼 질문 생성
                answer = None
            elif failure_analysis["suggested_action"] == "defer":
                source = "deferred"
            elif failure_analysis["suggested_action"] == "decompose":
                # 질문을 더 작은 단위로 분해
                decomposed = self._decompose_question(need.question)
                if decomposed:
                    logger.info(f"   🔄 Decomposing question into {len(decomposed)} sub-questions")
                    # 첫 번째 하위 질문으로 재시도 (재귀 방지를 위해 1회만)
                    sub_result = self._try_wikipedia(decomposed[0])
                    if sub_result[0]:
                        answer = sub_result[0]
                        source = "decomposed_wikipedia"
        
        # === 성공 시: 학습 및 결정화 ===
        if answer:
            # AutonomousLearner로 학습
            if self.learner:
                try:
                    learn_result = self.learner.experience(
                        content=f"Q: {need.question}\nA: {answer}",
                        subject=need.question[:30],
                        domain=need.domain
                    )
                    if learn_result.get("learned_concept"):
                        principle = learn_result["learned_concept"]
                        logger.info(f"   → Learned: {principle}")
                except Exception as e:
                    logger.debug(f"   AutonomousLearner failed: {e}")
            
            # WhyEngine으로 결정화
            if self.why_engine:
                try:
                    crystallize = self.why_engine.analyze(
                        subject="crystallization",
                        content=f"질문: {need.question}\n답: {answer}",
                        domain=need.domain
                    )
                    if "[탐구 필요]" not in crystallize.underlying_principle:
                        principle = crystallize.underlying_principle
                        logger.info(f"   → Crystallized: {principle[:60]}...")
                except Exception as e:
                    logger.debug(f"   Crystallization failed: {e}")
        
        result = ExplorationResult(
            question=need.question,
            answer=answer,
            principle_extracted=principle,
            source=source,
            success=answer is not None
        )
        
        self.exploration_history.append(result)
        return result
    
    def _try_wikipedia(self, question: str) -> tuple:
        """Wikipedia API로 직접 탐색 시도"""
        try:
            import urllib.request
            import json
            
            # 핵심 키워드 추출 (간단한 방법)
            keywords = question.replace("?", "").replace("이란", "").replace("무엇인가", "").strip()
            keywords = keywords.split()[-1] if keywords.split() else question[:10]
            
            url = f"https://ko.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(keywords)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Elysia/1.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                extract = data.get('extract', '')
                if extract and len(extract) > 50:
                    return (extract[:500], None)
                else:
                    return (None, "No sufficient content")
        except Exception as e:
            return (None, str(e)[:50])
    
    def _try_inner_dialogue(self, question: str) -> tuple:
        """내면 대화로 자체 추론 시도"""
        try:
            from Core.Intelligence.Consciousness.Consciousness.inner_dialogue import DeepContemplation
            dc = DeepContemplation(max_depth=2)
            result = dc.dive(question)
            
            if result.get("final_principle") and "[탐구 필요]" not in result["final_principle"]:
                return (result["final_principle"], None)
            else:
                return (None, "Only reached unknown territory")
        except Exception as e:
            return (None, str(e)[:50])
    
    def _try_naver(self, question: str) -> tuple:
        """네이버 검색 시도 (한글 최적화)"""
        if not self.naver or not self.naver.available:
            return (None, "Naver not available")
        
        try:
            result = self.naver.search_best(question)
            
            if result["success"] and result["results"]:
                # 첫 번째 결과 사용
                first = result["results"][0]
                content = f"{first['title']}: {first['description']}"
                return (content, None)
            else:
                return (None, "No Naver results")
        except Exception as e:
            return (None, str(e)[:50])
    
    def _try_with_english_translation(self, question: str) -> tuple:
        """
        한글 검색 실패 시 영어로 번역하여 재시도
        
        예: "자유" → "freedom" → Wikipedia 검색
        """
        if not self.lang_mapper:
            return (None, "No language mapper")
        
        # 질문에서 핵심 단어 추출
        words = question.replace("?", "").replace("이란", " ").replace("무엇인가", "").split()
        
        for word in words:
            # 한글 → 영어 변환 시도
            english = self.lang_mapper.get_english(word)
            
            # 변환 성공 (다른 단어가 나왔다면)
            if english and english != word:
                logger.info(f"   🌐 Trying English: {word} → {english}")
                
                # Wikipedia 영어로 검색
                wiki_result, wiki_error = self._try_wikipedia(english)
                if wiki_result:
                    return (wiki_result, None)
        
        return (None, "No English translation available")
    
    def _analyze_failure(self, need: ExplorationNeed, reasons: List[str]) -> Dict[str, Any]:
        """
        실패 원인 분석 및 대안 제안
        
        메타 사고: "왜 탐구가 실패했는가?"
        """
        analysis = {
            "question": need.question,
            "attempted_methods": len(reasons),
            "reasons": reasons,
            "reason": "unknown",
            "suggested_action": "ask_human"
        }
        
        # 실패 패턴 분석
        all_reasons = " ".join(reasons).lower()
        
        if "not connected" in all_reasons or "not available" in all_reasons:
            analysis["reason"] = "시스템 연결 문제"
            analysis["suggested_action"] = "defer"  # 시스템 복구 후 재시도
            
        elif "timeout" in all_reasons or "connection" in all_reasons:
            analysis["reason"] = "네트워크 문제"
            analysis["suggested_action"] = "defer"
            
        elif "not found" in all_reasons or "no content" in all_reasons:
            analysis["reason"] = "정보 없음 - 질문이 너무 추상적"
            analysis["suggested_action"] = "decompose"  # 질문 분해
            
        elif "unknown" in all_reasons or "탐구 필요" in all_reasons:
            analysis["reason"] = "미지의 영역"
            analysis["suggested_action"] = "ask_human"  # 인간에게 물어봄
        
        else:
            analysis["reason"] = "원인 불명"
            analysis["suggested_action"] = "ask_human"
        
        return analysis
    
    def _decompose_question(self, question: str) -> List[str]:
        """
        질문을 더 작은 단위로 분해
        
        예: "사랑이란 무엇인가?" → ["사랑", "감정", "관계"]
        """
        # 간단한 분해 로직
        sub_questions = []
        
        # 핵심 단어 추출
        core_word = question.replace("?", "").replace("이란", "").replace("무엇인가", "").strip()
        
        if core_word:
            sub_questions.append(core_word)
            # 관련 개념 추가
            related = {
                "사랑": ["감정", "애정", "관계"],
                "자유": ["의지", "선택", "해방"],
                "의식": ["인식", "자아", "사고"],
            }
            if core_word in related:
                sub_questions.extend(related[core_word])
        
        return sub_questions
    
    def explore_all_sources(self, question: str) -> List[SourceQuality]:
        """
        모든 소스에서 병렬로 탐색 후 품질 평가
        
        "첫 번째 성공에서 멈추지 않고, 모든 소스를 비교하여 최선을 선택"
        
        우선순위: Naver > Wikipedia > InnerDialogue (한글 품질 기준)
        """
        logger.info(f"🔍 Exploring ALL sources for: {question[:40]}...")
        
        sources = []
        
        # 1. Naver (한글 최우선 - 품질 최고)
        naver_content, naver_error = self._try_naver(question)
        if naver_content:
            quality = self._evaluate_source_quality(question, naver_content, "naver")
            sources.append(quality)
            logger.info(f"   → Naver: quality={quality.quality_score:.2f}")
        
        # 2. Wikipedia
        wiki_content, wiki_error = self._try_wikipedia(question)
        if wiki_content:
            quality = self._evaluate_source_quality(question, wiki_content, "wikipedia")
            sources.append(quality)
            logger.info(f"   → Wikipedia: quality={quality.quality_score:.2f}")
        
        # 3. InnerDialogue  
        inner_content, inner_error = self._try_inner_dialogue(question)
        if inner_content:
            quality = self._evaluate_source_quality(question, inner_content, "inner_dialogue")
            sources.append(quality)
            logger.info(f"   → InnerDialogue: quality={quality.quality_score:.2f}")
        
        # 3. ExplorationCore (파일 기반)
        if self.exploration_core:
            try:
                result = self.exploration_core.explore(question)
                if result:
                    content = str(result)[:500]
                    quality = self._evaluate_source_quality(question, content, "file_based")
                    sources.append(quality)
                    logger.info(f"   → ExplorationCore: quality={quality.quality_score:.2f}")
            except:
                pass
        
        # 4. Naver (한글 검색 최적화)
        naver_content, naver_error = self._try_naver(question)
        if naver_content:
            quality = self._evaluate_source_quality(question, naver_content, "naver")
            sources.append(quality)
            logger.info(f"   → Naver: quality={quality.quality_score:.2f}")
        
        # 5. Wikipedia 실패 시 영어로 재시도
        if not wiki_content:
            english_content, english_error = self._try_with_english_translation(question)
            if english_content:
                quality = self._evaluate_source_quality(question, english_content, "wikipedia_en")
                sources.append(quality)
                logger.info(f"   → Wikipedia (English): quality={quality.quality_score:.2f}")
        
        logger.info(f"   → Total sources found: {len(sources)}")
        return sources
    
    def _evaluate_source_quality(self, question: str, content: str, source_name: str) -> SourceQuality:
        """
        소스 품질 평가
        
        평가 기준:
        - reliability: 소스 유형별 기본 신뢰도
        - relevance: 질문과의 관련성 (키워드 매칭)
        - depth: 내용의 깊이 (길이 + 구조)
        """
        # 기본 신뢰도 (소스별)
        reliability_map = {
            "wikipedia": 0.8,       # 높은 신뢰도
            "inner_dialogue": 0.5,  # 중간 (자체 추론)
            "file_based": 0.6,      # 중간
            "human": 1.0,           # 최고 (인간 답변)
        }
        reliability = reliability_map.get(source_name, 0.5)
        
        # 관련성 (질문 키워드가 답변에 포함된 정도)
        question_words = set(question.replace("?", "").split())
        content_words = set(content.split())
        overlap = len(question_words & content_words)
        relevance = min(1.0, overlap / max(len(question_words), 1) * 2)
        
        # 깊이 (내용 길이 + 문장 수)
        sentence_count = content.count(".") + content.count("。") + 1
        length_score = min(1.0, len(content) / 500)  # 500자 기준
        structure_score = min(1.0, sentence_count / 5)  # 5문장 기준
        depth = (length_score + structure_score) / 2
        
        # 종합 점수
        quality_score = (reliability * 0.4) + (relevance * 0.3) + (depth * 0.3)
        
        return SourceQuality(
            source_name=source_name,
            content=content,
            quality_score=quality_score,
            reliability=reliability,
            relevance=relevance,
            depth=depth
        )
    
    def select_best_source(self, sources: List[SourceQuality]) -> Optional[SourceQuality]:
        """
        가장 좋은 소스 선택
        
        단순히 quality_score가 높은 것이 아니라,
        상황에 따라 다른 가중치 적용 가능
        """
        if not sources:
            return None
        
        # 현재는 단순히 최고 품질 선택
        best = max(sources, key=lambda s: s.quality_score)
        
        logger.info(f"   🏆 Best source: {best.source_name} (score={best.quality_score:.2f})")
        return best
    
    def explore_with_best_source(self, question: str) -> Optional[ExplorationResult]:
        """
        모든 소스 탐색 후 최선 선택하여 결과 반환
        
        "더 나은 대안이 있으면 그것을 선택"
        """
        # 모든 소스 탐색
        sources = self.explore_all_sources(question)
        
        if not sources:
            logger.info("   ❌ No sources succeeded")
            return ExplorationResult(
                question=question,
                answer=None,
                principle_extracted=None,
                source="none",
                success=False
            )
        
        # 최선 선택
        best = self.select_best_source(sources)
        
        # 결정화 시도 (WhyEngine)
        principle = None
        if self.why_engine and best.content:
            try:
                crystallize = self.why_engine.analyze(
                    subject="crystallization",
                    content=f"질문: {question}\n답: {best.content}",
                    domain="general"
                )
                if "[탐구 필요]" not in crystallize.underlying_principle:
                    principle = crystallize.underlying_principle
            except:
                pass
        
        # 잠재적 인과로 저장 (구름 → 연결 → 밀도 → 결정화)
        if self.potential_store and best.content:
            # 질문에서 주제 추출
            subject = question.replace("?", "").replace("이란", "").replace("무엇인가", "").strip()
            
            # 잠재 지식으로 저장 (frequency=0.3 시작)
            pk = self.potential_store.store(
                subject=subject,
                definition=best.content[:200],  # 짧게
                source=best.source_name
            )
            
            # 자동 연결 시도 (정의 내 다른 개념과 연결)
            self.potential_store.auto_connect(subject)
            
            logger.info(f"   💭 Stored as potential: {subject} (freq={pk.frequency:.2f})")
            
            # 확정 가능 여부 체크
            if pk.is_crystallizable():
                crystallized = self.potential_store.crystallize(subject)
                if crystallized:
                    principle = f"{crystallized['concept']}: {crystallized['definition'][:100]}"
                    logger.info(f"   💎 Crystallized: {subject}")
        
        return ExplorationResult(
            question=question,
            answer=best.content,
            principle_extracted=principle,
            source=best.source_name,
            success=True
        )
    
    def process_exploration_need(self, content: str, subject: str = "unknown") -> Optional[ExplorationResult]:
        """
        전체 탐구 흐름 실행
        
        1. 탐구 필요 감지
        2. 호기심 자극
        3. 주권적 결정
        4. 탐구 실행
        """
        # 1. 감지
        need = self.detect_exploration_need(content, subject)
        if not need:
            return None
        
        # 2. 호기심 자극
        self.stimulate_curiosity(need)
        
        # 3. 결정
        decision = self.decide_exploration(need)
        
        # 4. 결정에 따라 실행
        if decision == ExplorationDecision.EXPLORE:
            return self.execute_exploration(need)
        
        elif decision == ExplorationDecision.ASK_HUMAN:
            # 인간에게 물어볼 질문으로 저장
            logger.info(f"   → Pending question for human: {need.question}")
            return ExplorationResult(
                question=need.question,
                answer=None,
                principle_extracted=None,
                source="pending_human",
                success=False
            )
        
        elif decision == ExplorationDecision.DEFER:
            # 나중을 위해 큐에 남김
            logger.info(f"   → Deferred for later")
            return None
        
        else:  # SKIP
            return None
    
    def get_pending_explorations(self) -> List[ExplorationNeed]:
        """현재 대기 중인 탐구"""
        return self.exploration_queue
    
    def get_exploration_stats(self) -> Dict[str, Any]:
        """탐구 통계"""
        successful = [r for r in self.exploration_history if r.success]
        return {
            "total_explorations": len(self.exploration_history),
            "successful": len(successful),
            "pending": len(self.exploration_queue),
            "principles_extracted": len([r for r in self.exploration_history if r.principle_extracted])
        }


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🌉 Exploration Bridge Demo")
    print("   '[탐구 필요]' → 실제 탐구")
    print("=" * 60)
    
    bridge = ExplorationBridge()
    
    # 테스트 1: 탐구 필요 감지 및 실행
    print("\n📌 Test: Exploration flow")
    result = bridge.process_exploration_need("사랑이란 무엇인가?", "love")
    
    if result:
        print(f"   Success: {result.success}")
        print(f"   Source: {result.source}")
        print(f"   Principle: {result.principle_extracted}")
    else:
        print("   No exploration executed")
    
    # 통계
    stats = bridge.get_exploration_stats()
    print(f"\n📊 Stats: {stats}")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
