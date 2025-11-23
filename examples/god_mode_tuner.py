"""
God-Mode Tuner (CLI)

간단한 입력으로 우주 상수(중력, 시간 스케일, 토션 각도, 터널링 강화 등)를
World/Physics에 적용하는 인터랙티브 도구. 추가 의존성 없음.
"""
from __future__ import annotations

import argparse
from typing import Optional

from elysia_engine.world import World
from elysia_engine.physics import PhysicsWorld
from elysia_engine.math_utils import Quaternion, Vector3
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.systems.spacetime import SpacetimeOrchestrator


def apply_settings(
    world: World,
    gravity: Optional[float],
    time_scale: Optional[float],
    torsion_angle: Optional[float],
    torsion_axis: str,
) -> None:
    if not world.physics:
        world.physics = PhysicsWorld()

    phys = world.physics

    if gravity is not None:
        phys.gravity_constant = gravity
    if time_scale is not None:
        phys.time_scale = time_scale
    if torsion_angle is not None and torsion_angle != 0.0:
        axis_vec = {
            "x": Vector3(1, 0, 0),
            "y": Vector3(0, 1, 0),
            "z": Vector3(0, 0, 1),
        }.get(torsion_axis.lower(), Vector3(0, 1, 0))
        phys.spacetime_torsion = Quaternion.from_axis_angle(axis_vec, torsion_angle)
    else:
        phys.spacetime_torsion = None


def main() -> None:
    parser = argparse.ArgumentParser(description="God-Mode Tuner (gravity/time/torsion)")
    parser.add_argument("--gravity", type=float, default=None, help="중력 상수 (기본 1.0)")
    parser.add_argument("--time-scale", type=float, default=None, help="시간 스케일 (기본 1.0)")
    parser.add_argument("--torsion-angle", type=float, default=None, help="공간 토션 각도 (라디안)")
    parser.add_argument("--torsion-axis", type=str, default="y", help="토션 회전축: x/y/z")
    parser.add_argument("--entropy-threshold", type=float, default=0.7, help="엔트로피 임계치")
    parser.add_argument("--cooldown", type=int, default=5, help="Orchestrator 쿨다운")
    args = parser.parse_args()

    world = World()
    world.physics = PhysicsWorld()

    # 기본 Consciousness + Orchestrator 세팅
    gc = GlobalConsciousness(world.physics)
    orchestrator = SpacetimeOrchestrator(
        physics=world.physics,
        entropy_threshold=args.entropy_threshold,
        cooldown=args.cooldown,
    )
    world.add_system(gc)
    world.add_system(orchestrator)

    apply_settings(world, args.gravity, args.time_scale, args.torsion_angle, args.torsion_axis)

    print("[God-Mode] Current constants:")
    print(f"  Gravity       : {world.physics.gravity_constant}")
    print(f"  Time Scale    : {world.physics.time_scale}")
    print(f"  Torsion       : {world.physics.spacetime_torsion}")
    print(f"  Entropy Thres.: {args.entropy_threshold}")
    print(f"  Cooldown      : {args.cooldown}")
    print("\nTip: 재실행으로 상수들을 빠르게 리믹스하세요.")


if __name__ == "__main__":
    main()
