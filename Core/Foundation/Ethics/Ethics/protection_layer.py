"""Minimal protection/filter layer for data packets."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Tuple


class FilterResult(Enum):
    PASS = auto()
    BLOCK = auto()
    TRANSFORM = auto()
    DESTROY = auto()


class ThreatLevel(Enum):
    SAFE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class DataPacket:
    data: Any
    source: str
    data_type: str
    frequency: float
    intensity: float


class ProtectionLayer:
    def __init__(self):
        self.log: List[Tuple[DataPacket, FilterResult]] = []

    def process(self, packet: DataPacket) -> Tuple[Any, List["Report"]]:
        reports: List[Report] = []
        threat = self._assess(packet)
        if threat in (ThreatLevel.SAFE, ThreatLevel.LOW):
            reports.append(Report(packet, FilterResult.PASS))
            self.log.append((packet, FilterResult.PASS))
            return packet.data, reports
        if threat == ThreatLevel.MEDIUM:
            transformed = self.filter_with_love(packet.data, from_creator=False)
            reports.append(Report(packet, FilterResult.TRANSFORM))
            self.log.append((packet, FilterResult.TRANSFORM))
            return transformed, reports
        # HIGH or CRITICAL
        reports.append(Report(packet, FilterResult.BLOCK))
        self.log.append((packet, FilterResult.BLOCK))
        return None, reports

    def _assess(self, packet: DataPacket) -> ThreatLevel:
        if packet.source == "creator":
            return ThreatLevel.SAFE
        if packet.intensity > 2.0 or packet.frequency > 100.0:
            return ThreatLevel.HIGH
        if "malice" in packet.data_type.lower():
            return ThreatLevel.HIGH
        if packet.intensity > 1.0:
            return ThreatLevel.MEDIUM
        return ThreatLevel.LOW

    def filter_with_love(self, data: Any, from_creator: bool = False):
        try:
            arr = np.array(data, dtype=float)
            arr = np.clip(arr, -1.0, 1.0)
            return arr
        except Exception:
            return data


@dataclass
class Report:
    packet: DataPacket
    result: FilterResult


__all__ = ["ProtectionLayer", "DataPacket", "FilterResult", "ThreatLevel", "Report"]
