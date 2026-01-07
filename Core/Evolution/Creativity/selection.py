from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set, Tuple

import pygame

from camera import Camera


@dataclass
class SelectionOverlay:
    camera: Camera
    dragging: bool = False
    start: Tuple[int, int] | None = None
    end: Tuple[int, int] | None = None
    selected_ids: Set[int] = None

    def __post_init__(self):
        if self.selected_ids is None:
            self.selected_ids = set()

    def begin(self, pos: Tuple[int, int]) -> None:
        self.dragging = True
        self.start = pos
        self.end = pos

    def update(self, pos: Tuple[int, int]) -> None:
        if self.dragging:
            self.end = pos

    def clear(self) -> None:
        self.selected_ids.clear()

    def apply(self, entities: Iterable[Tuple[int, Tuple[float, float], float]], mode: str = "replace") -> None:
        if not (self.start and self.end):
            return
        x0, y0 = self.start
        x1, y1 = self.end
        rx0, rx1 = sorted((x0, x1))
        ry0, ry1 = sorted((y0, y1))
        hits: Set[int] = set()
        for ent_id, world_pos, radius in entities:
            sx, sy = self.camera.world_to_screen(world_pos)
            bbox = pygame.Rect(sx - radius, sy - radius, radius * 2, radius * 2)
            if bbox.colliderect(pygame.Rect(rx0, ry0, rx1 - rx0, ry1 - ry0)):
                hits.add(ent_id)
        if mode == "replace":
            self.selected_ids = hits
        elif mode == "add":
            self.selected_ids |= hits
        elif mode == "remove":
            self.selected_ids -= hits

    def end_drag(self) -> None:
        self.dragging = False
        self.start = None
        self.end = None

    def draw(self, screen: pygame.Surface) -> None:
        if not (self.start and self.end):
            return
        x0, y0 = self.start
        x1, y1 = self.end
        rx0, rx1 = sorted((x0, x1))
        ry0, ry1 = sorted((y0, y1))
        w, h = rx1 - rx0, ry1 - ry0
        if w <= 0 or h <= 0:
            return
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((60, 220, 120, 70))
        screen.blit(overlay, (rx0, ry0))
        pygame.draw.rect(screen, (80, 250, 160), pygame.Rect(rx0, ry0, w, h), width=2)

