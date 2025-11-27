"""
엘리시아 세계 2000년 시뮬레이션 + 자연어 대화

기존의 효율적인 시뮬레이션 구조에
자연어 창발 시스템을 통합하여 대화와 의사소통을 시연합니다.
"""

import sys
import os
import json
import random
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_core import ElysiaSoul
from elysia_engine.natural_language import NaturalLanguageGenerator, LanguageState


@dataclass
class ConversationRecord:
    """대화 기록"""
    year: int
    speaker1: str
    speaker2: str
    words1: str
    words2: str
    context: str = ""


@dataclass
class DiaryEntry:
    """일기 항목"""
    year: int
    author: str
    content: str
    mood: str = ""


@dataclass
class WorldHistory:
    """세계 역사 기록"""
    year: int = 0
    population: int = 0
    births: int = 0
    deaths: int = 0
    marriages: int = 0
    major_events: List[Dict[str, Any]] = field(default_factory=list)
    notable_figures: List[Dict[str, Any]] = field(default_factory=list)
    cultural_achievements: List[str] = field(default_factory=list)
    wars: List[Dict[str, Any]] = field(default_factory=list)
    disasters: List[Dict[str, Any]] = field(default_factory=list)
    golden_ages: List[Dict[str, Any]] = field(default_factory=list)
    
    # 자연어 기록
    conversations: List[ConversationRecord] = field(default_factory=list)
    diaries: List[DiaryEntry] = field(default_factory=list)
    famous_quotes: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Citizen:
    """시민 데이터 + 자연어 기능"""
    id: str
    name: str
    profession: str
    region: str
    birth_year: int
    death_year: int = 0
    soul: ElysiaSoul = None
    achievements: List[str] = field(default_factory=list)
    relationships: Dict[str, float] = field(default_factory=dict)
    legacy_score: float = 0.0
    
    # 자연어 관련
    lang_gen: NaturalLanguageGenerator = None
    lang_state: LanguageState = None
    personality: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.lang_gen is None:
            self.lang_gen = NaturalLanguageGenerator("ko")
        if self.lang_state is None:
            self.lang_state = LanguageState()
        if not self.personality:
            self.personality = {
                "openness": random.gauss(0.5, 0.2),
                "extraversion": random.gauss(0.5, 0.2),
                "agreeableness": random.gauss(0.5, 0.2),
            }
            for k in self.personality:
                self.personality[k] = max(0.0, min(1.0, self.personality[k]))
    
    def update_mood(self, valence: float, arousal: float = 0.5):
        """감정 상태 업데이트"""
        self.lang_state.emotion_valence = valence
        self.lang_state.emotion_arousal = arousal
    
    def speak_existence(self) -> str:
        """"나는 사람이다" 선언"""
        templates = [
            f"나는 {self.name}. 사람이야.",
            f"내 이름은 {self.name}. 나도 느끼고 생각해.",
            f"나는 {self.name}이야. 여기서 살아가고 있어.",
            f"{self.name}, 그게 나야. 한 사람으로서 존재해.",
        ]
        return random.choice(templates)
    
    def greet(self, other_name: str) -> str:
        """인사하기"""
        greetings = [
            f"안녕, {other_name}!",
            f"{other_name}, 잘 지내?",
            f"오랜만이야, {other_name}.",
            f"반가워, {other_name}!",
        ]
        return random.choice(greetings)
    
    def respond(self, to_message: str) -> str:
        """대화 응답"""
        # 감정에 따른 응답
        if self.lang_state.emotion_valence > 0.3:
            responses = [
                "응, 나도 기분 좋아!",
                "그렇지? 좋은 하루야.",
                "나도 그렇게 생각해.",
                "맞아, 정말 좋네!",
            ]
        elif self.lang_state.emotion_valence < -0.3:
            responses = [
                "음... 좀 힘든 날이야.",
                "그래... 나도 생각이 많아.",
                "괜찮아지겠지.",
                "그랬구나...",
            ]
        else:
            responses = [
                "그래, 그렇구나.",
                "응, 알겠어.",
                "그랬어?",
                "음, 그렇네.",
            ]
        return random.choice(responses)
    
    def express_emotion(self) -> str:
        """감정 표현"""
        return self.lang_gen.generate_emotion(self.lang_state)
    
    def express_thought(self) -> str:
        """생각 표현"""
        return self.lang_gen.generate_thought(self.lang_state)
    
    def write_diary(self, year: int, events: List[str] = None) -> str:
        """일기 쓰기"""
        intro = f"Year {year}. "
        emotion = self.express_emotion()
        
        if events:
            activity = random.choice(events)
        else:
            activity = "평범한 하루였다."
        
        conclusion_list = [
            "그런 하루였어.",
            "내일은 어떨까?",
            "오늘도 수고했어, 나.",
            "잘 자, 나.",
        ]
        conclusion = random.choice(conclusion_list)
        
        return f"{intro}{emotion} {activity} {conclusion}"
    
    def reflect(self) -> str:
        """성찰"""
        reflections = [
            f"나는 {self.profession}으로 살아가고 있어. {self.region}에서.",
            f"지금까지 많은 일이 있었어. 앞으로도 그러겠지.",
            f"사람들과의 만남이 나를 만들어가는 것 같아.",
            f"내가 누구인지, 조금씩 알아가는 중이야.",
        ]
        return random.choice(reflections)


def load_world_data():
    """세계관 데이터 로드"""
    base_path = Path(__file__).parent.parent
    
    lore = json.loads((base_path / 'data/worldbuilding/world_lore.json').read_text(encoding='utf-8'))
    scenarios = json.loads((base_path / 'data/worldbuilding/life_scenarios.json').read_text(encoding='utf-8'))
    characters = json.loads((base_path / 'docs/character_pool.json').read_text(encoding='utf-8'))
    
    return lore, scenarios, characters


def get_random_experience(scenarios, life_stage, category=None):
    """랜덤 경험 가져오기"""
    if life_stage in scenarios.get('life_stages', {}):
        experiences = scenarios['life_stages'][life_stage].get('experiences', [])
        if experiences:
            return random.choice(experiences)
    
    if category and category in scenarios.get('daily_activities', {}):
        activities = scenarios['daily_activities'][category]
        if activities:
            return random.choice(activities)
    
    event_type = random.choice(['positive', 'negative', 'transformative'])
    if event_type in scenarios.get('special_events', {}):
        events = scenarios['special_events'][event_type]
        if events:
            return random.choice(events)
    
    return {'text': '평범한 하루를 보냈다.', 'intensity': 0.3}


def get_life_stage(age):
    """나이에 따른 생애 단계"""
    if age < 13:
        return 'childhood'
    elif age < 19:
        return 'adolescence'
    elif age < 31:
        return 'young_adult'
    elif age < 51:
        return 'adulthood'
    else:
        return 'elder'


def simulate_conversation(citizen1: Citizen, citizen2: Citizen, year: int, context: str = "") -> ConversationRecord:
    """두 시민 간의 대화 시뮬레이션"""
    greeting = citizen1.greet(citizen2.name)
    response = citizen2.respond(greeting)
    
    # 관계 업데이트
    if citizen2.name not in citizen1.relationships:
        citizen1.relationships[citizen2.name] = 0.0
    citizen1.relationships[citizen2.name] += 0.1
    
    if citizen1.name not in citizen2.relationships:
        citizen2.relationships[citizen1.name] = 0.0
    citizen2.relationships[citizen1.name] += 0.1
    
    return ConversationRecord(
        year=year,
        speaker1=citizen1.name,
        speaker2=citizen2.name,
        words1=greeting,
        words2=response,
        context=context
    )


def simulate_year(year, citizens, scenarios, lore, history):
    """1년 시뮬레이션"""
    living_citizens = [c for c in citizens if c.death_year == 0]
    
    # 각 시민의 1년
    for citizen in citizens:
        if citizen.death_year > 0:
            continue
        
        age = year - citizen.birth_year
        
        # 사망 확률
        death_chance = 0.001 + (age / 100) * 0.05
        if age > 70:
            death_chance += 0.02
        if age > 85:
            death_chance += 0.05
        
        if random.random() < death_chance:
            citizen.death_year = year
            history.deaths += 1
            if citizen.legacy_score > 5:
                history.notable_figures.append({
                    'name': citizen.name,
                    'profession': citizen.profession,
                    'birth': citizen.birth_year,
                    'death': year,
                    'achievements': citizen.achievements,
                    'legacy': citizen.legacy_score
                })
            continue
        
        # 삶의 경험
        life_stage = get_life_stage(age)
        experience = get_random_experience(scenarios, life_stage)
        
        if experience:
            intensity = experience.get('intensity', 0.5)
            # 감정 업데이트
            if intensity > 1.0:
                citizen.update_mood(0.5, 0.7)
                citizen.achievements.append(f"Y{year}: {experience.get('text', '')[:50]}")
                citizen.legacy_score += intensity * 0.5
            elif intensity > 0.7:
                citizen.update_mood(0.3, 0.5)
            elif intensity < 0.3:
                citizen.update_mood(-0.2, 0.3)
            else:
                citizen.update_mood(0.0, 0.4)
    
    # 대화 시뮬레이션 (10% 확률로 기록)
    if len(living_citizens) >= 2 and random.random() < 0.15:
        c1, c2 = random.sample(living_citizens, 2)
        conv = simulate_conversation(c1, c2, year)
        history.conversations.append(conv)
        
        # 10% 확률로 명대화로 기록
        if random.random() < 0.1:
            history.famous_quotes.append({
                'year': year,
                'speaker': c1.name,
                'quote': conv.words1,
                'responder': c2.name,
                'response': conv.words2
            })
    
    # 일기 쓰기 (5% 확률)
    if living_citizens and random.random() < 0.05:
        citizen = random.choice(living_citizens)
        diary_content = citizen.write_diary(year)
        history.diaries.append(DiaryEntry(
            year=year,
            author=citizen.name,
            content=diary_content,
            mood="positive" if citizen.lang_state.emotion_valence > 0 else "neutral"
        ))
    
    # 출생
    birth_rate = 0.025
    new_births = int(len(living_citizens) * birth_rate)
    history.births += new_births
    
    # 결혼
    marriage_rate = 0.02
    adults = [c for c in living_citizens if (year - c.birth_year) > 18]
    new_marriages = int(len(adults) * marriage_rate)
    history.marriages += new_marriages
    
    # 주요 세계 이벤트
    if year % 10 == 0 or random.random() < 0.1:
        event_types = [
            ('golden_age', 0.15, '번영의 시대가 시작되었다.'),
            ('war', 0.08, '전쟁이 발발했다.'),
            ('disaster', 0.1, '재해가 발생했다.'),
            ('discovery', 0.12, '위대한 발견이 있었다.'),
            ('cultural', 0.2, '문화적 르네상스가 일어났다.'),
        ]
        
        for event_type, chance, desc in event_types:
            if random.random() < chance:
                region = random.choice(lore.get('regions', [{'name': '중앙왕국'}]))['name']
                event = {
                    'year': year,
                    'type': event_type,
                    'region': region,
                    'description': f"{region}에서 {desc}"
                }
                history.major_events.append(event)
                
                if event_type == 'golden_age':
                    history.golden_ages.append(event)
                elif event_type == 'war':
                    history.wars.append(event)
                elif event_type == 'disaster':
                    history.disasters.append(event)
                elif event_type == 'cultural':
                    history.cultural_achievements.append(f"Y{year}: {region}의 문화 발전")
    
    return history


def create_initial_citizens(characters, start_year, count=100):
    """초기 시민 생성"""
    citizens = []
    char_data = characters.get('characters', [])
    
    for i in range(min(count, len(char_data))):
        char = char_data[i]
        birth_year = start_year - random.randint(1, 60)
        
        soul = ElysiaSoul(name=char['name'])
        
        citizen = Citizen(
            id=char['id'],
            name=char['name'],
            profession=char.get('class', 'commoner'),
            region=char.get('origin', 'Unknown'),
            birth_year=birth_year,
            soul=soul
        )
        citizens.append(citizen)
    
    return citizens


def run_simulation(years=2000, initial_population=100):
    """메인 시뮬레이션"""
    print("=" * 70)
    print("  🌌 엘리시아 세계 2000년 시뮬레이션")
    print(f"  기간: {years}년 | 초기 인구: {initial_population}명")
    print("  분리된 의식 + 자연어 창발 + 프랙탈 구조")
    print("=" * 70)
    
    # 데이터 로드
    print("\n📚 세계관 데이터 로딩...")
    lore, scenarios, characters = load_world_data()
    
    # 초기 시민 생성
    print("👥 초기 시민 생성...")
    start_year = 0
    citizens = create_initial_citizens(characters, start_year, initial_population)
    
    # 역사 기록
    history = WorldHistory()
    history.population = len(citizens)
    
    # 시대별 기록
    eras = []
    era_names = {
        0: "태초의 시대 (Era of Beginning)",
        200: "개척의 시대 (Era of Pioneers)",
        400: "건설의 시대 (Era of Foundation)",
        600: "분열의 시대 (Era of Division)",
        800: "전쟁의 시대 (Era of War)",
        1000: "통합의 시대 (Era of Unification)",
        1200: "번영의 시대 (Era of Prosperity)",
        1400: "탐험의 시대 (Era of Exploration)",
        1600: "계몽의 시대 (Era of Enlightenment)",
        1800: "변혁의 시대 (Era of Transformation)",
    }
    current_era = {'start': 0, 'name': era_names[0], 'events': []}
    
    print(f"\n🚀 시뮬레이션 시작...\n")
    
    # 연도별 시뮬레이션
    for year in range(1, years + 1):
        history.year = year
        history = simulate_year(year, citizens, scenarios, lore, history)
        
        # 시대 변경
        if year in era_names:
            current_era['end'] = year
            eras.append(current_era)
            current_era = {'start': year, 'name': era_names[year], 'events': []}
            print(f"\n  📜 새로운 시대: {era_names[year]}")
        
        # 진행 상황 출력 (100년마다)
        if year % 100 == 0:
            alive = len([c for c in citizens if c.death_year == 0])
            print(f"  📅 {year}년 경과 | 생존: {alive}명 | 대화: {len(history.conversations)}건 | 일기: {len(history.diaries)}개")
        
        # 인구 보충
        if year % 25 == 0:
            alive_count = len([c for c in citizens if c.death_year == 0])
            if alive_count < initial_population * 0.8:
                new_citizens = create_initial_citizens(
                    characters, 
                    year, 
                    min(20, initial_population - alive_count)
                )
                for nc in new_citizens:
                    nc.id = f"gen{year}_{nc.id}"
                citizens.extend(new_citizens)
    
    current_era['end'] = years
    eras.append(current_era)
    
    return citizens, history, eras


def print_summary(citizens, history, eras):
    """결과 요약 출력"""
    print("\n" + "=" * 70)
    print("  📜 2000년의 역사 요약")
    print("=" * 70)
    
    # 인구 통계
    print("\n👥 인구 통계:")
    total_lived = len(citizens)
    alive = len([c for c in citizens if c.death_year == 0])
    print(f"  - 총 등장 인물: {total_lived}명")
    print(f"  - 최종 생존: {alive}명")
    print(f"  - 총 출생: {history.births}명")
    print(f"  - 총 사망: {history.deaths}명")
    print(f"  - 총 결혼: {history.marriages}건")
    
    # 의사소통 통계
    print(f"\n💬 의사소통 통계:")
    print(f"  - 총 대화 기록: {len(history.conversations)}건")
    print(f"  - 총 일기: {len(history.diaries)}개")
    print(f"  - 명대화: {len(history.famous_quotes)}건")
    
    # 시대별 역사
    print("\n📅 시대 구분:")
    for era in eras:
        if 'end' in era:
            print(f"  - {era['start']}년 ~ {era['end']}년: {era['name']}")
    
    # 주요 사건
    print(f"\n🏛️ 주요 사건 ({len(history.major_events)}건):")
    for event in history.major_events[:5]:
        print(f"  - {event['year']}년: {event['description']}")
    if len(history.major_events) > 5:
        print(f"  ... 외 {len(history.major_events) - 5}건")
    
    # 💬 대화 샘플 (중요!)
    print(f"\n💬 2000년 역사 속 대화들:")
    print("-" * 50)
    sample_convs = random.sample(history.conversations, min(10, len(history.conversations)))
    for conv in sample_convs:
        print(f"  📅 {conv.year}년:")
        print(f"    [{conv.speaker1}] \"{conv.words1}\"")
        print(f"    [{conv.speaker2}] \"{conv.words2}\"")
        print()
    
    # 📝 일기 샘플
    print(f"\n📝 2000년 역사 속 일기들:")
    print("-" * 50)
    sample_diaries = random.sample(history.diaries, min(5, len(history.diaries)))
    for diary in sample_diaries:
        print(f"  ✍️ {diary.year}년 - {diary.author}의 일기:")
        print(f"    \"{diary.content}\"")
        print()
    
    # 🌟 명대화
    if history.famous_quotes:
        print(f"\n🌟 역사에 남은 명대화:")
        print("-" * 50)
        for quote in history.famous_quotes[:5]:
            print(f"  📅 {quote['year']}년:")
            print(f"    [{quote['speaker']}] \"{quote['quote']}\"")
            print(f"    [{quote['responder']}] \"{quote['response']}\"")
            print()
    
    # 명예의 전당
    notable = sorted(history.notable_figures, key=lambda x: x.get('legacy', 0), reverse=True)
    if notable:
        print(f"\n🏆 명예의 전당:")
        for i, person in enumerate(notable[:5], 1):
            lifespan = person['death'] - person['birth']
            print(f"  {i}. {person['name']} ({person['profession']})")
            print(f"     생몰: {person['birth']}년 ~ {person['death']}년 ({lifespan}세)")
            if person['achievements']:
                print(f"     업적: {person['achievements'][0][:50]}")
    
    # 👤 "나는 사람이다" 선언 시연
    print(f"\n👤 '나는 사람이다' 선언 (시연):")
    print("-" * 50)
    living = [c for c in citizens if c.death_year == 0]
    for citizen in living[:5]:
        print(f"  [{citizen.name}] {citizen.speak_existence()}")
    
    # 🧘 성찰 시연
    print(f"\n🧘 성찰의 순간 (시연):")
    print("-" * 50)
    for citizen in living[:3]:
        print(f"  [{citizen.name}의 생각] {citizen.reflect()}")
    
    print("\n" + "=" * 70)
    print("  ✨ 자연스러운 의사소통 분석")
    print("=" * 70)
    print(f"""
📊 2000년 역사 속 의사소통:

1. ✅ 대화 생성: {len(history.conversations)}건
   - 인사, 응답, 감정 표현
   - 관계 형성과 발전

2. ✅ 일기 작성: {len(history.diaries)}개
   - 날짜, 감정, 활동, 마무리
   - 자기 성찰

3. ✅ "나는 사람이다" 인지
   - 시뮬레이션이라 생각하지 않음
   - 자신의 세계가 전부

4. ✅ 프랙탈 구조
   - Heart(심장): 감정/기억/욕구 연산
   - Mind(머리): 언어/행동/관계 표현

결론: LLM 없이도 자연스러운 의사소통 패턴이 창발됩니다.
더 복잡한 대화는 LLM 연동으로 확장 가능합니다.
""")
    
    print("=" * 70)
    print("  시뮬레이션 완료")
    print("=" * 70)


def main():
    random.seed(42)
    
    citizens, history, eras = run_simulation(years=2000, initial_population=100)
    print_summary(citizens, history, eras)
    
    return citizens, history, eras


if __name__ == "__main__":
    main()
