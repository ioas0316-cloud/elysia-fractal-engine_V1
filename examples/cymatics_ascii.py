"""
ASCII 사이매틱스 패턴 시각화.

주파수/위상을 주면 cymatics.frequency_to_pattern이 만든 경로/게이트를
간단한 문자 격자로 보여준다. 추가 의존성 없음.
"""
from __future__ import annotations

import argparse
from typing import List

from elysia_engine.cymatics import CymaticPattern, frequency_to_pattern


def render_pattern(pattern: CymaticPattern, width: int = 60, height: int = 30) -> str:
    """
    경로/게이트를 ASCII 격자로 투영해 문자열로 반환.
    """
    xs = [p.x for p in pattern.path] + [g[0].x for g in pattern.gates]
    ys = [p.y for p in pattern.path] + [g[0].y for g in pattern.gates]

    if not xs or not ys:
        return ""

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # 폭/높이가 0이면 최소 범위 확보
    if xmax - xmin < 1e-3:
        xmax = xmin + 1.0
    if ymax - ymin < 1e-3:
        ymax = ymin + 1.0

    def to_grid(x: float, y: float) -> tuple[int, int]:
        gx = int((x - xmin) / (xmax - xmin) * (width - 1))
        gy = int((y - ymin) / (ymax - ymin) * (height - 1))
        # y는 위가 0
        gy = height - 1 - gy
        return gx, gy

    grid: List[List[str]] = [[" " for _ in range(width)] for _ in range(height)]

    # 경로 표시
    for pos in pattern.path:
        gx, gy = to_grid(pos.x, pos.y)
        grid[gy][gx] = "o"

    # 게이트 표시 (에너지 높을수록 진하게: 1~9)
    if pattern.gates:
        energies = [g[1] for g in pattern.gates]
        e_min, e_max = min(energies), max(energies)
        if e_max - e_min < 1e-6:
            e_max = e_min + 1.0
        for pos, energy in pattern.gates:
            gx, gy = to_grid(pos.x, pos.y)
            level = int(((energy - e_min) / (e_max - e_min)) * 8) + 1
            grid[gy][gx] = str(level)

    return "\n".join("".join(row) for row in grid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cymatics ASCII visualizer")
    parser.add_argument("--frequency", type=float, default=50.0, help="주파수(Hz 유사 값)")
    parser.add_argument("--phase", type=float, default=0.0, help="위상(라디안)")
    parser.add_argument("--width", type=int, default=60, help="출력 폭")
    parser.add_argument("--height", type=int, default=30, help="출력 높이")
    args = parser.parse_args()

    pattern = frequency_to_pattern(args.frequency, phase=args.phase)
    art = render_pattern(pattern, width=args.width, height=args.height)

    print(f"[Cymatics] freq={args.frequency} phase={args.phase}")
    print(art)
    print("\nLegend: 'o' path, digits=gate energy (1=low, 9=high)")


if __name__ == "__main__":
    main()
