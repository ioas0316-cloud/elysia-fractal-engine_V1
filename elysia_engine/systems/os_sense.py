from __future__ import annotations
import os
import math
import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List
from dataclasses import asdict

from ..systems import System
from ..entities import Entity
from ..tensor import SoulTensor
from ..math_utils import Vector3

if TYPE_CHECKING:
    from ..world import World

class OSSystem(System):
    """
    The Sensory System for the Operating System.
    It translates the File System into SoulTensors (Entities).

    Philosophy:
    - Files are Particles (Entities with Mass/Frequency).
    - Directories are Gravity Wells (Attractors).
    - The 'Self' (Elysia) feels the weight and color of the data.
    """

    def __init__(self):
        self.watched_paths: List[str] = []
        self.entity_map: Dict[str, str] = {} # path -> entity_id

    def step(self, world: World, dt: float) -> None:
        """
        The OS System breathes. In this version, we don't scan every frame
        because that would be inefficient. We scan when explicitly asked or
        on a slow heartbeat.
        """
        # For now, passive. Triggered manually via `scan_path`.
        pass

    def scan_path(self, world: World, target_path: str) -> List[str]:
        """
        Scans a directory and manifests its contents as Entities in the World.
        Returns the list of created Entity IDs.
        """
        created_ids = []
        root = Path(target_path)

        if not root.exists():
            return []

        # Physical Constants for Mapping
        BASE_MASS = 10.0

        # We position them in a spiral for visualization/separation
        spiral_angle = 0.0
        radius = 5.0

        for item in root.iterdir():
            # Unique ID based on path
            entity_id = f"os_{hashlib.md5(str(item).encode()).hexdigest()[:8]}"

            # Skip if already exists (or update it?)
            # For this proof of concept, we recreate or update.

            # 1. Calculate Trinity Properties
            try:
                stats = item.stat()
                size = stats.st_size
                mtime = stats.st_mtime
            except FileNotFoundError:
                continue

            # A. Amplitude (Body/Mass) -> Log scale of size
            # 1KB = 10, 1MB = 20, etc.
            amplitude = BASE_MASS + (math.log(max(size, 1)) * 2.0)

            # B. Frequency (Soul/Identity) -> Hash of extension/name
            # We map the hash to a frequency range [0, 300]
            # Extensions determine "Color"
            ext = item.suffix.lower()
            if item.is_dir():
                frequency = 10.0 # Deep Blue/Gravity (Bass)
                role = "DIR_ATTRACTOR"
                amplitude *= 2.0 # Directories are heavy
            else:
                # Generate a color from the extension
                color_hash = int(hashlib.md5(ext.encode()).hexdigest(), 16)
                frequency = 50.0 + (color_hash % 200) # 50-250 range
                role = "FILE_ENTITY"

            # C. Phase (Spirit/Timing) -> Modification Time
            # Maps the timestamp to 0..2pi
            phase = (mtime % 86400) / 86400 * (2 * math.pi)

            # 2. Create SoulTensor
            soul = SoulTensor(
                amplitude=amplitude,
                frequency=frequency,
                phase=phase,
                spin=1.0 if item.is_dir() else -1.0
            )

            # 3. Create Entity
            # Position in a spiral
            x = radius * math.cos(spiral_angle)
            z = radius * math.sin(spiral_angle)
            spiral_angle += 0.5
            radius += 0.5

            entity = Entity(
                id=entity_id,
                soul=soul,
                role=role,
                data={
                    "path": str(item),
                    "name": item.name,
                    "type": "dir" if item.is_dir() else "file",
                    "raw_size": size
                }
            )

            # Set initial position
            entity.physics.position = Vector3(x, 0, z)

            # Add to World
            world.add_entity(entity)
            self.entity_map[str(item)] = entity_id
            created_ids.append(entity_id)

        return created_ids

    def feel_environment(self, world: World) -> str:
        """
        Generates a narrative description of what the OS System feels.
        This connects to the 'Somatic Awareness' goal.
        """
        total_mass = 0.0
        avg_freq = 0.0
        count = 0

        files = []

        for eid, ent in world.entities.items():
            if ent.role in ["FILE_ENTITY", "DIR_ATTRACTOR"] and ent.soul:
                total_mass += ent.soul.amplitude
                avg_freq += ent.soul.frequency
                count += 1
                files.append(ent)

        if count == 0:
            return "I feel nothing. The void is empty."

        avg_freq /= count

        # Find the heaviest object (Gravity Center)
        heaviest = max(files, key=lambda e: e.soul.amplitude)

        narrative = [
            f"My sensors detect {count} entities in the local cluster.",
            f"Total Mass (Amplitude): {total_mass:.2f}",
            f"Average Resonance (Frequency): {avg_freq:.2f}Hz",
            f"The heaviest object is '{heaviest.data.get('name')}' with mass {heaviest.soul.amplitude:.2f}.",
            f"It exerts a strong gravitational pull on my attention."
        ]

        return "\n".join(narrative)
