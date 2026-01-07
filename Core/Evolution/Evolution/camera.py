from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Camera:
    pos_x: float = 0.0
    pos_y: float = 0.0
    zoom: float = 1.0
    screen_size: Tuple[int, int] = (1024, 768)

    def set_screen_size(self, w: int, h: int) -> None:
        self.screen_size = (int(w), int(h))

    def clamp_zoom(self, z: float) -> float:
        return max(0.5, min(4.0, z))

    def set_zoom(self, z: float) -> None:
        self.zoom = self.clamp_zoom(z)

    def move(self, dx: float, dy: float) -> None:
        self.pos_x += dx
        self.pos_y += dy

    def world_to_screen(self, p: Tuple[float, float]) -> Tuple[float, float]:
        cx, cy = self.pos_x, self.pos_y
        w, h = self.screen_size
        return ((p[0] - cx) * self.zoom + w * 0.5, (p[1] - cy) * self.zoom + h * 0.5)

    def screen_to_world(self, s: Tuple[float, float]) -> Tuple[float, float]:
        cx, cy = self.pos_x, self.pos_y
        w, h = self.screen_size
        return ((s[0] - w * 0.5) / self.zoom + cx, (s[1] - h * 0.5) / self.zoom + cy)

