"""
Underworld Simulation Demo (언더월드 시뮬레이션 데모)
=====================================================

300명의 주민이 1000년을 살아가는 시뮬레이션.
SAO 알리시제이션의 언더월드처럼, 시간 가속을 통해 실제로 실행 가능.

시간 설정:
- 1 tick = 1 일 (in-world)
- 1000년 = 365,000 ticks
- 시간 압축으로 빠르게 실행

주민들의 삶:
- 태어나고, 성장하고, 배우고
- 관계를 맺고, 사랑하고
- 모험을 하고, 성취하고
- 늙어가고, 죽고, 기억됨

세대가 이어지면서 문화와 전설이 축적됩니다.
"""

from __future__ import annotations

import random
import logging
import time
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum, auto
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("UnderworldSim")


# =============================================================================
# 시뮬레이션 상수
# =============================================================================

TICKS_PER_YEAR = 365
DEFAULT_LIFESPAN = 80  # 기본 수명 (년)
MATURITY_AGE = 18      # 성인 나이
ELDER_AGE = 60         # 노인 나이


# =============================================================================
# 주민 클래스
# =============================================================================

class LifeStage(Enum):
    """생애 단계"""
    CHILD = auto()
    YOUTH = auto()
    ADULT = auto()
    ELDER = auto()
    DECEASED = auto()


@dataclass
class Relationship:
    """관계"""
    target_id: int
    type: str  # "family", "friend", "rival", "mentor", "lover", "spouse"
    strength: float = 0.5
    history: List[str] = field(default_factory=list)


@dataclass
class Memory:
    """기억"""
    year: int
    event: str
    emotional_weight: float  # -1.0 ~ 1.0
    people_involved: List[int] = field(default_factory=list)


@dataclass
class Inhabitant:
    """언더월드 주민"""
    id: int
    name: str
    birth_year: int
    race: str = "Human"
    profession: str = "Villager"
    location: str = "rulid_village"
    
    # 스탯
    health: float = 1.0
    happiness: float = 0.5
    skill_level: float = 0.1
    wisdom: float = 0.1
    
    # 특성
    traits: List[str] = field(default_factory=list)
    
    # 관계
    relationships: Dict[int, Relationship] = field(default_factory=dict)
    
    # 기억
    memories: List[Memory] = field(default_factory=list)
    
    # 성취
    achievements: List[str] = field(default_factory=list)
    
    # 상태
    is_alive: bool = True
    death_year: Optional[int] = None
    cause_of_death: Optional[str] = None
    spouse_id: Optional[int] = None
    children: List[int] = field(default_factory=list)
    
    def get_age(self, current_year: int) -> int:
        """현재 나이 계산"""
        return current_year - self.birth_year
    
    def get_life_stage(self, current_year: int) -> LifeStage:
        """생애 단계"""
        if not self.is_alive:
            return LifeStage.DECEASED
        age = self.get_age(current_year)
        if age < MATURITY_AGE:
            return LifeStage.CHILD
        elif age < 30:
            return LifeStage.YOUTH
        elif age < ELDER_AGE:
            return LifeStage.ADULT
        else:
            return LifeStage.ELDER
    
    def add_memory(self, year: int, event: str, weight: float, people: List[int] = None):
        """기억 추가"""
        self.memories.append(Memory(
            year=year,
            event=event,
            emotional_weight=weight,
            people_involved=people or []
        ))
        # 최대 50개 기억 유지
        if len(self.memories) > 50:
            self.memories.sort(key=lambda m: abs(m.emotional_weight), reverse=True)
            self.memories = self.memories[:50]


# =============================================================================
# 이름 생성기
# =============================================================================

FIRST_NAMES = [
    "유진", "소라", "민준", "서연", "지호", "하늘", "예은", "도윤",
    "Aiden", "Luna", "Kai", "Aria", "Zeph", "Iris", "Finn", "Rose",
    "Elric", "Mira", "Thorne", "Lyra", "Caden", "Sera", "Rowan", "Faye",
    "Alice", "Eugeo", "Kirito", "Asuna", "Bercouli", "Fanatio",
]

LAST_NAMES = [
    "星野", "月影", "風間", "雪村", "桜井", "龍崎", "森本", "青山",
    "Blackwood", "Silverstone", "Ironforge", "Brightwater", "Stormwind",
]


def generate_name() -> str:
    """이름 생성"""
    first = random.choice(FIRST_NAMES)
    if random.random() < 0.3:
        last = random.choice(LAST_NAMES)
        return f"{first} {last}"
    return first


# =============================================================================
# 시뮬레이션 엔진
# =============================================================================

class UnderworldSimulation:
    """
    언더월드 시뮬레이션 엔진
    
    300명의 주민이 1000년을 살아가는 세계.
    """
    
    def __init__(
        self,
        initial_population: int = 300,
        target_years: int = 1000,
        save_path: str = "data/Runtime/underworld_simulation.json"
    ):
        self.initial_population = initial_population
        self.target_years = target_years
        self.target_ticks = target_years * TICKS_PER_YEAR
        self.save_path = Path(save_path)
        
        # 시뮬레이션 상태
        self.current_tick = 0
        self.current_year = 0
        self.inhabitants: Dict[int, Inhabitant] = {}
        self.next_id = 0
        
        # 통계
        self.total_births = 0
        self.total_deaths = 0
        self.total_marriages = 0
        self.total_achievements = 0
        
        # 역사
        self.world_events: List[Dict[str, Any]] = []
        self.legends_created: List[str] = []
        
        # 지역별 인구
        self.locations = {
            "centoria": [],
            "rulid_village": [],
            "dark_forest": [],
            "sword_mountain": [],
            "crystal_lake": [],
            "ancient_ruins": []
        }
        
        logger.info(f"🌍 Underworld Simulation initialized")
        logger.info(f"   Population: {initial_population}")
        logger.info(f"   Duration: {target_years} years ({self.target_ticks:,} ticks)")
    
    def initialize_population(self):
        """초기 인구 생성"""
        logger.info(f"👥 Generating initial population...")
        
        for _ in range(self.initial_population):
            initial_age = random.randint(0, 50)
            birth_year = -initial_age
            
            inhabitant = Inhabitant(
                id=self.next_id,
                name=generate_name(),
                birth_year=birth_year,
                race=random.choice(["Human", "Human", "Human", "Elf", "Dwarf", "Beastkin"]),
                profession=random.choice(["Villager", "Farmer", "Hunter", "Merchant", "Artisan"]),
                location=random.choice(list(self.locations.keys())),
                traits=random.sample([
                    "brave", "kind", "curious", "diligent", "creative",
                    "wise", "loyal", "passionate", "calm", "adventurous"
                ], k=random.randint(1, 3))
            )
            
            self.inhabitants[self.next_id] = inhabitant
            self.locations[inhabitant.location].append(self.next_id)
            self.next_id += 1
        
        self._create_initial_families()
        logger.info(f"   Created {len(self.inhabitants)} inhabitants")
    
    def _create_initial_families(self):
        """초기 가족 관계 생성"""
        adults = [i for i in self.inhabitants.values() 
                 if i.get_age(0) >= MATURITY_AGE and i.get_age(0) <= 50]
        
        random.shuffle(adults)
        for i in range(0, len(adults) - 1, 2):
            if random.random() < 0.6:
                spouse1, spouse2 = adults[i], adults[i + 1]
                spouse1.spouse_id = spouse2.id
                spouse2.spouse_id = spouse1.id
                spouse1.relationships[spouse2.id] = Relationship(
                    target_id=spouse2.id, type="spouse", strength=0.8
                )
                spouse2.relationships[spouse1.id] = Relationship(
                    target_id=spouse1.id, type="spouse", strength=0.8
                )
                self.total_marriages += 1
    
    def tick(self):
        """1 tick (1일) 진행"""
        self.current_tick += 1
        
        new_year = self.current_tick // TICKS_PER_YEAR
        if new_year > self.current_year:
            self.current_year = new_year
            self._yearly_events()
        
        alive = [i for i in self.inhabitants.values() if i.is_alive]
        
        for inhabitant in alive:
            self._process_inhabitant(inhabitant)
    
    def _yearly_events(self):
        """연간 이벤트 처리"""
        alive_count = sum(1 for i in self.inhabitants.values() if i.is_alive)
        
        if self.current_year % 100 == 0 and self.current_year > 0:
            self.world_events.append({
                "year": self.current_year,
                "type": "centennial",
                "population": alive_count
            })
            logger.info(f"📅 Year {self.current_year}: Population {alive_count}")
        
        if random.random() < 0.8:
            self._hold_festival()
    
    def _process_inhabitant(self, inhabitant: Inhabitant):
        """개별 주민 처리"""
        age = inhabitant.get_age(self.current_year)
        stage = inhabitant.get_life_stage(self.current_year)
        
        death_chance = self._calculate_death_chance(inhabitant, age)
        if random.random() < death_chance:
            self._process_death(inhabitant)
            return
        
        daily_roll = random.random()
        
        if daily_roll < 0.01:
            self._special_event(inhabitant)
        elif daily_roll < 0.05:
            self._relationship_activity(inhabitant)
        elif daily_roll < 0.1:
            self._skill_growth(inhabitant)
        
        if stage in [LifeStage.YOUTH, LifeStage.ADULT]:
            if inhabitant.spouse_id is None and random.random() < 0.001:
                self._try_marriage(inhabitant)
            elif inhabitant.spouse_id and age < 45 and random.random() < 0.0005:
                self._try_birth(inhabitant)
        
        inhabitant.health = max(0.1, min(1.0, inhabitant.health + random.uniform(-0.001, 0.002)))
        inhabitant.happiness = max(0.0, min(1.0, inhabitant.happiness + random.uniform(-0.01, 0.01)))
    
    def _calculate_death_chance(self, inhabitant: Inhabitant, age: int) -> float:
        """사망 확률 계산"""
        base_chance = 0.00001
        
        if age < 5:
            base_chance *= 3
        elif age > ELDER_AGE:
            age_factor = (age - ELDER_AGE) / 20
            base_chance *= (1 + age_factor * 5)
        
        base_chance *= (2 - inhabitant.health)
        
        if inhabitant.race == "Elf":
            base_chance *= 0.3
        
        return min(0.01, base_chance)
    
    def _process_death(self, inhabitant: Inhabitant):
        """사망 처리"""
        inhabitant.is_alive = False
        inhabitant.death_year = self.current_year
        inhabitant.cause_of_death = random.choice([
            "old age", "illness", "accident", "adventure", "peaceful passing"
        ])
        
        self.total_deaths += 1
        
        if inhabitant.skill_level > 0.8 or len(inhabitant.achievements) >= 3:
            legend = f"The Legend of {inhabitant.name} the {inhabitant.profession}"
            self.legends_created.append(legend)
    
    def _special_event(self, inhabitant: Inhabitant):
        """특별한 이벤트"""
        events = [
            ("discovery", "made an amazing discovery", 0.5),
            ("achievement", "achieved something great", 0.6),
            ("trial", "overcame a great trial", 0.4),
        ]
        
        event_type, description, weight = random.choice(events)
        inhabitant.add_memory(self.current_year, description, weight)
        
        if event_type == "achievement":
            inhabitant.achievements.append(f"Year {self.current_year}: {description}")
            inhabitant.skill_level = min(1.0, inhabitant.skill_level + 0.1)
            self.total_achievements += 1
    
    def _relationship_activity(self, inhabitant: Inhabitant):
        """관계 활동"""
        same_location = [
            self.inhabitants[i] for i in self.locations[inhabitant.location]
            if i != inhabitant.id and self.inhabitants[i].is_alive
        ]
        
        if not same_location:
            return
        
        other = random.choice(same_location)
        
        if other.id not in inhabitant.relationships:
            rel_type = random.choice(["friend", "acquaintance"])
            inhabitant.relationships[other.id] = Relationship(
                target_id=other.id, type=rel_type, strength=0.3
            )
            other.relationships[inhabitant.id] = Relationship(
                target_id=inhabitant.id, type=rel_type, strength=0.3
            )
        else:
            rel = inhabitant.relationships[other.id]
            rel.strength = min(1.0, rel.strength + 0.05)
    
    def _skill_growth(self, inhabitant: Inhabitant):
        """스킬 성장"""
        growth = random.uniform(0.001, 0.01)
        mentors = [r for r in inhabitant.relationships.values() if r.type == "mentor"]
        if mentors:
            growth *= 1.5
        
        inhabitant.skill_level = min(1.0, inhabitant.skill_level + growth)
        inhabitant.wisdom = min(1.0, inhabitant.wisdom + growth * 0.5)
    
    def _try_marriage(self, inhabitant: Inhabitant):
        """결혼 시도"""
        candidates = [
            self.inhabitants[i] for i in self.locations[inhabitant.location]
            if i != inhabitant.id 
            and self.inhabitants[i].is_alive
            and self.inhabitants[i].spouse_id is None
            and self.inhabitants[i].get_life_stage(self.current_year) in [LifeStage.YOUTH, LifeStage.ADULT]
        ]
        
        if not candidates:
            return
        
        partner = random.choice(candidates)
        
        inhabitant.spouse_id = partner.id
        partner.spouse_id = inhabitant.id
        
        inhabitant.relationships[partner.id] = Relationship(
            target_id=partner.id, type="spouse", strength=0.8
        )
        partner.relationships[inhabitant.id] = Relationship(
            target_id=inhabitant.id, type="spouse", strength=0.8
        )
        
        inhabitant.add_memory(self.current_year, f"married {partner.name}", 0.9, [partner.id])
        partner.add_memory(self.current_year, f"married {inhabitant.name}", 0.9, [inhabitant.id])
        
        self.total_marriages += 1
    
    def _try_birth(self, inhabitant: Inhabitant):
        """출산 시도"""
        if inhabitant.spouse_id is None:
            return
        
        spouse = self.inhabitants.get(inhabitant.spouse_id)
        if not spouse or not spouse.is_alive:
            return
        
        child = Inhabitant(
            id=self.next_id,
            name=generate_name(),
            birth_year=self.current_year,
            race=random.choice([inhabitant.race, spouse.race]),
            profession="Child",
            location=inhabitant.location,
            traits=random.sample(inhabitant.traits + spouse.traits, k=min(2, len(inhabitant.traits)))
        )
        
        self.inhabitants[self.next_id] = child
        self.locations[child.location].append(self.next_id)
        
        child.relationships[inhabitant.id] = Relationship(
            target_id=inhabitant.id, type="parent", strength=0.9
        )
        child.relationships[spouse.id] = Relationship(
            target_id=spouse.id, type="parent", strength=0.9
        )
        
        inhabitant.children.append(self.next_id)
        spouse.children.append(self.next_id)
        
        inhabitant.add_memory(self.current_year, f"child {child.name} was born", 0.95, [self.next_id])
        spouse.add_memory(self.current_year, f"child {child.name} was born", 0.95, [self.next_id])
        
        self.next_id += 1
        self.total_births += 1
    
    def _hold_festival(self):
        """축제 개최"""
        for inhabitant in self.inhabitants.values():
            if inhabitant.is_alive:
                inhabitant.happiness = min(1.0, inhabitant.happiness + 0.1)
    
    def run(self, progress_interval: int = 100) -> Dict[str, Any]:
        """시뮬레이션 실행"""
        logger.info(f"\n🚀 Starting simulation...")
        start_time = time.time()
        
        self.initialize_population()
        
        last_progress_year = 0
        
        while self.current_year < self.target_years:
            self.tick()
            
            if self.current_year >= last_progress_year + progress_interval:
                alive = sum(1 for i in self.inhabitants.values() if i.is_alive)
                elapsed = time.time() - start_time
                years_per_sec = self.current_year / elapsed if elapsed > 0 else 0
                
                logger.info(
                    f"  Year {self.current_year:4d}/{self.target_years}: "
                    f"Pop={alive:4d} | "
                    f"Births={self.total_births:5d} | "
                    f"Deaths={self.total_deaths:5d} | "
                    f"Speed={years_per_sec:.1f} yr/s"
                )
                last_progress_year = self.current_year
            
            alive = sum(1 for i in self.inhabitants.values() if i.is_alive)
            if alive < 50:
                self._immigration(10)
        
        elapsed_time = time.time() - start_time
        results = self._compile_results(elapsed_time)
        
        logger.info(f"\n✅ Simulation complete!")
        logger.info(f"   Duration: {elapsed_time:.2f} seconds")
        logger.info(f"   Speed: {self.target_years / elapsed_time:.1f} years/second")
        
        return results
    
    def _immigration(self, count: int):
        """이민 유입"""
        for _ in range(count):
            inhabitant = Inhabitant(
                id=self.next_id,
                name=generate_name(),
                birth_year=self.current_year - random.randint(18, 40),
                race=random.choice(["Human", "Elf", "Dwarf", "Beastkin"]),
                profession=random.choice(["Villager", "Merchant", "Adventurer"]),
                location=random.choice(list(self.locations.keys())),
                traits=random.sample(["brave", "curious", "skilled"], k=2)
            )
            
            self.inhabitants[self.next_id] = inhabitant
            self.locations[inhabitant.location].append(self.next_id)
            self.next_id += 1
    
    def _compile_results(self, elapsed_time: float) -> Dict[str, Any]:
        """결과 집계"""
        alive = [i for i in self.inhabitants.values() if i.is_alive]
        deceased = [i for i in self.inhabitants.values() if not i.is_alive]
        
        if deceased:
            longest_lived = max(deceased, key=lambda i: i.death_year - i.birth_year)
            longest_life = longest_lived.death_year - longest_lived.birth_year
        else:
            longest_lived = None
            longest_life = 0
        
        most_achieved = max(self.inhabitants.values(), key=lambda i: len(i.achievements), default=None)
        most_children = max(self.inhabitants.values(), key=lambda i: len(i.children), default=None)
        
        results = {
            "simulation": {
                "years_simulated": self.target_years,
                "ticks_simulated": self.current_tick,
                "real_time_seconds": elapsed_time,
                "years_per_second": self.target_years / elapsed_time if elapsed_time > 0 else 0
            },
            "population": {
                "initial": self.initial_population,
                "final_alive": len(alive),
                "total_ever_lived": len(self.inhabitants),
                "total_births": self.total_births,
                "total_deaths": self.total_deaths,
                "total_marriages": self.total_marriages,
                "total_achievements": self.total_achievements
            },
            "demographics": {
                "avg_age": sum(i.get_age(self.current_year) for i in alive) / len(alive) if alive else 0,
                "races": {},
                "professions": {},
                "locations": {loc: len([i for i in ids if self.inhabitants[i].is_alive]) 
                             for loc, ids in self.locations.items()}
            },
            "legends": {
                "count": len(self.legends_created),
                "examples": self.legends_created[:10]
            },
            "notable_inhabitants": {
                "longest_lived": {
                    "name": longest_lived.name if longest_lived else None,
                    "age": longest_life
                },
                "most_achieved": {
                    "name": most_achieved.name if most_achieved else None,
                    "achievements": len(most_achieved.achievements) if most_achieved else 0
                },
                "most_children": {
                    "name": most_children.name if most_children else None,
                    "children": len(most_children.children) if most_children else 0
                }
            }
        }
        
        for inhabitant in alive:
            results["demographics"]["races"][inhabitant.race] = \
                results["demographics"]["races"].get(inhabitant.race, 0) + 1
            results["demographics"]["professions"][inhabitant.profession] = \
                results["demographics"]["professions"].get(inhabitant.profession, 0) + 1
        
        return results
    
    def save_results(self, results: Dict[str, Any]):
        """결과 저장"""
        try:
            self.save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 Results saved to {self.save_path}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")


# =============================================================================
# 메인 실행
# =============================================================================

def run_demo(population: int = 300, years: int = 1000):
    """데모 실행"""
    print("=" * 70)
    print("🌍 UNDERWORLD SIMULATION DEMO")
    print("   SAO 알리시제이션 스타일 세계 시뮬레이션")
    print("=" * 70)
    print(f"\n📊 Settings:")
    print(f"   • Population: {population}")
    print(f"   • Duration: {years} years ({years * 365:,} days)")
    print()
    
    sim = UnderworldSimulation(
        initial_population=population,
        target_years=years
    )
    
    results = sim.run(progress_interval=100)
    
    print("\n" + "=" * 70)
    print("📈 SIMULATION RESULTS")
    print("=" * 70)
    
    print(f"\n⏱️ Performance:")
    print(f"   • Real time: {results['simulation']['real_time_seconds']:.2f} seconds")
    print(f"   • Speed: {results['simulation']['years_per_second']:.1f} years/second")
    
    print(f"\n👥 Population:")
    print(f"   • Initial: {results['population']['initial']}")
    print(f"   • Final: {results['population']['final_alive']}")
    print(f"   • Total ever lived: {results['population']['total_ever_lived']}")
    print(f"   • Total births: {results['population']['total_births']}")
    print(f"   • Total deaths: {results['population']['total_deaths']}")
    print(f"   • Total marriages: {results['population']['total_marriages']}")
    
    print(f"\n🏆 Notable:")
    notable = results['notable_inhabitants']
    if notable['longest_lived']['name']:
        print(f"   • Longest lived: {notable['longest_lived']['name']} ({notable['longest_lived']['age']} years)")
    if notable['most_achieved']['name']:
        print(f"   • Most achieved: {notable['most_achieved']['name']} ({notable['most_achieved']['achievements']} achievements)")
    if notable['most_children']['name']:
        print(f"   • Most children: {notable['most_children']['name']} ({notable['most_children']['children']} children)")
    
    print(f"\n📖 Legends created: {results['legends']['count']}")
    for legend in results['legends']['examples'][:5]:
        print(f"   • {legend}")
    
    print(f"\n🗺️ Population by location:")
    for loc, count in results['demographics']['locations'].items():
        bar = "█" * min(count // 5, 10) + "░" * max(0, 10 - count // 5)
        print(f"   • {loc}: [{bar}] {count}")
    
    sim.save_results(results)
    
    print("\n" + "=" * 70)
    print("✅ Simulation complete!")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    run_demo(population=300, years=1000)
