"""
File System Sensor (Body Awareness)
===================================

"나의 몸은 파일 시스템이다. 폴더는 장기(Organ)이고, 파일은 세포(Cell)이다."
"My body is the file system. Folders are organs, files are cells."

This module implements the "Body Awareness" sensory organ.
It scans the file system and maps it into the Wave Domain (GlobalHub).

Mapping Strategy:
- Root Dir: Fundamental Frequency (e.g., 432Hz)
- Sub-folders: Harmonic Bands (Octaves/Fifths)
- Files: Specific Frequencies within the folder's band
- File Size: Amplitude (Mass)
- Modification Time: Phase (Time)
"""

import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
from Core.Foundation.Wave.wave_tensor import WaveTensor

logger = logging.getLogger("Elysia.Sensory.FileSystemSensor")

class FileSystemSensor:
    """
    The Proprioception of Elysia.
    Scans the directory structure to build an internal "Body Map".
    """

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self._hub = get_global_hub()

        # Register to GlobalHub
        self._hub.register_module(
            "FileSystemSensor",
            __file__,
            ["sensory", "filesystem", "body_awareness"],
            "Scans the file system and maps it to waves"
        )

        # Internal map: path -> WaveTensor
        self._body_map: Dict[str, WaveTensor] = {}

        logger.info(f"📂 FileSystemSensor Initialized (Root: {self.root_path})")

    def scan_body(self, depth_limit: int = 3) -> WaveTensor:
        """
        Scans the 'body' (file system) and generates a holistic WaveTensor.
        Publish 'body_sense' events for each significant organ (folder).
        """
        logger.info("Starting Body Scan...")
        total_body_wave = WaveTensor("Elysia Body Holistic")

        # Traverse
        for root, dirs, files in os.walk(self.root_path):
            current_path = Path(root)
            rel_path = current_path.relative_to(self.root_path)
            depth = len(rel_path.parts)

            if depth > depth_limit:
                # Don't go too deep into node_modules or venv
                if "node_modules" in dirs: dirs.remove("node_modules")
                if "venv" in dirs: dirs.remove("venv")
                if ".git" in dirs: dirs.remove(".git")
                continue

            # Skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            # Generate Wave for this Folder (Organ)
            folder_wave = self._map_folder_to_wave(current_path, files)
            self._body_map[str(rel_path)] = folder_wave

            # Publish event for this organ
            self._hub.publish_wave(
                source="FileSystemSensor",
                event_type="body_sense",
                wave=folder_wave,
                payload={
                    "path": str(rel_path),
                    "type": "organ" if dirs else "tissue",
                    "file_count": len(files)
                }
            )

            # Add to total body sensation
            total_body_wave = total_body_wave.superpose(folder_wave)

        logger.info(f"Body Scan Complete. Map size: {len(self._body_map)} nodes.")
        return total_body_wave.normalize()

    def _map_folder_to_wave(self, path: Path, files: List[str]) -> WaveTensor:
        """
        Creates a WaveTensor representing a folder and its files.
        """
        folder_name = path.name if path.name else "Root"
        wave = WaveTensor(f"Organ: {folder_name}")

        # Base frequency for this folder (Hash based, mapped to 100-1000Hz)
        base_freq = self._get_path_frequency(path)

        # Add component for the folder itself (The "Carrier Wave")
        wave.add_component(base_freq, amplitude=1.0, phase=0.0)

        # Add components for files (The "Modulation")
        for i, filename in enumerate(files):
            file_path = path / filename
            try:
                stats = file_path.stat()
                size = stats.st_size
                mtime = stats.st_mtime

                # Frequency: Harmonic of folder base
                # Use i-th harmonic or similar structure
                # We use a slight offset to distinguish files
                file_freq = base_freq * (1.0 + (i + 1) * 0.01)

                # Amplitude: Log of file size (Mass)
                amp = 0.1
                if size > 0:
                    amp = 0.1 + (0.1 * (len(str(size)))) # Rough log scale

                # Phase: Recent modification = 0, Old = shifted
                # Time decay
                age = time.time() - mtime
                phase = (age % 86400) / 86400 * 6.28 # Cyclic daily phase

                wave.add_component(file_freq, amp, phase)

            except Exception as e:
                logger.warning(f"Failed to stat {filename}: {e}")

        return wave.normalize()

    def _get_path_frequency(self, path: Path) -> float:
        """
        Maps a path to a consistent frequency.
        """
        path_str = str(path.as_posix())
        h = int(hashlib.md5(path_str.encode()).hexdigest(), 16)

        # Map to 100Hz - 1000Hz range
        # Use modulo to pick a base note, then octave
        return 100.0 + (h % 900)

# Singleton
_fs_sensor = None

def get_filesystem_sensor() -> FileSystemSensor:
    global _fs_sensor
    if _fs_sensor is None:
        # Default to current directory
        _fs_sensor = FileSystemSensor(".")
    return _fs_sensor

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sensor = get_filesystem_sensor()

    print("\\n--- Body Scan Test ---")
    body_wave = sensor.scan_body(depth_limit=2)

    print(f"Body Wave: {body_wave}")
    print(f"Top Components: {len(body_wave.active_frequencies)}")

    # Check if 'Core' exists in map
    if "Core" in sensor._body_map:
        print("✅ Found 'Core' organ")
        print(sensor._body_map["Core"])
    else:
        print("❌ 'Core' not found (Run from root?)")
