"""
Organ System (The Biological Loader)
====================================

"The Body knows its Parts."

This module implements the **Dynamic Organ Discovery Protocol**.
Instead of hardcoding imports in `living_elysia.py` (which causes dependency hell),
this system scans the "Body" (Directory Structure) and awakens Organs that adhere
to the `OrganManifest` protocol.

It acts as the "connective tissue" between the File System and the Living Being.
"""

import importlib
import inspect
import logging
import os
import pkgutil
from dataclasses import dataclass
from typing import Dict, Any, Type, List

logger = logging.getLogger("OrganSystem")

@dataclass
class OrganManifest:
    """The DNA of an Organ."""
    name: str
    purpose: str
    frequency: float = 440.0 # Standard A4 (Resonance Base)
    dependencies: List[str] = None

class Organ:
    """
    Base class for all Living Organs.
    """
    MANIFEST: OrganManifest = None

    def __init__(self, resonance_field=None, **kwargs):
        self.resonance_field = resonance_field
        self.is_active = False

    def awaken(self):
        """Called when the body wakes up."""
        self.is_active = True
        logger.info(f"🫀 Organ '{self.MANIFEST.name}' awakened at {self.MANIFEST.frequency}Hz.")

    def sleep(self):
        """Called when the body rests."""
        self.is_active = False

class OrganSystem:
    def __init__(self, resonance_field):
        self.resonance_field = resonance_field
        self.organs: Dict[str, Any] = {}
        self.manifests: Dict[str, OrganManifest] = {}

    def scan_and_awaken(self, root_package: str = "Core"):
        """
        Recursively scans the package for classes inheriting from Organ
        or adhering to the Manifest protocol.
        """
        logger.info(f"🔍 Scanning '{root_package}' for biological tissue...")

        # We need to walk the directory to find packages
        # This is a simplified scanner that looks for known paths to avoid
        # importing everything and crashing on broken legacy code.

        # Target Sectors (The "Chakras")
        sectors = [
            "Core.Sensory",
            "Core.Memory",
            "Core.Cognition",
            "Core.Expression",
            "Core.Ether",
            "Core.Foundation" # Self-referential, but useful for tools
        ]

        found_count = 0

        for sector in sectors:
            try:
                module = importlib.import_module(sector)
                # Scan submodules
                if hasattr(module, "__path__"):
                    for _, name, is_pkg in pkgutil.iter_modules(module.__path__):
                        full_name = f"{sector}.{name}"
                        self._inspect_module(full_name)
                        found_count += 1
            except ImportError as e:
                logger.warning(f"⚠️ Sector '{sector}' damaged or missing: {e}")
            except Exception as e:
                logger.warning(f"⚠️ Error scanning sector '{sector}': {e}")

        logger.info(f"🧬 Scan complete. {len(self.organs)} organs connected.")

    def _inspect_module(self, module_name: str):
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    # Check 1: Is it an Organ subclass?
                    if issubclass(obj, Organ) and obj is not Organ:
                        self._graft_organ(obj)
                    # Check 2: Does it have a MANIFEST? (Duck Typing)
                    elif hasattr(obj, "MANIFEST") and isinstance(obj.MANIFEST, OrganManifest):
                        self._graft_organ(obj)
        except Exception:
            # Silent fail for now, we don't want to stop the heartbeat
            pass

    def _graft_organ(self, organ_class: Type):
        manifest = getattr(organ_class, "MANIFEST", None)
        if not manifest:
            # Auto-generate manifest for "Wild Organs"
            manifest = OrganManifest(
                name=organ_class.__name__,
                purpose=organ_class.__doc__ or "Unknown Function",
                frequency=440.0
            )

        if manifest.name in self.organs:
            return # Already grafted

        try:
            # Instantiate
            # We try to inject resonance_field if acceptable
            try:
                instance = organ_class(resonance_field=self.resonance_field)
            except TypeError:
                instance = organ_class() # Fallback to no-arg

            self.organs[manifest.name] = instance
            self.manifests[manifest.name] = manifest

            if hasattr(instance, "awaken"):
                instance.awaken()

            logger.info(f"   ✨ Connected: {manifest.name}")

        except Exception as e:
            logger.error(f"   ❌ Rejected: {manifest.name} (Incompatible Tissue) - {e}")

    def get_organ(self, name: str) -> Any:
        return self.organs.get(name)
