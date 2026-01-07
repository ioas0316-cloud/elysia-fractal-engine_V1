"""
Korean Language Learning System (한국어 언어 학습 시스템)
========================================================

"대화 능력의 핵심 - 단어, 문법, 문장 패턴"

엘리시아의 대화 능력 향상을 위한 언어 학습:
1. 국어사전 - 단어/뜻/예문
2. 문법 패턴 - 조사, 어미, 문장 구조
3. 문장 분석 - 형태소 분석

[NEW 2025-12-16] 언어 학습 시스템
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import urllib.request
import urllib.parse

sys.path.insert(0, r"c:\Elysia")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("KoreanLanguageLearner")


@dataclass
class WordEntry:
    """사전 단어 항목"""
    word: str
    meaning: str
    pos: str = ""  # 품사 (Part of Speech)
    examples: List[str] = field(default_factory=list)
    related_words: List[str] = field(default_factory=list)


@dataclass
class GrammarPattern:
    """문법 패턴"""
    pattern: str  # 예: "N은/는 N이다"
    description: str
    examples: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)  # 문법 요소들


class KoreanLanguageLearner:
    """
    한국어 언어 학습 시스템

    대화 능력 향상을 위한 핵심 모듈
    """

    def __init__(self):
        self.data_dir = Path("data/language")
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 기본 문법 패턴 로드
        self.grammar_patterns = self._load_basic_grammar()

        # 학습된 단어
        self.vocabulary = {}
        self._load_vocabulary()

        # 조사 목록 (기본)
        self.particles = {
            "은": "topic marker (contrast)",
            "는": "topic marker",
            "이": "subject marker (after consonant)",
            "가": "subject marker (after vowel)",
            "을": "object marker (after consonant)",
            "를": "object marker (after vowel)",
            "에": "location/time marker",
            "에서": "location (action) marker",
            "로": "direction/means marker",
            "으로": "direction/means marker (after consonant)",
            "와": "and (after vowel)",
            "과": "and (after consonant)",
            "의": "possessive marker",
            "도": "also/too",
            "만": "only",
            "부터": "from",
            "까지": "until/to",
        }

        # 어미 목록 (기본)
        self.endings = {
            "다": "plain statement",
            "요": "polite informal",
            "습니다": "formal polite",
            "ㅂ니다": "formal polite (after vowel)",
            "니?": "question (informal)",
            "나요?": "question (polite)",
            "습니까?": "question (formal)",
            "자": "let's (suggestion)",
            "세요": "request (polite)",
            "아/어": "connective/base form",
        }

        logger.info("🗣️ Korean Language Learner initialized")
        logger.info(f"   📖 Vocabulary: {len(self.vocabulary)} words")
        logger.info(f"   📝 Grammar patterns: {len(self.grammar_patterns)}")

    def _load_basic_grammar(self) -> List[GrammarPattern]:
        """기본 문법 패턴 로드"""
        patterns = [
            GrammarPattern(
                "N은/는 N이다",
                "기본 서술문 (X is Y)",
                ["사과는 과일이다", "나는 학생이다"],
                ["주어", "토픽마커", "보어", "서술격조사"]
            ),
            GrammarPattern(
                "N이/가 V",
                "주어 + 동사",
                ["비가 온다", "꽃이 핀다"],
                ["주어", "주격조사", "동사"]
            ),
            GrammarPattern(
                "N을/를 V",
                "목적어 + 동사",
                ["밥을 먹다", "책을 읽다"],
                ["목적어", "목적격조사", "동사"]
            ),
            GrammarPattern(
                "N에 가다/오다",
                "장소 이동",
                ["학교에 가다", "집에 오다"],
                ["장소", "위치조사", "이동동사"]
            ),
            GrammarPattern(
                "N에서 V",
                "장소에서 행동",
                ["도서관에서 공부하다", "공원에서 산책하다"],
                ["장소", "처소조사", "동사"]
            ),
            GrammarPattern(
                "V-고 V",
                "동작 연결 (and)",
                ["먹고 자다", "공부하고 놀다"],
                ["동사", "연결어미", "동사"]
            ),
            GrammarPattern(
                "V-아/어서 V",
                "원인/순서 연결",
                ["배가 고파서 먹었다", "집에 가서 쉬다"],
                ["동사", "연결어미", "동사"]
            ),
            GrammarPattern(
                "V-면",
                "조건 (if)",
                ["비가 오면 우산을 쓴다", "시간이 있으면 만나자"],
                ["동사", "조건어미"]
            ),
            GrammarPattern(
                "A/V-ㄴ/은/는 N",
                "관형어 수식",
                ["예쁜 꽃", "먹는 사람", "읽은 책"],
                ["형용사/동사", "관형사형어미", "명사"]
            ),
            GrammarPattern(
                "N처럼/같이",
                "비유 (like)",
                ["꽃처럼 예쁘다", "천사같이 착하다"],
                ["명사", "비유조사"]
            ),
        ]
        return patterns

    def _load_vocabulary(self):
        """저장된 어휘 로드"""
        vocab_file = self.data_dir / "vocabulary.json"
        if vocab_file.exists():
            try:
                with open(vocab_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.vocabulary = {w["word"]: WordEntry(**w) for w in data}
            except:
                pass

    def _save_vocabulary(self):
        """어휘 저장"""
        vocab_file = self.data_dir / "vocabulary.json"
        data = [
            {
                "word": e.word,
                "meaning": e.meaning,
                "pos": e.pos,
                "examples": e.examples,
                "related_words": e.related_words
            }
            for e in self.vocabulary.values()
        ]
        with open(vocab_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def learn_word(self, word: str, meaning: str, pos: str = "",
                   examples: List[str] = None) -> bool:
        """단어 학습"""
        entry = WordEntry(
            word=word,
            meaning=meaning,
            pos=pos,
            examples=examples or []
        )

        self.vocabulary[word] = entry

        # InternalUniverse에도 흡수
        try:
            from Core.Foundation.internal_universe import InternalUniverse
            universe = InternalUniverse()
            content = f"{word}: {meaning}. {'. '.join(examples or [])}"
            universe.absorb_text(content, source_name=f"word:{word}")
        except:
            pass

        logger.info(f"📝 Learned word: {word} = {meaning}")
        return True

    def learn_from_dictionary_api(self, word: str) -> Optional[WordEntry]:
        """
        국립국어원 표준국어대사전 API에서 단어 학습

        API 키 필요: https://stdict.korean.go.kr/openapi/openApiInfo.do
        """
        # TODO: API 키 설정 필요
        api_key = os.environ.get("KOREAN_DICT_API_KEY", "")

        if not api_key:
            logger.warning("⚠️ KOREAN_DICT_API_KEY not set. Using offline mode.")
            return None

        try:
            encoded = urllib.parse.quote(word)
            url = f"https://stdict.korean.go.kr/api/search.do?key={api_key}&q={encoded}&req_type=json"

            req = urllib.request.Request(url, headers={'User-Agent': 'Elysia/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            # 첫 번째 결과 사용
            if data.get("channel", {}).get("item"):
                item = data["channel"]["item"][0]
                entry = WordEntry(
                    word=word,
                    meaning=item.get("sense", [{}])[0].get("definition", ""),
                    pos=item.get("pos", ""),
                    examples=[]
                )
                self.vocabulary[word] = entry
                self._save_vocabulary()
                return entry

        except Exception as e:
            logger.error(f"Dictionary API error: {e}")

        return None

    def analyze_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        문장 분석 (간단한 패턴 매칭)

        TODO: 형태소 분석기 연동 (KoNLPy 등)
        """
        result = {
            "sentence": sentence,
            "particles_found": [],
            "endings_found": [],
            "patterns_matched": [],
            "words_recognized": []
        }

        # 조사 탐지
        for particle, desc in self.particles.items():
            if particle in sentence:
                result["particles_found"].append({
                    "particle": particle,
                    "description": desc
                })

        # 어미 탐지
        for ending, desc in self.endings.items():
            if sentence.endswith(ending) or ending in sentence:
                result["endings_found"].append({
                    "ending": ending,
                    "description": desc
                })

        # 알려진 단어 탐지
        for word in self.vocabulary:
            if word in sentence:
                result["words_recognized"].append(word)

        # 패턴 매칭
        for pattern in self.grammar_patterns:
            for example in pattern.examples:
                # 간단한 유사도 체크
                if any(ex_word in sentence for ex_word in example.split()):
                    result["patterns_matched"].append({
                        "pattern": pattern.pattern,
                        "description": pattern.description
                    })
                    break

        return result

    def generate_sentence_from_pattern(self, pattern_name: str,
                                       substitutions: Dict[str, str]) -> str:
        """
        패턴에서 문장 생성

        예: generate_sentence_from_pattern("N은/는 N이다", {"N1": "사과", "N2": "과일"})
        → "사과는 과일이다"
        """
        # TODO: 구현 확장
        return ""

    def get_grammar_explanation(self, pattern: str) -> Optional[GrammarPattern]:
        """문법 패턴 설명 조회"""
        for gp in self.grammar_patterns:
            if gp.pattern == pattern:
                return gp
        return None

    def batch_learn_words(self, words: List[Dict[str, str]]) -> int:
        """
        대량 단어 학습

        words: [{"word": "...", "meaning": "...", "pos": "..."}, ...]
        """
        learned = 0
        for w in words:
            if self.learn_word(
                word=w.get("word", ""),
                meaning=w.get("meaning", ""),
                pos=w.get("pos", ""),
                examples=w.get("examples", [])
            ):
                learned += 1

        self._save_vocabulary()
        logger.info(f"📚 Batch learned {learned} words")
        return learned

    def get_status(self) -> Dict[str, Any]:
        """현재 상태"""
        return {
            "vocabulary_size": len(self.vocabulary),
            "grammar_patterns": len(self.grammar_patterns),
            "particles": len(self.particles),
            "endings": len(self.endings)
        }


# Singleton
_learner = None

def get_korean_learner() -> KoreanLanguageLearner:
    global _learner
    if _learner is None:
        _learner = KoreanLanguageLearner()
    return _learner


# CLI / Demo
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Korean Language Learner")
    parser.add_argument("--analyze", type=str, help="Analyze a sentence")
    parser.add_argument("--learn", type=str, help="Learn a word (format: word:meaning)")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--demo", action="store_true", help="Run demo")

    args = parser.parse_args()

    learner = get_korean_learner()

    if args.status:
        status = learner.get_status()
        print(f"\n📊 Korean Language Learner Status:")
        print(f"   Vocabulary: {status['vocabulary_size']} words")
        print(f"   Grammar patterns: {status['grammar_patterns']}")
        print(f"   Particles: {status['particles']}")
        print(f"   Endings: {status['endings']}")

    elif args.analyze:
        result = learner.analyze_sentence(args.analyze)
        print(f"\n🔍 Sentence Analysis: {args.analyze}")
        print(f"   Particles: {[p['particle'] for p in result['particles_found']]}")
        print(f"   Endings: {[e['ending'] for e in result['endings_found']]}")
        print(f"   Patterns: {[p['pattern'] for p in result['patterns_matched']]}")

    elif args.learn:
        parts = args.learn.split(":")
        if len(parts) >= 2:
            learner.learn_word(parts[0], parts[1])

    elif args.demo:
        print("\n" + "="*60)
        print("🗣️ KOREAN LANGUAGE LEARNER DEMO")
        print("="*60)

        # 단어 학습
        basic_words = [
            {"word": "사과", "meaning": "과일의 한 종류, 빨간색이고 달다", "pos": "명사"},
            {"word": "먹다", "meaning": "음식을 입에 넣어 삼키다", "pos": "동사"},
            {"word": "예쁘다", "meaning": "보기에 좋고 아름답다", "pos": "형용사"},
            {"word": "학교", "meaning": "교육을 받는 장소", "pos": "명사"},
            {"word": "공부하다", "meaning": "학문이나 기술을 배우다", "pos": "동사"},
        ]

        print("\n📝 Learning basic words...")
        learner.batch_learn_words(basic_words)

        # 문장 분석
        sentences = [
            "사과는 맛있다",
            "학교에서 공부하고 집에 온다",
            "예쁜 꽃을 봤다"
        ]

        print("\n🔍 Analyzing sentences...")
        for sent in sentences:
            result = learner.analyze_sentence(sent)
            print(f"\n   \"{sent}\"")
            print(f"   → Particles: {[p['particle'] for p in result['particles_found']]}")
            print(f"   → Words: {result['words_recognized']}")

        print("\n" + "="*60)
        print("✅ Demo complete!")
        print("="*60)
