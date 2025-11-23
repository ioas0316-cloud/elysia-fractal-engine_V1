"""
Garden of Thoughts

엔티티들이 주어진 법칙(중력/시간/토션) 아래서 알아서 정렬·결합하도록
방치하는 시뮬레이션. 랜덤 초기 상태에서 시작해 GlobalConsciousness가
엔트로피를 측정하고 SpacetimeOrchestrator가 상수를 미세 조정한다.
추가 의존성 없음.
"""
from __future__ import annotations

import random
from dataclasses import asdict
from typing import List

from elysia_engine.world import World
from elysia_engine.entities import Entity
from elysia_engine.tensor import SoulTensor
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.math_utils import Vector3
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.systems.spacetime import SpacetimeOrchestrator


def _spawn_entities(rng: random.Random, count: int = 8) -> List[Entity]:
    entities: List[Entity] = []
    for idx in range(count):
        # 위치를 작은 구 안에서 랜덤 배치
        pos = Vector3(
            rng.uniform(-5, 5),
            rng.uniform(-1, 1),
            rng.uniform(-5, 5),
        )
        soul = SoulTensor(
            amplitude=rng.uniform(5, 15),
            frequency=rng.uniform(10, 80),
            phase=rng.uniform(0, 6.283),
            spin=rng.choice([-1.0, 1.0]),
            polarity=rng.choice([-1.0, 1.0]),
        )
        ent = Entity(id=f"seed_{idx}", soul=soul)
        ent.physics.position = pos
        entities.append(ent)
    return entities


def run_garden(steps: int = 30, seed: int = 42, verbose: bool = True) -> dict:
    rng = random.Random(seed)

    world = World()
    physics = PhysicsWorld()
    world.physics = physics

    # 중심 Attractor로 "의도"를 둔다.
    physics.add_attractor(Attractor(id="truth", position=Vector3(0, 0, 0), mass=200.0))

    # 시스템: 의식 + 스페이스타임 조정
    gc = GlobalConsciousness(physics=physics)
    orchestrator = SpacetimeOrchestrator(
        physics=physics,
        entropy_threshold=0.6,
        cooldown=2,
        torsion_angle=0.6,
    )
    world.add_system(gc)
    world.add_system(orchestrator)

    # 엔티티 생성 및 등록
    for ent in _spawn_entities(rng):
        world.add_entity(ent)
        physics.register_entity(ent)

    snapshots = []
    for _ in range(steps):
        world.step()
        if world.tick % 5 == 0 or world.tick == steps:
            snapshots.append(
                {
                    "tick": world.tick,
                    "entropy": gc.global_entropy,
                    "gravity": physics.gravity_constant,
                    "time_scale": physics.time_scale,
                }
            )

    if verbose:
        print("=== Garden of Thoughts ===")
        for snap in snapshots:
            print(
                f"[Tick {snap['tick']:02d}] entropy={snap['entropy']:.3f} "
                f"G={snap['gravity']:.2f} time_scale={snap['time_scale']:.2f}"
            )

    return {
        "final_entropy": gc.global_entropy,
        "ticks": world.tick,
        "entities": [asdict(ent.physics) for ent in world.entities.values()],
    }


def main() -> None:
    run_garden()


if __name__ == "__main__":
    main()
