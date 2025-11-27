"""
엘리시아 세계 1000년 시뮬레이션

가상세계 주민들이 1000년 동안 어떤 삶을 살았는지 시뮬레이션합니다.
"""

import sys
import os
import json
import random
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_core import ElysiaSoul


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


@dataclass
class Citizen:
    """시민 데이터"""
    id: str
    name: str
    profession: str
    region: str
    birth_year: int
    death_year: int = 0
    soul: ElysiaSoul = None
    achievements: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)
    legacy_score: float = 0.0


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
    
    # 특별 이벤트
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


def simulate_year(year, citizens, scenarios, lore, history):
    """1년 시뮬레이션"""
    year_events = []
    
    # 각 시민의 1년
    for citizen in citizens:
        if citizen.death_year > 0:
            continue  # 이미 사망
        
        age = year - citizen.birth_year
        
        # 사망 확률 (나이에 따라 증가)
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
        
        if citizen.soul and experience:
            thought = citizen.soul.process(experience.get('text', ''))
            
            # 특별한 경험은 업적으로 기록
            intensity = experience.get('intensity', 0.5)
            if intensity > 1.0:
                citizen.achievements.append(f"Y{year}: {experience.get('text', '')[:50]}")
                citizen.legacy_score += intensity * 0.5
    
    # 출생 (인구 유지를 위해)
    birth_rate = 0.025  # 2.5%
    new_births = int(len([c for c in citizens if c.death_year == 0]) * birth_rate)
    history.births += new_births
    
    # 결혼
    marriage_rate = 0.02
    new_marriages = int(len([c for c in citizens if c.death_year == 0 and (year - c.birth_year) > 18]) * marriage_rate)
    history.marriages += new_marriages
    
    # 주요 세계 이벤트 (10년마다 또는 랜덤)
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
        birth_year = start_year - random.randint(1, 60)  # 1~60세
        
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


def run_simulation(years=1000, initial_population=100):
    """메인 시뮬레이션"""
    print("=" * 70)
    print("  엘리시아 세계 시뮬레이션")
    print(f"  기간: {years}년 | 초기 인구: {initial_population}명")
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
    current_era = {'start': 0, 'name': '태초의 시대', 'events': []}
    
    print(f"\n🚀 시뮬레이션 시작...\n")
    
    # 연도별 시뮬레이션
    for year in range(1, years + 1):
        history.year = year
        history = simulate_year(year, citizens, scenarios, lore, history)
        
        # 진행 상황 출력 (100년마다)
        if year % 100 == 0:
            alive = len([c for c in citizens if c.death_year == 0])
            print(f"  📅 {year}년 경과 | 생존 인구: {alive}명 | 주요 사건: {len(history.major_events)}개")
            
            # 새 시대 시작
            if year % 250 == 0:
                era_names = ['개척의 시대', '성장의 시대', '번영의 시대', '혼란의 시대', '재건의 시대']
                current_era['end'] = year
                eras.append(current_era)
                current_era = {
                    'start': year,
                    'name': random.choice(era_names),
                    'events': []
                }
        
        # 인구 보충 (세대 교체)
        if year % 25 == 0:
            alive_count = len([c for c in citizens if c.death_year == 0])
            if alive_count < initial_population * 0.8:
                # 새 세대 추가
                new_citizens = create_initial_citizens(
                    characters, 
                    year, 
                    min(20, initial_population - alive_count)
                )
                for nc in new_citizens:
                    nc.id = f"gen{year}_{nc.id}"
                citizens.extend(new_citizens)
    
    # 마지막 시대 종료
    current_era['end'] = years
    eras.append(current_era)
    
    return citizens, history, eras


def print_summary(citizens, history, eras):
    """결과 요약 출력"""
    print("\n" + "=" * 70)
    print("  📜 1000년의 역사 요약")
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
    
    # 시대별 역사
    print("\n📅 시대 구분:")
    for era in eras:
        if 'end' in era:
            print(f"  - {era['start']}년 ~ {era['end']}년: {era['name']}")
    
    # 주요 사건
    print(f"\n🏛️ 주요 사건 ({len(history.major_events)}건):")
    for event in history.major_events[:10]:
        print(f"  - {event['year']}년: {event['description']}")
    if len(history.major_events) > 10:
        print(f"  ... 외 {len(history.major_events) - 10}건")
    
    # 전쟁
    if history.wars:
        print(f"\n⚔️ 전쟁 ({len(history.wars)}건):")
        for war in history.wars[:5]:
            print(f"  - {war['year']}년: {war['description']}")
    
    # 재해
    if history.disasters:
        print(f"\n🌋 재해 ({len(history.disasters)}건):")
        for disaster in history.disasters[:5]:
            print(f"  - {disaster['year']}년: {disaster['description']}")
    
    # 황금기
    if history.golden_ages:
        print(f"\n✨ 번영의 시대 ({len(history.golden_ages)}건):")
        for golden in history.golden_ages[:5]:
            print(f"  - {golden['year']}년: {golden['description']}")
    
    # 문화 업적
    if history.cultural_achievements:
        print(f"\n🎨 문화적 성취 ({len(history.cultural_achievements)}건):")
        for ach in history.cultural_achievements[:5]:
            print(f"  - {ach}")
    
    # 명예의 전당 (가장 영향력 있던 인물들)
    notable = sorted(history.notable_figures, key=lambda x: x.get('legacy', 0), reverse=True)
    if notable:
        print(f"\n🏆 명예의 전당 (가장 영향력 있던 인물들):")
        for i, person in enumerate(notable[:10], 1):
            lifespan = person['death'] - person['birth']
            print(f"  {i}. {person['name']} ({person['profession']})")
            print(f"     생몰: {person['birth']}년 ~ {person['death']}년 ({lifespan}세)")
            if person['achievements']:
                print(f"     업적: {person['achievements'][0]}")
    
    # 직업 분포
    professions = Counter(c.profession for c in citizens)
    print(f"\n💼 직업 분포 (상위 10개):")
    for prof, count in professions.most_common(10):
        print(f"  - {prof}: {count}명")
    
    # 지역 분포
    regions = Counter(c.region for c in citizens)
    print(f"\n🗺️ 지역 분포:")
    for region, count in regions.most_common(8):
        print(f"  - {region}: {count}명")
    
    print("\n" + "=" * 70)
    print("  시뮬레이션 완료")
    print("=" * 70)


def main():
    random.seed(42)  # 재현 가능성을 위한 시드
    
    citizens, history, eras = run_simulation(years=1000, initial_population=100)
    print_summary(citizens, history, eras)
    
    return citizens, history, eras


if __name__ == "__main__":
    main()
