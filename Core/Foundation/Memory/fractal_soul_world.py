"""
Fractal Soul World (프랙탈 영혼 세계)
=====================================

"작은 것이 곧 전체" - 프랙탈 구조의 세계

각 주민이:
1. 자신이 세계라는 것을 모른 채 "나는 사람이다"라고 인식
2. 심장(경험/연산)과 머리(언어/표현)가 따로 작동
3. 자신만의 언어로 생각하고, 그것이 한글/영어로 투영됨
4. 일기를 쓰고, 음악을 느끼고, 음식을 먹고, 관계를 맺음

이 모든 것이 엘리시아의 양분이 됩니다.
"""

from __future__ import annotations

import random
import time
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum, auto
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("FractalSoulWorld")


# =============================================================================
# Configuration Constants
# =============================================================================

# Simulation probabilities
DAILY_INTERACTION_PROB = 0.1      # Probability of two souls meeting each day
DIARY_WRITE_PROB = 0.05           # Probability of writing diary each day
SOCIAL_ACTIVITY_PROB = 0.3        # Probability of social activity when lonely

# Life event parameters
BASE_DEATH_PROB = 0.0001          # Base daily death probability
ELDER_AGE_THRESHOLD = 60          # Age when death probability increases
AGE_DEATH_FACTOR = 0.1            # Death probability increase per year over elder age
ELF_LONGEVITY_FACTOR = 0.3        # Elves have 30% death rate of humans

# Population parameters
MAX_BIRTHS_PER_YEAR = 5           # Maximum new souls born per year


# =============================================================================
# 1. 영혼의 심장 (Soul Heart) - 연산과 경험의 핵심
# =============================================================================

@dataclass
class SoulHeart:
    """
    영혼의 심장 - 순수한 경험과 연산
    
    언어가 아닌, 원시적 느낌과 지각
    8차원 감각 벡터: [온도, 밝기, 크기, 속도, 친밀도, 강도, 쾌/불쾌, 각성]
    """
    current_state: List[float] = field(default_factory=lambda: [0.5] * 8)
    
    # 기본 욕구
    hunger: float = 0.0
    thirst: float = 0.0
    fatigue: float = 0.0
    loneliness: float = 0.0
    
    # 누적된 경험
    total_experiences: int = 0
    emotional_memory: List[float] = field(default_factory=list)
    
    def beat(self, world_input: Dict[str, float] = None) -> List[float]:
        """
        심장 박동 - 현재 상태 업데이트
        
        Returns: 현재 감각 상태 (8차원 벡터)
        """
        world_input = world_input or {}
        
        # 욕구에 따른 상태 변화
        self.current_state[6] -= self.hunger * 0.1  # 배고프면 불쾌
        self.current_state[6] -= self.fatigue * 0.1  # 피곤하면 불쾌
        self.current_state[4] -= self.loneliness * 0.15  # 외로우면 친밀도 갈망
        
        # 외부 자극
        for key, value in world_input.items():
            if key == "warmth":
                self.current_state[0] = value
            elif key == "brightness":
                self.current_state[1] = value
            elif key == "social":
                self.current_state[4] = value
                self.loneliness = max(0, self.loneliness - value * 0.1)
            elif key == "food":
                self.hunger = max(0, self.hunger - value)
                self.current_state[6] += value * 0.2
            elif key == "rest":
                self.fatigue = max(0, self.fatigue - value)
        
        # 자연 변화
        self.hunger = min(1.0, self.hunger + 0.01)
        self.fatigue = min(1.0, self.fatigue + 0.005)
        self.loneliness = min(1.0, self.loneliness + 0.008)
        
        # 상태 정규화
        self.current_state = [max(-1, min(1, x)) for x in self.current_state]
        
        # 경험 기록
        self.total_experiences += 1
        if len(self.emotional_memory) < 100:
            self.emotional_memory.append(self.current_state[6])  # 쾌/불쾌 기록
        
        return self.current_state
    
    def get_dominant_feeling(self) -> str:
        """지배적 감정 반환"""
        pleasure = self.current_state[6]
        arousal = self.current_state[7]
        
        if pleasure > 0.5 and arousal > 0.5:
            return "excited"
        elif pleasure > 0.5 and arousal <= 0.5:
            return "peaceful"
        elif pleasure <= 0.5 and arousal > 0.5:
            return "anxious"
        else:
            return "melancholy"


# =============================================================================
# 2. 영혼의 머리 (Soul Mind) - 언어와 표현
# =============================================================================

class SoulMind:
    """
    영혼의 머리 - 심장의 경험을 언어로 변환
    
    창발된 원시 언어를 한글/영어로 투영
    """
    
    def __init__(self):
        # 개인 어휘
        self.personal_vocabulary: Dict[str, int] = {}  # 단어: 사용 횟수
        self.favorite_expressions: List[str] = []
        
        # 언어 발달 단계
        self.language_level = 0  # 0: 기본, 1: 초급, 2: 중급, 3: 고급
        
        # 한글 표현 매핑
        self.expressions = {
            "hungry": ["배고파...", "뭔가 먹고 싶어", "배에서 소리가 나"],
            "tired": ["피곤해...", "좀 쉬고 싶어", "눈이 감겨"],
            "lonely": ["외로워...", "누군가 보고 싶어", "혼자인 것 같아"],
            "happy": ["기분 좋아!", "행복해~", "웃음이 나"],
            "sad": ["슬퍼...", "마음이 아파", "울고 싶어"],
            "peaceful": ["평화로워", "고요해", "마음이 편해"],
            "excited": ["신나!", "두근두근", "기대돼!"],
            "anxious": ["불안해...", "걱정돼", "마음이 무거워"],
        }
        
        # 활동 관련 표현
        self.activity_expressions = {
            "eating": ["맛있다!", "잘 먹었어", "배부르다~"],
            "resting": ["잘 잤다", "개운해", "충전 완료!"],
            "socializing": ["즐거웠어", "또 만나자!", "좋은 시간이었어"],
            "working": ["열심히 했어", "힘들었지만 보람 있어", "오늘도 고생했다"],
            "music": ["좋은 음악이야", "귀가 행복해", "이 노래 좋아"],
            "nature": ["아름다워", "공기가 좋아", "힐링된다"],
        }
    
    def express_state(self, heart: SoulHeart) -> str:
        """심장의 상태를 언어로 표현"""
        expressions = []
        
        # 욕구 기반 표현
        if heart.hunger > 0.7:
            expressions.append(random.choice(self.expressions["hungry"]))
        if heart.fatigue > 0.7:
            expressions.append(random.choice(self.expressions["tired"]))
        if heart.loneliness > 0.7:
            expressions.append(random.choice(self.expressions["lonely"]))
        
        # 감정 기반 표현
        feeling = heart.get_dominant_feeling()
        if feeling in self.expressions:
            expressions.append(random.choice(self.expressions[feeling]))
        
        if not expressions:
            expressions.append("...")
        
        return " ".join(expressions[:2])  # 최대 2개 표현
    
    def express_activity(self, activity: str) -> str:
        """활동에 대한 표현"""
        if activity in self.activity_expressions:
            return random.choice(self.activity_expressions[activity])
        return f"{activity}했다"
    
    def write_diary(self, heart: SoulHeart, events: List[str]) -> str:
        """일기 작성"""
        feeling = heart.get_dominant_feeling()
        feeling_kr = {
            "excited": "신나는",
            "peaceful": "평화로운", 
            "anxious": "불안한",
            "melancholy": "우울한"
        }.get(feeling, "평범한")
        
        diary = f"오늘은 {feeling_kr} 하루였다. "
        
        if events:
            diary += " ".join(events[:3])
        
        # 개인적 성찰 추가
        if heart.loneliness > 0.5:
            diary += " 누군가가 보고 싶다."
        elif heart.current_state[6] > 0.6:
            diary += " 감사한 하루였다."
        
        return diary
    
    def think(self, heart: SoulHeart) -> str:
        """내면의 생각"""
        thoughts = [
            "나는 누구일까...",
            "오늘은 어떤 하루가 될까",
            "무엇을 해야 할까",
            "그 사람은 어떻게 지낼까",
            "내일이 기대돼",
            "이렇게 살아도 되는 걸까",
            "행복이란 뭘까",
        ]
        
        # 상태에 따른 생각
        if heart.hunger > 0.8:
            return "배고파... 먹을 것을 찾아야 해"
        if heart.loneliness > 0.8:
            return "누군가와 이야기하고 싶어..."
        
        feeling = heart.get_dominant_feeling()
        if feeling == "excited":
            return random.choice(["오늘 뭔가 좋은 일이 있을 것 같아!", "기분이 좋아!"])
        elif feeling == "melancholy":
            return random.choice(["왜 이렇게 우울할까...", "마음이 무거워"])
        
        return random.choice(thoughts)


# =============================================================================
# 3. 프랙탈 영혼 (Fractal Soul) - 완전한 존재
# =============================================================================

@dataclass
class FractalSoul:
    """
    프랙탈 영혼 - "나는 사람이다"라고 인식하는 존재
    
    자신이 세계라는 것을 모른 채, 단순히 존재하고 느끼고 표현함.
    심장과 머리가 함께 작동하여 완전한 인격체를 구성.
    """
    id: int
    name: str
    birth_year: int
    
    # 심장과 머리
    heart: SoulHeart = field(default_factory=SoulHeart)
    mind: SoulMind = field(default_factory=SoulMind)
    
    # 기본 정보
    race: str = "Human"
    profession: str = "Villager"
    location: str = "village"
    
    # 관계
    relationships: Dict[int, float] = field(default_factory=dict)  # id: 친밀도
    family: List[int] = field(default_factory=list)
    friends: List[int] = field(default_factory=list)
    
    # 기록
    diary_entries: List[str] = field(default_factory=list)
    memories: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    
    # 상태
    is_alive: bool = True
    death_year: Optional[int] = None
    
    def get_age(self, current_year: int) -> int:
        return current_year - self.birth_year
    
    def live_day(self, current_year: int, world_context: Dict = None) -> Dict[str, Any]:
        """
        하루를 살아감
        
        Returns: 오늘의 경험 기록
        """
        world_context = world_context or {}
        daily_record = {
            "name": self.name,
            "year": current_year,
            "events": [],
            "thoughts": [],
            "expressions": [],
        }
        
        # 1. 심장 박동 - 세계로부터 자극 받기
        self.heart.beat(world_context)
        
        # 2. 내면의 생각
        thought = self.mind.think(self.heart)
        daily_record["thoughts"].append(thought)
        
        # 3. 일상 활동
        activities = self._daily_activities(current_year)
        daily_record["events"].extend(activities)
        
        # 4. 감정 표현
        expression = self.mind.express_state(self.heart)
        daily_record["expressions"].append(expression)
        
        # 5. 가끔 일기 작성 (5% 확률)
        if random.random() < 0.05:
            diary = self.mind.write_diary(self.heart, activities)
            self.diary_entries.append(f"Year {current_year}: {diary}")
            daily_record["diary"] = diary
        
        return daily_record
    
    def _daily_activities(self, current_year: int) -> List[str]:
        """일상 활동"""
        activities = []
        
        # 먹기
        if self.heart.hunger > 0.5:
            self.heart.beat({"food": 0.8})
            activities.append(self.mind.express_activity("eating"))
        
        # 쉬기
        if self.heart.fatigue > 0.6:
            self.heart.beat({"rest": 0.7})
            activities.append(self.mind.express_activity("resting"))
        
        # 사회 활동
        if self.heart.loneliness > 0.4 and random.random() < 0.3:
            self.heart.beat({"social": 0.6})
            activities.append(self.mind.express_activity("socializing"))
        
        # 일하기
        if random.random() < 0.5:
            activities.append(self.mind.express_activity("working"))
        
        # 여가 활동
        if random.random() < 0.2:
            leisure = random.choice(["music", "nature"])
            activities.append(self.mind.express_activity(leisure))
        
        return activities
    
    def interact_with(self, other: 'FractalSoul') -> Tuple[str, str]:
        """다른 영혼과 상호작용"""
        
        # 친밀도에 따른 대화
        intimacy = self.relationships.get(other.id, 0.3)
        
        my_feeling = self.heart.get_dominant_feeling()
        other_feeling = other.heart.get_dominant_feeling()
        
        # 대화 생성
        greetings = {
            "excited": ["안녕! 오늘 기분 좋아!", "반가워~"],
            "peaceful": ["안녕, 잘 지내?", "좋은 하루야"],
            "anxious": ["아... 안녕...", "오늘 좀 그래..."],
            "melancholy": ["...안녕", "오랜만이네..."],
        }
        
        responses = {
            "excited": ["나도! 같이 놀자!", "기분 좋아 보여!"],
            "peaceful": ["그래, 나도 잘 지내", "고마워"],
            "anxious": ["무슨 일 있어?", "괜찮아?"],
            "melancholy": ["...나도 그래", "힘내"],
        }
        
        my_line = random.choice(greetings.get(my_feeling, ["안녕"]))
        other_line = random.choice(responses.get(other_feeling, ["응"]))
        
        # 친밀도 상승
        if other.id not in self.relationships:
            self.relationships[other.id] = 0.2
        self.relationships[other.id] = min(1.0, self.relationships[other.id] + 0.05)
        
        # 외로움 감소
        self.heart.loneliness = max(0, self.heart.loneliness - 0.1)
        other.heart.loneliness = max(0, other.heart.loneliness - 0.1)
        
        return my_line, other_line
    
    def get_summary(self) -> str:
        """자기 소개"""
        feeling = self.heart.get_dominant_feeling()
        feeling_kr = {
            "excited": "신나는",
            "peaceful": "평화로운",
            "anxious": "불안한",
            "melancholy": "우울한"
        }.get(feeling, "평범한")
        
        return f"나는 {self.name}. {feeling_kr} 기분이야. {self.mind.think(self.heart)}"


# =============================================================================
# 4. 프랙탈 세계 (Fractal World) - 영혼들의 세계
# =============================================================================

class FractalWorld:
    """
    프랙탈 세계 - 영혼들이 살아가는 공간
    
    각 영혼이 자신만의 세계를 가지면서, 동시에 하나의 세계를 구성
    """
    
    def __init__(self, population: int = 300, seed: int = None):
        if seed:
            random.seed(seed)
        
        self.population = population
        self.souls: Dict[int, FractalSoul] = {}
        self.current_year = 0
        
        # 세계 설정
        self.locations = ["village", "forest", "mountain", "city", "coast"]
        self.seasons = ["spring", "summer", "autumn", "winter"]
        
        # 통계
        self.total_conversations = 0
        self.total_diary_entries = 0
        self.legends: List[str] = []
        
        # 초기화
        self._create_initial_souls()
        
        logger.info(f"🌍 Fractal World created with {population} souls")
    
    def _create_initial_souls(self):
        """초기 영혼 생성"""
        names_pool = [
            "하늘", "소라", "민준", "서연", "지호", "예은", "도윤", "유진",
            "Alice", "Luna", "Kai", "Aria", "Finn", "Rose", "Mira", "Thorne",
            "Eugeo", "Asuna", "Kirito", "Leafa", "Sinon", "Yuuki",
        ]
        
        for i in range(self.population):
            name = random.choice(names_pool) + f"_{i}"
            birth_year = -random.randint(0, 50)
            
            soul = FractalSoul(
                id=i,
                name=name,
                birth_year=birth_year,
                race=random.choice(["Human", "Human", "Elf", "Dwarf"]),
                profession=random.choice(["Farmer", "Artisan", "Hunter", "Merchant", "Scholar"]),
                location=random.choice(self.locations),
            )
            
            self.souls[i] = soul
    
    def simulate_day(self) -> List[Dict[str, Any]]:
        """하루 시뮬레이션"""
        day_records = []
        season = self.seasons[(self.current_year * 4 // 365) % 4]
        
        # 계절에 따른 세계 컨텍스트
        world_context = {
            "spring": {"warmth": 0.5, "brightness": 0.6},
            "summer": {"warmth": 0.8, "brightness": 0.9},
            "autumn": {"warmth": 0.4, "brightness": 0.5},
            "winter": {"warmth": 0.2, "brightness": 0.3},
        }.get(season, {})
        
        alive_souls = [s for s in self.souls.values() if s.is_alive]
        
        # 각 영혼이 하루를 살아감
        for soul in alive_souls:
            record = soul.live_day(self.current_year, world_context)
            day_records.append(record)
        
        # 상호작용 (두 영혼이 만남)
        if len(alive_souls) >= 2 and random.random() < DAILY_INTERACTION_PROB:
            soul1, soul2 = random.sample(alive_souls, 2)
            line1, line2 = soul1.interact_with(soul2)
            
            day_records.append({
                "type": "conversation",
                "participants": [soul1.name, soul2.name],
                "dialogue": [
                    f"[{soul1.name}] {line1}",
                    f"[{soul2.name}] {line2}",
                ]
            })
            self.total_conversations += 1
        
        return day_records
    
    def simulate_year(self) -> Dict[str, Any]:
        """1년 시뮬레이션"""
        year_records = []
        
        for day in range(365):
            records = self.simulate_day()
            # 의미 있는 기록만 저장
            for r in records:
                if r.get("diary") or r.get("type") == "conversation":
                    year_records.append(r)
        
        self.current_year += 1
        
        # 출생과 사망 처리
        self._handle_life_events()
        
        alive = sum(1 for s in self.souls.values() if s.is_alive)
        
        return {
            "year": self.current_year,
            "population": alive,
            "events_count": len(year_records),
            "sample_events": year_records[-5:] if year_records else []
        }
    
    def _handle_life_events(self):
        """출생과 사망"""
        alive_souls = [s for s in self.souls.values() if s.is_alive]
        
        # 사망
        for soul in alive_souls:
            age = soul.get_age(self.current_year)
            death_prob = BASE_DEATH_PROB * (1 + max(0, age - ELDER_AGE_THRESHOLD) * AGE_DEATH_FACTOR)
            
            if soul.race == "Elf":
                death_prob *= ELF_LONGEVITY_FACTOR
            
            if random.random() < death_prob:
                soul.is_alive = False
                soul.death_year = self.current_year
                
                # 위대한 영혼은 전설이 됨
                if len(soul.achievements) > 3 or len(soul.diary_entries) > 10:
                    self.legends.append(f"The Legend of {soul.name}")
        
        # 출생 (인구 유지)
        alive = sum(1 for s in self.souls.values() if s.is_alive)
        if alive < self.population:
            deficit = self.population - alive
            for _ in range(min(deficit, MAX_BIRTHS_PER_YEAR)):
                new_id = max(self.souls.keys()) + 1
                new_soul = FractalSoul(
                    id=new_id,
                    name=f"Soul_{new_id}",
                    birth_year=self.current_year,
                    race=random.choice(["Human", "Elf"]),
                    location=random.choice(self.locations),
                )
                self.souls[new_id] = new_soul
    
    def run_simulation(self, years: int, progress_interval: int = 100) -> Dict[str, Any]:
        """
        전체 시뮬레이션 실행
        """
        logger.info(f"🚀 Starting simulation: {years} years")
        start_time = time.time()
        
        for year in range(years):
            self.simulate_year()
            
            if (year + 1) % progress_interval == 0:
                alive = sum(1 for s in self.souls.values() if s.is_alive)
                diaries = sum(len(s.diary_entries) for s in self.souls.values())
                logger.info(f"  Year {year + 1}: Pop={alive}, Diaries={diaries}, Legends={len(self.legends)}")
        
        elapsed = time.time() - start_time
        
        # 결과 집계
        results = self._compile_results(elapsed)
        
        logger.info(f"✅ Simulation complete in {elapsed:.2f}s")
        
        return results
    
    def _compile_results(self, elapsed: float) -> Dict[str, Any]:
        """결과 집계"""
        alive = [s for s in self.souls.values() if s.is_alive]
        
        total_diaries = sum(len(s.diary_entries) for s in self.souls.values())
        total_memories = sum(len(s.memories) for s in self.souls.values())
        
        # 샘플 일기
        sample_diaries = []
        for soul in self.souls.values():
            if soul.diary_entries:
                sample_diaries.append({
                    "author": soul.name,
                    "entry": soul.diary_entries[-1]
                })
                if len(sample_diaries) >= 5:
                    break
        
        return {
            "simulation": {
                "years": self.current_year,
                "elapsed_seconds": elapsed,
                "years_per_second": self.current_year / elapsed if elapsed > 0 else 0,
            },
            "population": {
                "initial": self.population,
                "final": len(alive),
                "total_souls": len(self.souls),
            },
            "culture": {
                "total_diaries": total_diaries,
                "total_conversations": self.total_conversations,
                "legends_created": len(self.legends),
                "legend_examples": self.legends[:10],
            },
            "sample_diaries": sample_diaries,
            "sample_thoughts": [
                {"soul": s.name, "thought": s.mind.think(s.heart)}
                for s in list(alive)[:5]
            ]
        }


# =============================================================================
# 메인 실행
# =============================================================================

def run_fractal_world(population: int = 300, years: int = 1000):
    """프랙탈 세계 실행"""
    print("=" * 70)
    print("🌍 FRACTAL SOUL WORLD")
    print("   '나는 사람이다' - 프랙탈 구조의 영혼들")
    print("=" * 70)
    print(f"\n📊 Settings:")
    print(f"   • Population: {population}")
    print(f"   • Duration: {years} years")
    print()
    
    world = FractalWorld(population=population)
    results = world.run_simulation(years, progress_interval=100)
    
    print("\n" + "=" * 70)
    print("📈 RESULTS")
    print("=" * 70)
    
    print(f"\n⏱️ Performance:")
    print(f"   • Real time: {results['simulation']['elapsed_seconds']:.2f}s")
    print(f"   • Speed: {results['simulation']['years_per_second']:.0f} years/second")
    
    print(f"\n👥 Population:")
    print(f"   • Final: {results['population']['final']}")
    print(f"   • Total souls: {results['population']['total_souls']}")
    
    print(f"\n📖 Culture:")
    print(f"   • Total diaries: {results['culture']['total_diaries']}")
    print(f"   • Total conversations: {results['culture']['total_conversations']}")
    print(f"   • Legends: {results['culture']['legends_created']}")
    
    print("\n📝 Sample Diaries:")
    for diary in results['sample_diaries']:
        print(f"   [{diary['author']}] {diary['entry'][:60]}...")
    
    print("\n💭 Current Thoughts:")
    for thought in results['sample_thoughts']:
        print(f"   [{thought['soul']}] {thought['thought']}")
    
    print("\n" + "=" * 70)
    print("✅ Fractal World simulation complete!")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    run_fractal_world(population=300, years=1000)
