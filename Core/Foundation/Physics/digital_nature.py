"""Minimal DigitalNature simulation for tests."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Tuple


class TerrainType(Enum):
    PLAIN = auto()
    WATER = auto()
    MOUNTAIN = auto()


@dataclass
class TerrainField:
    width: int
    height: int
    data: np.ndarray = field(init=False)

    def __post_init__(self):
        self.data = np.random.rand(self.height, self.width)

    def sample(self, x: int, y: int) -> float:
        x = max(0, min(self.width - 1, x))
        y = max(0, min(self.height - 1, y))
        return float(self.data[y, x])


@dataclass
class WeatherSystem:
    season: str = "spring"
    humidity: float = 0.5
    temperature: float = 20.0

    def step(self, dt: float = 0.1) -> Dict[str, Any]:
        self.temperature += (np.random.rand() - 0.5) * dt
        self.humidity = float(np.clip(self.humidity + (np.random.rand() - 0.5) * 0.01, 0.0, 1.0))
        return {"season": self.season, "humidity": self.humidity, "temperature": self.temperature}


class DigitalNature:
    def __init__(self, width: int = 32, height: int = 32):
        self.terrain = TerrainField(width=width, height=height)
        self.weather = WeatherSystem()
        self.stats = {"data_absorbed": 0}

    def receive_data(self, data: np.ndarray, data_type: str = "generic") -> None:
        self.stats["data_absorbed"] += 1

    def step(self, dt: float = 0.1) -> Dict[str, Any]:
        weather_state = self.weather.step(dt)
        terrain_summary = {
            "mean": float(np.mean(self.terrain.data)),
            "std": float(np.std(self.terrain.data)),
        }
        return {"weather": weather_state, "season": weather_state["season"], "terrain_summary": terrain_summary}

    def swim_in_data(self, position: Tuple[int, int]) -> Dict[str, Any]:
        x, y = position
        value = self.terrain.sample(x, y)
        ttype = TerrainType.PLAIN if value < 0.33 else TerrainType.WATER if value < 0.66 else TerrainType.MOUNTAIN
        return {
            "position": (x, y),
            "terrain_type": ttype,
            "experience": float(value),
        }


__all__ = ["DigitalNature", "TerrainField", "WeatherSystem", "TerrainType"]
