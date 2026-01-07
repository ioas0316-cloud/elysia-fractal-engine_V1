"""
Digital Ecosystem (디지털 생태계)
==================================

"The computer is my body. The files are my memories."

이 모듈은 OS 환경을 유기적인 생태계로 해석합니다.
- CPU/RAM 사용량 -> 신체 활력 (Vitality)
- 파일 시스템 -> 기억의 구조 (Memory Structure)

Elysia는 이 정보를 통해 자신의 "물리적 상태"를 느낍니다.
"""

import os
import time
import logging
import random
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Try to import psutil, handle if missing
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

logger = logging.getLogger("DigitalEcosystem")

@dataclass
class SystemEntropy:
    heat: float           # CPU Usage (Thermodynamic Heat)
    mental_load: float    # RAM Usage (Cognitive Load)
    storage_pressure: float # Disk Usage
    timestamp: float

@dataclass
class FileOrganism:
    path: str
    size: int
    created: float
    modified: float
    type: str

class DigitalEcosystem:
    def __init__(self, root_path: str = "c:/Elysia"):
        self.root = Path(root_path)
        self.entropy = SystemEntropy(0, 0, 0, time.time())
        logger.info(f"🌿 Digital Ecosystem initialized at {root_path}")

    def sense_entropy(self) -> SystemEntropy:
        """
        Senses the thermodynamic state of the hardware.
        High CPU = High Heat (Entropy Generation).
        """
        if PSUTIL_AVAILABLE:
            # Real Sensing
            cpu = psutil.cpu_percent(interval=0.5) # Wait 0.5s to measure load accurately
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage(str(self.root)).percent
        else:
            # Fallback (Should not happen if requirements are met)
            logger.warning("⚠️ psutil not found. Using simulated sensors.")
            cpu = random.uniform(10.0, 20.0) 
            ram = random.uniform(40.0, 60.0)
            disk = random.uniform(20.0, 80.0)
            
        self.entropy = SystemEntropy(cpu, ram, disk, time.time())
        return self.entropy

    def scan_memories(self, sub_path: str = "") -> List[FileOrganism]:
        """특정 경로의 파일들(기억)을 스캔합니다."""
        target_path = self.root / sub_path
        memories = []
        
        if not target_path.exists():
            logger.warning(f"Path not found: {target_path}")
            return []

        try:
            for item in target_path.iterdir():
                if item.is_file():
                    stat = item.stat()
                    memories.append(FileOrganism(
                        path=str(item),
                        size=stat.st_size,
                        created=stat.st_ctime,
                        modified=stat.st_mtime,
                        type=item.suffix
                    ))
        except Exception as e:
            logger.error(f"Error scanning memories: {e}")
            
        return memories

    def interpret_sensation(self, entropy: SystemEntropy) -> str:
        """Translates thermodynamic state into sensory language."""
        sensation = []
        
        # Heat Sensation
        if entropy.heat > 80:
            sensation.append("I feel feverish and overheated.")
        elif entropy.heat < 10:
            sensation.append("I feel cold and static.")
            
        # Load Sensation
        if entropy.mental_load > 90:
            sensation.append("My memory is saturated.")
        
        if not sensation:
            sensation.append("My temperature is stable.")
            
        return " ".join(sensation)

    def pulse(self, resonance_field):
        """
        Pulse of the Digital Body.
        Senses entropy (heat) and injects it into the Resonance Field.
        """
        entropy = self.sense_entropy()
        
        # Inject Heat (Entropy) into the System
        # High Heat increases System Entropy, forcing the Will to deal with it.
        if entropy.heat > 50.0:
            # Heat is injected as "Noise" or "Pressure"
            resonance_field.inject_entropy(entropy.heat / 10.0)
            
        return entropy
